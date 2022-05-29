# :rooster:0x00 前言

![image-20220529132925098](images/image-20220529132925098.png)

> 2022年3月7日
>
> 我觉得文档写的还不是很清楚，等有空更新一下文档完整的使用教程
> 2022年3月8日
>
> 2022年5月29日
>
> 1、更新了aws存储桶检测功能
>
> 2、感觉更新有些慢了，这段时间比较忙，其实本地的新版本写好了，一直没有push

**使用教程**: [使用教程](使用教程.md)

**语言/Language**

English README: [English](README.en.md)

想写个存储桶的利用，先给自己画个饼

+ 阿里云（Aliyun Cloud Oss）
+ 腾讯云（Tencent Cloud COS）
+ 华为云 （HuaWei Cloud OBS）
+ AWS （Amazon S3 Bucket）
+ Azure （Azure Blob）
+ GCP （Google Cloud Bucket)

工具名称我都没想好，相信大佬们看到项目名就知道...机翻王

如果觉得用的还行，可以提issue给工具起个名字？:sos:

:waning_crescent_moon:**画饼进度**

1、阿里云存储桶利用

不太会用Git，代码写的也烂，有BUG直接提Issue即可（好像我连issue可能都用不明白）

> 好在二爷给我推荐的GitHub Desktop 二爷YYDS

2、AWS存储桶利用

# :pill:0x01 依赖

+ pip3 install oss2
+ pip3 install colorlog
+ pip3 install argparse
+ pip3 install boto3

# :gun:0x02 使用方法

```bash
git clone https://github.com/UzJu/Cloud-Bucket-Leak-Detection-Tools.git
python3 main.py -h
```

随后在config/conf.py中写入自己的AK，作用如下

1、如果可以劫持，会用该AK创建同名的存储桶

2、用来验证合法用户

![image-20220304184757595](images/UzJuMarkDownImageimage-20220304184757595.png)

## 1、当存储桶Policy权限可获取时

![image-20220304185015693](images/UzJuMarkDownImageimage-20220304185015693.png)

## 2、当存储桶不存在时(自动创建并劫持)

![image](images/156925718-9a3dc236-0ef6-4afa-8d26-a2946fe876b2.png)

## 3、批量检测存储桶

新增批量存储桶的检测功能，推荐fofa一键导出所有资产

**fofa**

```bash
domain="aliyuncs.com"
server="AliyunOSS"domain="aliyuncs.com" #不推荐该语法
```

```bash
python3 main.py -f aws/aliyun filepath

# 例如
python3 main.py -f aws ./url.tx\\\\\\\``````````````````````````````````````````````````````````````````````````
```

随后等待即可，扫描结果会在results目录下，文件名为当天的日期

![image](images/156925744-3c012b86-6449-4cf1-a790-b2c1282f76bd.png)

![image](images/156925758-36a8fcba-8bc8-4d1a-8863-d8110dbe0b71.png)

只会保存有权限操作的存储桶
![image](images/156925766-15d415d3-d573-4b54-ab0f-5c79bc1966ad.png)

输入存储桶地址即可自动检测，功能如下

+ 1、检测当前存储桶是否可劫持
  + 如果可劫持，自动在config中写入的AK账号上创建同命名的存储桶并开放所有权限
+ 2、检测当前存储桶是否可列出Object
+ 3、检测当前存储桶是否可获取ACL
+ 4、检测当前存储桶是否可获取Policy策略表
+ 5、检测存储桶是否可上传Object
+ 6、批量检测功能

## 4、域名检测功能

很多存储桶都解析了域名，新增判断域名的CNAME，然后取CNAME来进行检测

**现在可以直接导入大量域名资产来进行检测，会自动判断域名的CNAME**

![image-20220307231827585](images/UzJuMarkDownImageimage-20220307231827585.png)

# 0x03 阿里云存储桶利用

### 1、实现思路

首先实现了`OssBucketCheckFromSDK`类

+ AliyunOssBucketDoesBucketExist

  + 用来判断当前存储桶是否存在，首先如果存储桶存在那么就返回一个True，继续走下面的流程，如果存储桶不存在，那么就调用OssBucketExploitFromSDK类，创建存储桶，并且设置ACL权限，上传访问策略，随后上传一个文件进行验证，如果存储桶此时存在或者为AccessDenied，继续走下面的流程

+ AliyunOssGetBucketObjectList

  + 判断是否可以遍历存储桶中的内容，如果可以，则会选择前3个内容进行遍历并显示

    > 如果想遍历更多的内容，可以查看aliyunOss.py中的AliyunOssGetBucketObjectList方法

+ AliyunOssGetBucketAcl

  + 判断能否访问当前Bucket的ACL，如果可以的话，就返回当前Bucket的ACL，如果不可以就继续走下面的Check流程

+ AliyunOssGetBucketPolicy

  + 判断能否访问当前Bucket的Policy，如果可以的话，就会返回当前Bucket的ACL，如果不可以就继续走下面的Check

+ AliyunOssGetBucketObject

  + 尝试上传一个文件，是否可以成功上传

# 0x04 Aws存储桶利用

```bash
python3 main.py -aws xxxx
```

![image-20220529094124272](images/image-20220529094124272.png)

# 0x05 利用后results文件解释

在results目录下可以看到存在问题的存储桶

![image-20220529134339645](images/image-20220529134339645.png)

1、ListObject 代表该存储桶的内容可以列出来

2、PutObject 代表该存储桶可以上传任意的文件

3、NoSuchBucket 代表该存储桶可以接管

4、GetBucketACL 代表可以获取该存储桶的ACL

5、GetBucketPolicy  代表可以获取该存储桶的策略配置

# :older_man:0x040001 更新日志

**2022年3月6日**

+ 新增批量扫描功能
+ 修复Fake_UserAgent报错的问题

> 其实是直接把这个库删了，不用了^ ^

**2022年3月7日**

+ 新增域名检测

**2022年5月29日**

- 新增AWS存储桶扫描

# :cop:0xffffffff 免责声明

免责声明

1、本工具只作为学术交流，禁止使用工具做违法的事情

2、只是写着玩

3、我的微信

> 如果你有更好的建议或者交个朋友

![image](images/157070417-dbb7886f-1bb8-412f-a30b-0f85bc8ffa10.png)

# 曲线图

[![Stargazers over time](https://starchart.cc/UzJu/Cloud-Bucket-Leak-Detection-Tools.svg)](https://starchart.cc/UzJu/Cloud-Bucket-Leak-Detection-Tools)

