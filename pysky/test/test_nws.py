import unittest, os, urllib2, re, datetime
from pysky import noaa_ws

from bs4 import BeautifulSoup
from pysky import forecast

_dow = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
latitude = '38.0676808'
longitude = '-81.078070'

class TestNws(unittest.TestCase):

    def test_nws(self):

        nws_data = self._nws_data()
        print(nws_data)

        
        xml = noaa_ws.xml(latitude, longitude)
        pysky_data = forecast.process_xml(xml, False)
        print(pysky_data)

        for d in pysky_data['daily']:
            date = d['date']
            if date in nws_data.keys():
                self.assertEquals(nws_data[date]['high'], d['high'])
                self.assertEquals(nws_data[date]['low'], d['low'])
                #self.assertEquals(nws_data[date]['symbol'].split('.')[0], d['symbol'].split('.')[0])

    def _nws_data(self):

        page = urllib2.urlopen('http://forecast.weather.gov/MapClick.php?lat={0}&lon={1}'.format(latitude, longitude)).read()
        soup = BeautifulSoup(page)
        
        nws_data = {} 
        today = datetime.date.today()
        today_dow = today.weekday()

        for div in soup.find_all('div', 'one-ninth-first'):
            entry_data = {}
           
            # Day string
            day_tags = div.find('p', 'txt-ctr-caps').contents
            day_parts = [c.string for c in day_tags if c.string]
            dow_string = day_parts[0]
            is_night = len(day_parts) == 2

            if not dow_string in _dow:
                continue

            dow = _dow.index(dow_string)

            # Sunday (6) - Monday (0), 1; Wed (2) - Thur(3) = 1
            day_diff = dow - today_dow if dow > today_dow else dow + 7 - today_dow

            date = today + datetime.timedelta(days=day_diff)
            key = date.strftime('%Y-%m-%d')

            if key in nws_data.keys():
                entry_data = nws_data[key]

            #date_string = ' '.join(day_parts)
            #entry_data['date_string'] = date_string

            # Symbol
            symbol = div.find('img').get('src').split('/')[-1]
            symbol_key = 'symbol_night' if is_night else 'symbol'
            entry_data[symbol_key] = symbol

            m = re.search(r'\d+', symbol)
            if m:
                precip_key = 'precip_night' if is_night else 'precip_day'
                entry_data[precip_key] = m.group(0)

            # High/low
            temp_tag = div.find('p', re.compile('^point-forecast-icons-'))
            temp = re.sub(r'\D', '', temp_tag.string)
            temp_type = 'low' if 'point-forecast-icons-low' in temp_tag.get('class') else 'high'
            entry_data[temp_type] = temp

            nws_data[date.strftime('%Y-%m-%d')] = entry_data

        return nws_data

if __name__ == '__main__':
    unittest.main()
