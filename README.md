# Data Repository Service

This is a proof of concept server implementation of the [GA4GH Data
Repository Service](https://github.com/ga4gh/data-repository-service-schemas) 1.0.0 API.

It provides a simple file system backend.  Files are identified by their hex-encoded sha256 sums, and directories (bundles) also by sha256 using the algorithm described in the DRS specification.  It works with the [GA4GH DRS Client](https://github.com/ga4gh/ga4gh-drs-client).

# Installation

Not yet on PyPi.  Install locally for development:

```
$ pip install .
```

# Run service

Requires SSL.  You can generate a self-signed one for testing using openssl:

```
$ openssl req -x509 -newkey rsa:2048 -nodes -out cert.pem -keyout key.pem -days 365
```

Run as a standalone flask app:

```
$ drs-server
```
