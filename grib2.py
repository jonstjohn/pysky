# Base URL for downloading grib2 files
base_url = 'http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus'
noaa_params = ['maxt', 'temp', 'mint', 'pop12', 'sky', 'wspd', 'apt', 'qpf', 'snow', 'wx', 'wgust', 'icons', 'rhm']
#noaa_params = ['wx']

verbose = False

# Degrib path
degrib_path = '/usr/local/bin/degrib'

def download(data_dir):
    """
    Download grib2 files to data directory

    args:
        data_dir Directory to store data files
    """
    import urllib, re, os, sys, time, urllib2, dateutil
    from datetime import datetime
    from dateutil import tz
    from dateutil.parser import parse

    # Loop over directories that have forecast data files
    for dir in ['VP.001-003','VP.004-007']: # loop over remote directories

        data_subdir = "{0}/{1}".format(data_dir, dir)

        info('Checking directory {0}'.format(dir))

        # Create directory if it doesn't exist
        if not os.path.exists(data_subdir):
            os.mkdir(data_subdir)

        # Get directory listing so we can see if we need a newer version
        f = urllib.urlopen("{0}/{1}/ls-l".format(base_url, dir))
        data = f.read()
        lines = data.split("\n")
  
        # Loop over lines in directory listing
        for line in lines:

            # Check file modified date if this is a .bin file
            if line.find(".bin") != -1:

                # Split line to get date and filename
                month, day, rtime, filename = re.split("\s+", line)[5:9]

                # Split filename to get noaa param name
                param = filename.split('.')[1]

                # Only download files if we are interested in this parameter
                if param in noaa_params:

                    info("%s last modified %s/%s @ %s" % (filename, month, day, rtime))

                    remote_path = "%s/%s/%s" % (base_url, dir, filename)
                    local_path = "{0}/{1}/{2}".format(data_dir, dir, filename)
                    local_time = os.stat(local_path).st_mtime

                    furl = urllib2.urlopen(remote_path)
                    last_modified_str = furl.info()['Last-Modified']
                    remote_time = _utc2local(parse(last_modified_str))

                    # If file does not exist or the local file is older than the remote file, download
                    if not os.path.exists(local_path) or local_time < remote_time:
                        info('Downloading remote file')
                        _download_file(furl, local_path)
                        os.utime(local_path, (remote_time, remote_time))
                    # Otherwise, just log some information
                    else:
                        info('Local file modified: {0} - Remote file modified: {1}'.format(local_time, remote_time))
                        info('Local file is up-to-date, skipping download')
                    
    # Cube data files if any were downloaded - TODO check to see if files were actually downloaded
    cmd = "{degrib} {data_dir}/VP.001-003/*.bin {data_dir}/VP.004-007/*.bin -Data -Index {data_dir}/all.ind -out {data_dir}/all.dat".format(
        degrib = degrib_path,
        data_dir = data_dir
    )
    info(cmd)
    output = ""
    for line in os.popen(cmd).readlines():
    
        output += line
    
    info(output)

def xml(data_dir, latitude, longitude):
    """
    Generate XML file from grib2 data cube

    args:
        data_dir - Directory where grib2 data cube is located
        latitude - Latitude
        longitude - Longitude

    returns - xml string
    """

    import os

    # build and execute command
    cmd = "{degrib_path} {data_dir}/all.ind -DP -pnt {latitude},{longitude} -XML 1 -geoData {data_dir}/geodata".format(
        data_dir = data_dir, latitude = latitude, longitude = longitude, degrib_path = degrib_path)

    info(cmd)
    xml = ""
    for line in os.popen(cmd).readlines():

        xml += line

    # return output
    return xml

def _utc2local(utc):
    """ Convert utc datetime object to local datetime """
    from dateutil import tz
    import time
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = utc.replace(tzinfo = from_zone)
    return time.mktime(utc.astimezone(to_zone).timetuple())

def _download_file(furl, local_path):
    """ Download file given a urllib2 urlopen from remote path to local path """
    with open(local_path, 'wb') as f:
        f.write(furl.read())

def info(str):

    if verbose:

        print(str)
