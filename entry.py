
class Entry:
    
    def __init__(self, appName, startTime, duration, device):
        self.appName = appName
        self.startTime = startTime
        self.duration = duration
        self.device = device

    def __str__(self):
        return "{}. From: {} to {}".format(self.appName, self.startTime, self.endTime)