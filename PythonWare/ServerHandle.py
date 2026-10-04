import json
import subprocess

from http.server import BaseHTTPRequestHandler, HTTPServer
from Init import serverSettings

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
        settings = self.server.settings

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            passAttempt = data.get("pass")
            if passAttempt == settings.passWord:
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
