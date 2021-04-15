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


sys.path.insert(
    os.path.abspath(
        os.path.join(
            os.path.join(
                os.path.join(__file__, os.pardir), os.pardir), 'src')))


class TestCase(IntEnum):
    NONE = 0
    GET_THROTTLE_RANGE = auto()
    GET_ROLL_RANGE = auto()
    GET_PITCH_RANGE = auto()
    GET_YAW_RANGE = auto()
    GET_ARM_RANGE = auto()


testcase = TestCase.NONE


class FirmataRCGetRangesTestCase(unittest.TestCase):
    @unittest.skipIf(testcase != TestCase.GET_THROTTLE_RANGE, "Turned off the blocking test untill it is really needed")
    def test_throttle_range(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        while True:
            print(f'throttle : {board.throttle}')
            time.sleep(0.1)

    @unittest.skipIf(testcase != TestCase.GET_ROLL_RANGE, "Turned off the blocking test untill it is really needed")
    def test_roll_range(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        while True:
            print(f'roll : {board.roll}')
            time.sleep(0.1)

    @unittest.skipIf(testcase != TestCase.GET_PITCH_RANGE, "Turned off the blocking test untill it is really needed")
    def test_pitch_range(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        while True:
            print(f'pitch : {board.pitch}')
            time.sleep(0.1)

    @unittest.skipIf(testcase != TestCase.GET_YAW_RANGE, "Turned off the blocking test untill it is really needed")
    def test_yaw_range(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        while True:
            print(f'yaw : {board.yaw}')
            time.sleep(0.1)

    @unittest.skipIf(testcase != TestCase.GET_ARM_RANGE, "Turned off the blocking test untill it is really needed")
    def test_arm_range(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        while True:
            print(f'arm : {board.arm}')
            time.sleep(0.1)


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'test_reports'
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output_dir),
                  failfast=False, buffer=False, catchbreak=False)



class FirmataRCGetRangesTestCase(unittest.TestCase):
    def test_board_init(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)

    @unittest.SkipTest
    def test_throttle(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.throttle, 0)
        board.throttle = 155
        self.assertEqual(board.throttle, 155)
        board.throttle = 8196
        self.assertEqual(board.throttle, 8196)

    @unittest.SkipTest
    def test_roll(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.roll, 0)
        board.roll = 155
        self.assertEqual(board.roll, 155)
        board.roll = 8196
        self.assertEqual(board.roll, 8196)

    @unittest.SkipTest
    def test_pitch(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.pitch, 0)
        board.pitch = 155
        self.assertEqual(board.pitch, 155)
        board.pitch = 8196
        self.assertEqual(board.pitch, 8196)

    def test_yaw(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.yaw, 0)
        board.yaw = 257
        self.assertEqual(board.yaw, 257)
        board.yaw = 8196
        self.assertEqual(board.yaw, 8196)

    @unittest.SkipTest
    def test_arm(self):
        from firmatarc import FirmataRC
        board = FirmataRC(FirmataRC.AUTODETECT)
        self.assertEqual(board.arm, 0)
        board.arm = 155
        self.assertEqual(board.arm, 155)
        board.arm = 8196
        self.assertEqual(board.arm, 8196)


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'test_reports'
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output_dir),
                  failfast=False, buffer=False, catchbreak=False)
