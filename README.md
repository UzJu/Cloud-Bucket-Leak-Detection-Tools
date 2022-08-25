![image-20220703203021188](images/image-20220703203021188.png)

# :rooster:使用教程

```bash
git clone https://github.com/UzJu/Cloud-Bucket-Leak-Detection-Tools.git
cd Cloud-Bucket-Leak-Detection-Tools/
# 安装依赖 建议使用Python3.8以上的版本 我的版本: Python 3.9.13 (main, May 24 2022, 21:28:31)
# 已经测试版本如下
# 1、python3.8.9
# 2、python3.9.13
# 3、python3.7
# 4、python3.6.15
# 5、python3.9.6
pip3 install -r requirements.txt
python3 main.py -h
```

![image-20220716140707903](images/image-20220716140707903.png)

使用之前需要在`config/conf.py`文件配置自己对应的云厂商AK

![image-20220716140934866](images/image-20220716140934866.png)

## 1、阿里云存储桶

### 1.1、单个存储桶检测

```bash
python3 main.py -aliyun [存储桶URL]
```

![image-20220716141132931](images/image-20220716141132931.png)

### 1.2、自动存储桶劫持

当如果检测存储桶不存在时会自动劫持该存储桶

![image-20220703202339058](images/image-20220703202339058.png)

### 1.3、批量存储桶地址检测

```bash
# fofa语法
domain="aliyuncs.com"
server="AliyunOSS"domain="aliyuncs.com"
```

```bash
# 使用-faliyun
python3 main.py -faliyun url.txt
```

![image-20220716141356518](images/image-20220716141356518.png)

## 2、腾讯云存储桶

```bash
python3 main.py -tcloud [存储桶地址]
```

![image-20220716141554856](images/image-20220716141554856.png)

## 3、华为云存储桶

```bash
python3 main.py -hcloud [存储桶地址]
```

![image-20220716141948046](images/image-20220716141948046.png)

## 4、AWS存储桶

```bash
python3 main.py -aws [存储桶地址]
```

![image-20220716142431142](images/image-20220716142431142.png)

## 5、扫描结果保存

扫描结果会存放在`results`目录下

![image-20220716142617997](images/image-20220716142617997.png)

![image-20220716142641883](images/image-20220716142641883.png)

# :cop:0xFFFFFFFF 免责声明

1、本工具只作为学术交流，禁止使用工具做违法的事情

2、只是写着玩

3、我的微信

> 如果你有更好的建议或者交个朋友

<img src="images/157070417-dbb7886f-1bb8-412f-a30b-0f85bc8ffa10.png" alt="image" style="zoom:33%;" />

4、博客: UzzJu.com
5、公众号

![image-20220716143619529](images/image-20220716143619529.png)

## 404星链计划
![](https://github.com/knownsec/404StarLink-Project/raw/master/logo.png)

**Cloud-Bucket-Leak-Detection-Tools** 现已加入 [404星链计划](https://github.com/knownsec/404StarLink)

# 曲线图

[![Stargazers over time](images/Cloud-Bucket-Leak-Detection-Tools.svg)](https://starchart.cc/UzJu/Cloud-Bucket-Leak-Detection-Tools)