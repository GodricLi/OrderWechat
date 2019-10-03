# _*_coding:utf-8 _*_
# @Author　 : Ric
import base64
import hashlib
import random
import string


class UserService:
    @staticmethod
    def gene_auth_code(user_info=None):
        m = hashlib.md5()
        s = f'{user_info.uid}-{user_info.login_name}-{user_info.login_pwd}-{user_info.login_salt}'
        m.update(s.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def gene_pwd(pwd, salt):
        m = hashlib.md5()
        s = f"{base64.encodebytes(pwd.encode('utf-8'))}-{salt}"
        m.update(s.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def get_salt(length=16):
        key_list = [random.choice((string.ascii_letters + string.digits)) for _i in range(length)]
        return "".join(key_list)
