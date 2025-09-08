import os
import sys

import unittest
from unittest.mock import MagicMock, patch, call

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import data_base


class TestDatabaseFunctions(unittest.TestCase):

    @patch('sqlite3.connect', return_value=MagicMock())
    def test_connect_db(self, mock_connect):
        connection = data_base.connect_db()
        self.assertIsNotNone(connection)
        mock_connect.assert_called_once_with('database.db')

    @patch('sqlite3.connect', return_value=MagicMock())
    def test_create_db(self, mock_connect):
        data_base.create_db()
        mock_connection = mock_connect.return_value
        mock_connection.cursor.assert_called_once()
        mock_connection.cursor().execute.assert_called_once_with('''
    CREATE TABLE IF NOT EXISTS database (
        month DATETIME PRIMARY KEY,
        average REAL
    )
    ''')
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch('sqlite3.connect', return_value=MagicMock())
    def test_save_data(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        data_base.save_data('2025-08', 3.6)
        mock_cursor.execute.assert_called_once_with('''
        INSERT INTO database (month, average)
        VALUES (?, ?)
    ''', ('2025-08', 3.6))
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('sqlite3.connect', return_value=MagicMock())
    def test_print_data(self, mock_connect):
        mock_rows = [('2023-01', 1.0), ('2023-02', 1.5)]

        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = mock_rows

        with patch('builtins.print') as mock_print:
            data_base.print_data()
            mock_print.assert_has_calls([call(row) for row in mock_rows], any_order=True)

        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(''' SELECT * FROM database ''')
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
