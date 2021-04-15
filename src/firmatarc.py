from dataclasses import dataclass
from enum import auto, Enum, IntEnum
from pyfirmata2 import Arduino

from cmds import RC_CMD, RC_CMD_STATUS, Constants
from msgs import MsgCreator

import logging
import time


@dataclass
class Configuration:
    channels: int = 0
    framelen: int = 0
    minpulse: int = 0
    maxpulse: int = 0
    ptt: int = 0


@dataclass
class RcChannel:
    value: int = 0
    status: bool = False


class RC_CHANNEL(IntEnum):
        ROLL = 0
        PITCH = 1
        THROTTLE = 2
        YAW = 3
        ARM = 4
        RESERVED1 = 5
        RESERVED2 = 6


class FirmataRC(Arduino):
    class ERROR(IntEnum):
        INVALID_CHANNEL = auto()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._logger = logging.getLogger('firmatarc')
        self._conf = Configuration()
        self._channels = dict()
        self._req_queue = dict()

        self._setup_handlers()
        self.reset()

    def _setup_handlers(self):
        self.add_cmd_handler(RC_CMD.TX_CFG_READ, self._get_conf_handler)
        self.add_cmd_handler(RC_CMD.TX_CFG_WRITE, self._set_conf_handler)
        self.add_cmd_handler(RC_CMD.CH_VAL_SET, self._set_channel_handler)
        self.add_cmd_handler(RC_CMD.CH_VAL_GET, self._get_channel_handler)
        self.add_cmd_handler(RC_CMD.CH_VAL_GET_ALL, self._get_all_channels_handler)
        self.add_cmd_handler(RC_CMD.PTT_SET, self._ptt_handler)
        self.add_cmd_handler(RC_CMD.RESET, self._reset_handler)

    def _check_status(self, cmd, status):
        is_ok = False
        if status != RC_CMD_STATUS.OK:
            try:
                estatus = RC_CMD_STATUS(status)
            except KeyError:
                estatus = status
            self._logger.error(f'RC error : {RC_CMD(cmd)} returned {estatus}')
            is_ok = False
        else:
            self._logger.debug(f'RC result : {RC_CMD(cmd)} returned {RC_CMD_STATUS.OK}')
            is_ok = True
        return is_ok

    def _set_conf_handler(self, *data):
        result = data[0]
        is_ok = self._check_status(RC_CMD.TF_CFG_WRITE, result)

        self._task_done(RC_CMD.TF_CFG_WRITE)
        return is_ok

    def _get_conf_handler(self, *data):
        status = data[0]
        is_ok = self._check_status(RC_CMD.TX_CFG_READ, status)
        if is_ok:
            try:
                data = data[1:]
                self._conf.channels = data[0]
                self._conf.minpulse = (
                    (data[1] & Constants.BYTE_MASK) |
                    ((data[2] & Constants.BYTE_MASK) << Constants.BYTE_SIZE))
                self._conf.maxpulse = (
                    (data[3] & Constants.BYTE_MASK) |
                    ((data[4] & Constants.BYTE_MASK) << Constants.BYTE_SIZE))
                self._conf.framelen = (
                    (data[5] & Constants.BYTE_MASK) |
                    ((data[6] & Constants.BYTE_MASK) << Constants.BYTE_SIZE) |
                    ((data[7] & Constants.BYTE_MASK) << Constants.BYTE_SIZE * 2) |
                    ((data[8] & Constants.BYTE_MASK) << Constants.BYTE_SIZE * 3))
            except IndexError:
                self._logger.error(f'Broken response for {RC_CMD.TX_CFG_READ} : {data}')
                is_ok = False

        self._task_done(RC_CMD.TX_CFG_READ)
        return is_ok

    def _set_channel_handler(self, *data):
        status = data[0]
        is_ok = self._check_status(RC_CMD.CH_VAL_SET, status)
        if is_ok:
            data = data[1:]
            channel_numer = data[0]

        self._task_done(RC_CMD.CH_VAL_SET)
        return is_ok

    def _get_channel_handler(self, *data):
        status = data[0]
        is_ok = self._check_status(RC_CMD.CH_VAL_GET, status)
        if is_ok:
            data = data[1:]

            ch_number = data[0]
            ch_value = (
                (data[1] & Constants.BYTE_MASK) |
                ((data[2] & Constants.BYTE_MASK) << Constants.BYTE_SIZE))

            if ch_number in self._channels:
                self._channels[ch_number].value = ch_value
                self._channels[ch_number].status = True
            else:
                ch = RcChannel(value=ch_value, status=True)
                self._channels[ch_number] = ch

        self._task_done(RC_CMD.CH_VAL_GET)
        return is_ok

    def _get_all_channels_handler(self, *data):
        status = data[0]
        is_ok = self._check_status(RC_CMD.CH_VAL_GET_ALL, status)
        if is_ok:
            self._conf.channels = data[1]
            data = data[2:]
            self._channels.clear()
            for i in range(self._conf.channels):
                ch_value = (                
                    (data[2*i] & Constants.BYTE_MASK) |
                    ((data[2*i+1] & Constants.BYTE_MASK) << Constants.BYTE_SIZE))
                ch = RcChannel(value=ch_value, status=True)
                self._channels[i] = ch

        self._task_done(RC_CMD.CH_VAL_GET_ALL)
        return is_ok

    def _ptt_handler(self, *data):
        status = data[0]
        is_ok = self._check_status(RC_CMD.PTT_SET, status)
        if is_ok:
            data = data[1:]
            self._conf.ptt = data[0]

        self._task_done(RC_CMD.PTT_SET)
        return is_ok

    def _reset_handler(self, *data):
        status = data[0]
        is_ok = self._check_status(RC_CMD.RESET, status)
        self._task_done(RC_CMD.RESET)
        return is_ok

    def _task_sched(self, cmd):
        val = self._req_queue.get(cmd, 0) + 1
        self._req_queue[cmd] = val
        return val

    def _task_done(self, cmd):
        if cmd in self._req_queue:
            curr_val = self._req_queue[cmd]
            self._req_queue[cmd] = max(0, curr_val-1)

    def _wait_cmd(self, cmd, val):
        while True:
            curr_id = self._req_queue.get(cmd, 0)
            if curr_id < val:
                break

            if not self.bytes_available():
                time.sleep(1e-3)
                continue
            self.iterate()

        return curr_id

    def wait_all(self):
        for k, v in self._req_queue:
            self._wait_cmd(k, 1)

    def send(self, cmd, data, block=False):
        val = self._task_sched(cmd)
        self.send_sysex(cmd, data)
        if block:
            self._wait_cmd(cmd, val)

    def reset(self):
        msg = MsgCreator.rst_msg()
        self.send(msg[0], msg[1:], block=True)
        msg = MsgCreator.ptt_msg(1)
        self.send(msg[0], msg[1:], block=True)
        msg = MsgCreator.get_conf_msg()
        self.send(msg[0], msg[1:], block=True)
        msg = MsgCreator.get_all_channels_msg()
        self.send(msg[0], msg[1:], block=True)
        self.roll = 255
        self.send(msg[0], msg[1:], block=True)

    def get_channel(self, ch):
        if ch < 0 or ch >= self._conf.channels:
            return FirmataRC.ERROR.INVALID_CHANNEL

        if ch not in self._channels:
            self._channels[ch] = RcChannel(value=None, status=False)
        else:
            self._channels[ch].status = False

        msg = MsgCreator.get_channel_msg(ch)
        self.send(msg[0], msg[1:], block=True)
        return self._channels[ch].value

    def set_channel(self, ch, value):
        if ch < 0 or ch >= self._conf.channels:
            return FirmataRC.ERROR.INVALID_CHANNEL

        if ch not in self._channels:
            self._channels[ch] = RcChannel(value=None, status=False)
        else:
            self._channels[ch].status = False

        msg = MsgCreator.set_channel_msg(ch, value)
        self.send(msg[0], msg[1:])

    def set_throttle(self, value):
        return self.set_channel(RC_CHANNEL.THROTTLE, value)

    def set_roll(self, value):
        return self.set_channel(RC_CHANNEL.ROLL, value)

    def set_pitch(self, value):
        return self.set_channel(RC_CHANNEL.PITCH, value)

    def set_yaw(self, value):
        return self.set_channel(RC_CHANNEL.YAW, value)

    def set_arm(self, value):
        return self.set_channel(RC_CHANNEL.ARM, value)

    def get_throttle(self):
        return self.get_channel(RC_CHANNEL.THROTTLE)

    def get_roll(self):
        return self.get_channel(RC_CHANNEL.ROLL)

    def get_pitch(self):
        return self.get_channel(RC_CHANNEL.PITCH)

    def get_yaw(self):
        return self.get_channel(RC_CHANNEL.YAW)

    def get_arm(self):
        return self.get_channel(RC_CHANNEL.ARM)

    # // Property section
    # //// Getters

    @property
    def n_channels(self):
        return self._conf.channels

    @property
    def throttle(self):
        return self.get_throttle()

    @property
    def roll(self):
        return self.get_roll()

    @property
    def pitch(self):
        return self.get_pitch()

    @property
    def yaw(self):
        return self.get_yaw()

    @property
    def arm(self):
        return self.get_arm()

    # //// Setters

    @throttle.setter
    def throttle(self, val):
        return self.set_throttle(val)

    @roll.setter
    def roll(self, val):
        return self.set_roll(val)

    @pitch.setter
    def pitch(self, val):
        return self.set_pitch(val)

    @yaw.setter
    def yaw(self, val):
        return self.set_yaw(val)

    @arm.setter
    def arm(self, val):
        return self.set_arm(val)
