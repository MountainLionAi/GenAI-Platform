from genaipf.conf.server import SERVICE_NAME

EMAIL_INFO = {
    'REGISTER': {
        'subject': {
            'zh': f'【{SERVICE_NAME}】注册验证码',
            'en': f'【{SERVICE_NAME}】Registration Verification Code'
        }
    },
    'FORGET_PASSWORD': {
        'subject': {
                    'zh': f'【{SERVICE_NAME}】忘记密码',
                    'en': f'【{SERVICE_NAME}】Forgot Password'
        }
    }
}
