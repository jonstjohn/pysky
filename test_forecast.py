import unittest, os

import forecast

class TestForecast(unittest.TestCase):

    def test_format_wsym(self):
        data = {
            '': '',
            'test.jpg': 'test.jpg',
            '/test.jpg': 'test.jpg',
            '/test/test.jpg': 'test.jpg',
            '/test/test.gif': 'test.gif',
            'http://www.image.com/img/test.png': 'test.png'
        }

        for val, expected in data.iteritems():
            self.assertEqual(forecast._format_wsym(val), expected)

    def test_format_weather(self):
        data = {
            '|coverage:chance|intensity:moderate|weather-type:rain showers|qualifier:none|coverage:slight chance|intensity:none|weather-type:thunderstorms|qualifier:none': 'chance of moderate rain showers',
            '|coverage:slight chance|intensity:moderate|weather-type:rain showers|qualifier:none': 'slight chance of moderate rain showers',
            '|coverage:likely|instensity:heavy|weather-type:rain showers|qualifier:none': 'heavy rain showers likely',
            '': '',
            '|coverage|': ''
        }

        for val, expected in data.iteritems():
            self.assertEqual(forecast._format_weather(val), expected)

    def test_format_wind(self):
        data = {
            '': '',
            '1': '1.2',
            '3': '3.5'
        }
        for val, expected in data.iteritems():
            self.assertEqual(forecast._format_wind(val), expected)

    def test_pre_values(self):

        self.assertEqual(
            forecast._pre_values([{'value': '1', 'startDate': '2011-01-01'}, {'value': '5', 'startDate': '2011-01-02'}]),
            ['1', '5']
        )

    def test_pre_precip_day(self):

        self.assertEqual(
            forecast._pre_precip_day([
                {'value': '1', 'startDate': '2011-01-01', 'endDate': '2011-01-01'},
                {'value': '2', 'startDate': '2011-01-01', 'endDate': '2011-01-02'},
                {'value': '3', 'startDate': '2011-01-01', 'endDate': '2011-01-01'}
            ]),
            ['1', '3']
        )

    def test_pre_precip_night(self):

        self.assertEqual(
            forecast._pre_precip_night([
                {'value': '1', 'startDate': '2011-01-01', 'endDate': '2011-01-01'},
                {'value': '2', 'startDate': '2011-01-01', 'endDate': '2011-01-02'},
                {'value': '3', 'startDate': '2011-01-01', 'endDate': '2011-01-01'}
            ]),
            ['2']
        )

if __name__ == '__main__':
    unittest.main()
