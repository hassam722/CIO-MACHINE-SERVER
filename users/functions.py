from users.models import *
from datetime import datetime,timedelta
from users.constant import *

def authenticate(nfc_num=None,id=None):
    if id:
        try:
            _user  =user.objects.get(id= id)
        except user.DoesNotExist:
            return False
        return True    
    
    try:
        _user  =user.objects.get(nfcnum= nfc_num)
    except user.DoesNotExist:
        return False
    return True


def authenticate_with_name(user_name):
    try:
        _user  =user.objects.get(username= user_name)
    except user.DoesNotExist:
        return False
    return True
    


def add_user_nfc(id,nfcnum):
    _user = user.objects.get(id=id)
    _user.nfcnum = nfcnum
    _user.save()
    
def checkin(nfc_num):
    _user = user.objects.get(nfcnum= nfc_num)
    _date_time= datetime.now()
    _date = _date_time.date()
    _time = _date_time.time()
    try:
        _user_data = user_data.objects.get(date =_date,userid =_user)
        # return createmsg(103)
        return str("3")
    except user_data.DoesNotExist:
        temp = user_data(date = _date,checkintime = _time,userid = _user)
        temp.save()
        # return createmsg(102)
        return str("2")
    

        
    
def checkout(nfc_num):
    _user = user.objects.get(nfcnum= nfc_num)
    _date_time= datetime.now()
    _date = _date_time.date()
    _time = _date_time.time()
    try:
        _user_data = user_data.objects.get(date =_date,userid = _user)
    except user_data.DoesNotExist:
        # return createmsg(105)
        return str("5")
    if(_user_data.checkouttime==None):
        _user_data.checkouttime = _time
        time_diff = timedelta(hours=_time.hour,minutes=_time.minute,seconds=_time.second) - timedelta(hours=_user_data.checkintime.hour,minutes=_user_data.checkintime.minute,seconds=_user_data.checkintime.second)
        _user_data.timediff = str(time_diff)
        _user_data.save()
        # return createmsg(102)
        return str("2")
    else:
        # return createmsg(104)
        return str("4")

    
def createmsg(msg_num):
    temp = {CHECK:MESSAGES[msg_num]}
    return str(temp)

def createmsgdict(msg_num):
    temp = {CHECK:MESSAGES[msg_num]}
    return temp
