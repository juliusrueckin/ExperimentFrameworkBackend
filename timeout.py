from sacred.observers import RunObserver
from sacred.config.config_files import load_config_file
from datetime import timedelta
import sys
import re

class TimeoutObserver(RunObserver):

    @classmethod
    def from_config(cls, filename, expInstance):
        d = load_config_file(filename)
        obs = None
        if 'defaultTimeout' in d and 'maxTimeSinceLastStatusMsg' in d and 'outputPattern' in d and 'errorPattern' in d and 'minLossFunctionImprovementSinceLastIteration' in d and 'accuracyPattern' in d and 'minAccuracyFunctionImprovementSinceLastIteration' in d:
            obs = cls(d['defaultTimeout'], d['outputPattern'], d['maxTimeSinceLastStatusMsg'], expInstance, d['errorPattern'], d['minLossFunctionImprovementSinceLastIteration'], d['accuracyPattern'], d['minAccuracyFunctionImprovementSinceLastIteration'])
        else:
            raise ValueError("Timeout configuration file must contain "
                             "an entry for 'defaultTimeout', 'outputPattern' and 'maxTimeSinceLastStatusMsg'!")

        return obs

    def __init__(self, defaultTimeout, outputPattern, maxTimeSinceLastStatusMsg, expInstance, errorPattern, minLossFunctionImprovementSinceLastIteration, accuracyPattern, minAccuracyFunctionImprovementSinceLastIteration):
        self.errorPattern = errorPattern
        self.minLossFunctionImprovementSinceLastIteration = minLossFunctionImprovementSinceLastIteration
        
        self.accuracyPattern = accuracyPattern
        self.minAccuracyFunctionImprovementSinceLastIteration = minAccuracyFunctionImprovementSinceLastIteration

        self.defaultTimeout = defaultTimeout
        self.outputPattern = outputPattern
        self.maxTimeSinceLastStatusMsg = maxTimeSinceLastStatusMsg
        self.expInstance = expInstance

        self.totalRunTime = 0
        self.lastHeartbeat = -1
        self.lastMsgDependetHeartbeat = -1
        self.timeSinceLastStatusMsg = 0
        self.statusMsgCount = 0
        self.run = None
        self.message = ""

        self.errorMsgCount = 0
        self.currentErrorValue = -1

        self.accuracyMsgCount = 0
        self.currentAccuracyValue = -1

    def defaultTimeoutBoundExceeded(self):
        return self.totalRunTime > self.defaultTimeout

    def statusMsgDependentTimeoutBoundExceeded(self):
        return self.timeSinceLastStatusMsg > self.maxTimeSinceLastStatusMsg

    def newRequiredStatsMsgOccurred(self):
        with open(self.run['config']['title'] + 'StatusMessages.txt') as statusMsgFile:
            for rowCount, linesStatusMsg in enumerate(statusMsgFile):
                if rowCount <= self.statusMsgCount:
                    continue

                if linesStatusMsg.rstrip() == self.outputPattern:
                    self.statusMsgCount = len(statusMsgFile.readlines())
                    return True

        return False

    def newRequiredErrorMsgOccurred(self):
        with open(self.run['config']['title'] + 'StatusMessages.txt') as statusMsgFile:
            for rowCount, errorMsg in enumerate(statusMsgFile):
                if rowCount <= self.errorMsgCount:
                    continue

                if self.errorPattern in errorMsg.rstrip():
                    self.errorMsgCount = rowCount
                    self.currentErrorValue = int(errorMsg.rstrip().split(self.errorPattern)[-1])
                    return True

        return False

    def newRequiredAccuracyMsgOccurred(self):
        with open(self.run['config']['title'] + 'StatusMessages.txt') as statusMsgFile:
            for rowCount, accuracyMsg in enumerate(statusMsgFile):
                if rowCount <= self.accuracyMsgCount:
                    continue

                if self.accuracyPattern in accuracyMsg.rstrip():
                    self.accuracyMsgCount = rowCount
                    self.currentAccuracyValue = int(accuracyMsg.rstrip().split(self.accuracyPattern)[-1])
                    return True

        return False

    def errorImprovedEnough(self, lastErrorValue):
        if lastErrorValue - self.currentErrorValue >= self.minLossFunctionImprovementSinceLastIteration:
            return True

        return False

    def accuracyImprovedEnough(self, lastAccuracyValue):
        if self.currentAccuracyValue - lastAccuracyValue >= self.minAccuracyFunctionImprovementSinceLastIteration:
            return True

        return False

    def handleDefaultTimeout(self, beat_time):
        if self.lastHeartbeat == -1:
            self.lastHeartbeat = beat_time

        currentBeatTime = beat_time
        timeSinceLastBeat = timedelta(microseconds=-1)
        timeSinceLastBeat = currentBeatTime - self.lastHeartbeat
        self.lastHeartbeat = currentBeatTime

        self.totalRunTime += timeSinceLastBeat.seconds

        if self.totalRunTime > 0:
            print(self.get_heartbeat_text())

        if self.defaultTimeoutBoundExceeded():
            print("Default timeout bound exceeded! Default timeout after " + str(self.defaultTimeout) + "sec.")
            self.expInstance.forceKill()

    def handleOutputPatternBasedTimeout(self, beat_time):
        if self.lastMsgDependetHeartbeat == -1:
            self.lastMsgDependetHeartbeat = beat_time

        currentBeatTime = beat_time
        timeSinceLastBeat = timedelta(microseconds=-1)
        timeSinceLastBeat = currentBeatTime - self.lastMsgDependetHeartbeat
        self.lastMsgDependetHeartbeat = currentBeatTime

        self.timeSinceLastStatusMsg += timeSinceLastBeat.seconds

        if self.statusMsgDependentTimeoutBoundExceeded():
            if self.newRequiredStatsMsgOccurred() is False:
                print("Status message dependent timeout bound exceeded! Status message dependent timeout after " + str(self.maxTimeSinceLastStatusMsg) + "sec., since last status message")
                self.expInstance.forceKill()

            self.timeSinceLastStatusMsg = 0
            self.lastMsgDependetHeartbeat = -1

    def handleErrorPatternBasedTimeout(self):
        if self.currentErrorValue == -1:
            self.newRequiredErrorMsgOccurred()
            return
        
        lastErrorValue = self.currentErrorValue
         
        if self.newRequiredErrorMsgOccurred():
            if self.errorImprovedEnough(lastErrorValue) is False:
                print("Loss function did not improve by " + str(self.minLossFunctionImprovementSinceLastIteration) + "! Algorithm terminated!")
                self.expInstance.forceKill() 

    def handleAccuracyPatternBasedTimeout(self):
        if self.currentAccuracyValue == -1:
            self.newRequiredAccuracyMsgOccurred()
            return
        
        lastAccuracyValue = self.currentAccuracyValue
         
        if self.newRequiredAccuracyMsgOccurred():
            if self.accuracyImprovedEnough(lastAccuracyValue) is False:
                print("Accuracy function did not improve by " + str(self.minAccuracyFunctionImprovementSinceLastIteration) + "! Algorithm terminated!")
                self.expInstance.forceKill() 

    def get_heartbeat_text(self):
        return "\n\n" + self.run['config']['title'] + " is running for " + str(self.totalRunTime) + " seconds!\n\n"

    def started_event(self, ex_info, command, host_info, start_time,
                  config, meta_info, _id):
        self.run = {
            '_id': _id,
            'config': config,
            'start_time': start_time,
            'experiment': ex_info,
            'command': command,
            'host_info': host_info
        }

    def heartbeat_event(self, info, captured_out, beat_time, result):
        self.handleDefaultTimeout(beat_time)
        self.handleOutputPatternBasedTimeout(beat_time)

        self.handleErrorPatternBasedTimeout()
        self.handleAccuracyPatternBasedTimeout()


    def completed_event(self, stop_time, result):
        self.totalRunTime = 0

    def interrupted_event(self, interrupt_time, status):
        self.totalRunTime = 0

    def failed_event(self, fail_time, fail_trace):
        self.totalRunTime = 0