REDIS_KEYS = {
    'USER_KEYS': {
        'USER_TOKEN': 'USER_TOKEN_{}_{}',
        'EMAIL_CODE': 'EMAIL_CODE_{}_{}',
        'CAPTCHA_CODE': 'CAPTCHA_CODE_{}',
        'EMAIL_LIMIT': 'EMAIL:{}:{}',
        'EMAIL_CONTINUE': 'EMAIL_CONTINUE_{}',
        'EMAIL_CODE_OTHER': 'EMAIL_CODE_OTHER_{}_{}_{}',
        'EMAIL_CODE_DEVICE_LIMIT': 'EMAIL_CODE_DEVICE_{}_{}',
        'MODIFY_PASSWORD_WRONG_TIME': 'MODIFY_PASSWORD_WRONG_TIME_{}',
    },
    'RAG_API_KEYS': {
        'KEYS_STATUS': 'KEYS_STATUS_{}'
    },
    'REQUEST_API_KEYS': {
        'API_KEYS': 'API_KEYS',
        'API_KEY_LIMIT': 'REQUEST_API_KEYS:{}_{}',
        'FORBID_API_KEYS': 'FORBID_API_KEYS:{}_{}',
    }
}
