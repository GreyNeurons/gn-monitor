import requests
import OpenSSL
import ssl
from datetime import datetime
from datetime import date

# url = "https://www.labboozcafeandlodge.com/"
# url = "https://www.google.com"
url = "http://www.icicibank.com"
# url = "https://abvz.com"
# url = "https://expired.badssl.com"

isSSL = False
try:
    response = requests.get(url, verify=True)
    if response.url.startswith("https://"):
        print(f"The URL '{url}' is using SSL")
        isSSL = True
    else:
        print(f"The URL'{url}' is not using SSL")
except requests.exceptions.SSLError:
    print(f"SSL certificate has expired")
except requests.exceptions.ConnectionError:
    print(f"Cannot connect to '{url}'")
except requests.exceptions.Timeout:
    print(f"Connection to {url} timed out")
except requests.exceptions.RequestException as e:
    print(f"An error occurred {e}")

if isSSL:
    # Strip off protocol from the URL
    indx = url.find("//")
    if indx != -1:
        url = url[indx + 2 :]
    # print (f"The URL is '{url}'")

    # Get SSL expiry date
    cert = ssl.get_server_certificate((url, 443))
    cryptcert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    tsbytes = cryptcert.get_notAfter()
    certts = tsbytes.decode("utf-8")
    certdtstr = datetime.strptime(certts, "%Y%m%d%H%M%S%z").date().isoformat()
    certdt = datetime.strptime(certdtstr, "%Y-%m-%d").date()
    print(f"SSL expiry date is {certdt}")

    # Get current date & find difference between current & SSL expiry dates
    currdt = date.today()
    print(f"Current date is {currdt}")
    dtdiff = certdt - currdt
    print(f"Difference in current & SSL expiry dates is {dtdiff.days} days")

    # If SSL expiry date is less than 30 days away then send notification
    if dtdiff.days < 30:
        print("isNotify is TRUE")
    else:
        print("isNotify is FALSE")
