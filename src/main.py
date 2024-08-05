import whois
from pydantic import HttpUrl
from fastapi import FastAPI
from lib.check_access import access_url


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/reachable")
async def read_item(url: HttpUrl):
    accesible, resp_time, is_secure = access_url(url)
    return {
        "url": url,
        "accessible": accesible,
        "response_time": resp_time,
        "is_secure": is_secure,
    }


def get_domain_expiry_date(url):
    try:
        domain_info = whois.whois(url)
        expiry_date = domain_info.expiration_date
        if isinstance(expiry_date, list):
            return expiry_date
        else:
            return [expiry_date]
    except Exception as e:
        print(f"Error retrieving domain information: {e}")
        return None
