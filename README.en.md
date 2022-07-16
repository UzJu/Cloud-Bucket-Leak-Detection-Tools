![image-20220703203021188](images/image-20220703203021188.png)

# :rooster:Tutorial

```bash
git clone https://github.com/UzJu/Cloud-Bucket-Leak-Detection-Tools.git
cd Cloud-Bucket-Leak-Detection-Tools/
pip3 install -r requirements.txt
python3 main.py -h
```

![image-20220716140707903](images/image-20220716140707903.png)

You need to configure your corresponding cloud vendor AK in the `config/conf.py` file before using it.

![image-20220716140934866](images/image-20220716140934866.png)

## 1、Ariyun storage bucket

### 1.1, single storage bucket detection

```bash
python3 main.py -aliyun [BucketURL]
```

![image-20220716141132931](images/image-20220716141132931.png)

### 1.2. Automatic bucket hijacking

Automatically hijack a bucket when it is detected as not existing

![image-20220703202339058](images/image-20220703202339058.png)

### 1.3. Bulk bucket address detection

```bash
# fofa syntax
domain="aliyuncs.com"
server="AliyunOSS" domain="aliyuncs.com"
```

```bash
# Use -faliyun
python3 main.py -faliyun url.txt
```

![image-20220716141356518](images/image-20220716141356518.png)

## 2. Tencent cloud storage bucket

```bash
python3 main.py -tcloud [storage bucket address]
```

![image-20220716141554856](images/image-20220716141554856.png)

## 3. Huawei cloud storage bucket

```bash
python3 main.py -hcloud [storage bucket address]
```

![image-20220716141948046](images/image-20220716141948046.png)

## 4. AWS storage bucket

```bash
python3 main.py -aws [storage bucket address]
```

![image-20220716142431142](images/image-20220716142431142.png)images/image-20220716142431142.png)

## 5. Scan results saving

The scan results will be stored in the `results` directory

![image-20220716142617997](images/image-20220716142617997.png)

![image-20220716142641883](images/image-20220716142641883.png)

# :cop:0xFFFFFFFF Disclaimer

1、This tool is only for academic exchange, it is forbidden to use the tool to do illegal things

2, just writing for fun

3、My WeChat

> If you have a better suggestion or make a friend

<img src="images/157070417-dbb7886f-1bb8-412f-a30b-0f85bc8ffa10.png" alt="image" style="zoom:33%;" />

4、Blog: UzzJu.com
5、Public

![image-20220716143619529](images/image-20220716143619529.png)

# Curve chart

[![Stargazers over time](images/Cloud-Bucket-Leak-Detection-Tools.svg)](https://starchart.cc/UzJu/Cloud-Bucket-Leak-Detection-Tools)