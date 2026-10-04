class serverSettings:
    def __init__(
        self,
        hostName = "localhost",
        serverPort = 9999,
        passWord = "localhost"
    ):
        self.hostName = hostName
        self.serverPort = serverPort
        self.passWord = passWord

def InitSettings(args):

    print("Initializing settings for server")

    cacheSettings = serverSettings()

    maxLength = len(args)
    
    for i in args[1:]:
        match i:
            case "-host":
                if i + 1 <= maxLength:
                    cacheSettings.hostName = args[i + 1]
            case "-port":
                if i + 1 <= maxLength:
                    cacheSettings.serverPort = args[i + 1]
            case "-pass":
                if i + 1 <= maxLength:
                    cacheSettings.passWord = args[i + 1]

    print("server engaged, running on \n")
    print("Hostname: % s" % cacheSettings.hostName, "\n")
    print("serverPort: % s" % cacheSettings.serverPort, "\n")
    print("passWord: %s" % cacheSettings.passWord, "\n")

    return cacheSettings
