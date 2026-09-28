import sys
import subprocess
import json

from http.server import BaseHTTPRequestHandler, HTTPServer

print("Starting Program")

for i in sys.argv[1:]:
    print("arg = " + i)

print(len(sys.argv))

if len(sys.argv) != 4:
    print("Incorrect argumentCount")
    quit()

if sys.argv[1] == "" or sys.argv[2] == "" or sys.argv[3] == "":
    print("Inadequate arguments, Provide: \nhostName port password")
    quit()

hostName = sys.argv[1]
serverPort = int(sys.argv[2])
password = sys.argv[3]

class Server(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        print("Request received \n")
        super().__init__(request, client_address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("Burn...","utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            passAttempt = data.get("pass")
            if passAttempt == password:
                self.wfile.write(bytes("Password Success \n", "utf-8"))
                jsonBody = data.get("body")
                command = jsonBody.get("Command")
                inst = jsonBody.get("Inst")

                print("Command received: ", command)
                print("Command Instructions", inst)

                match command:
                    case "Execute":
                        print("executing")
                        result = self.HandleRunCommand(inst, "Custom")
                        self.wfile.write(bytes("% s" % result,"utf-8"))
                    case "Script":
                        foundScript = self.FindScript(inst)
                        if foundScript != None:
                            print("Found script")
                            result = self.HandleRunCommand(foundScript, inst)
                            self.wfile.write(bytes("Script ran... \n % s" % result,"utf-8"))
                        else:
                            print("Failed to collect script")
                            self.wfile.write(bytes("Failed to find script","utf-8"))
                    case _:
                        self.wfile.write(bytes("Incompatible command, Failed","utf-8"))
            else:
                self.wfile.write(bytes("Failure","utf-8"))

        except json.JSONDecodeError as err:
            print("Failed to parse Json", err)

    def HandleRunCommand(self, inst, title):
        print("Running script... % s " % title)
        execResult = subprocess.check_output(inst, shell = True)
        print("Script complete")
        return execResult

    def FindScript(self, scriptTitle):
        print("Checking for script for % s" % scriptTitle)
        match scriptTitle:
            case "Test":
                return 'echo -e "Successfully tested script"'
            case _:
                return None

webServer = HTTPServer((hostName, serverPort), Server)
print("Server started http://%s:%s" % (hostName, serverPort))

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()

print("Program Complete")
