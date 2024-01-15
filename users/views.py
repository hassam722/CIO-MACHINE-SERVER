from django.shortcuts import render,redirect
from users.models import *
from datetime import datetime,timedelta
from functools import wraps
from django.http import HttpResponseForbidden
from django.http import JsonResponse
import json
from users.functions import authenticate_with_name,createmsgdict


def restrict_direct_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Add your access control logic here
        # For example, check for custom headers, authentication, or IP whitelisting
        
        # Example: Check for a custom header
        custom_header_value = request.headers
        # print(custom_header_value)
        try:
            if custom_header_value["header-check"] != 'function-request':
                return HttpResponseForbidden("Access denied")
        except KeyError:
            return HttpResponseForbidden("Access denied")
        
        return view_func(request, *args, **kwargs)

    return _wrapped_view





# Create your views here.
def get_all_users():
    _users = user.objects.values_list("username","id","nfcnum")
    temp_list = []
    for item in _users:
        temp_dict = dict()
        temp_dict["id"]=item[1]
        temp_dict["name"]=item[0]
        temp_dict["nfc"] = item[2]
        temp_list.append(temp_dict)
    return temp_list


def getUsers(request,user_data=None):
    users_list = get_all_users()
    context_dic = {}
    if len(users_list)==0:
        context_dic["message"]="NoUserPresent"
    else:
        context_dic["users_list"]=list(users_list)

    if user_data:
        context_dic["one_day_data"] =user_data
    return render(request,"user.html",context=context_dic)


def getSpecficUser(request,username):
    _date_time = datetime.now()
    if not authenticate_with_name(user_name=username):
        error_dic= {"error_title":"NoUrlFound","actual_error":"NoPageFound"}
        return render(request,"error.html",context=error_dic)
    _user = user.objects.get(username = username)

    try:
        user_data_ = user_data.objects.get(date = _date_time.date(),userid = _user)
        temp_dic = {"date":user_data_.date,"checkintime":user_data_.checkintime,"checkouttime":user_data_.checkouttime,"timediff":str(user_data_.timediff)}
    except:
        user_data_=user_data(date="-",checkintime="-",checkouttime="-",timediff="-")
        temp_dic = {"date":user_data_.date,"checkintime":user_data_.checkintime,"checkouttime":user_data_.checkouttime,"timediff":str(user_data_.timediff)}

    return getUsers(request,temp_dic)



def time_format(time:str):
    h,m,s = time.split(":")
    if int(h) in range(0,12):
        return h+":"+m+" a.m."
    else:
        h1 = int(h)%12
        return str(h1)+":"+m+" p.m."


@restrict_direct_access
def week_data(request):
    custom_header_value = request.headers
    garbage, username = custom_header_value["username"].split('/')
    user_ = user.objects.get(username =username)
    x=datetime.now()
    yesterday_date =  (x-timedelta(days=1)).strftime("%Y-%m-%d")
    week_date = (x-timedelta(days=7)).strftime("%Y-%m-%d")
    return JsonResponse(sort_the_data(from_date=week_date,to_date=yesterday_date,user=user_))

@restrict_direct_access
def month_data(request):
    custom_header_value = request.headers
    garbage, username = custom_header_value["username"].split('/')
    user_ = user.objects.get(username =username)
    x=datetime.now()
    yesterday_date =  (x-timedelta(days=1)).strftime("%Y-%m-%d")
    month_date = (x-timedelta(days=30)).strftime("%Y-%m-%d")
    return JsonResponse(sort_the_data(from_date=month_date,to_date=yesterday_date,user = user_))



@restrict_direct_access
def year_data(request):
    custom_header_value = request.headers
    garbage, username = custom_header_value["username"].split('/')
    user_ = user.objects.get(username =username)
    x=datetime.now()
    yesterday_date =  (x-timedelta(days=1)).strftime("%Y-%m-%d")
    year_date = (x-timedelta(days=365)).strftime("%Y-%m-%d")
    return JsonResponse(sort_the_data(from_date=year_date,to_date=yesterday_date,user=user_))


@restrict_direct_access
def add_user(request):
    body_dict =json.loads(request.body)
    first_name = body_dict["firstname"]
    last_name = body_dict["lastname"]
    username = str(first_name).capitalize()+str(last_name).capitalize()
    if(authenticate_with_name(user_name=username)):
        return JsonResponse(createmsgdict(106))       
    user_ = user(username=username).save()
    return JsonResponse(createmsgdict(102))



def sort_the_data(from_date,to_date,user):
    temp_dict =dict()
    data = user_data.objects.raw(f"select * from users_user_data where date <='{to_date}' and date>='{from_date}' and userid_id ={user.id}")
    i = 0
    for s_data in data:
        temp_dict[i] = {"date":s_data.date.strftime("%b. %d, %Y"),"checkintime":time_format(str(s_data.checkintime)),"checkouttime":time_format(str(s_data.checkouttime)),"timediff":str(s_data.timediff)}
        i+=1
    # print(temp_dict)
    return temp_dict