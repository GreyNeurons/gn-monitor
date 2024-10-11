import datetime
from lib.check_domain import get_domain_expiry_date


def test_expiry():
    url = "https://www.greyneuronsconsulting.com"
    expected_date = datetime.datetime(2025, 2, 10, 5, 17, 38)

    expiry_dates = get_domain_expiry_date(url)
    assert expiry_dates

    for date in expiry_dates:
        assert date == expected_date


def test_no_expiry():
    expiry_dates = get_domain_expiry_date("https://thisshouldnot.exist")
    assert expiry_dates[0] is None
