Corbeau
=======

.. image:: https://secure.travis-ci.org/kilink/corbeau.png?branch=master
   :target: http://travis-ci.org/kilink/corbeau

.. image:: https://coveralls.io/repos/kilink/corbeau/badge.png
   :target: https://coveralls.io/r/kilink/corbeau

Corbeau is an extension to `Raven <https://github.com/getsentry/raven-python>`_,
that adds an HTTPS transport which verifies SSL certificates.

Corbeau provides a drop-in replacement for raven.Client:

.. code-block:: pycon

    >>> url = "https://foo:bar@example.com/project"
    >>> client = corbeau.Client(url)
    >>> client is raven.base.Raven
    True
    >>> client.registry.get_transport(urlparse.urlparse(url))
    <corbeau.VerifiedHTTPSTransport object at 0x...>

Under the hood, the Corbeau client uses `Requests <https://github.com/kennethreitz/requests>`_
to do SSL certificate verification.

The transport uses a requests.Session object to make requests, accessible
at corbeau.session.  This means that keep-alive will be used if the
server supports it.
