import requests
import OpenSSL
import ssl
from datetime import datetime
from datetime import date


def check_ssl(url):
    isNotify = False
    notifyText = ""
    isSSL = False
    try:
        response = requests.get(url, verify=True)
        if response.url.startswith("https://"):
            isSSL = True
    except requests.exceptions.SSLError:
        isNotify = True
        notifyText = "SSL certificate has expired."
    except requests.exceptions.ConnectionError:
        isNotify = True
        notifyText = "Cannot connect to: " + url
    except requests.exceptions.Timeout:
        isNotify = True
        notifyText = "Connection to " + url + " timed out."
    except requests.exceptions.RequestException as e:
        isNotify = True
        notifyText = "An error occured: " + e

    if isSSL:
        # Strip off protocol from the URL
        try:
            # url is AnyUrl object, not a string
            # So string manipulation not needed. Just get the host
            url = url.host
        except AttributeError:
            # This may be from the test where directly string
            # is passed to this function
            url = str(url).split('/')[2]

        # Get SSL expiry date
        cert = ssl.get_server_certificate((url, 443))
        cryptcert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        tsbytes = cryptcert.get_notAfter()
        certts = tsbytes.decode("utf-8")
        certdtstr = datetime.strptime(certts, "%Y%m%d%H%M%S%z").date().isoformat()
        certdt = datetime.strptime(certdtstr, "%Y-%m-%d").date()

        # Get current date & find difference between current & SSL expiry dates
        currdt = date.today()
        dtdiff = certdt - currdt

        # If SSL expiry date is less than 30 days away then send notification
        if dtdiff.days < 30:
            isNotify = True
            notifyText = "SSL certificate will expire within 30 days."

    return isNotify, notifyText
