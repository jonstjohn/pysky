PySky - the Python Weather Toolkit
==================================

** Warning: PySky is still under development and incomplete. **

PySky is a python weather toolkit that provides access into a number of publicly available weather databases.  The goal of PySky is to provide a fast and easy-to-use interface to weather data in a pythonic way.  The current implementation focuses on United States weather data from NOAA, although future weather systems will be incorporated.  In particular, it provides hourly and daily forecast summaries.

Working with the module
-----------------------

The toolkit has several command-line scripts that return formatted weather data.  

To obtain forecast data, forecast.py is used.  For quick and dirty forecasts, forecast.py will use the NOAA XML web service to obtain forecast information.  For more robust applications, users of forecast.py will want to use the grib2 option.  The grib2 option downloads NOAA grib2 files which provide forecast elements for the entire United States.  Querying grib2 data is much faster and efficient than querying the XML web service.

.. code-block:: bash

    python bin/download (--grib2-dir=DIR) (--verbose)
    python bin/forecast (--hourly) (--grib2-dir=DIR) (--verbose) LATITUDE LONGITUDE

    Examples:
    python bin/download # download to current directory
    python bin/download --grib2-dir=/tmp # download data files to /tmp
    python bin/forecast --grib2-dir=/tmp -- 38 -81 # get forecast for latitude 38 and longitude -81

Output for the forecast action are JSON encoded values of the following format::

    { 
        'daily' : [
            {
                'date' : *date*
                'high' : *high*,
                'low' : *low*,
                'humidity' : *humidity*,
                'precip_day' : *daytime % chance of precip*,
                'precip_night' : *night time % chance of precip*,
                'rain_amount' : *rain amount in inches*,
                'snow_amount' : *snow amount in inches*,
                'weather': *weather description*,
                'symbol': *weather symbol used by NOAA*,
                'wind_sustained': *sustained wind in MPH*,
                'wind_gust': *wind gusts in MPH* 
            }, ...
        ],
        'hourly' : [
            {
                'date' : *date*,
                'time' : *time*,
                'temp' : *temperature*,
                'humidity' : *% humidity*,
                'precip' : *% chance of precipitation*,
                'rain_amount' : *rain amount in inches*,
                'snow_amount' : *snow amount in inches*,
                'sky' : *% cloud cover*:
                'weather: *weather description*,
                'wind_sustained': *sustained wind in MPH*,
                'wind_gust': *wind guests in MPH 
            }, ...
        ]
     ]   

Requirements
------------

If using grib2 files (not web service), the NOAA degrib library must be installed http://www.nws.noaa.gov/mdl/degrib/ .  In addition, the geodata directory included with the degrib source must be copied to the grib2 data directory.
