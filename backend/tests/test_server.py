import unittest
from unittest.mock import patch
from server import app

class TestApp(unittest.TestCase):

    @patch('server.requests.get')
    def test_get_data_success(self, mock_get):
        app.config['TESTING'] = True
        client = app.test_client()
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'''
            <data>
                <Obs TIME_PERIOD="2023-01" OBS_VALUE="3.445285714"/>
                <Obs TIME_PERIOD="2023-02" OBS_VALUE="3.500000000"/>
            </data>
        '''
        response = client.get('/?first_day=2023-01&last_day=2023-02')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['exchange_rates'][0], {'date': '2023-01', 'rate': '3.445285714'})
        self.assertEqual(data['exchange_rates'][1], {'date': '2023-02', 'rate': '3.500000000'})

    @patch('server.requests.get')
    def test_get_data_failure(self, mock_get):
        app.config['TESTING'] = True
        client = app.test_client()
        mock_get.return_value.status_code = 404
        response = client.get('/?first_day=2023-01&last_day=2023-02')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {'error': 'Unable to fetch data'})

if __name__ == '__main__':
    unittest.main()
