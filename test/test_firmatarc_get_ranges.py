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
