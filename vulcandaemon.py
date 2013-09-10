from os import getpid

import sys
import argparse
import yaml

import setproctitle

from twisted.python import log
from twisted.python.log import NullFile
from twisted.python import syslog

import vulcan


def parse_args():
    p = argparse.ArgumentParser(
        description="Proxies HTTP(S) and SMTP requests")

    p.add_argument("--http-port", "-p", default=8080, type=int,
                   metavar='<PORT>', help="HTTP port number to listen on.")
    p.add_argument("--config", "-c", metavar='<FILENAME>', required=True,
                   help="config file name")
    p.add_argument('--pid-file', help="pid file path")
    p.add_argument('--syslog', nargs='?', const=True, default=False, type=bool,
                   help="Log to syslog, not to stdout")

    return p.parse_args()


def initialize(args, process_name="vulcan"):

    with open(args.config) as f:
        params = yaml.load(f)

    vulcan.initialize(params)

    # Create the pidfile:
    if args.pid_file:
        with open(args.pid_file, 'w') as pidfile:
            pidfile.write(str(getpid()))

    # Change the name of the process to "vulcan"
    setproctitle.setproctitle(process_name)

    # initialize logging
    if args.syslog:
        syslog.startLogging(prefix=process_name)
    else:
        log.startLogging(sys.stdout)


def main():
    args = parse_args()
    initialize(args)

    from twisted.internet import reactor

    from vulcan.httpserver import HTTPFactory
    from vulcan import cassandra

    cassandra.pool.startService()
    reactor.listenTCP(args.http_port, HTTPFactory())
    reactor.suggestThreadPoolSize(10)
    reactor.run()


if __name__ == '__main__':
    main()
