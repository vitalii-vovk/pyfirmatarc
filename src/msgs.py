from cmds import RC_CMD, Constants


class MsgCreator():
    @staticmethod
    def set_conf_msg(channels, minpulse, maxpulse, frame_len):
        msg_bytes = bytearray(
            (
                RC_CMD.TX_CFG_WRITE,
                channels & Constants.BYTE_MASK,
                minpulse & Constants.BYTE_MASK,
                (minpulse >> Constants.BYTE_SIZE) & Constants.BYTE_MASK,
                maxpulse & Constants.BYTE_MASK,
                (maxpulse >> Constants.BYTE_SIZE) & Constants.BYTE_MASK,
                frame_len & Constants.BYTE_MASK,
                (frame_len >> Constants.BYTE_SIZE) & Constants.BYTE_MASK,
                (frame_len >> (Constants.BYTE_SIZE * 2)) & Constants.BYTE_MASK,
                (frame_len >> (Constants.BYTE_SIZE * 3)) & Constants.BYTE_MASK,
            )
        )
        return msg_bytes

    @staticmethod
    def get_conf_msg():
        msg_bytes = bytearray(
            (
                RC_CMD.TX_CFG_READ,
            )
        )
        return msg_bytes

    @staticmethod
    def set_channel_msg(channel, value):
        msg_bytes = bytearray(
            (
                RC_CMD.CH_VAL_SET,
                channel & Constants.BYTE_MASK,
                value & Constants.BYTE_MASK,
                (value >> Constants.BYTE_SIZE) & Constants.BYTE_MASK,
            )
        )
        return msg_bytes

    @staticmethod
    def get_channel_msg(channel):
        msg_bytes = bytearray(
            (
                RC_CMD.CH_VAL_GET,
                channel & Constants.BYTE_MASK,
            )
        )
        return msg_bytes

    @staticmethod
    def get_all_channels_msg():
        msg_bytes = bytearray(
            (
                RC_CMD.CH_VAL_GET_ALL,
            )
        )
        return msg_bytes

    @staticmethod
    def ptt_msg(val):
        msg_bytes = bytearray(
            (
                RC_CMD.PTT_SET,
                val & Constants.BYTE_MASK,
            )
        )
        return msg_bytes

    @staticmethod
    def rst_msg():
        msg_bytes = bytearray(
            (
                RC_CMD.RESET,
            )
        )
        return msg_bytes
