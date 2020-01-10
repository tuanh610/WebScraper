class SourceInfo:
    def __init__(self, updateTime, ignoreTerm):
        self.updateTime = updateTime
        self.ignoreTerm = ignoreTerm


class SourceData:
    def __init__(self, url: str, name: str, info: SourceInfo = None):
        self.url = url
        self.name = name
        self.info = info
