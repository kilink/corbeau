"""
Corbeau
=======

Corbeau is an extension of the
`Raven https://github.com/getsentry/raven-python` client for Sentry
that adds a cert-verifying HTTPS transport.
"""


from setuptools import setup

setup(
    name="corbeau",
    version="0.1",
    author="Patrick Strawderman",
    author_email="patrick@kilink.net",
    url="https://github/kilink/corbeau",
    license="MIT",
    package_data={"": ["*.py"]},
    include_package_data=True,
    install_requires=["setuptools", "raven", "requests"],
    extras_require=dict(test=["mock"]),
    package_dir={"": "src"},
    py_modules=["corbeau"],
    )
