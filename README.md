# Cloud-Bucket-Leak-Detection-Tools

想写个存储桶的利用，先给自己画个饼

**画饼进度**

1、阿里云存储桶利用

不太会用Git，代码写的也烂，有BUG直接提Issue即可（好像我连issue可能都用不明白）

# 0x00 依赖

+ pip3 install oss2
+ pip3 install colorlog
+ pip3 install logging
+ pip3 argparse

# 0x01 使用方法

```bash
git clone https://github.com/UzJu/Cloud-Bucket-Leak-Detection-Tools.git
python3 main.py -h
```

随后在config/conf.py中写入自己的阿里云AK，作用如下

1、如果可以劫持，会用该AK创建同名的存储桶

2、用来验证合法用户

![image-20220304184757595](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220304184757595.png)

## 1、当存储桶Policy权限可获取时

![image-20220304185015693](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220304185015693.png)

## 2、当存储桶不存在时(自动创建并劫持)

![image-20220304185434168](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220304185434168.png)

输入存储桶地址即可自动检测，功能如下

+ 1、检测当前存储桶是否可劫持
  + 如果可劫持，自动在config中写入的AK账号上创建同命名的存储桶并开放所有权限
+ 2、检测当前存储桶是否可列出Object
+ 3、检测当前存储桶是否可获取ACL
+ 4、检测当前存储桶是否可获取Policy策略表
+ 5、检测存储桶是否可上传Object

## 一、阿里云存储桶利用

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

### 



