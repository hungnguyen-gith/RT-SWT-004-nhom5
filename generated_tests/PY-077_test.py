import pytest

class ProxyManager:
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


@pytest.fixture
def capabilities():
    return {}


def test_add_to_capabilities_with_all_fields(capabilities):
    manager = ProxyManager(
        proxyType='manual',
        autodetect=True,
        ftpProxy='ftp://proxy.example.com',
        httpProxy='http://proxy.example.com',
        proxyAutoconfigUrl='http://proxy.pac',
        sslProxy='https://proxy.example.com',
        noProxy='localhost,127.0.0.1',
        socksProxy='socks://proxy.example.com',
        socksUsername='user',
        socksPassword='pass'
    )
    manager.add_to_capabilities(capabilities)
    assert capabilities['proxy'] == {
        'proxyType': 'manual',
        'autodetect': True,
        'ftpProxy': 'ftp://proxy.example.com',
        'httpProxy': 'http://proxy.example.com',
        'proxyAutoconfigUrl': 'http://proxy.pac',
        'sslProxy': 'https://proxy.example.com',
        'noProxy': 'localhost,127.0.0.1',
        'socksProxy': 'socks://proxy.example.com',
        'socksUsername': 'user',
        'socksPassword': 'pass'
    }


def test_add_to_capabilities_with_no_optional_fields(capabilities):
    manager = ProxyManager(proxyType='manual')
    manager.add_to_capabilities(capabilities)
    assert capabilities['proxy'] == {
        'proxyType': 'manual'
    }


def test_add_to_capabilities_with_only_autodetect(capabilities):
    manager = ProxyManager(proxyType='manual', autodetect=True)
    manager.add_to_capabilities(capabilities)
    assert capabilities['proxy'] == {
        'proxyType': 'manual',
        'autodetect': True
    }


def test_add_to_capabilities_with_empty_capabilities(capabilities):
    manager = ProxyManager(proxyType='manual')
    manager.add_to_capabilities(capabilities)
    assert capabilities == {'proxy': {'proxyType': 'manual'}}


def test_add_to_capabilities_with_none_values(capabilities):
    manager = ProxyManager(
        proxyType='manual',
        ftpProxy=None,
        httpProxy=None,
        proxyAutoconfigUrl=None,
        sslProxy=None,
        noProxy=None,
        socksProxy=None,
        socksUsername=None,
        socksPassword=None
    )
    manager.add_to_capabilities(capabilities)
    assert capabilities['proxy'] == {
        'proxyType': 'manual'
    }