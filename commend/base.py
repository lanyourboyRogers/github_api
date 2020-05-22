import requests
import json as json_parser
"""
todo：编写公共方法
1.连接接口的鉴权：github登录的凭证为用户名和密码（放在auth）或者token（放在headers）
2.为了减少代码量，将request各方法封装一下
3.将响应的返回值预处理下，避免之后断言出错
"""

class RestClient():
    def __init__(self, api_root_url, username=None, password=None, token=None):
        self.api_root_url = api_root_url
        self.session = requests.session()
        if username and password:
            self.session.auth = (username, password)
        elif token:
            self.session.headers["Authorization"] = "token {}".format(token)

    def get(self, url, **kwargs):
        return self.request(url, "get", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request(url, "post", data, json, **kwargs)

    def options(self, url, **kwargs):
        return self.request(url, "potions", **kwargs)

    def head(self, url, **kwargs):
        return self.request(url, "head", **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(url, "put", data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(url, "patch", data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, "delete", **kwargs)

    def request(self, url, method_name, data=None, json=None, **kwargs):
        url = self.api_root_url + url
        if method_name == "get":
            return process(self.session.get(url, **kwargs))
        if method_name == "post":
            return process(self.session.post(url, data, json, **kwargs))
        if method_name == "options":
            return process(self.session.options(url, **kwargs))
        if method_name == "head":
            return process(self.session.head(url, **kwargs))
        if method_name == "put":
            return process(self.session.put(url, data, **kwargs))
        if method_name == "patch":
            if json:
                data = json_parser.dumps(json)
            return process(self.session.patch(url, data, **kwargs))
        if method_name == "delete":
            return process(self.session.delete(url, **kwargs))

class Response():
    def __init__(self):
        self.status_code=None
        self.content=None
        self.raw=None

def process(raw_response) -> Response:
    response=Response()
    response.raw=raw_response
    response.status_code=raw_response.status_code
    try:
        response.content=raw_response.json()
    except:
        response.content=raw_response.content
    return response
