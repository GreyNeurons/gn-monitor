from lib.check_ssl import check_ssl


def test_noURL():
    assert check_ssl("https://abvz.com") == (
        True,
        "Cannot connect to: https://abvz.com",
    )


def test_sslExpired1():
    assert check_ssl("https://www.labboozcafeandlodge.com/") == (
        True,
        "SSL certificate has expired.",
    )


def test_sslExpired2():
    assert check_ssl("https://expired.badssl.com/") == (
        True,
        "SSL certificate has expired.",
    )


def test_sslValidRedirect():
    assert check_ssl("http://www.icicibank.com") == (False, "")


def test_sslValidNoNotify():
    assert check_ssl("https://www.icicibank.com") == (False, "")


def test_sslValidNotify():
    assert check_ssl("https://www.google.com") == (
        True,
        "SSL certificate will expire within 65 days.",
    )
