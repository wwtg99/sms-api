import time
import uuid
import hashlib
import json
import base64
import requests
from flask import g, current_app
from werkzeug.utils import import_string


def create_sms():
    provider = current_app.config['SMS_PROVIDER']
    sms_config = current_app.config['SMS_CONF']
    if provider in sms_config:
        cls = sms_config[provider]['provider_cls']
        conf = sms_config[provider]['config']
        sms = import_string(cls)(**conf)
        return sms
    return None


def get_sms():
    if 'sms' not in g:
        g.sms = create_sms()
    return g.sms


class SmsProvider:

    def __init__(self, **kwargs):
        self.conf = kwargs

    def send(self, template, receivers, **kwargs):
        pass


class AliyunSmsProvider(SmsProvider):

    def send(self, template, receivers, **kwargs):
        from aliyunsdkcore.request import CommonRequest
        client = self.get_client(self.conf['app_key'], self.conf['app_secret'], self.conf['region_id'])
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain(self.conf['domain'])
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version(self.conf['version'])
        request.set_action_name('SendSms')
        request.add_query_param('RegionId', self.conf['region_id'])
        request.add_query_param('PhoneNumbers', receivers)
        request.add_query_param('SignName', self.conf['sign_name'])
        request.add_query_param('TemplateCode', self.get_template_id(template))
        request.add_query_param('TemplateParam', self.build_template_params(**kwargs))
        return client.do_action_with_exception(request)

    def get_template_id(self, name):
        if name in self.conf['template_id_map']:
            return self.conf['template_id_map'][name]
        else:
            raise ValueError('no template {} found!'.format(name))

    @staticmethod
    def get_client(app_key, app_secret, region_id):
        from aliyunsdkcore.client import AcsClient
        return AcsClient(app_key, app_secret, region_id)

    @staticmethod
    def build_template_params(**kwargs):
        if 'params' in kwargs and kwargs['params']:
            return json.dumps(kwargs['params'])
        else:
            return ''


class HuaweiSmsProvider(SmsProvider):

    def send(self, template, receivers, **kwargs):
        header = {'Authorization': 'WSSE realm="SDP",profile="UsernameToken",type="Appkey"',
                  'X-WSSE': self.build_wsse_header(self.conf['app_key'], self.conf['app_secret'])}
        form_data = {
            'from': self.conf['sender'],
            'to': receivers,
            'templateId': self.get_template_id(template),
            'templateParas': self.build_template_params(**kwargs),
        }
        r = requests.post(self.conf['url'], data=form_data, headers=header, verify=False)
        return r

    def get_template_id(self, name):
        if name in self.conf['template_id_map']:
            return self.conf['template_id_map'][name]
        else:
            raise ValueError('no template {} found!'.format(name))

    @staticmethod
    def build_wsse_header(app_key, app_secret):
        now = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        nonce = str(uuid.uuid4()).replace('-', '')
        digest = hashlib.sha256((nonce + now + app_secret).encode()).hexdigest()
        digest_base64 = base64.b64encode(digest.encode()).decode()
        return 'UsernameToken Username="{}",PasswordDigest="{}",Nonce="{}",Created="{}"'.format(app_key, digest_base64,
                                                                                                nonce, now)

    @staticmethod
    def build_template_params(**kwargs):
        if 'params' in kwargs and kwargs['params']:
            return json.dumps(list(kwargs['params'].values()))
        else:
            return ''
