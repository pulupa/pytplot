import hashlib
import os.path
import re
import urllib2
import numpy as np

def sha1hash(filepath):
    """Return the SHA1 hash of an input file."""
    f=open(filepath,'rb')
    fstr = f.read()
    sha1 = hashlib.sha1(fstr)
    sha1_str = sha1.hexdigest()
    return sha1_str

def get_cdaweb_cdf(year,mon,day,spacecraft,instrument,datatype,prefix):
    """Download data from CDAWeb
    
    This function determines whether a local copy of a CDF file exists, 
    checks it against the CDAWeb website, and downloads a copy if the
    folder is not present or is outdated.  CDAWeb directories contain
    lists of SHA1 hash values for each file in the directory, which is 
    used to test whether a new file needs to be downloaded.  A string
    containing the local location of the relevant CDF file is returned.
    
    year -- the year
    mon  -- the month
    day  -- the day of the month
    spacecraft -- the spacecraft
    instrument -- the instrument
    datatype -- the type of data
    prefix -- CDF file prefix

    Note that the spacecraft, instrument, and datatype keywords should,
    when concatenated, correspond to a subdirectory of the CDAWeb file system.
    That subdirectory should contain per-year folders of the desired data, 
    with each of the per-year folders containing CDF files beginning with
    the prefix keyword.  The exact syntax of the file structure varies by 
    spacecraft and instrument.  Since all the program does is concatenate them,
    all that matters is that they point to the right directory once they have
    been concatenated.
    
    Current limitations:
    1. Uses a hardwired local data directory (should be user settable).
    2. Must be online (should default to local directory if offline).
    3. Needs to be able to gracefully handle incorrect input (currently just
    chokes on a HTTP 404 if, e.g., there is a typo in the directory)
    
    """
    home_dir = os.path.expanduser("~")
    local_base_dir = os.path.join(home_dir,"Data/cdaweb")
    local_item_dir = os.path.join(spacecraft,instrument,datatype)
    cdf_regex = prefix + '_' + "{0:04d}".format(year) + "{0:02d}".format(mon) + "{0:02d}".format(day) + "_v\d\d.cdf"
    cdaweb_url = "http://cdaweb.gsfc.nasa.gov/pub/data/"

    local_full_dir = os.path.join(local_base_dir,local_item_dir,"{0:04d}".format(year))
    if not os.path.exists(local_full_dir):
        os.makedirs(local_full_dir)

    remote_full_dir = os.path.join(cdaweb_url,local_item_dir,"{0:04d}".format(year))
    #print(remote_full_dir)

    remote_index = np.genfromtxt(urllib2.urlopen(remote_full_dir + "/SHA1SUM"),
                                 comments='#',delimiter='  ',dtype='str')
    index_sha1 = remote_index[:,0]
    index_cdfs = remote_index[:,1]

    #print(index_sha1)
    #print(index_cdfs)
    #print(cdf_regex)

    re_cdf = re.compile(cdf_regex)

    cdf_search = filter(re_cdf.search,index_cdfs)

    cdf_found = len(cdf_search) > 0

    if cdf_found:
        cdf_name = (max(cdf_search))
        remote_file = os.path.join(remote_full_dir,cdf_name)
        remote_sha1 = index_sha1[(np.where(index_cdfs==cdf_name))[0][0]]
        #print(remote_sha1)
        local_file = os.path.join(local_full_dir,cdf_name)
        if os.path.isfile(local_file):
            local_sha1 = sha1hash(local_file)
        else:
            local_sha1 = ""
        #print(local_sha1)
        #print(remote_sha1)
        print("Latest version of file on CDAWeb server:")
        print(remote_file)
        if local_sha1 != remote_sha1:
            print("Downloading file to:")
            print(local_file + "\n")
            u_download = urllib2.urlopen(remote_file)
            f_download = open(local_file,'w')
            f_download.write(u_download.read())
            f_download.close()
        else:
            print("Current version already downloaded in local file:")
            print(local_file+ "\n")
        return(local_file)
    else:
        print("No CDF found matching " + cdf_name)
        return("")
'''
Created on Jul 11, 2013

@author: pulupa
'''
