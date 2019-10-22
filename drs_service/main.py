#!/usr/bin/env python
import argparse
import pkg_resources  # part of setuptools
import sys
import ruamel.yaml
import os
import logging
import connexion
import connexion.utils as utils
from connexion.resolver import Resolver

logging.basicConfig(level=logging.INFO)


def setup(args=None):
    if args is None:
        args = argparse.Namespace()

    configfile = "config.yml"
    if os.path.isfile(configfile):
        logging.info("Loading %s", configfile)
        with open(configfile, "r") as f:
            config = ruamel.yaml.safe_load(f)
        for c in config:
            setattr(args, c, config[c])

    logging.info("Using config:")
    for n in args.__dict__:
        logging.info("  %s: %s", n, getattr(args, n))

    app = connexion.App(__name__)
    backend = utils.get_function_from_name(
        args.backend + ".create_backend")(app, args.opt)

    def rs(x):
        return getattr(backend, x.split('.')[-1])

    app.add_api(
        'openapi/data_repository_service.swagger.yaml',
        resolver=Resolver(rs))

    return app


def auth(apikey, required_scopes):
    if apikey.startswith("Bearer "):
        apikey = apikey[len("Bearer "):]
    else:
        return None
    return {'sub': apikey}


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Data Repository Service')
    parser.add_argument("--backend", type=str, default="drs_service.fs_drs",
                        help="Either: '--backend=drs_service.fs_drs' or '--backend=drs_service.arvados_drs'")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--opt", type=str, action="append",
                        help="Example: '--opt runner=cwltoil --opt extra=--logLevel=CRITICAL' "
                             "or '--opt extra=--workDir=/'.  Accepts multiple values.")
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--version", action="store_true", default=False)
    args = parser.parse_args(argv)

    if args.version:
        pkg = pkg_resources.require("drs_service")
        print(u"%s %s" % (sys.argv[0], pkg[0].version))
        exit(0)

    app = setup(args)

    app.run(port=args.port, debug=args.debug, ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    main(sys.argv[1:])
