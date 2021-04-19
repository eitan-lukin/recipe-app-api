from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available."""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # The patch decorator sends a 'ts' value to the function. 
    # The idea is to change the default behavior which waits 
    # one second because calls to the DB. This is to save test time.
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db."""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Raise and OperationError 5 times and send a 
            # successfule DB access on the 6th time
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
