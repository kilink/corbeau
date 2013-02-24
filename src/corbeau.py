import raven
import raven.transport
import raven.transport.registry
import raven.transport.threaded
import requests


class VerifiedHTTPSTransport(raven.transport.HTTPTransport):

    certs = True

    def send(self, data, headers):
        response = requests.post(self._url, headers=headers,
            timeout=self.timeout, verify=self.certs)
        response.raise_for_status()
        return response.content


class ThreadedHTTPTransport(VerifiedHTTPSTransport):

    scheme = ['threaded+http', 'threaded+https']

    def __init__(self, parsed_url):
        super(ThreadedHTTPTransport, self).__init__(parsed_url)

        # remove the threaded+ from the protocol, as it is not a real protocol
        self._url = self._url.split('+', 1)[-1]

    def get_worker(self):
        if not hasattr(self, '_worker'):
            self._worker = raven.transport.threaded.AsyncWorker()
        return self._worker

    def send_sync(self, data, headers):
        super(ThreadedHTTPTransport, self).send(data, headers)

    def send(self, data, headers):
        self.get_worker().queue(self.send_sync, data, headers)


default_transports = [
    VerifiedHTTPSTransport,
    ThreadedHTTPTransport,
]

class TransportRegistry(raven.transport.registry.TransportRegistry):

    def override_scheme(self, scheme, cls):
        if scheme in self._scheme:
            del self._scheme[scheme]
        self.register_transport(scheme, cls)
    

class Client(raven.Client):

    _registry = TransportRegistry(default_transports) 

    @classmethod
    def override_scheme(cls, scheme, transport_class):
        self._registry.override_scheme(scheme, transport_class)
