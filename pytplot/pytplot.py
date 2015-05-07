'''
Created on Jul 10, 2013

@author: pulupa
'''
from pandas import DataFrame
from pandas import DatetimeIndex
import datetime
import re
import matplotlib.gridspec as gridspec
import matplotlib.patches
import matplotlib.pyplot as plt
import spacepy_utils
from matplotlib import rcParams
from numpy import mean

def datesFromTimeRange(timerange):
    ndays = (max(timerange).date()-min(timerange).date()).days
    if max(timerange).replace(hour=0,minute=0,second=0,microsecond=0) < max(timerange):
        ndays = ndays + 1
    if ndays == 0:
        ndays = 1
    dateList = [min(timerange).date() + datetime.timedelta(days=x) for x in range(0,ndays) ]
    return dateList

class pytplotItem(object):
    def __init__(self, data):
        self.data = data
        self.options = {}
    
    def set_options(self,options):
        self.options.update(options)
        
    def tplot(self,ax,trange,legend=False):
        
        import numpy as np
        import itertools
        import matplotlib.transforms as transforms
            
        if 'ylog' in self.options:
            if self.options['ylog']:
                ax.set_yscale("log", nonposy='clip')
        if 'ylim' in self.options:
            ax.set_ylim(self.options['ylim'])
        if 'yticks' in self.options:
            ax.set_yticks(self.options['yticks'])
        if 'ylabel' in self.options:
            ax.set_ylabel(self.options['ylabel'],multialignment='center')
        if rcParams['text.usetex']:
            if 'ylabel_tex' in self.options:
                ax.set_ylabel(self.options['ylabel_tex'],multialignment='center')
        if 'specplot' in self.options and self.options['specplot'] == True:
            self.specplot(ax,trange)
        else:
            if 'reduced' in self.options and 'level' in self.options:
                plotlines = [n for n, l in enumerate(self.data.columns) if l[:1].isdigit()]
                labels = [l for l in self.data.columns if l.startswith(self.options['reduced'])]
                it = itertools.cycle(['b', 'r', 'g', 'y', 'k']); my_colors=[next(it) for i in xrange(len(labels))]
                self.data[plotlines].plot(ax=ax,legend=legend,color=my_colors)
                for i, label in enumerate(labels):
                    label_text = '{0:.1f} eV'.format(np.mean(self.data[label]))
                    matplotlib.pyplot.text(1.02, (i+0.5)/float(len(labels)),label_text,
                           horizontalalignment='left',color=my_colors[i],
                           transform = ax.transAxes,size='small')
            else:    
                mplot = self.data.plot(ax=ax,legend=legend)
                mplot_leglines = (mplot.get_legend_handles_labels())[0]
                if len(mplot_leglines) > 1:
                    cols = [mplot_leglines[i].get_color() for i in range(len(mplot_leglines))]

                    ylabs = self.interp([max(trange)]).values.flatten()
                    ylabs = self.data[:max(trange)].tail(1).values.flatten()

                    trans = transforms.blended_transform_factory(ax.transAxes, ax.transData)

                    for i in range(len(ylabs)):
                        label_text = self.data.columns[i]
                        matplotlib.pyplot.text(1.02, ylabs[i],label_text,
                                               horizontalalignment='left',color=cols[i],
                                               transform = trans)

            fig = plt.gcf()
            from mpl_toolkits.axes_grid1 import make_axes_locatable
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", "3%", pad="3%")
            fig.add_axes(cax)
            cax.axis('off')

        spacepy_utils.applySmartTimeTicks(ax,trange,dolimit=True)
       
    def specplot(self,ax,trange):
        import numpy as np
        import math
        
        zcols = [n for n, l in enumerate(self.data.columns) if l[:1].isdigit()]
        ycols = [n for n, l in enumerate(self.data.columns) if l.startswith(self.options['reduced'])]

        zdata0 = self.data[zcols]
        ydata0 = self.data[ycols]

        patch_nan = ydata0*np.NaN
        patch_nan.plot(ax=ax,legend=False)
        spacepy_utils.applySmartTimeTicks(ax,trange,dolimit=True)

        patch_nan = ydata0*np.NaN
        patch_nan.plot(ax=ax,legend=False)
        spacepy_utils.applySmartTimeTicks(ax,trange,dolimit=True)
               
        ydata = ydata0[trange[0]:trange[1]]
        zdata = zdata0[trange[0]:trange[1]]
        zdata.columns = ydata.columns

        trange_d = DatetimeIndex(trange).values.astype('d')
        xinterp = np.linspace(min(trange_d),max(trange_d),400)

        yrange = ax.get_ylim()
        yinterp = np.linspace(min(yrange),max(yrange),200)
        #print(yinterp)
        
        x_i = ydata.index.values.astype('d')
        y = ydata.values
        x = np.empty(shape = y.shape,dtype=float)

        for i in range(len(ydata.columns)):
            x[:,i]=x_i

        xind = np.empty(shape=(len(xinterp),len(yinterp)),dtype=int)
        xind_i = [(np.abs(x[:,0]-xt)).argmin() for xt in xinterp]
        for index in range(len(yinterp)):
            xind[:,index] = xind_i

        yind = np.empty(shape=(len(xinterp),len(yinterp)),dtype=int)
        old_yx_ind = [-1]
        for index in range(len(xinterp)):
            yx_ind = xind[index,0]
            if yx_ind != old_yx_ind:
                yind_i = [(np.abs(y[yx_ind,:]-yt)).argmin() for yt in yinterp]
                old_yx_ind = yx_ind
            yind[index,:] = yind_i
            
        zint = (np.log10(zdata.values))[xind,yind].transpose()


        plt.imshow(zint,extent = [min(ax.get_xlim()),max(ax.get_xlim()),
                                  min(yrange),max(yrange)],
                                  interpolation='nearest',origin='lower',
                                  aspect='auto')
        
        zmax = np.nanmax(np.log10(zdata.values))
        zmin = np.nanmin(np.log10(zdata.values))
                
        zticks = range(int(math.floor(zmin)),int(math.ceil(zmax)))
        
        sm = plt.cm.ScalarMappable(cmap=plt.cm.get_cmap('jet'), norm=plt.Normalize(vmin=zmin, vmax=zmax))
        sm._A = []
        fig = plt.gcf()
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", "3%", pad="3%")
        fig.add_axes(cax)
        cbar = plt.colorbar(sm,cax=cax)
        if 'zlabel' in self.options:
            cbar.ax.set_ylabel(self.options['zlabel'])
        cbar.set_ticks(zticks)

    def reduce(self,level,index):
        import pandas
        
        leveldata = self.data.xs('-',axis=1,level=level)
        data = self.data.xs(index,axis=1,level=level)

        levelcol = leveldata.columns
        levelcol = [str(x) for x in range(len(levelcol))]
        levels = self.data.axes[1].names
        levels_remaining = []
        for level_test in levels:
            if level_test != level:
                levels_remaining.append(level_test)
        levelcol = ["".join([levels_remaining[0],levelcol[x]]) for x in range(len(levelcol))]
        leveldata.columns = levelcol

        datacol = data.columns
        datacol = [str(x) for x in datacol]
        datacol[-1] = level
        data.columns = datacol
        
        reduced_DataFrame = pandas.concat([leveldata,data],axis=1)
        
        reduced = self.__class__(reduced_DataFrame)
                
        if 'ylabel' in self.options:
            old_ylabel = self.options['ylabel']
        else:
            old_ylabel = ''
        
        level_ylabel = '{0:.1f}'.format(data[level].mean())

        if levels_remaining[0] == 'pangle':
            reduced.set_options({'specplot':True})        
            reduced.set_options({'ylim':[0.,180.],'yticks':[0.,45.,90.,135.,180.],
                                 'ylabel':old_ylabel + ' PAD\n' + level_ylabel + ' eV',
                                 'zlabel':'Log Flux'})
            
        if levels_remaining[0] == 'energy':
            reduced.set_options({'ylog':True,'panel_size':2.,
                                 'ylabel':old_ylabel + ' Flux\n' + level_ylabel + ' deg.'})
        reduced.set_options({'index':index})
        reduced.set_options({'level':level})
        reduced.set_options({'reduced':levels_remaining[0]})
        
        
        return(reduced)
                
    def unset_options(self,keys):
        for key in keys:
            if key in self.options:
                del self.options[key]
                
    def interp(self,times):
        from scipy.interpolate import interp1d
        import numpy as np
        int_ts = self.data.dropna()
        xi = int_ts.index.values.astype('d')
        xo = DatetimeIndex(times).values.astype('d')
        yo = np.empty([len(int_ts.columns),len(xo)])
        for idx, col in enumerate(int_ts.columns):
            int_f = interp1d(xi,int_ts[col].values,bounds_error=False)
            yo[idx,:] = int_f(xo)
        return DataFrame(yo.T, index = times, columns = int_ts.columns)


                
class pytplot():
    def __init__(self,timerange):
        self.timerange = timerange
        self.items = {}
        self.tplot_items = []
        self.options = {}
        
    def set_options(self,options):
        self.options.update(options)
                
    def unset_options(self,keys):
        for key in keys:
            if key in self.options:
                del self.options[key]

    def store(self,newitems):
        self.items.update(newitems)
        
    def names(self,regex):
        matching_keys = []
        reObj = re.compile(regex)
        for key in self.items.keys():
            if(reObj.match(key)):
                matching_keys.append(key)
        return matching_keys
    
    def tplot(self, tplot_items = None, filename = None):
 
        #from matplotlib.dates import DateFormatter
        if tplot_items is None:
            tplot_items = self.tplot_items
        else:
            self.tplot_items = tplot_items
        fig=plt.figure(figsize=(8.5,11))
        panel_sizes = []
        for key in tplot_items:
            if isinstance(key, basestring):
                panel_size = self.items[key].options.get('panel_size',1)
            else:
                panel_size = self.items[key[0]].options.get('panel_size',1)
            panel_sizes.append(panel_size)
        gs = gridspec.GridSpec(len(tplot_items), 1, height_ratios = panel_sizes,hspace=0.2)
        for idx, key in enumerate(tplot_items):
            ax = plt.subplot(gs[idx, 0])
            if 'tlimit' in self.options:
                tlimit = self.options['tlimit']
            else:
                tlimit = self.timerange
            if isinstance(key, basestring):
                self.items[key].tplot(ax,tlimit)
            if idx == 0:
                if 'title' in self.options:
                    ax.set_title(self.options['title'])
            if idx != len(tplot_items)-1:
                #ax.xaxis.set_major_formatter(DateFormatter(""))
                plt.setp(ax.get_xticklabels(),visible=False)
        if filename is None:
            def onclick(event):
                if event.xdata != None and event.ydata != None:
                    print(event.xdata, event.ydata)
            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            plt.show()
        else:
            #fig.tight_layout() #something wrong here
            fig.savefig(filename,dpi=300)
