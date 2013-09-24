import raven
import raven.transport
import raven.transport.registry
import raven.transport.threaded
import requests


session = requests.Session()


class VerifiedHTTPSTransport(raven.transport.HTTPTransport):

    certs = True

    def send(self, data, headers):
        response = session.post(self._url, headers=headers,
                                timeout=self.timeout, verify=self.certs,
                                data=data)
        response.raise_for_status()
        return response.content


class ThreadedHTTPTransport(raven.transport.threaded.ThreadedHTTPTransport,
                            VerifiedHTTPSTransport):
    pass

default_transports = [
    VerifiedHTTPSTransport,
    ThreadedHTTPTransport,
]


class TransportRegistry(raven.transport.registry.TransportRegistry):

    def override_scheme(self, scheme, cls):
        if scheme in self._schemes:
            del self._schemes[scheme]
        self.register_scheme(scheme, cls)


class Client(raven.Client):

    _registry = TransportRegistry(default_transports)

    @property
    def registry(self):
        return self._registry

    @registry.setter
    def registry(self, inst):
        self._registry = inst

    @classmethod
    def override_scheme(cls, scheme, transport_class):
        cls._registry.override_scheme(scheme, transport_class)
