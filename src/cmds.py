from enum import IntEnum
import pyfirmata2


class Constants(IntEnum):
    BYTE_MASK = 0x7F
    BYTE_SIZE = 0x07


class RC_CMD_STATUS(IntEnum):
    OK = 0
    INVALID_ARGUMENT = 1
    INVALID_CHANNEL = 2
    UNKNOWN_ERROR = 126
    UNKNOWN = 127


class RC_CMD(IntEnum):
    SYSEX_START = pyfirmata2.START_SYSEX
    SYSEX_END = pyfirmata2.END_SYSEX

    TX_CFG_WRITE = 0x50
    TX_CFG_READ = 0x51

    CH_VAL_SET = 0x52
    CH_VAL_GET = 0x53
    CH_VAL_GET_ALL = 0x54

    PTT_SET = 0x55

    RESET = 0x5F



# // Set configuration (0x50)
# Send:
# 0xF0               Start Sysex
# 0x50               Configure transmitter
# Channels           Number of transmitter channels 7-bits
# Minpulse           minimum pulse length (ms) LSB 7-bits
# Minpulse           minimum pulse length (ms) MSB 7-bits
# Maxpulse           maximum pulse length (ms) LSB 7-bits
# Maxpulse           maximum pulse length (ms) MSB 7-bits
# Frame len          PPM frame length (ms) LSB 7-bits
# Frame len          PPM frame length (ms) 7-bits
# Frame len          PPM frame length (ms) 7-bits
# Frame len          PPM frame length (ms) MSB 7-bits
# 0xF7               End Sysex

# Receive:
# 0xF0               Start Sysex
# 0x50               Configure transmitter
# Result             0x00 = OK, everything else = error 7-bits
# 0xF7               End Sysex
 

# // Read configuration (0x51)
# Send:
# 0xF0               Start Sysex
# 0x51               Read transmitter configuration
# 0xF7               End Sysex

# Receive:
# 0xF0               Start Sysex
# 0x51               Read transmitter configuration
# Result             0x00 = OK, everything else = error 7-bits
# --- if Result == OK packet contains following fields ---
# Channels           Number of transmitter channels 7-bits
# Minpulse           minimum pulse length (ms) LSB 7-bits
# Minpulse           minimum pulse length (ms) MSB 7-bits
# Maxpulse           maximum pulse length (ms) LSB 7-bits
# Maxpulse           maximum pulse length (ms) MSB 7-bits
# Frame len          PPM frame length (ms) LSB 7-bits
# Frame len          PPM frame length (ms) 7-bits
# Frame len          PPM frame length (ms) 7-bits
# Frame len          PPM frame length (ms) MSB 7-bits
# --- packet always ends with 0xF7 regardless of status ---
# 0xF7               End Sysex
 

# // Set channel value (0x52)
# Send:
# 0xF0               Start Sysex
# 0x52               Set channel value
# Channel            Channel number (0-127) 7-bits
# Value              Channel value LSB 7-bits
# Value              Channel value MSB 7-bits
# 0xF7               End Sysex

# Receive:
# 0xF0               Start Sysex
# 0x52               Set channel value
# Result             0x00 = OK, everything else = error 7-bits
# Channel            Channel number (0-127) 7-bits
# 0xF7               End Sysex
 

# // Read channel value (0x53)
# Send:
# 0xF0               Start Sysex
# 0x53               Read channel value
# Channel            Channel number (0-127) 7-bits
# 0xF7               End Sysex

# Receive:
# 0xF0               Start Sysex
# 0x53               Read channel value
# Result             0x00 = OK, everything else = error 7-bits
# Channel            Channel number (0-127) 7-bits
# --- if Result == OK packet contains following fields ---
# Value              Channel value LSB 7-bits
# Value              Channel value MSB 7-bits
# --- packet always ends with 0xF7 regardless of status ---
# 0xF7               End Sysex
 

# // Read all channel values (0x54)
# Send:
# 0xF0               Start Sysex
# 0x54               Read all channel values
# 0xF7               End Sysex

# Receive:
# 0xF0               Start Sysex
# 0x54               Read all channel values
# Result             0x00 = OK, everything else = error 7-bits
# --- if Result == OK packet contains following fields ---
# Channels           Number of transmitter channels 7-bits
# Channel-0          Current value for channel number 0 LSB 7-bits
# Channel-0          Current value for channel number 0 MSB 7-bits
#    :
# Channel-N          Current value for channel number N LSB 7-bits
# Channel-N          Current value for channel number N MSB 7-bits
# --- packet always ends with 0xF7 regardless of status ---
# 0xF7               End Sysex
 

# // Set PTT (Push To Transmit) (0x55)
# Send:
# 0xF0               Start Sysex
# 0x55               Set PTT
# PTT                PTT value, 0 = PTT low; > 0 PTT high; 7-bits
# 0xF7               End Sysex

# Receive:
# 0xF0               Start Sysex
# 0x55               Set PTT
# Result             0x00 = OK, everything else = error 7-bits
# --- if Result == OK packet contains following fields ---
# PTT                PTT value, 0 = PTT low; > 0 PTT high; 7-bits
# --- packet always ends with 0xF7 regardless of status ---
# 0xF7               End Sysex
 

# // Reset (0x5F)
# Send:
# 0xF0               Start Sysex
# 0x5F               Reset all settings (config and chanels) to default value
# 0xF7               End Sysex

# Receive:
# 0xF0               Start Sysex
# 0x5F               Reset all settings (config and chanels) to default value
# Result             0x00 = OK, everything else = error 7-bits
# 0xF7               End Sysex