import sys
import datetime
import logging
logger = logging.getLogger("omblepy")

sys.path.append('..')
from sharedDriver import sharedDeviceDriverCode

class deviceSpecificDriver(sharedDeviceDriverCode):
    deviceEndianess                 = "big"
    userStartAdressesList           = [0x2e8, 0x860]
    perUserRecordsCountList         = [100  , 100  ]
    recordByteSize                  = 0x0e
    transmissionBlockSize           = 0x38

    settingsReadAddress             = 0x0260
    settingsWriteAddress            = 0x02A4

    settingsUnreadRecordsBytes      = [0x00, 0x08]
    settingsTimeSyncBytes           = [0x14, 0x1e] #this is probably not correct

    def deviceSpecific_ParseRecordFormat(self, singleRecordAsByteArray):
        recordDict             = dict()
        recordDict["dia"]      = self._bytearrayBitsToInt(singleRecordAsByteArray, 0, 7)
        recordDict["sys"]      = self._bytearrayBitsToInt(singleRecordAsByteArray, 8, 15) + 25
        year                   = self._bytearrayBitsToInt(singleRecordAsByteArray, 18, 23) + 2000
        recordDict["bpm"]      = self._bytearrayBitsToInt(singleRecordAsByteArray, 24, 31)
        recordDict["ihb"]      = self._bytearrayBitsToInt(singleRecordAsByteArray, 32, 32)
        recordDict["mov"]      = self._bytearrayBitsToInt(singleRecordAsByteArray, 33, 33)
        month                  = self._bytearrayBitsToInt(singleRecordAsByteArray, 34, 37)
        day                    = self._bytearrayBitsToInt(singleRecordAsByteArray, 38, 42)
        hour                   = self._bytearrayBitsToInt(singleRecordAsByteArray, 43, 47)
        minute                 = self._bytearrayBitsToInt(singleRecordAsByteArray, 52, 57)
        second                 = self._bytearrayBitsToInt(singleRecordAsByteArray, 58, 63)
        second                 = min([second, 59]) #for some reason the second value can range up to 63
        recordDict["datetime"] = datetime.datetime(year, month, day, hour, minute, second)
        return recordDict

    def deviceSpecific_syncWithSystemTime(self):
        raise ValueError("Not supported yet.")
        """
        timeSyncSettingsCopy = self.cachedSettingsBytes[slice(*self.settingsTimeSyncBytes)]
        #read current time from cached settings bytes
        month, year, hour, day, second, minute = [int(byte) for byte in timeSyncSettingsCopy[2:8]]
        try:
            logger.info(f"device is set to date: {datetime.datetime(year + 2000, month, day, hour, minute, second).strftime('%Y-%m-%d %H:%M:%S')}")
        except:
            logger.warning(f"device is set to an invalid date")

        #write the current time into the cached settings which will be written later
        currentTime = datetime.datetime.now()
        setNewTimeDataBytes = timeSyncSettingsCopy[0:2]
        setNewTimeDataBytes += bytes([currentTime.month, currentTime.year - 2000, currentTime.hour, currentTime.day, currentTime.second, currentTime.minute])
        setNewTimeDataBytes += bytes([0x00, sum(setNewTimeDataBytes) & 0xff])           #first byte does not seem to matter, second byte is crc generated by sum over data and only using lower 8 bits
        self.cachedSettingsBytes[slice(*self.settingsTimeSyncBytes)] = setNewTimeDataBytes

        logger.info(f"settings updated to new date {currentTime.strftime('%Y-%m-%d %H:%M:%S')}")
        return
        """
