from lib.check_access import access_url


class TestUrl:
    def test_access_url(self):
        accessible, resp_time, secure = access_url("http://abc")
        assert not accessible
