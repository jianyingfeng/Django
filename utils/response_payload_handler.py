# 重写处理payload的函数
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'userid': user.id,
        'username': user.username,
        'token': token,
    }