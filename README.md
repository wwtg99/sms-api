Flask 短信微服务
==============

# Description

基于公有云 API 的短信微服务，提供统一的接口。

支持的公有云：
- 阿里云
- 华为云

# Environments

- SMS_PROVIDER: which cloud provider to use，使用哪个公有云服务，["aliyun", "huawei"]

Aliyun 阿里云配置

- ALIYUN_SMS_VERSION：API 版本，默认 2017-05-25
- ALIYUN_SMS_APP_KEY：App key，阿里云控制台获取
- ALIYUN_SMS_APP_SECRET：App secret，阿里云控制台获取
- ALIYUN_SMS_REGION_ID：Region ID，阿里云区域
- ALIYUN_SMS_SIGN_NAME：Sign name，短信签名，阿里云后台创建审核后提供

HuaweiCloud 华为云配置

- HUAWEI_URL：华为云 API URL
- HUAWEI_SMS_APP_KEY：App key，华为云控制台获取
- HUAWEI_SMS_APP_SECRET：App secret，华为云控制台获取
- HUAWEI_SMS_SENDER_ID：Sender ID，发送签名 ID

# Usage

Run in dev mode

```
python run.sh
```

Run in production mode

```
gunicorn -b 0.0.0.0:80 server:app
```

Run in Docker

Use `Dockerfile` to build docker image and run.

```
docker build -t <image>:<tag> .
docker run -d -p 80:80 <image>:<tag>
```

