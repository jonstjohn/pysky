import unittest, os

import forecast

class TestForecast(unittest.TestCase):

    expected_hourly = [
        {'date': '2012-03-17', 'snow': u'0.00', 'qpf': u'0.00', 'pop12': u'34', 'time': '08:00:00'},
        {'temp': u'68', 'sky': u'69', 'qpf': u'0.00', 'snow': u'0.00', 'sym': u'shra30.jpg', 'wgust': '5.8', 'rhm': u'55', 'wspd': '5.8', 'time': '14:00:00', 'date': '2012-03-17', 'wx': u'slight chance of light rain showers'},
        {'temp': u'72', 'sky': u'72', 'sym': u'tsra30.jpg', 'wgust': '5.8', 'rhm': u'46', 'wspd': '5.8', 'time': '17:00:00', 'date': '2012-03-17', 'wx': u'chance of light rain showers'},
        {'temp': u'66', 'sky': u'78', 'qpf': u'0.02', 'snow': u'0.00', 'sym': u'ntsra30.jpg', 'wgust': '3.5', 'rhm': u'58', 'pop12': u'38', 'wspd': '3.5', 'time': '20:00:00', 'date': '2012-03-17', 'wx': u'chance of light rain showers'},
        {'temp': u'61', 'sky': u'82', 'sym': u'ntsra40.jpg', 'wgust': '3.5', 'rhm': u'70', 'wspd': '3.5', 'time': '23:00:00', 'date': '2012-03-17', 'wx': u'chance of light rain showers'},
        {'temp': u'59', 'sky': u'86', 'qpf': u'0.02', 'snow': u'0.00', 'sym': u'nra40.jpg', 'wgust': '2.3', 'rhm': u'77', 'wspd': '2.3', 'time': '02:00:00', 'date': '2012-03-18', 'wx': u'chance of light rain showers'},
        {'temp': u'57', 'sky': u'91', 'sym': u'nra40.jpg', 'wgust': '2.3', 'rhm': u'84', 'wspd': '2.3', 'time': '05:00:00', 'date': '2012-03-18', 'wx': u'chance of light rain showers'},
        {'temp': u'55', 'sky': u'95', 'qpf': u'0.06', 'snow': u'0.00', 'sym': u'shra40.jpg', 'wgust': '4.6', 'rhm': u'83', 'pop12': u'41', 'wspd': '3.5', 'time': '08:00:00', 'date': '2012-03-18', 'wx': u'chance of light rain showers'},
        {'temp': u'63', 'sky': u'89', 'sym': u'shra40.jpg', 'wgust': '6.9', 'rhm': u'70', 'wspd': '5.8', 'time': '11:00:00', 'date': '2012-03-18', 'wx': u'chance of light rain showers'},
        {'temp': u'68', 'sky': u'84', 'qpf': u'0.04', 'snow': u'0.00', 'sym': u'tsra40.jpg', 'wgust': '9.2', 'rhm': u'61', 'wspd': '6.9', 'time': '14:00:00', 'date': '2012-03-18', 'wx': u'chance of  thunderstorms'},
        {'temp': u'70', 'sky': u'78', 'sym': u'tsra40.jpg', 'wgust': '8.1', 'rhm': u'53', 'wspd': '5.8', 'time': '17:00:00', 'date': '2012-03-18', 'wx': u'chance of  thunderstorms'},
        {'temp': u'66', 'sky': u'72', 'qpf': u'0.00', 'sym': u'ntsra40.jpg', 'wgust': '6.9', 'rhm': u'58', 'pop12': u'30', 'wspd': '4.6', 'time': '20:00:00', 'date': '2012-03-18', 'wx': u'chance of  thunderstorms'},
        {'temp': u'61', 'sky': u'72', 'sym': u'nra30.jpg', 'wgust': '5.8', 'rhm': u'69', 'wspd': '4.6', 'time': '23:00:00', 'date': '2012-03-18', 'wx': u'chance of light rain showers'},
        {'temp': u'57', 'sky': u'72', 'qpf': u'0.00', 'sym': u'nra30.jpg', 'wgust': '4.6', 'rhm': u'80', 'wspd': '3.5', 'time': '02:00:00', 'date': '2012-03-19', 'wx': u'slight chance of light rain showers'},
        {'temp': u'54', 'sky': u'67', 'sym': u'nra30.jpg', 'wgust': '4.6', 'rhm': u'87', 'wspd': '3.5', 'time': '05:00:00', 'date': '2012-03-19', 'wx': u'slight chance of light rain showers'},
        {'temp': u'54', 'sky': u'62', 'qpf': u'0.00', 'sym': u'shra30.jpg', 'wgust': '4.6', 'rhm': u'83', 'pop12': u'18', 'wspd': '3.5', 'time': '08:00:00', 'date': '2012-03-19', 'wx': u'slight chance of light rain showers'},
        {'temp': u'64', 'sky': u'58', 'sym': u'shra20.jpg', 'wgust': '6.9', 'rhm': u'62', 'wspd': '5.8', 'time': '11:00:00', 'date': '2012-03-19', 'wx': u'slight chance of light rain showers'},
        {'temp': u'72', 'sky': u'55', 'qpf': u'0.00', 'sym': u'shra20.jpg', 'wgust': '9.2', 'rhm': u'50', 'wspd': '6.9', 'time': '14:00:00', 'date': '2012-03-19', 'wx': u'slight chance of light rain showers'},
        {'temp': u'75', 'sky': u'52', 'sym': u'bkn.jpg', 'wgust': '9.2', 'rhm': u'45', 'wspd': '6.9', 'time': '17:00:00', 'date': '2012-03-19', 'wx': ''},
        {'temp': u'69', 'sky': u'50', 'sym': u'nsct.jpg', 'wgust': '9.2', 'rhm': u'53', 'pop12': u'11', 'wspd': '6.9', 'time': '20:00:00', 'date': '2012-03-19', 'wx': ''},
        {'temp': u'57', 'sky': u'48', 'sym': u'nsct.jpg', 'rhm': u'77', 'wspd': '4.6', 'time': '02:00:00', 'date': '2012-03-20', 'wx': ''},
        {'temp': u'53', 'sky': u'46', 'sym': u'sct.jpg', 'rhm': u'90', 'pop12': u'9', 'wspd': '4.6', 'time': '08:00:00', 'date': '2012-03-20', 'wx': ''},
        {'temp': u'72', 'sky': u'44', 'sym': u'sct.jpg', 'rhm': u'47', 'wspd': '2.3', 'time': '14:00:00', 'date': '2012-03-20', 'wx': ''},
        {'temp': u'70', 'sky': u'40', 'sym': u'nsct.jpg', 'rhm': u'49', 'pop12': u'12', 'wspd': '5.8', 'time': '20:00:00', 'date': '2012-03-20', 'wx': ''},
        {'temp': u'59', 'sky': u'40', 'sym': u'nsct.jpg', 'rhm': u'78', 'wspd': '6.9', 'time': '02:00:00', 'date': '2012-03-21', 'wx': ''},
        {'temp': u'55', 'sky': u'41', 'sym': u'sct.jpg', 'rhm': u'90', 'pop12': u'15', 'wspd': '8.1', 'time': '08:00:00', 'date': '2012-03-21', 'wx': ''},
        {'temp': u'71', 'sky': u'48', 'sym': u'sct.jpg', 'rhm': u'49', 'wspd': '8.1', 'time': '14:00:00', 'date': '2012-03-21', 'wx': ''},
        {'temp': u'68', 'sky': u'52', 'sym': u'nra20.jpg', 'rhm': u'57', 'pop12': u'22', 'wspd': '9.2', 'time': '20:00:00', 'date': '2012-03-21', 'wx': u'slight chance of light rain showers'},
        {'temp': u'55', 'sky': u'59', 'sym': u'nra20.jpg', 'rhm': u'77', 'wspd': '9.2', 'time': '02:00:00', 'date': '2012-03-22', 'wx': u'slight chance of light rain showers'},
        {'temp': u'51', 'sky': u'65', 'sym': u'shra20.jpg', 'rhm': u'86', 'pop12': u'21', 'wspd': '8.1', 'time': '08:00:00', 'date': '2012-03-22', 'wx': u'slight chance of light rain showers'},
        {'temp': u'68', 'sky': u'57', 'sym': u'shra20.jpg', 'rhm': u'51', 'wspd': '6.9', 'time': '14:00:00', 'date': '2012-03-22', 'wx': u'slight chance of light rain showers'},
        {'temp': u'65', 'sky': u'57', 'sym': u'nra20.jpg', 'rhm': u'57', 'pop12': u'37', 'wspd': '8.1', 'time': '20:00:00', 'date': '2012-03-22', 'wx': u'slight chance of light rain showers'},
        {'temp': u'54', 'sky': u'57', 'sym': u'nra40.jpg', 'rhm': u'75', 'wspd': '6.9', 'time': '02:00:00', 'date': '2012-03-23', 'wx': u'chance of light rain showers'},
        {'temp': u'51', 'sky': u'65', 'sym': u'tsra40.jpg', 'rhm': u'80', 'pop12': u'40', 'wspd': '8.1', 'time': '08:00:00', 'date': '2012-03-23', 'wx': u'chance of light rain showers'},
        {'temp': u'67', 'sky': u'63', 'sym': u'tsra40.jpg', 'rhm': u'47', 'wspd': '4.6', 'time': '14:00:00', 'date': '2012-03-23', 'wx': u'chance of light rain showers'},
        {'temp': u'66', 'sky': u'62', 'sym': u'ntsra40.jpg', 'rhm': u'51', 'wspd': '5.8', 'time': '20:00:00', 'date': '2012-03-23', 'wx': u'chance of light rain showers'}
    ]

    expected_daily = [
        {'qpf': 0.0, 'maxt': u'76', 'wgust': '9.2', 'sym': u'shra20.jpg', 'rhm': 65.714285714285708,
            'pop12': u'11', 'wspd': '5.3', 'date': u'2012-03-19', 'wx': u'slight chance of light rain showers'},
        {'qpf': 0.12, 'snow': 0.0, 'maxt': u'71', 'wgust': '9.2', 'sym': u'shra40.jpg', 'rhm': 69.375,
            'pop12': u'30', 'wspd': '4.5', 'date': u'2012-03-18', 'wx': u'chance of light rain showers'},
        {'qpf': 0.02, 'maxt': u'73', 'wgust': '5.8', 'sym': u'tsra30.jpg', 'rhm': 57.25,
            'pop12': u'38', 'wspd': '4.6', 'date': u'2012-03-17', 'wx': u'slight chance of light rain showers'},
        {'maxt': u'76', 'sym': u'nsct.jpg', 'rhm': 65.75, 'pop12': u'12', 'wspd': '4.3',
            'date': u'2012-03-20', 'wx': ''}, 
        {'maxt': u'74', 'sym': u'sct.jpg', 'rhm': 68.5, 'pop12': u'22', 'wspd': '8.1',
            'date': u'2012-03-21', 'wx': ''},
        {'maxt': u'71', 'sym': u'shra20.jpg', 'rhm': 67.75, 'pop12': u'37', 'wspd': '8.1',
            'date': u'2012-03-22', 'wx': u'slight chance of light rain showers'},
        {'maxt': u'70', 'sym': u'tsra40.jpg', 'rhm': 63.25, 'pop12': None, 'wspd': '6.3',
            'date': u'2012-03-23', 'wx': u'chance of light rain showers'}
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

    def test_frequent(self):

        self.assertEqual(forecast._frequent(['apple', 'orange', 'banana', 'apple']), 'apple')

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
                self.assertEqual(expected[i][k], daily_data[i][k])

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
                self.assertEqual(expected[i][k], hourly_data[i][k])

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

if __name__ == '__main__':
    unittest.main()
