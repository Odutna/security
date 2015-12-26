import unittest
from unittest.mock import patch, MagicMock

import bhnet
import handler


class TestBhnet(unittest.TestCase):
    test_opt = MagicMock(
        return_value=MagicMock(
            target='localhost',
            port=9999,
            listen=False,
            udp=False,
        )
    )
    test_connect = MagicMock()

    @patch('handler.TCPClientHandler.connect', test_connect)
    @patch('bhnet.parse_options', test_opt)
    def test_tcp_chat(self):
            bhnet.main()

if __name__ == '__main__':
    unittest.main()
