# 错误码
ERROR_CODE = {
    "PARAMS_ERROR": 1001,
    "USER_NOT_EXIST": 2001,
    "PWD_ERROR": 2002,
    "EMPTY_USER_TOKEN": 2003,
    "CAPTCHA_ERROR": 2004,
    "USER_EXIST": 2005,
    "VERIFY_CODE_ERROR": 2006,
    "EMAIL_LIMIT": 2007,
    "EMAIL_TIME_LIMIT": 2008,
    "REGISTER_ERROR": 2009,
    "MODIFY_PASSWORD_ERROR": 2010,
    "LOGIN_EXPIRED": 2011,
    "WALLET_SIGN_ERROR": 2012,
    "NOT_AUTHORIZED": 4001,
    "TOKEN_NOT_SUPPORTED": 5001,
    "PLATFORM_NOT_SUPPORTED": 5003,
    "NO_REMAINING_TIMES": 5004,
    "PATH_API_ERROR": 6001,
    "SWAP_OUT_OF_RANGE": 6002,
    "SWAP_ADDRESS_ERROR": 6003
}

# 错误信息
ERROR_MESSAGE = {
    1001: 'Params error',
    2001: 'User not exist',
    2002: 'User password error',
    2003: 'User Token is empty',
    2004: 'Captcha code error',
    2005: 'User already exists, please use another email',
    2006: 'Email verify-code error',
    2007: 'Send Email Limit',
    2008: 'Send Email Time-limit, Please Try Later',
    2009: 'User Register Error',
    2010: 'User Modify Password Error',
    2011: 'User Login Time Out',
    2012: 'User Wallet Sign Message Error',
    4001: 'User Not Authorized',
    5001: 'The token you mentioned not supported',
    5003: 'The platform not supported swap',
    5004: 'No remaining times',
    6001: 'Path Api Request Error',
    6002: 'Exchange Out of Range',
    6003: 'Swap From or To Address Error'
}
