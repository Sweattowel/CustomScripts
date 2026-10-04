import sys

from http.server import HTTPServer

from ServerHandle import Server
from Init import InitSettings

print("Starting Program")

serverSettings = InitSettings(sys.argv)

webServer = HTTPServer(
    (
        serverSettings.hostName,
        serverSettings.serverPort
    ), Server)

webServer.settings = serverSettings

print(
    "Server started http://%s:%s" % (serverSettings.hostName, serverSettings.serverPort)
    )

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()

print("Program Complete")
