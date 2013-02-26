Corbeau
=======

.. image:: https://secure.travis-ci.org/kilink/corbeau.png?branch=master
   :target: http://travis-ci.org/kilink/corbeau

Corbeau is an extension to `Raven <https://github.com/getsentry/raven>`_
which adds a cert-verifying HTTPS transport.

It is a drop-in replacement for raven.Client:

.. code-block:: pycon

    >>> url = "https://foo:bar@example.com/project"
    >>> client = corbeau.Client(url)
    >>> client is raven.base.Raven
    True
    >>> client.registry.get_transport(urlparse.urlparse(url))
    <corbeau.VerifiedHTTPSTransport object at 0x...>

The transport the corbeau client uses does verification of SSL certs
for HTTPS connections, thanks to `Requests <https://github.com/kennethreitz/requests>`_.

The transport uses a requests.Session object to make requests, accessible
at corbeau.session.  This means that keep-alive will be used if the
server supports it.
