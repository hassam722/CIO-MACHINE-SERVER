from channels.generic.websocket import WebsocketConsumer
from users.constant import *
import json
from users.functions import *


class machineConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        json_data = json.loads(text_data)

        if(json_data.get(CHECK)==CHECKIN):
            nfc_num=json_data.get(CHECKIN)
            if(authenticate(nfc_num)):
                msg =checkin(nfc_num)
                self.send(msg)
            else:
                print(createmsg(101))
                # self.send(createmsg(101))
                self.send(str("1"))
        elif(json_data.get(CHECK)==CHECKOUT):
            nfc_num=json_data.get(CHECKOUT)
            if(authenticate(nfc_num)):
                msg =checkout(nfc_num)
                self.send(msg)
            else:
                print(createmsg(101))
                # self.send(createmsg(101))
                self.send(str("1"))
        elif(json_data.get(CHECK)==OPENDOOR):
            nfc_num=json_data.get(OPENDOOR)
            if(authenticate(nfc_num)):
                # self.send(createmsg(102))
                self.send(str("2"))
            else:
                print(createmsg(101))
                # self.send(createmsg(101))
                self.send(str("1"))
        elif(json_data.get(CHECK)==ADDUSER):
            id=json_data.get("id")
            if(authenticate(id=id)):
                nfcnum= json_data.get(ADDUSER)
                if( not authenticate(nfc_num=nfcnum)):
                    add_user_nfc(id,nfcnum)   
            
        else:
            self.disconnect(1000)
    
    def disconnect(self, close_code):
        # Called when the socket closes
        self.close(close_code)
        