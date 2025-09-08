import os
import sys

import unittest
from unittest.mock import MagicMock, patch, call

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import function

class TestDatabaseFunctions(unittest.TestCase):

    def test_last_day_of_month(self):
        with patch('calendar.monthrange', return_value=(1, 31)):
            assert function.last_day_of_month(2025, 1) == 31

    @patch('function.last_month', return_value='2023-05-01')  # שנה על פי הצורך
    @patch('function.last_day_of_month', return_value='2023-05-31')  # שנה על פי הצורך
    def test_found_date(self, mock_last_month, mock_last_day_of_month):
        expected_first_day = '2023-05-01'
        expected_last_day = '2023-05-31'

        first_day, last_day = function.found_date()

        self.assertEqual(first_day, expected_first_day)
        self.assertEqual(last_day, expected_last_day)

    def test_last_month(self):
        result = function.last_month(2023, 1)
        self.assertEqual(result, '2022-12')
        result = function.last_month(2023, 12)
        self.assertEqual(result, '2023-11')

    def test_date_format(self):
        self.assertEqual(function.date_format('2024-01'), '2024-01')

    @patch('requests.get')
    def test_send_request_to_server( self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'exchange_rates': [{'date': '2023-01', 'rate': '3.445285714'}]
            }
        month = '2023-05-01'
        last_day = '2023-05-31'
        result = function.send_request_to_server(month, last_day)
        self.assertEqual(result, [{'date': '2023-01', 'rate': '3.445285714'}])
        mock_get.assert_called_once_with(f'http://host.docker.internal:8000/?first_day={month}&last_day={last_day}')

        mock_get.return_value.status_code = 404
        mock_get.return_value.text = 'Not Found'
        month = '2023-05-01'
        last_day = '2023-05-31'
        result = function.send_request_to_server(month, last_day)
        self.assertEqual(result, 'Error: 404, Not Found')

    @patch('data_base.create_db')
    @patch('function.send_request_to_server')
    @patch('data_base.save_data')
    def test_create_db_with_data(self, mock_save_data, mock_send_request, mock_create_db):
        mock_send_request.return_value = [{'date': '2023-01-01', 'rate': '3.445285714'}]
        function.create_db_with_data()
        mock_create_db.assert_called_once()
        mock_send_request.assert_called_once()
        mock_save_data.assert_called_once_with('2023-01-01', '3.445285714')

        mock_send_request.return_value = [{'date': '2023-01-01', 'rate': '3.445285714'}]
        mock_save_data.side_effect = ValueError("Insert Error")
        with self.assertRaises(ValueError):
            function.create_db_with_data()

if __name__ == '__main__':
    unittest.main()
   