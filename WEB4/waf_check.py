import requests
from functools import wraps
from flask import request


def waf_check(waf_url, api_key):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            path = request.path.lstrip('/')
            try:
                body_data = request.get_data()
                response = requests.request(
                    method=request.method,
                    url=f"{waf_url}/{path}",
                    headers={
                        "X-API-Key": api_key,
                        "Content-Type": request.headers.get('Content-Type', ''),
                        "X-Real-IP": request.remote_addr
                    },
                    params=request.args,
                    data=body_data,
                    cookies=request.cookies,
                    timeout=30
                )
                if response.status_code == 403:
                    return response.content, 403

                return f(*args, **kwargs)

            except Exception as e:
                print(f"❌ Ошибка WAF: {e}")
                return f(*args, **kwargs)

        return decorated_function

    return decorator