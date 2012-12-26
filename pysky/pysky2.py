#!/usr/bin/python

from pysky import grib2
from pysky import dwml
from pysky import forecast
from pysky import noaa_ws
import json

degrib_path = '/usr/local/bin/degrib'
verbose = False


def get_forecast(latitude, longitude,
                 include_hourly=False, grib2_dir=None):
    """
    Main method determines forecast based on latitude and longitude and returns
    json-formatted result

    Args:
        latitude - forecast point latitude
        longitude - forecast point longitude
        include_hourly - flag to include hourly forecast, defaults to false
        grib2_dir - grib2 data directory, if omitted,
            the SOAP web service will be used

    Returns: json-formatted string - see README
    """

    info("Latitude: {0}".format(latitude))
    info("Longitude: {0}".format(longitude))
    if include_hourly:
        info("Include hourly forecast")
    if grib2_dir:
        info("Using grib2 dir: {0}".format(grib2_dir))

    # If grib2 directory is provided, use grib2 files
    if grib2_dir:
        grib2.verbose = verbose
        xml = grib2.xml(grib2_dir, latitude, longitude)
        info(xml)
    # Otherwise, use SOAP web service
    else:
        xml = noaa_ws.xml(latitude, longitude)
        info(xml)

    # Initialize object for data
    print(forecast.process_xml(xml, include_hourly))  # TODO fix json call
    #print(json.dumps(forecast.process_xml(xml, include_hourly))) # TODO fix


def download(grib2_dir=None):
    """
    Download grib2 files

    Args:
        grib2_dir - grib2 data directory, if omitted, the current directory is used
    """
    import os

    grib2.verbose = verbose
    grib2_dir = grib2_dir if grib2_dir else os.path.abspath(os.path.dirname(__file__)) # use current dir if none provided
    grib2.download(grib2_dir)


def info(str):
    """
    Print info string, to STDOUT when verbose mode is enabled

    Args:
        str - info string
    """
    if verbose:

        print(str)


if __name__ == '__main__':

    from optparse import OptionParser

    usage = "usage:\n%prog download [options]\n%prog forecast [options] LATITUDE LONGITUDE"
    parser = OptionParser(usage)

    parser.add_option('-o', '--hourly', dest='include_hourly', default=False,
        action='store_true',
        help='Include hourly forecast')
    parser.add_option('-g', '--grib2-dir', dest='grib2_dir',
        action='store',
        help='Directory to download grib2 files to')
    parser.add_option('-v', '--verbose', dest='verbose', default=False,
        action='store_true',
        help='Show verbose output')

    (options, args) = parser.parse_args()

    # Get action, either 'forecast' or 'download'
    if len(args) == 0 or args[0] not in ('download', 'forecast'):
        parser.error("Action 'download' or 'forecast' is required as the first argument")

    action = args[0]
    verbose = options.verbose

    # Download action
    if action == 'download':

        download(options.grib2_dir)

    # Forecast action
    elif action == 'forecast':
        
        if len(args) != 3:
            parser.error("Latitude and longitude are required arguments")

        latitude = args[1]
        longitude = args[2]
        get_forecast(latitude, longitude, options.include_hourly, options.grib2_dir)
