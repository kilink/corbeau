import corbeau
import doctest
import mock
import raven
import raven.base
import requests.adapters
import urlparse
import unittest


class DummyAdapter(requests.adapters.BaseAdapter):

    request = None
    kwargs = None

    def send(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        response = requests.models.Response()
        response.request = request
        return response

    def close(self):
        pass


class CorbeauTest(unittest.TestCase):

    dsn = "https://foo:bar@httpbin.org/post"

    def test_registration(self):
        """Demonstrate that the corbeau HTTPS transport is registered
           when using the client subclass.
        """
        client = corbeau.Client(self.dsn)
        registry = client._registry
        transport = registry.get_transport(urlparse.urlparse(self.dsn))
        self.assertTrue(isinstance(transport, corbeau.VerifiedHTTPSTransport))

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
