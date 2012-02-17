# PySky - the Python Weather Toolkit

PySky is a python weather toolkit that provides access into a number of publicly available weather databases.  The goal of PySky is to provide a fast and easy-to-use interface to weather data in a pythonic way.  The current implementation focuses on United States weather data from NOAA, although future weather systems will be incorporated.  In particularly, it provides hourly and daily forecast summaries.

## Working with the module

The toolkit has several command-line scripts that return formatted weather data.  

To obtain forecast data, forecast.py is used.  For quick and dirty forecasts, forecast.py will use the NOAA XML web service to obtain forecast information.  For more robust applications, users of forecast.py will want to use the grib2 option.  The grib2 option downloads NOAA grib2 files which provide forecast elements for the entire United States.  Querying grib2 data is much faster and efficient than querying the XML web service.

    forecast.py (--hourly) (--grid2) [latitude] [longitude]

Return values are JSON encoded arrays/objects. 

