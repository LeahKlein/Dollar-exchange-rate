import os
import sys

import unittest
from unittest.mock import MagicMock, patch, call

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import server

class TestServer(unittest.TestCase):

    @patch('function.save_data')
    @patch('function.send_request_to_server', return_value=MagicMock())
    @patch('function.found_date', return_value=('2023-01-01', '2023-01-31'))
    def test_job(self, mock_found_date, mock_send_request, mock_save_data):
        mock_send_request.return_value = [{'date': '2023-01-01', 'rate': '3.445285714'}]
        server.job()
        mock_send_request.assert_called_with('2023-01-01', '2023-01-01-31')
        mock_save_data.assert_called_once_with('2023-01-01', '3.445285714')

    @patch('scheduler.start')
    @patch('function.create_db_with_data', return_value=('2023-01-01', '2023-01-31'))
    def test_main(self, mock_create_db_with_data, mock_scheduler_start):
        server.main()
        mock_create_db_with_data.assert_called_once()
        mock_scheduler_start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
