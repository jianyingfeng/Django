# 重写处理payload的函数
# 原函数路径：rest_framework_jwt.utils.jwt_response_payload_handler
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'userid': user.id,
        'username': user.username,
        'token': token,
    }