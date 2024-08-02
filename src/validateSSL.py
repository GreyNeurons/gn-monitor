import requests 

#url = "https://www.labboozcafeandlodge.com/"
#url = "http://www.google.com"
#url = "http://icicibank.com"
#url = "https://abvz.com"
url = "https://expired.badssl.com"
try:
    response = requests.get(url, verify=True)
    if response.url.startswith("https://"):
        print (f"The URL '{url}' is using SSL")
    else:
        print (f"The URL'{url}' is not using SSL")
except requests.exceptions.SSLError:
    print (f"SSL certificate has expired")
except requests.exceptions.ConnectionError:
    print (f"Cannot connect to '{url}'")
except requests.exceptions.Timeout:
    print (f"Connection to {url} timed out")
except requests.exceptions.RequestException as e:
    print (f"An error occurred {e}")
    
