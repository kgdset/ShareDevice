class _Banner():
    version=0
    maxcontacts=0
    maxx=0
    maxy=0
    maxpressure=0
    pid=0
    percentx=0.0
    percenty=0.0
    def ToString(self):
        return "Banner [Version=" + self.version +\
               ", Pid="+ self.pid + ", MaxContacts=" + self.maxcontacts + ", Maxx="+ self.maxx +\
               ", MaxY=" +self.maxy+ ", MaxPressure=" + self.maxpressure + "]";
