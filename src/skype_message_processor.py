import json
# from bson import json_util
import sys
from datetime import datetime, timezone
from skpy import Skype, SkypeAuthException, SkypeEventLoop, SkypeNewMessageEvent

class SkypeMessageProcessor(SkypeEventLoop):

    username = ""
    password = ""
    token = ""

    def onEvent(self, event):
        try:
            if isinstance(event, SkypeNewMessageEvent) \
              and not event.msg.userId == self.userId:
                # event.msg.chat.sendMsg("Pong!")
                print("Message: " + event.msg.content)
                dt = event.msg.time
                ntime = dt.strftime("%Y-%m-%d %H:%M:%S")
                print("time: ", ntime)
                print(json.dumps({
                    "event": "NewMessage",
                    "source": u"skype",
                    "author": event.msg.userId,
                    "contentType": event.msg.type,
                    "content": event.msg.content,
                    # "time": event.msg.time
                    "time": ntime
                }, separators=(',',':')))
                if event.msg.content == "logintoagain":
                    print ("Loggin into again")
                    self.logIntoSkype(self.username, self.password, self.token)
        except Exception as ex:
            dt = datetime.now(timezone.utc)
            ntime = dt.strftime("%Y-%m-%d %H:%M:%S")
            sys.stderr.write(json.dumps({
                    "event": "Error",
                    "source": u"skype_message_processor",
                    "type": ex.__class__.__name__,
                    "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "time": ntime,
                    "content": str(ex)
                }, separators=(',',':')))
            sys.stderr.write("Loggin into skype accout again")
            self.logIntoSkype(self.username, self.password, self.token)

    def logIntoSkype(self, username, password, token):
        self.username = username
        self.password = password
        self.token = token
        try:
            self.conn.tokenFile = token
            try:
                self.conn.readToken()
                print ("Token already exists. Connect with it")
                print(self.conn)
            except (SkypeAuthException, IOError):
                if (not username or not password):
                    sys.stderr.write(json.dumps({
						"username": username,
						"password": password,
                        "event": "Error",
                        "source": u"skype_message_processor",
                        "type": "Internal",
                        "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                        "content": "Token is invalid and username or password was not specified"
                    }, separators=(',',':')))
                    sys.exit(-1)
                print(SkypeAuthException)
                # Prompt the user for their credentials.
                self.conn.setUserPwd(username, password)
                # Create token file and Reconnect
                self.conn.getSkypeToken()
                self.conn.readToken()
                print(self.conn)

        except Exception as ex:
            sys.stderr.write(json.dumps({
                "event": "Error",
                "source": u"skype_message_processor",
                "type": ex.__class__.__name__,
                "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "content": str(ex)
            }, separators=(',',':')))
            sys.exit(-1)