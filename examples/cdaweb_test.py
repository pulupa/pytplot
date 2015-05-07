import cdaweb
from spacepy import pycdf

year = 2010
month = 1
day = 10

wi_mfi_h0_cdf_file = cdaweb.get_cdaweb_cdf(year, month, day, 'wind', 'mfi', 'mfi_h0', 'wi_h0_mfi')

tha_fgm_cdf_file = cdaweb.get_cdaweb_cdf(year, month, day, 'themis/tha', 'l1/fgm', '', 'tha_l1_fgm')

wi_mfi_h2_cdf_file = cdaweb.get_cdaweb_cdf(year, month, day, 'wind', 'mfi', 'mfi_h2', 'wi_h2_mfi')

print(pycdf.CDF(wi_mfi_h2_cdf_file))


'''
Created on Jul 11, 2013

@author: pulupa
'''
