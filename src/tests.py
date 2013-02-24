import corbeau
import mock
import urlparse
import unittest

class CorbeauTest(unittest.TestCase):

    dsn = "https://foo:bar@httpbin.org/post"

    def test_registration(self):
        client = corbeau.Client(self.dsn)
        registry = client._registry
        transport = registry.get_transport(urlparse.urlparse(self.dsn))
        self.assertTrue(isinstance(transport, corbeau.VerifiedHTTPSTransport))

    @mock.patch("requests.post")
    def test_cert_verification(self, post):
        client = corbeau.Client(self.dsn)
        client.send()
        kwargs = post.call_args[-1]
        self.assertTrue(kwargs["verify"])
        self.assertEqual(kwargs["timeout"], 1)
        self.assertTrue("X-Sentry-Auth" in kwargs["headers"])
