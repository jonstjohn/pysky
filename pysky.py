#!/usr/bin/python

import grib2, dwml, forecast, noaa_ws, json

degrib_path = '/usr/local/bin/degrib'
verbose = False

def main(latitude, longitude, include_hourly = False, grib2_dir = None):
    """
    Main method determines forecast based on latitude and longitude and returns json-formatted result

    Args:
        latitude - forecast point latitude
        longitude - forecast point longitude
        include_hourly - flag to include hourly forecast, defaults to false
        grib2_dir - grib2 data directory, if not provided, the SOAP web service will be used

    Returns: json-formatted string - see README
    """

    info("Latitude: {0}".format(latitude))
    info("Longitude: {0}".format(longitude))
    if include_hourly:
        info("Include hourly forecast")
    if grib2_dir:
        info("Using grib2 dir: {0}".format(grib2_dir))

    # If using grib2, use rsync to download if newer data files exist
    if grib2_dir:
        grib2.verbose = verbose
        grib2.download(grib2_dir)
        xml = grib2.xml(grib2_dir, latitude, longitude)
        info(xml)
    else:
        xml = noaa_ws.xml(latitude, longitude)
        info(xml)

    # Initialize object for data
    print(json.dumps(forecast.process_xml(xml, include_hourly))) # TODO fix json call

def info(str):

    if verbose:

        print(str)


if __name__ == '__main__':

    from optparse import OptionParser
    usage = "usage: %prog [options] latitude longitude"
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

    verbose = options.verbose

    if len(args) != 1:
        parser.error("Latitude and longitude are required arguments")

    latitude, longitude = args[0].split(',')

    main(latitude, longitude, options.include_hourly, options.grib2_dir)
