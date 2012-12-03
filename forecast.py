import dwml

_hourly_params = { 'snow_amount': 'snow', 'temp': 'temp', 'humidity': 'rhm', 'precip': 'pop12', 'rain_amount': 'qpf',
     'sky': 'sky', 'weather': 'wx', 'symbol': 'sym', 'wind_gust': 'wgust', 'wind_sustained': 'wspd'}

class forecastData(dict):

    def __repr__(self):
        """
        Display forecast data dictionary as well-formatted string
        """
        str = "Hourly:\n"
        date = ''
        for h in self['hourly']:
            if  date != h['date']:
                str += "  {0}\n".format(h['date'])
                date = h['date']
            str += "    {0} -- ".format(h['time'])
            for param in ('temp', 'precip', 'rain_amount', 'snow_amount', 'sky', 'wind_gust', 'wind_sustained', 'humidity', 'symbol', 'weather'):
                if param in h:
                    str += "{0}: {1} ".format(param, h[param] if len(h[param]) else '-')
            str += "\n"

        str += "Daily:\n"
        for d in self['daily']:
            str += "  {0} -- ".format(d['date'])
            for param in ('high', 'low', 'precip_day', 'precip_night', 'rain_amount', 'snow_amount', 'humidity', 'wind_speed', 'wind_gust', 'symbol', 'weather'):
                if param in d:
                    str += "{0}: {1} ".format(param, d[param] if d[param] else '-')
            str += "\n"

        return str

def process_xml(xml, include_hourly = False):
    """
    Process XML string and return forecast data
    
    args:
        xml - XML string
        include_hourly - Include hourly forecast

    returns: dictionary, see README
    """
    # Parse DWML into python object
    xml_data = dwml.parse_xml(xml)

    return forecastData({'daily': _daily(xml_data), 'hourly': _hourly(xml_data)})
    #self._cleanup()

def _daily(xml_data):
    """
    Get daily forecast data

    args:
        xml_data - dictionary returned from process_xml, see README
    returns: list, see README
    """
    daily_data = []
    # Organize data by date
    #   Format will be tmp_data with date as keys
    #       tmp_data[*date*][*code*] = {values: [*vals*], startDate: *startDate*, endDate: *endDate*}
    tmp_data = {}
    for code in xml_data:
        for val_data in xml_data[code]['values']:
            date = val_data['startDate'] # Use start date as daily date
            if date not in tmp_data:
                tmp_data[date] = {}
                #daily_data[date] = {}
            if code not in tmp_data[date]:
                tmp_data[date][code] = []
            tmp_data[date][code].append(val_data)

    # Loop over tmp_data
    config = _daily_config
    dates = tmp_data.keys()
    dates.sort()
    for date in dates: # date
        date_data = {'date': date}
        for key in config: # key
            code = config[key]['code']
            if code in tmp_data[date]:
                date_data[key] = _aggregate_values(
                    tmp_data[date][code], 
                    config[key]['aggregator'],
                    config[key]['pre_filter'] if 'pre_filter' in config[key] else None,
                    config[key]['formatter'] if 'formatter' in config[key] else None
                )

        daily_data.append(date_data)

    return daily_data

def _hourly(xml_data):
    """
    Get hourly forecast data

    args:
        xml_data - dictionary returned from process_xml, see README
    returns: list, see README
    """
    # Organize data by date/time
    #       tmp_data[*date*][*time*][*code*] = *value*
    tmp_data = {}
    for code in _hourly_params.itervalues():
        for val_data in xml_data[code]['values']:
            date = val_data['startDate']
            time = val_data['startTime']
            if date not in tmp_data:
                tmp_data[date] = {}
            if time not in tmp_data[date]:
                tmp_data[date][time] = {}
            tmp_data[date][time][code] = val_data['value']
    config = _hourly_config
    
    # Sort into correct order
    date_times = []
    for date in tmp_data:
        for time in tmp_data[date]:
            date_times.append("{0} {1}".format(date, time))

    date_times.sort()

    # Add to hourly data list
    hourly_data = []
    for dt in date_times:
        date, time = dt.split(' ')
        time_data = {'date': date, 'time': time}
        for key in config:
            code = config[key]['code']
            if code in tmp_data[date][time]:
                val = tmp_data[date][time][code] if 'formatter' not in config[key] else config[key]['formatter'](tmp_data[date][time][code])
                time_data[key] = val 
        hourly_data.append(time_data)
    return hourly_data

def _first(values):
    """
    Aggregate by first value
    Arg: values - list of values
    Returns: first value
    """
    return values[0] if len(values) else None

def _average(values):

    """
    Aggregate by average value
    Arg: values - list of values
    Returns: average value
    """
    if not len(values):
     return None

    return sum([float(x) for x in values])/len(values)

def _first_nonempty(values):
    """
    Aggregate by first non-empty
    Args: values - list of values
    Returns: first non-empty value
    """
    if not len(values):
        return None

    for val in values:
        if len(val) > 0:
            return val

def _frequent_sym(values):
    """
    Aggregate by most frequently used values
    Args: values - list of values
    Returns: most frequently appearing value
    """
    if not len(values):
        return None

    counts = {}
    for val in values:
        # Skip night-time
        if val.split('/')[-1][0] == 'n':
            continue
        if not counts.has_key(val):
            counts[val] = 0
        counts[val] += 1
    maxCount = 0
    for k, v in counts.iteritems():
        if v > maxCount:
            val = k
            maxCount = v
    return val

def _aggregate_values(value_data, aggregator, pre_filter=None, formatter=None):
    """
    Aggregate values using optional filter and format functions

    args:
        values - list of values to aggregate
        pre_filter - filter function
        formatter - format function
    """
    # Apply filter
    values = pre_filter(value_data) if pre_filter else _pre_values(value_data)

    # Aggregate
    val = aggregator(values)

    # Apply formatter
    if formatter:
        val = formatter(val)

    return val

def _pre_values(value_data):
    """
    Convert extra values from value data, which also contains date/time information.  Default pre- filter
    args:
        value_data - array of dictionaries containing value and date data
    returns:
        values - list of values
    """
    return [val['value'] for val in value_data]
       
def _pre_precip_day(value_data):
    """
    Pre- filter function for daily precipitation % that excludes 12-hour precipitation data
        that crosses a date (e.g., start=1/1/12 end=1/2/12)
    """
    return [val['value'] for val in value_data if val['startDate'] == val['endDate']]

def _pre_precip_night(value_data):

    """
    Pre- filter function for nightly precipitation % that excludes 12-hour precipitation data
        that is on the same date (e.g., start=1/1/12 end=1/2/12)
    """
    return [val['value'] for val in value_data if val['startDate'] != val['endDate']]

def _pre_rain_amount(value_data):
    """
    Pre- filter for rain amount
      Removes zero-length values and converts remaining to float and rounds to 2 decimals
    """
    return [round(float(val['value']), 2) for val in value_data if len(val['value'])]

def _pre_snow_amount(value_data):
    """
    Pre- filter for snow amount
        Removes zero-length values and converts remaining to float and rounds to 1 decimal
    """
    return [round(float(val['value']), 1) for val in value_data if len(val['value'])]

def _pre_weather(value_data):
    """
    Pre- filter for weather that skips weather between 6PM and 6AM so we get daytime conditions
    """
    return [val['value'] for val in value_data if val['startTime'] >= '06:00:00' and val['startTime'] <= '18:00:00']

def _pre_wsym(value_data):
    """
    Pre- filter for weather symbols, skips if empty or does not contain path
    """
    return [val['value'] for val in value_data if len(val['value']) and val['value'].find('/') != -1]

def _format_wind(value):
    """
    Format function for wind, convert from knots to MPH
    """
    return "%.1f" % round(float(value) * 1.15077945, 1) if value else '' # convert from knots to MPH

def _format_weather(value):
    """
    Format function for weather
    """
    # Check for format
    if not value or len(value.strip('|').split('|')) < 3:
        return ''

    # Get coverage, intensity and weather type elements
    coverage_element, intensity_element, weather_type_element = value.strip('|').split('|')[0:3]

    # Get coverage from coverage element
    coverage = coverage_element.split(':')[1]

    # Get intensity from intensity element
    intensity = intensity_element.split(':')[1]
    weather = weather_type_element.split(':')[1]

    if intensity != 'none':
        weather = "{0} {1}".format(intensity, weather)

    str = ''
    if coverage == 'likely':
        str = "{0} {1}".format(weather, coverage)
    elif coverage == 'chance' or coverage == 'slight chance':
        str = "{0} of {1}".format(coverage, weather)
    elif coverage == 'definitely':
        str = weather
    else:
        str = "{0} {1}".format(coverage, weather)

    return str


def _format_wsym(value):
    """
    Form function for symbols, return only image
    """
    return value.split('/')[-1] if value else ''

# Parsing configuration
# Includes:
#   DWML NOAA code - required
#   aggregator: determines how to aggregate the data - required
#   pre-filter: method that takes values as arguments and returns values that should be aggregated
#   formatter: method that applies formatting to resulting aggregated value
_daily_config = {
    'high': {'code': 'maxt', 'aggregator': _first},
    'low': {'code': 'mint', 'aggregator': _first},
    'precip_day': {'code': 'pop12', 'aggregator': _first, 'pre_filter': _pre_precip_day},
    'precip_night': {'code': 'pop12', 'aggregator': _first, 'pre_filter': _pre_precip_night},
    'rain_amount': {'code': 'qpf', 'aggregator': sum, 'pre_filter': _pre_rain_amount},
    'snow_amount': {'code': 'snow', 'aggregator': sum, 'pre_filter': _pre_snow_amount},
    'humidity': {'code': 'rhm', 'aggregator': _average},
    'wind_gust': {'code': 'wgust', 'aggregator': max, 'formatter': _format_wind},
    'wind_sustained': {'code': 'wspd', 'aggregator': _average, 'formatter': _format_wind},
    'weather': {'code': 'wx', 'aggregator': _first_nonempty, 'pre_filter': _pre_weather, 'formatter': _format_weather},
    'symbol': {'code': 'sym', 'aggregator': _frequent_sym, 'pre_filter': _pre_wsym, 'formatter': _format_wsym}
}

_hourly_config = {
    'temp': {'code': 'temp'},
    'precip': {'code': 'pop12'},
    'humidity': {'code': 'rhm'},
    'rain_amount': {'code': 'qpf'},
    'snow_amount': {'code': 'snow'},
    'wind_gust': {'code': 'wgust', 'formatter': _format_wind},
    'wind_sustained': {'code': 'wspd', 'formatter': _format_wind},
    'sky': {'code': 'sky'},
    'weather': {'code': 'wx', 'formatter': _format_weather},
    'symbol': {'code': 'sym', 'formatter': _format_wsym}
}



# Aggregate 3-hour values using a function
# @param int code Noaa parameter code
# @param string function Name of aggregate function, 'sum', 'average', 'max', 'min'
# @param boolean isNumeric T: value is numeric
# @param int decimal Number of places to round to
# @param function skipFunction Function used to determine if value should be skipped
# @param function formatFunction Function used to format value
# @return null
#def _aggregate(xml_data, code, label, function, isNumeric = True, decimal = 0, 
#                   skipFunction = None, formatFunction = None):
#       
#    # Setup tmpData to store temporary data ??
#    tmpData = {}
#
#    # Loop over the values associated with this parameter
#    #   Initialize tmpData for each date and add values
#    for vData in xml_data[code]['values']:
#           
#        # Get start date and initialize temporary data with start date key
#        startDate = vData['startDate']
#        if startDate not in tmpData:
#            tmpData[startDate] = []
#            
#        # Get value
#        val = vData['value']
#        
#        # Convert to float if this value is supposed to be numeric and has length
#        if isNumeric and len(val) > 0:
#            val = float(val)
#           
#        # Check to see that skip function does not exist, or when applied to value does not get skipped
#        #    Add to tmpData
#        if not skipFunction or not skipFunction(vData):
#            tmpData[startDate].append(val)
#               
#    # Loop over all the dates
#    for date in tmpData:
#           
#        # Initialize date in forecast data
#        #self._initDate(date)
#        if date not in self.forecastData['daily']:
#            self.forecastData['daily'][date] = {}
#       
#        # Get values for date
#        vals = tmpData[date]
#           
#        # If not values for this date, continue
#        if len(vals) == 0:
#                
#            continue
#            
#        # If measuring rain amount and don't have a full 3 data points
#        # May be slightly inaccurate
#        if code in ('qpf', 'snow') and len(vals) < 3:
#                
#            continue
#            
#        # Apply aggregate function
#        if function == 'average':
#            val = sum(vals)/len(vals)
#        elif function == 'sum':
#            val = sum(vals)
#        elif function == 'max':
#            val = max(vals)
#        elif function == 'min':
#            val = min(vals)
#        elif function == 'first':
#            val = vals[0]
#        elif function == 'first-nonempty':
#            for val in vals:
#                if len(val) > 0:
#                    break
#        elif function == 'frequent':
#            counts = {}
#            for val in vals:
#                if not counts.has_key(val):
#                    counts[val] = 0
#                counts[val] = counts[val] + 1
#            maxCount = 0
#            for k, v in counts.iteritems():
#                if v > maxCount:
#                    val = k
#                    maxCount = v
#        else:
#            val = vals[0]
#            
#        if isNumeric:
#            if decimal == 0:
#                val = int(val)
#            else:
#                val = round(val, decimal)
#                
#        if formatFunction:
#            
#            val = formatFunction(val)
#           
#        return val 
#        #self.forecastData['daily'][date][label] = val

# Convert XML date to SQL - TODO - look at what we are doing here with the timezone offset
#def _convert_xml_datetime_sql(xml_date):
#
#    if len(xml_date):
#
#        sql_date, sql_time = xml_date.split('T')
#        #date_str = date_str.replace('-04:00','')
#        sql_time, offset = sql_time.split('-') # do nothing with offset - this is local time
#        hour, minute, second = sql_time.split(':')
#        #offset_hour, offset_minute = offset.split(':')
#        #offset_hour_difference = int(offset_hour) - 4 # Use 4 since this is what our standard was initially - will probably need to change
#        #hour = int(hour)+int(offset_hour_difference)
#        sql_time = "%s:%s:%s" % (hour, minute, second)
#        return sql_date + ' ' + sql_time
#
#    else:
#
#        return ''
