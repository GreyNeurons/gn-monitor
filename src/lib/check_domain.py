import whois


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
