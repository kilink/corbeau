import corbeau
import doctest
import httplib
import io
import mock
import raven
import raven.base
import requests.adapters
import requests.models
import requests.packages.urllib3
import urlparse
import unittest


class HTTPResponse(object):

    def __init__(self):
        self.msg = httplib.HTTPMessage(io.BytesIO())


class DummyAdapter(requests.adapters.HTTPAdapter):

    request = None
    kwargs = None

    def send(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        response = requests.packages.urllib3.HTTPResponse(
            original_response=HTTPResponse())
        return self.build_response(request, response)

    def close(self):
        pass


class CorbeauTest(unittest.TestCase):

    dsn = "https://foo:bar@httpbin.org/post"

    def test_registration(self):
        """Demonstrate that the corbeau HTTPS transport is registered
           when using the client subclass.
        """
        client = corbeau.Client(self.dsn)
        registry = client.registry
        transport = registry.get_transport(urlparse.urlparse(self.dsn))
        self.assertTrue(isinstance(transport, corbeau.VerifiedHTTPSTransport))
        threaded = "threaded+" + self.dsn
        transport = registry.get_transport(urlparse.urlparse(threaded))
        self.assertTrue(isinstance(transport, corbeau.ThreadedHTTPTransport))

    @mock.patch("corbeau.session", new_callable=requests.session)
    def test_cert_verification(self, session):
        """Demonstrate that requests is passed the appropriate arguments
           to ensure cert verification is performed.
        """
        adapter = DummyAdapter()
        session.mount("https://", adapter)
        client = corbeau.Client(self.dsn)
        client.captureMessage("oh noes!")
        request = adapter.request
        kwargs = adapter.kwargs
        self.assertTrue(kwargs["verify"])
        self.assertEqual(kwargs["timeout"], 1)
        self.assertTrue("X-Sentry-Auth" in request.headers)
        self.assertTrue(request.body)


def setUp(test):
    raven.base.Raven = None
    test.globs.update(dict(
        corbeau=corbeau,
        raven=raven,
        urlparse=urlparse))


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(CorbeauTest)
    suite.addTest(doctest.DocFileSuite(
        "../README.rst",
        optionflags=doctest.ELLIPSIS,
        setUp=setUp))
    return suite
