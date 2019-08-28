
class Entry:
    
    def __init__(self, appName, startTime, endTime, device):
        self.appName = appName
        self.startTime = startTime
        self.endTime = endTime
        self.device = device

    def __str__(self):
        return "{}. From: {} to {}".format(self.appName, self.startTime, self.endTime)