import unittest, os

from pysky import forecast

class TestForecast(unittest.TestCase):

    expected_hourly = [
        {'date': '2012-03-17', 'snow_amount': u'0.00', 'rain_amount': u'0.00', 'precip': u'34', 'time': '08:00:00'},
        {'temp': u'68', 'sky': u'69', 'rain_amount': u'0.00', 'snow_amount': u'0.00', 'symbol': u'shra30.jpg', 'wind_gust': '5.8', 'humidity': u'55', 'wind_sustained': '5.8', 'time': '14:00:00', 'date': '2012-03-17', 'weather': u'slight chance of light rain showers'},
        {'temp': u'72', 'sky': u'72', 'symbol': u'tsra30.jpg', 'wind_gust': '5.8', 'humidity': u'46', 'wind_sustained': '5.8', 'time': '17:00:00', 'date': '2012-03-17', 'weather': u'chance of light rain showers'},
        {'temp': u'66', 'sky': u'78', 'rain_amount': u'0.02', 'snow_amount': u'0.00', 'symbol': u'ntsra30.jpg', 'wind_gust': '3.5', 'humidity': u'58', 'precip': u'38', 'wind_sustained': '3.5', 'time': '20:00:00', 'date': '2012-03-17', 'weather': u'chance of light rain showers'},
        {'temp': u'61', 'sky': u'82', 'symbol': u'ntsra40.jpg', 'wind_gust': '3.5', 'humidity': u'70', 'wind_sustained': '3.5', 'time': '23:00:00', 'date': '2012-03-17', 'weather': u'chance of light rain showers'},
        {'temp': u'59', 'sky': u'86', 'rain_amount': u'0.02', 'snow_amount': u'0.00', 'symbol': u'nra40.jpg', 'wind_gust': '2.3', 'humidity': u'77', 'wind_sustained': '2.3', 'time': '02:00:00', 'date': '2012-03-18', 'weather': u'chance of light rain showers'},
        {'temp': u'57', 'sky': u'91', 'symbol': u'nra40.jpg', 'wind_gust': '2.3', 'humidity': u'84', 'wind_sustained': '2.3', 'time': '05:00:00', 'date': '2012-03-18', 'weather': u'chance of light rain showers'},
        {'temp': u'55', 'sky': u'95', 'rain_amount': u'0.06', 'snow_amount': u'0.00', 'symbol': u'shra40.jpg', 'wind_gust': '4.6', 'humidity': u'83', 'precip': u'41', 'wind_sustained': '3.5', 'time': '08:00:00', 'date': '2012-03-18', 'weather': u'chance of light rain showers'},
        {'temp': u'63', 'sky': u'89', 'symbol': u'shra40.jpg', 'wind_gust': '6.9', 'humidity': u'70', 'wind_sustained': '5.8', 'time': '11:00:00', 'date': '2012-03-18', 'weather': u'chance of light rain showers'},
        {'temp': u'68', 'sky': u'84', 'rain_amount': u'0.04', 'snow_amount': u'0.00', 'symbol': u'tsra40.jpg', 'wind_gust': '9.2', 'humidity': u'61', 'wind_sustained': '6.9', 'time': '14:00:00', 'date': '2012-03-18', 'weather': u'chance of thunderstorms'},
        {'temp': u'70', 'sky': u'78', 'symbol': u'tsra40.jpg', 'wind_gust': '8.1', 'humidity': u'53', 'wind_sustained': '5.8', 'time': '17:00:00', 'date': '2012-03-18', 'weather': u'chance of thunderstorms'},
        {'temp': u'66', 'sky': u'72', 'rain_amount': u'0.00', 'symbol': u'ntsra40.jpg', 'wind_gust': '6.9', 'humidity': u'58', 'precip': u'30', 'wind_sustained': '4.6', 'time': '20:00:00', 'date': '2012-03-18', 'weather': u'chance of thunderstorms'},
        {'temp': u'61', 'sky': u'72', 'symbol': u'nra30.jpg', 'wind_gust': '5.8', 'humidity': u'69', 'wind_sustained': '4.6', 'time': '23:00:00', 'date': '2012-03-18', 'weather': u'chance of light rain showers'},
        {'temp': u'57', 'sky': u'72', 'rain_amount': u'0.00', 'symbol': u'nra30.jpg', 'wind_gust': '4.6', 'humidity': u'80', 'wind_sustained': '3.5', 'time': '02:00:00', 'date': '2012-03-19', 'weather': u'slight chance of light rain showers'},
        {'temp': u'54', 'sky': u'67', 'symbol': u'nra30.jpg', 'wind_gust': '4.6', 'humidity': u'87', 'wind_sustained': '3.5', 'time': '05:00:00', 'date': '2012-03-19', 'weather': u'slight chance of light rain showers'},
        {'temp': u'54', 'sky': u'62', 'rain_amount': u'0.00', 'symbol': u'shra30.jpg', 'wind_gust': '4.6', 'humidity': u'83', 'precip': u'18', 'wind_sustained': '3.5', 'time': '08:00:00', 'date': '2012-03-19', 'weather': u'slight chance of light rain showers'},
        {'temp': u'64', 'sky': u'58', 'symbol': u'shra20.jpg', 'wind_gust': '6.9', 'humidity': u'62', 'wind_sustained': '5.8', 'time': '11:00:00', 'date': '2012-03-19', 'weather': u'slight chance of light rain showers'},
        {'temp': u'72', 'sky': u'55', 'rain_amount': u'0.00', 'symbol': u'shra20.jpg', 'wind_gust': '9.2', 'humidity': u'50', 'wind_sustained': '6.9', 'time': '14:00:00', 'date': '2012-03-19', 'weather': u'slight chance of light rain showers'},
        {'temp': u'75', 'sky': u'52', 'symbol': u'bkn.jpg', 'wind_gust': '9.2', 'humidity': u'45', 'wind_sustained': '6.9', 'time': '17:00:00', 'date': '2012-03-19', 'weather': ''},
        {'temp': u'69', 'sky': u'50', 'symbol': u'nsct.jpg', 'wind_gust': '9.2', 'humidity': u'53', 'precip': u'11', 'wind_sustained': '6.9', 'time': '20:00:00', 'date': '2012-03-19', 'weather': ''},
        {'temp': u'57', 'sky': u'48', 'symbol': u'nsct.jpg', 'humidity': u'77', 'wind_sustained': '4.6', 'time': '02:00:00', 'date': '2012-03-20', 'weather': ''},
        {'temp': u'53', 'sky': u'46', 'symbol': u'sct.jpg', 'humidity': u'90', 'precip': u'9', 'wind_sustained': '4.6', 'time': '08:00:00', 'date': '2012-03-20', 'weather': ''},
        {'temp': u'72', 'sky': u'44', 'symbol': u'sct.jpg', 'humidity': u'47', 'wind_sustained': '2.3', 'time': '14:00:00', 'date': '2012-03-20', 'weather': ''},
        {'temp': u'70', 'sky': u'40', 'symbol': u'nsct.jpg', 'humidity': u'49', 'precip': u'12', 'wind_sustained': '5.8', 'time': '20:00:00', 'date': '2012-03-20', 'weather': ''},
        {'temp': u'59', 'sky': u'40', 'symbol': u'nsct.jpg', 'humidity': u'78', 'wind_sustained': '6.9', 'time': '02:00:00', 'date': '2012-03-21', 'weather': ''},
        {'temp': u'55', 'sky': u'41', 'symbol': u'sct.jpg', 'humidity': u'90', 'precip': u'15', 'wind_sustained': '8.1', 'time': '08:00:00', 'date': '2012-03-21', 'weather': ''},
        {'temp': u'71', 'sky': u'48', 'symbol': u'sct.jpg', 'humidity': u'49', 'wind_sustained': '8.1', 'time': '14:00:00', 'date': '2012-03-21', 'weather': ''},
        {'temp': u'68', 'sky': u'52', 'symbol': u'nra20.jpg', 'humidity': u'57', 'precip': u'22', 'wind_sustained': '9.2', 'time': '20:00:00', 'date': '2012-03-21', 'weather': u'slight chance of light rain showers'},
        {'temp': u'55', 'sky': u'59', 'symbol': u'nra20.jpg', 'humidity': u'77', 'wind_sustained': '9.2', 'time': '02:00:00', 'date': '2012-03-22', 'weather': u'slight chance of light rain showers'},
        {'temp': u'51', 'sky': u'65', 'symbol': u'shra20.jpg', 'humidity': u'86', 'precip': u'21', 'wind_sustained': '8.1', 'time': '08:00:00', 'date': '2012-03-22', 'weather': u'slight chance of light rain showers'},
        {'temp': u'68', 'sky': u'57', 'symbol': u'shra20.jpg', 'humidity': u'51', 'wind_sustained': '6.9', 'time': '14:00:00', 'date': '2012-03-22', 'weather': u'slight chance of light rain showers'},
        {'temp': u'65', 'sky': u'57', 'symbol': u'nra20.jpg', 'humidity': u'57', 'precip': u'37', 'wind_sustained': '8.1', 'time': '20:00:00', 'date': '2012-03-22', 'weather': u'slight chance of light rain showers'},
        {'temp': u'54', 'sky': u'57', 'symbol': u'nra40.jpg', 'humidity': u'75', 'wind_sustained': '6.9', 'time': '02:00:00', 'date': '2012-03-23', 'weather': u'chance of light rain showers'},
        {'temp': u'51', 'sky': u'65', 'symbol': u'tsra40.jpg', 'humidity': u'80', 'precip': u'40', 'wind_sustained': '8.1', 'time': '08:00:00', 'date': '2012-03-23', 'weather': u'chance of light rain showers'},
        {'temp': u'67', 'sky': u'63', 'symbol': u'tsra40.jpg', 'humidity': u'47', 'wind_sustained': '4.6', 'time': '14:00:00', 'date': '2012-03-23', 'weather': u'chance of light rain showers'},
        {'temp': u'66', 'sky': u'62', 'symbol': u'ntsra40.jpg', 'humidity': u'51', 'wind_sustained': '5.8', 'time': '20:00:00', 'date': '2012-03-23', 'weather': u'chance of light rain showers'}
    ]

    expected_daily = [
        {'rain_amount': 0.02, 'high': u'73', 'wind_gust': '5.8', 'symbol': u'tsra30.jpg', 'humidity': 57.25,
            'precip_day': u'38', 'wind_sustained': '4.6', 'date': u'2012-03-17', 'weather': u'slight chance of light rain showers'},
        {'rain_amount': 0.12, 'snow_amount': 0.0, 'high': u'71', 'wind_gust': '9.2', 'symbol': u'tsra40.jpg', 'humidity': 69.375,
            'precip_day': u'41', 'wind_sustained': '4.5', 'date': u'2012-03-18', 'weather': u'chance of light rain showers'},
        {'rain_amount': 0.0, 'high': u'76', 'wind_gust': '9.2', 'symbol': u'shra20.jpg', 'humidity': 65.714285714285708,
            'precip_day': u'18', 'wind_sustained': '5.3', 'date': u'2012-03-19', 'weather': u'slight chance of light rain showers'},
        {'high': u'76', 'symbol': u'sct.jpg', 'humidity': 65.75, 'precip_day': u'9', 'wind_sustained': '4.3',
            'date': u'2012-03-20', 'weather': ''}, 
        {'high': u'74', 'symbol': u'sct.jpg', 'humidity': 68.5, 'precip_day': u'15', 'wind_sustained': '8.1',
            'date': u'2012-03-21', 'weather': ''},
        {'high': u'71', 'symbol': u'shra20.jpg', 'humidity': 67.75, 'precip_day': u'21', 'wind_sustained': '8.1',
            'date': u'2012-03-22', 'weather': u'slight chance of light rain showers'},
        {'high': u'70', 'symbol': u'tsra40.jpg', 'humidity': 63.25, 'precip_day': u'40', 'wind_sustained': '6.3',
            'date': u'2012-03-23', 'weather': u'chance of light rain showers'}
    ]



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

    def test_pre_rain_amount(self):

        test_data = [['1', 1], ['5', 5], ['1.25', 1.25], ['1.888', 1.89], ['', None]]
        value_data = [{'value': x} for x, y in test_data]
        tolerance = .001

        values = forecast._pre_rain_amount(value_data)

        self.assertEqual(len(values), len(test_data) - 1) # less invalid
        for parameter, expected in test_data:
            if expected:
                correct = False
                for val in values:
                    if val > expected - tolerance and val < expected + tolerance:
                        correct = True
                        break
                self.assertTrue(correct)

    def test_pre_snow_amount(self):

        test_data = [['1', 1], ['5', 5], ['1.25', 1.3], ['1.888', 1.9], ['', None]]
        value_data = [{'value': x} for x, y in test_data]
        tolerance = .001

        values = forecast._pre_snow_amount(value_data)

        self.assertEqual(len(values), len(test_data) - 1) # less invalid
        for parameter, expected in test_data:
            if expected:
                correct = False
                for val in values:
                    if val > expected - tolerance and val < expected + tolerance:
                        correct = True
                        break
                self.assertTrue(correct)

    def test_pre_weather(self):

        self.assertEqual(
            forecast._pre_weather([
                {'value': '1', 'startTime': '08:00:00'},
                {'value': '2', 'startTime': '04:00:00'},
                {'value': '3', 'startTime': '17:00:00'},
                {'value': '4', 'startTime': '19:00:00'}
            ]),
            ['1', '3']
        )

    def test_pre_wsym(self):

        self.assertEqual(
            forecast._pre_wsym([
                {'value': ''},
                {'value': '/test.jpg'},
                {'value': 'http://www.image.com/img.jpg'}
            ]),
            ['/test.jpg', 'http://www.image.com/img.jpg']
        )
        
    def test_first(self):

        self.assertEqual(forecast._first(['1', '2', '3', '4']), '1')
        self.assertEqual(forecast._first([]), None)

    def test_first_nonempty(self):

        self.assertEqual(forecast._first_nonempty(['', '', '8', '4']), '8')
        self.assertEqual(forecast._first_nonempty([]), None)

    def test_average(self):

        self.assertEqual(forecast._average(['1', '2', '3', '4']), 2.5)

    def test_frequent_sym(self):

        self.assertEqual(forecast._frequent_sym(['apple', 'orange', 'banana', 'apple']), 'apple')

    def test_daily(self):

        import json
        f = open('test_xml_data.json', 'r')
        xml_data = json.loads(f.read())
        f.close()

        daily_data = forecast._daily(xml_data)

        # Exactly 7 days of forecast
        self.assertEqual(7, len(daily_data))

        # Expected data
        expected = self.expected_daily

        # Assert all values are as expected
        for i in range(1, len(expected)):
            for k, v in expected[i].iteritems():
                self.assertEqual(expected[i][k], daily_data[i][k], 'Expected {0} got {1} for {2} on {3}'.format(expected[i][k], daily_data[i][k], k, daily_data[i]['date']))

    def test_hourly(self):

        import json
        f = open('test_xml_data.json', 'r')
        xml_data = json.loads(f.read())
        f.close()

        hourly_data = forecast._hourly(xml_data)

        expected = self.expected_hourly
        
        # Assert all values are as expected
        for i in range(1, len(expected)):
            for k, v in expected[i].iteritems():
                self.assertEqual(expected[i][k], hourly_data[i][k], "Expected '{0}' got '{1}' for {2} on {3} {4}".format(expected[i][k], hourly_data[i][k], k, hourly_data[i]['date'], hourly_data[i]['time']))
                #self.assertEqual(expected[i][k], hourly_data[i][k])

    def test_process_xml(self):

        f = open('test.xml')
        xml = f.read()
        data = forecast.process_xml(xml)

        # Assert all values are as expected
        daily_data = data['daily']
        expected = self.expected_daily
        for i in range(1, len(expected)):
            for k, v in expected[i].iteritems():
                self.assertEqual(expected[i][k], daily_data[i][k])

        # Assert all values are as expected
        hourly_data = data['hourly']
        expected = self.expected_hourly
        for i in range(1, len(expected)):
            for k, v in expected[i].iteritems():
                self.assertEqual(expected[i][k], hourly_data[i][k])

    def test_average(self):

        vals = [3, 3, 3, 5, 6, 6, 6]
        self.assertEquals(4.6, round(forecast._average(vals), 1))

if __name__ == '__main__':
    unittest.main()
