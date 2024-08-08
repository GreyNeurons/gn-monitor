import datetime 
from lib.check_domain import get_domain_expiry_date


def test_url():
    url = "https://www.greyneuronsconsulting.com"  # Replace with your URL
    expiry_dates = get_domain_expiry_date(url)
    print(expiry_dates)
    if expiry_dates:
        for date in expiry_dates:
            print(f"Domain Expiry Date for {url}: {date}")
            assert date == datetime.datetime(2025, 2, 10, 5, 17, 38)
    else:
        print("Could not retrieve domain expiry date.")
