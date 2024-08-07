import requests


def access_url(url):
    accessible = False
    response_time = 0
    is_secure = False

    try:
        res = requests.get(url)
        accessible = True
        response_time = res.elapsed.microseconds
        is_secure = res.url.split(":")[0] == "https"
    except Exception as e:
        # accessible is already False, so no action required
        print(url, e)

    return accessible, response_time, is_secure
