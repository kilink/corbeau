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
    version="0.2",
    author="Patrick Strawderman",
    author_email="patrick@kilink.net",
    description="A Sentry client based on Raven that verifies SSL certs",
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    url="https://github.com/kilink/corbeau",
    license="MIT",
    package_data={"": ["*.py", "*.rst"]},
    include_package_data=True,
    install_requires=["setuptools", "raven", "requests"],
    extras_require=dict(test=["mock"]),
    package_dir={"": "src"},
    py_modules=["corbeau"],
    classifiers =[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        ],
    )
