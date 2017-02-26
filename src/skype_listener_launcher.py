# from time import timezone
from skype_message_processor import SkypeMessageProcessor
import json
# from bson import json_util
import sys
import signal
from datetime import datetime, timezone

def signal_handler(signal, frame):
	print('You pressed Ctrl+C!')
	sys.exit(0)

if __name__ == "__main__":
    username = ""
    password = ""
    token = ""
    if (len(sys.argv) == 1 or len(sys.argv) == 3 or len(sys.argv) > 4):
        print("Skype incoming message listener")
        print()
        print("Usage:")
        print("\"skype_listener_launcher.py tokenname\" to call with an auth token filename")
        print("\"skype_listener_launcher.py username password tokenname\" to call with an auth token filename and a username and password for a case when token ain't working")
        sys.exit(-1)

    if (len(sys.argv) == 2):
        token = sys.argv[1]
    if (len(sys.argv) == 4):
        username = sys.argv[1]
        password = sys.argv[2]
        token = sys.argv[3]

    try:
        signal.signal(signal.SIGINT, signal_handler)
        print ("Init")
        skype = SkypeMessageProcessor()
        skype.logIntoSkype(username, password, token)
        print ("Loaded")
        skype.loop()
    except Exception as ex:
        sys.stderr.write(json.dumps({
            "event": "Error",
            "source": u"skype_listenner_lanucher",
            "type": ex.__class__.__name__,
            "content": str(ex),
            "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        }, separators=(',',':')))
        print ("$$$$$$$$  SYS  $$$$$$$: ", sys)
        sys.exit(-1)