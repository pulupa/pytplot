# Load dependencies
import pytplot
import datetime as dt
import os
import matplotlib
from matplotlib import rcParams
import load_wi

# Set matplotlib parameters

rcParams['xtick.direction'] = 'out'; rcParams['ytick.direction'] = 'out';

# Set PATH parameters.  I needed to do this in the Eclipse IDE, whether or not this is necessary 
# depends on your environment setup.  In my IDE, if these were not set, the program could not
# find LaTeX or ghostscript.

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'
os.environ['PATH'] = os.environ['PATH'] + ':/usr/local/bin'

# Select a time range
trange = [dt.datetime(1998,8,26,0),dt.datetime(1998,8,27,0)]

# Create a tplot item with the specified time range.  This item is analogous to the 
# TPLOT structure in the IDL version of TDAS.  It functions as a container for the
# various time series items.
tp = pytplot.pytplot(trange)
tp.set_options({'title':'Wind: 26 Aug 1998'})

# Load and store Wind MFI data and Wind 3DP electron data.
tp.store(load_wi.load_wi_mfi(trange))
tp.store(load_wi.load_wi_elpd(trange))

# Get a list of all stored items, using a regular expression.
print(tp.names("\S*"))

# Retrieve a single data item.
wi_dat = tp.items['wi_mfi_h0_B3GSE']

# Print a time subrange.
print(wi_dat.data[dt.datetime(1998,8,26,6,59,50):dt.datetime(1998,8,26,7,0,10)])

# Print the first point after a specific time.
print(wi_dat.data[dt.datetime(1998,8,26,7):].head(1))

# Print the three points previous to a specific time.
print(wi_dat.data[:dt.datetime(1998,8,26,7)].tail(3))

# Interpolate to several specified times (outside of the loaded timerange returns NaN).
print(wi_dat.interp([dt.datetime(1998,8,26,7),dt.datetime(1998,8,26,7,0,10),dt.datetime(1998,8,31)]))

# Create pitch angle distribution for energy channel 5
el_pad = tp.items['wi_3dp_elpd'].reduce('energy',5)
tp.store({'wi_3dp_elpd_pad_5':el_pad})

# Create energy plot for pitch angle 5
el_spec = tp.items['wi_3dp_elpd'].reduce('pangle',5)
tp.store({'wi_3dp_elpd_espec_5':el_spec})

# Make a plot.
tp.tplot(tplot_items = ['wi_mfi_h0_B3GSE', 'wi_mfi_h0_B3F1','wi_3dp_elpd_pad_5','wi_3dp_elpd_espec_5'])

#tp.select()

# Set the plot time range and plot again.
tp.set_options({'tlimit':[dt.datetime(1998,8,26,6,10),dt.datetime(1998,8,26,7,20)]})
tp.tplot()

# Output an EPS plot, using TeX to format text.
rcParams['text.usetex'] = 'True'
plotfile = os.path.join(os.path.expanduser("~"),"Dropbox/pytplot/plots") + "/wi_mfi_test.eps"
tp.tplot(filename = plotfile)

plotfile = os.path.join(os.path.expanduser("~"),"Dropbox/pytplot/plots") + "/wi_mfi_test.png"
tp.tplot(filename = plotfile)
