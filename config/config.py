import os


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    DEBUG = False
    TESTING = False

    # SMS config
    SMS_PROVIDER = os.environ.get('SMS_PROVIDER')
    SMS_CONF = {
        'aliyun': {
            'provider_cls': 'app.sms.AliyunSmsProvider',
            'config': {
                'domain': 'dysmsapi.aliyuncs.com',
                'version': os.environ.get('ALIYUN_SMS_VERSION') or '2017-05-25',
                'app_key': os.environ.get('ALIYUN_SMS_APP_KEY'),
                'app_secret': os.environ.get('ALIYUN_SMS_APP_SECRET'),
                'region_id': os.environ.get('ALIYUN_SMS_REGION_ID'),
                'sign_name': os.environ.get('ALIYUN_SMS_SIGN_NAME'),
                'template_id_map': {
                    'captcha': 'xxx'
                }
            }
        },
        'huawei': {
            'provider_cls': 'app.sms.HuaweiSmsProvider',
            'config': {
                'url': os.environ.get('HUAWEI_URL'),
                'app_key': os.environ.get('HUAWEI_SMS_APP_KEY'),
                'app_secret': os.environ.get('HUAWEI_SMS_APP_SECRET'),
                'sender': os.environ.get('HUAWEI_SMS_SENDER_ID'),
                'template_id_map': {
                    'captcha': 'xxx'
                }
            }
        }
    }


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


registered_app = [
    'app'
]

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
