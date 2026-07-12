from functions.PY_077 import add_to_capabilities

class Stub:
    def __init__(self, proxyType, autodetect=None, ftpProxy=None, httpProxy=None,
                 proxyAutoconfigUrl=None, sslProxy=None, noProxy=None,
                 socksProxy=None, socksUsername=None, socksPassword=None):
        self.proxyType = proxyType
        self.autodetect = autodetect
        self.ftpProxy = ftpProxy
        self.httpProxy = httpProxy
        self.proxyAutoconfigUrl = proxyAutoconfigUrl
        self.sslProxy = sslProxy
        self.noProxy = noProxy
        self.socksProxy = socksProxy
        self.socksUsername = socksUsername
        self.socksPassword = socksPassword

def test_add_to_capabilities_with_all_proxies():
    capabilities = {}
    stub = Stub(
        proxyType={'string': 'manual'},
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
    add_to_capabilities(stub, capabilities)
    assert 'proxy' in capabilities
    assert capabilities['proxy']['proxyType'] == 'manual'
    assert capabilities['proxy']['autodetect'] is True
    assert capabilities['proxy']['ftpProxy'] == 'ftp://proxy.example.com'
    assert capabilities['proxy']['httpProxy'] == 'http://proxy.example.com'
    assert capabilities['proxy']['proxyAutoconfigUrl'] == 'http://proxy.pac'
    assert capabilities['proxy']['sslProxy'] == 'https://proxy.example.com'
    assert capabilities['proxy']['noProxy'] == 'localhost,127.0.0.1'
    assert capabilities['proxy']['socksProxy'] == 'socks://proxy.example.com'
    assert capabilities['proxy']['socksUsername'] == 'user'
    assert capabilities['proxy']['socksPassword'] == 'pass'

def test_add_to_capabilities_with_minimal_proxies():
    capabilities = {}
    stub = Stub(
        proxyType={'string': 'manual'}
    )
    add_to_capabilities(stub, capabilities)
    assert 'proxy' in capabilities
    assert capabilities['proxy']['proxyType'] == 'manual'
    assert 'autodetect' not in capabilities['proxy']
    assert 'ftpProxy' not in capabilities['proxy']
    assert 'httpProxy' not in capabilities['proxy']
    assert 'proxyAutoconfigUrl' not in capabilities['proxy']
    assert 'sslProxy' not in capabilities['proxy']
    assert 'noProxy' not in capabilities['proxy']
    assert 'socksProxy' not in capabilities['proxy']
    assert 'socksUsername' not in capabilities['proxy']
    assert 'socksPassword' not in capabilities['proxy']

def test_add_to_capabilities_with_no_proxy_type():
    capabilities = {}
    stub = Stub(
        proxyType={'string': None}  # Changed to a dictionary with None value
    )
    add_to_capabilities(stub, capabilities)
    assert 'proxy' in capabilities
    assert capabilities['proxy']['proxyType'] is None

def test_add_to_capabilities_with_empty_capabilities():
    capabilities = {}
    stub = Stub(
        proxyType={'string': 'manual'},
        autodetect=False
    )
    add_to_capabilities(stub, capabilities)
    assert 'proxy' in capabilities
    assert capabilities['proxy']['proxyType'] == 'manual'
    assert 'autodetect' not in capabilities['proxy']

def test_add_to_capabilities_with_invalid_proxy_type():
    capabilities = {}
    stub = Stub(
        proxyType={'string': 123}  # Invalid type
    )
    add_to_capabilities(stub, capabilities)
    assert 'proxy' in capabilities
    assert capabilities['proxy']['proxyType'] == 123  # Should accept invalid type

def test_add_to_capabilities_with_none_values():
    capabilities = {}
    stub = Stub(
        proxyType={'string': 'manual'},
        autodetect=None,
        ftpProxy=None,
        httpProxy=None,
        proxyAutoconfigUrl=None,
        sslProxy=None,
        noProxy=None,
        socksProxy=None,
        socksUsername=None,
        socksPassword=None
    )
    add_to_capabilities(stub, capabilities)
    assert 'proxy' in capabilities
    assert capabilities['proxy']['proxyType'] == 'manual'
    assert 'autodetect' not in capabilities['proxy']
    assert 'ftpProxy' not in capabilities['proxy']
    assert 'httpProxy' not in capabilities['proxy']
    assert 'proxyAutoconfigUrl' not in capabilities['proxy']
    assert 'sslProxy' not in capabilities['proxy']
    assert 'noProxy' not in capabilities['proxy']
    assert 'socksProxy' not in capabilities['proxy']
    assert 'socksUsername' not in capabilities['proxy']
    assert 'socksPassword' not in capabilities['proxy']