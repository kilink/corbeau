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


class ThreadedHTTPTransport(raven.transport.AsyncTransport,
                            VerifiedHTTPSTransport):

    scheme = ['threaded+http', 'threaded+https']

    def __init__(self, parsed_url):
        super(ThreadedHTTPTransport, self).__init__(parsed_url)

        # remove the threaded+ from the protocol, as it is not a real protocol
        self._url = self._url.split('+', 1)[-1]

    def get_worker(self):
        if not hasattr(self, '_worker'):
            self._worker = raven.transport.threaded.AsyncWorker()
        return self._worker

    def send_sync(self, data, headers, success_cb, failure_cb):
        try:
            super(ThreadedHTTPTransport, self).send(data, headers)
        except Exception as e:
            failure_cb(e)
        else:
            success_cb()

    def async_send(self, data, headers, success_cb, failure_cb):
        self.get_worker().queue(self.send_sync, data, headers, success_cb,
                                failure_cb)


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
