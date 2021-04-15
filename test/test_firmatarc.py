import os
import time
import sys
import unittest
import xmlrunner

from enum import auto, IntEnum


import os
import time
import sys
import unittest
import xmlrunner

from enum import auto, IntEnum


sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.join(
                os.path.join(__file__, os.pardir), os.pardir), 'src')))


class FirmataRCGetRangesTestCase(unittest.TestCase):
    def test_board_init(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)

    @unittest.SkipTest
    def test_throttle(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.throttle, 0)
        board.throttle = 255
        self.assertEqual(board.throttle, 255)
        board.throttle = 257
        self.assertEqual(board.throttle, 1)

    @unittest.SkipTest
    def test_roll(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.roll, 0)
        board.roll = 255
        self.assertEqual(board.roll, 255)
        board.roll = 257
        self.assertEqual(board.roll, 1)

    @unittest.SkipTest
    def test_pitch(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.pitch, 0)
        board.pitch = 255
        self.assertEqual(board.pitch, 255)
        board.pitch = 257
        self.assertEqual(board.pitch, 1)

    @unittest.SkipTest
    def test_yaw(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.yaw, 0)
        board.yaw = 255
        self.assertEqual(board.yaw, 255)
        board.yaw = 257
        self.assertEqual(board.yaw, 1)

    @unittest.SkipTest
    def test_arm(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.arm, 0)
        board.arm = 255
        self.assertEqual(board.arm, 255)
        board.arm = 257
        self.assertEqual(board.arm, 1)


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'test_reports'
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output_dir),
                  failfast=False, buffer=False, catchbreak=False)