import pytest

class TestAddToCapabilities:
    class MockClass:
        def __init__(self, proxyType, autodetect=False, ftpProxy=None, httpProxy=None,
                     proxyAutoconfigUrl=None, sslProxy=None, noProxy=None,
                     socksProxy=None, socksUsername=None, socksPassword=None):
            self.proxyType = {'string': proxyType}
            self.autodetect = autodetect
            self.ftpProxy = ftpProxy
            self.httpProxy = httpProxy
            self.proxyAutoconfigUrl = proxyAutoconfigUrl
            self.sslProxy = sslProxy
            self.noProxy = noProxy
            self.socksProxy = socksProxy
            self.socksUsername = socksUsername
            self.socksPassword = socksPassword

        def add_to_capabilities(self, capabilities):
            proxy_caps = {}
            proxy_caps['proxyType'] = self.proxyType['string']
            if self.autodetect:
                proxy_caps['autodetect'] = self.autodetect
            if self.ftpProxy:
                proxy_caps['ftpProxy'] = self.ftpProxy
            if self.httpProxy:
                proxy_caps['httpProxy'] = self.httpProxy
            if self.proxyAutoconfigUrl:
                proxy_caps['proxyAutoconfigUrl'] = self.proxyAutoconfigUrl
            if self.sslProxy:
                proxy_caps['sslProxy'] = self.sslProxy
            if self.noProxy:
                proxy_caps['noProxy'] = self.noProxy
            if self.socksProxy:
                proxy_caps['socksProxy'] = self.socksProxy
            if self.socksUsername:
                proxy_caps['socksUsername'] = self.socksUsername
            if self.socksPassword:
                proxy_caps['socksPassword'] = self.socksPassword
            capabilities['proxy'] = proxy_caps

    def test_add_to_capabilities_normal(self):
        capabilities = {}
        proxy_instance = self.MockClass(proxyType='manual', httpProxy='http://example.com:8080')
        proxy_instance.add_to_capabilities(capabilities)
        assert capabilities['proxy']['proxyType'] == 'manual'
        assert capabilities['proxy']['httpProxy'] == 'http://example.com:8080'

    def test_add_to_capabilities_with_autodetect(self):
        capabilities = {}
        proxy_instance = self.MockClass(proxyType='auto', autodetect=True)
        proxy_instance.add_to_capabilities(capabilities)
        assert capabilities['proxy']['autodetect'] is True

    def test_add_to_capabilities_with_all_fields(self):
        capabilities = {}
        proxy_instance = self.MockClass(
            proxyType='manual',
            autodetect=True,
            ftpProxy='ftp://example.com:21',
            httpProxy='http://example.com:8080',
            proxyAutoconfigUrl='http://example.com/proxy.pac',
            sslProxy='https://example.com:443',
            noProxy='localhost,127.0.0.1',
            socksProxy='socks5://example.com:1080',
            socksUsername='user',
            socksPassword='pass'
        )
        proxy_instance.add_to_capabilities(capabilities)
        assert capabilities['proxy']['proxyType'] == 'manual'
        assert capabilities['proxy']['autodetect'] is True
        assert capabilities['proxy']['ftpProxy'] == 'ftp://example.com:21'
        assert capabilities['proxy']['httpProxy'] == 'http://example.com:8080'
        assert capabilities['proxy']['proxyAutoconfigUrl'] == 'http://example.com/proxy.pac'
        assert capabilities['proxy']['sslProxy'] == 'https://example.com:443'
        assert capabilities['proxy']['noProxy'] == 'localhost,127.0.0.1'
        assert capabilities['proxy']['socksProxy'] == 'socks5://example.com:1080'
        assert capabilities['proxy']['socksUsername'] == 'user'
        assert capabilities['proxy']['socksPassword'] == 'pass'

    def test_add_to_capabilities_empty_capabilities(self):
        capabilities = {}
        proxy_instance = self.MockClass(proxyType='manual')
        proxy_instance.add_to_capabilities(capabilities)
        assert 'proxy' in capabilities
        assert capabilities['proxy']['proxyType'] == 'manual'

    def test_add_to_capabilities_no_proxy(self):
        capabilities = {}
        proxy_instance = self.MockClass(proxyType='manual', httpProxy=None)
        proxy_instance.add_to_capabilities(capabilities)
        assert 'httpProxy' not in capabilities['proxy']

    def test_add_to_capabilities_boundary_case(self):
        capabilities = {}
        proxy_instance = self.MockClass(proxyType='manual', noProxy='')
        proxy_instance.add_to_capabilities(capabilities)
        assert 'noProxy' in capabilities['proxy']
        assert capabilities['proxy']['noProxy'] == ''

    def test_add_to_capabilities_edge_case(self):
        capabilities = {}
        proxy_instance = self.MockClass(proxyType='manual', socksUsername=None, socksPassword=None)
        proxy_instance.add_to_capabilities(capabilities)
        assert 'socksUsername' not in capabilities['proxy']
        assert 'socksPassword' not in capabilities['proxy']