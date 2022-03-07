# :rooster:0x00 Preface

Want to write a storage bucket utilization, first draw a pie for yourself

+ Aliyun Cloud (Aliyun Cloud Oss)
+ Tencent Cloud COS
+ Huawei Cloud OBS
+ AWS (Amazon S3 Bucket)
+ Azure (Azure Blob)
+ GCP (Google Cloud Bucket)

I don't even think about the name of the tool, I believe the big guys will know when they see the project name... King of machine flip

If you think it works fine, you can raise an issue to give the tool a name? :sos:

:waning_crescent_moon:**painting pie progress**

1, Ali cloud storage bucket use

Not too good with Git, code writing also sucks, there are bugs directly mention Issue can (as if I may not even use issue to understand)

> good in the second master to my recommended GitHub Desktop second master YYDS

# :pill:0x01 dependency

+ pip3 install oss2
+ pip3 install colorlog
+ pip3 install logging
+ pip3 install argparse

# :gun:0x02 Usage

```bash
git clone https://github.com/UzJu/Cloud-Bucket-Leak-Detection-Tools.git
python3 main.py -h
```

Then write your own Aliyun AK in config/conf.py, the role is as follows

1, if you can hijack, will use the AK to create a storage bucket of the same name

2, used to verify the legitimate user


![image-20220304184757595](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220304184757595.png)

## 1. When storage bucket Policy permission is available
![image-20220304185015693](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220304185015693.png)

## 2. When the storage bucket does not exist (automatically created and hijacked)
![image-20220304185434168](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220304185434168.png)

## 3、Batch detection of storage bucket

New detection function of batch storage bucket, recommend fofa to export all assets in one click
**fofa**

```bash
domain="aliyuncs.com"
server="AliyunOSS"domain="aliyuncs.com" #This syntax is not recommended
```

```bash
python3 main.py -f filepath
```
Then just wait, the scan results will be in the results directory, the file name is the date of the day
![image-20220306211140577](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220306211140577.png)

![image-20220306211025275](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220306211025275.png)
Only buckets that have permission to operate will be saved
![image-20220306211225341](https://uzjumakdown-1256190082.cos.ap-guangzhou.myqcloud.com/UzJuMarkDownImageimage-20220306211225341.png)
Enter the storage bucket address to automatically detect, the function is as follows

+ 1. Detect whether the current bucket can be hijacked
  + If it can be hijacked, automatically create a bucket with the same name on the AK account written in the config and open all permissions
+ 2. detect whether the current bucket can list Object
+ 3. Check if the current bucket can get ACL
+ 4、Check if the current bucket can get Policy policy table
+ 5、Detect whether the bucket can upload Objects
+ 6、Batch detection function

# 0x03 Ali cloud storage bucket utilization

### 1、Implementation idea

First implement the `OssBucketCheckFromSDK` class

+ AliyunOssBucketDoesBucketExist

  + AliyunOssBucketDoesBucketExist is used to determine whether the current storage bucket exists, first if the bucket exists then return a True, continue with the following process, if the bucket does not exist, then call the OssBucketExploitFromSDK class, create the bucket, and set ACL permissions, upload access policy, then upload a file for verification, if the bucket exists at this time or AccessDenied, continue with the following process

+ AliyunOssGetBucketObjectList

  + determine if the contents of the bucket can be traversed, if so, the first 3 contents will be selected for traversal and displayed

    > If you want to iterate through more content, you can check the AliyunOssGetBucketObjectList method in aliyunOss.py

+ AliyunOssGetBucketAcl

  + determine if the current Bucket's ACL can be accessed, if so, return the current Bucket's ACL, if not, continue with the following Check process

+ AliyunOssGetBucketPolicy

  + Determine if the policy of the current Bucket can be accessed, if so, the ACL of the current Bucket will be returned, if not, continue with the following Check process

+ AliyunOssGetBucketObject

  + Try to upload a file, whether it can be successfully uploaded

# :older_man:0x040001 Update Log

**March 6, 2022**

+ Add batch scan function
+ Fix the problem of Fake_UserAgent reporting errors

> actually just delete this library, don't use it ^ ^

# :cop:0xffffffff Disclaimer

Disclaimers

1、This tool is only for academic exchange, it is forbidden to use the tool to do illegal things

2, just writing for fun
