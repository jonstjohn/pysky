from xml.etree import ElementTree

_codes =  {
    'Daily Maximum Temperature' : 'maxt',
    'Daily Minimum Temperature' : 'mint',
    '12 Hourly Probability of Precipitation' : 'pop12',
    'Temperature' : 'temp',
    'Dew Point' : 'td',
    'Apparent Temperature' : 'apt',
    'Cloud Cover Amount' : 'sky',
    'Wind Direction' : 'wdir',
    'Wind Speed' : 'wspd',
    'Wind Speed Gust' : 'wgust',
    'Weather Type, Coverage, and Intensity' : 'wx',
    'Liquid Precipitation Amount' : 'qpf',
    'Snow Amount' : 'snow',
    'Relative Humidity' : 'rhm',
    'Conditions Icons' : 'sym'
}

# Parse xml string
def parse_xml(xml):
        
    tree = ElementTree.fromstring(xml)

    # Parse timelayouts
    timelayouts = _parse_time_layouts(tree)

    # Parse parameter data
    data = _parse_parameter_data(tree, timelayouts)

    return data
        
def _parse_time_layouts(tree):
    """
    Parse time layouts

    args:
        tree - etree tree
    returns:
        dictionary of timelayouts
            key is DWML unique layout key
            value is list of start date and end date
    """        
        
    timelayouts = {}
    for timelayout in tree.getiterator("time-layout"):
            
        currentKey = ''
        position = -1
        for child in timelayout.getchildren():
            
            if (child.tag == 'layout-key'):
                currentKey = child.text
                position = -1
                timelayouts[child.text] = []
                    
            if (child.tag == 'start-valid-time'):
                position = position + 1
                timelayouts[currentKey].append(['',''])
                xmlDate = child.text
                        
                timelayouts[currentKey][position][0] = _convert_xml_date(xmlDate)
                    
            if (child.tag == 'end-valid-time'):
                    
                xmlDate = child.text
                        
                timelayouts[currentKey][position][1] = _convert_xml_date(xmlDate)
                    
    return timelayouts
        
def _parse_parameter_data(tree, timelayouts):
        
    parameter_data = {}
        
    # Loop over parameters
    for parameters in tree.getiterator('parameters'):
            
        currentCode = ''
            
        # Loop over each parameter
        for parameter in parameters.getchildren():
                
            # If a time-layout attribute exists, we have a parameter element
            if 'time-layout' in parameter.attrib:
                    
                valueCount = 0
                timeLayoutKey = parameter.attrib['time-layout']
                
                for child in parameter.getchildren():
                        
                    value = ''
                    if child.tag == 'name':
                            
                        name = child.text
                        currentCode = _codes[name]
                        parameter_data[currentCode] = {
                            'name': name, 
                            'values': []
                            }
                        continue
                        
                    # Grab values for regular 'value' or 'icon-link' tags
                    elif child.tag == 'value' or child.tag == 'icon-link':
                        value = child.text
                        if value is None:
                            value = ''
                            
                    # Special values for weather conditions
                    elif child.tag == 'weather-conditions':
                        
                        value = ''
                        for nextchild in child.getchildren():
                            
                            if nextchild.tag == 'value':
                                
                                weatherData = {'coverage':'', 'intensity':'', 'weather-type':'', 'qualifier':''}
                                for k, v in nextchild.attrib.items():
                                    weatherData[k] = v
                                    
                                value += "|coverage:{0}|intensity:{1}|weather-type:{2}|qualifier:{3}".format(weatherData['coverage'], weatherData['intensity'], weatherData['weather-type'], weatherData['qualifier'])
                                #value += "|{0}:{1}".format(k, v)
                                        
                    else:
                            
                        continue
                    #if value is not None or child.tag == 'weather-conditions': # weather-conditions has blank values
                        #print timeLayoutKey
                        #print timelayouts[timeLayoutKey]
                    start = timelayouts[timeLayoutKey][valueCount][0]
                    startDate, startTime = start.split(' ') if len(start) else ['', '']
                    end = timelayouts[timeLayoutKey][valueCount][1]
                    endDate, endTime = end.split(' ') if len(end) else ['', '']
                    parameter_data[currentCode]['values'].append(
                        { 
                            'value': value, 
                            'start': start,
                            'startDate': startDate,
                            'startTime': startTime,
                            'end': end,
                            'endDate': endDate,
                            'endTime': endTime
                        }
                    )
                    
                    valueCount += 1

    return parameter_data
                
def _get_xml_from_date_object(dateObject):
        
    return dateObject.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
def _get_date_object_from_xml(xmlDate):
        
    import datetime
    from datetime import timedelta
    year = int(xmlDate[0:4])
    month = int(xmlDate[5:7])
    day = int (xmlDate[8:10])
    hour = int(xmlDate[11:13])
    min = int(xmlDate[14:16])
    sec = int(xmlDate[17:19])
    offsetDirection = xmlDate[19:20]
    offsetHour = int(xmlDate[20:22])
    offsetMinute = int(xmlDate[23:25])
    d = datetime.datetime(year, month, day, hour, min, sec)
    return d

# Convert XML date to SQL
def _convert_xml_date(xml_date):

    if not len(xml_date):
        return ''

    sql_date, sql_time = xml_date.split('T')
    sql_time, offset = sql_time.split('-')
    hour, minute, second = sql_time.split(':')
    sql_time = "%s:%s:%s" % (hour, minute, second)
    return sql_date + ' ' + sql_time
