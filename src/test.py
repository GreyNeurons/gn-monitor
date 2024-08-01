from main import *

if __name__ == "__main__":
    url = "https://www.greyneuronsconsulting.com"  # Replace with your URL
    expiry_dates = get_domain_expiry_date(url)
    if expiry_dates:
        for date in expiry_dates:
            print(f"Domain Expiry Date for {url}: {date}")
    else:
        print("Could not retrieve domain expiry date.")
