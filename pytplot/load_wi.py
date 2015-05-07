import pytplot
import cdaweb
from spacepy import pycdf
from numpy import append,concatenate
from pandas import DataFrame

def load_wi_mfi(timerange):
    dates = pytplot.datesFromTimeRange(timerange)

    for x in range(len(dates)):
        wi_mfi_cdf_file = cdaweb.get_cdaweb_cdf(dates[x].year, dates[x].month, dates[x].day, 'wind', 'mfi', 'mfi_h0', 'wi_h0_mfi')
        cdf=pycdf.CDF(wi_mfi_cdf_file)
        if x == 0:
            epoch3 = cdf['Epoch3'][...].flatten()
            data_B3F1 = cdf['B3F1'][...]
            data_B3GSE = cdf['B3GSE'][...]
        else:
            epoch3 = append(epoch3, cdf['Epoch3'][...].flatten(),0)
            data_B3F1=append(data_B3F1,cdf['B3F1'][...],0) # don't forget the [...]
            data_B3GSE=append(data_B3GSE,cdf['B3GSE'][...],0) # don't forget the [...]
        cdf.close()
        
    B3F1 = pytplot.pytplotItem(DataFrame(data_B3F1,index=epoch3,columns=['B']))
    B3GSE = pytplot.pytplotItem(DataFrame(data_B3GSE,index=epoch3,columns=['Bx','By','Bz']))

    B3F1.data = B3F1.data[B3F1.data > -1e10]
    B3GSE.data = B3GSE.data[B3GSE.data > -1e10]
    B3GSE.data = B3GSE.data[B3GSE.data < 1e10]

    B3F1.set_options({'ylim':[0,30],
                      'ylabel':"|B|\n[nT]",'ylabel_tex':"$\mathbf{|B|}$\n$\mathrm{[nT]}$"})
    B3GSE.set_options({'ylim':[-30,30],
                       'ylabel':"B GSE \n [nT]",
                       'ylabel_tex':"$\mathrm{B_{GSE}}$ \n $\mathrm{[nT]}$",
                       "panel_size":1.5})


    return {'wi_mfi_h0_B3F1':B3F1,'wi_mfi_h0_B3GSE':B3GSE}

def load_wi_elpd(timerange):
    import itertools
    import pandas

    dates = pytplot.datesFromTimeRange(timerange)
    for x in range(len(dates)):
        wi_3dp_elpd_cdf_file = cdaweb.get_cdaweb_cdf(dates[x].year, dates[x].month, dates[x].day, 'wind', '3dp', '3dp_elpd', 'wi_elpd_3dp')
        cdf=pycdf.CDF(wi_3dp_elpd_cdf_file)
        
        if x==0:
            epoch = cdf['Epoch'][...].flatten()
            energy = cdf['ENERGY'][...]
            pang = cdf['PANGLE'][...]
            flux = cdf['FLUX'][...]
        else:
            epoch = append(epoch,cdf['Epoch'][...].flatten(),0)
            energy = append(energy,cdf['ENERGY'][...],0)
            pang = append(pang,cdf['PANGLE'][...],0)
            flux = append(flux,cdf['FLUX'][...],0)
        cdf.close()

    n_pang = pang.shape[1]
    n_ebin = energy.shape[1]

    arrays = [range(n_pang),range(n_ebin)]
    errays = [['-'],range(n_ebin)]
    prrays = [range(n_pang),['-']]

    tuples = list(itertools.product(*arrays)) + list(itertools.product(*errays)) + list(itertools.product(*prrays))

    cols = pandas.MultiIndex.from_tuples(tuples, names=['pangle','energy'])

    data = concatenate((flux.reshape(len(epoch),n_pang*n_ebin),energy,pang),axis=1)

    elpd = pytplot.pytplotItem(DataFrame(data, columns=cols, index=epoch))
        
    elpd.set_options({'ylabel':'EESA-L'})
    return {'wi_3dp_elpd':elpd}
'''
Created on Jul 14, 2013

@author: pulupa
'''
