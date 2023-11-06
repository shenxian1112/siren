导入请求
导入base64
导入时间

base_url="http://www.plcly.cn:97/api/bd"
AccountNumber="农夫山泉牛逼"#固定的账号

user_cardIds=[]

# 输入名字和身份证的信息
打印("请输入用户数据，格式为：名字身份证号，每行一条数据，输入完成后请输入空行：")
当为True时：
input_line=input()
如果不是输入线(_L)：
打破
用户，CardID=input_line.split()
user_cardIds.append((用户，CardID))

对于用户，user_cardIds中的CardID：
params={"user"：user，"CardID"：CardID，"accountNumber"：accountNumber}
start_time=time.time()#获取开始时间
response=requests.get(base_url，params=params，timeout=300)#设置超时时间为300秒
end_time=time.time()#获取结束时间
eapsed_time=end_time-start_time#计算请求耗时
data=response.json()
# 处理返回的数据
result=data.get("result")

如果结果不是None：
image_data=base64.b64decode(结果)
# 保存图片到当前目录下
image_path=f"{user}_{CardID}.jpg"
将打开(image_path，"wb")作为文件：
file.write(image_data)
打印(f"图片已保存：{image_path}")
其他：
打印("未检测到结果")

如果经过时间>300：#如果超出5分钟，则终止程序
打印(f”请求超时（5分钟），终止程序。")
打破
