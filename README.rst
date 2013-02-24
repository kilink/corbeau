Corbeau
=======

.. image:: https://secure.travis-ci.org/kilink/corbeau.png?branch=master
   :target: http://travis-ci.org/kilink/corbeau

Corbeau is an extension to `Raven <https://github.com/getsentry/raven>`_
which adds a cert-verifying HTTPS transport.

.. code-block:: pycon

    >>> client = corbeau.Client("https://foo:bar@example.com/project")
    >>> client is raven.base.Raven
    True
    >>> client.registry.get_transport(urlparse.urlparse(client.servers[0]))
    <corbeau.VerifiedHTTPSTransport object at 0x...>
