# -*- coding: utf-8 -*-
# vim:syntax=python:sw=4:ts=4:expandtab
#

from vogelerunner import __version__ as version
from amqplib import client_0_8 as amqp
import urlparse,logging,sys,platform

# Configure Logs
log = logging.getLogger('vogeler-runner')

# Correct problem with urlparse in python < 2.6
SCHEME="amqp"
urlparse.uses_netloc.append(SCHEME)
urlparse.uses_fragment.append(SCHEME)

try:
    import simplejson as json
except ImportError:
    import json

class Manager(object):
    def __init__(self,config, options):
        self.config = config
        self.options = options
        self.broadcast_exchange = config.get('main', 'broadcast_exchange')

        self.ch = self.setup_amqp()

    def setup_amqp(self):
        dsn = self.config.get('main', 'amqpserver')
        parsed = urlparse.urlparse(dsn)
        u,p,h,pt,vh = (parsed.username, parsed.password, parsed.hostname,
                       parsed.port, parsed.path)
        try:
            conn = amqp.Connection(host=h, port=pt,
                                   userid=u, password=p,
                                   virtual_host=vh,
                                   insist=False)
            ch = conn.channel()
            ch.access_request(vh,active=True, read=True, write=True)
        except Exception,e:
            log.fatal('Unable to connect to amqp: %s' % e)
            sys.exit(1)
        return ch

    def message(self, message, routing_key, durable=True):
        try:
            log.debug("Vogeler is sending a message")
            msg = amqp.Message(json.dumps(message))
            if durable:
                msg.properties['delivery_mode'] = 2
            self.ch.basic_publish(msg, exchange=self.broadcast_exchange,
                                       routing_key=routing_key)
        except Exception,e:
            log.fatal("Could not publish message to the queue")

    def process_request(self,request):
        log.info("Received request for: %s" % request)
        # Run plugin HERE
        results = {'hello': 'world', }
        c.message(results)
        log.debug('Results: %s' % results)

    def callback(self, msg):
        log.debug('Message received')
        try:
            message = json.loads(msg.body)
        except Exception,e:
            log.warn("Message not in JSON format")
        self.process_request(message)


def main(config,options,args):
    print "vogelerunner version",version

    m = Manager(config, options)

    # Choose the plugin(s) to use
    if options.plugins:
        plugins = options.plugins.split(',')
    else:
        plugins = ['facter','dpkg','ps']

    # Choose the destination (only one for now)
    if options.machine:
        destination = options.machine
    else:
        destination = 'broadcasts.*'

    for plugin in plugins:
        command = {'myrequest': plugin,}
        log.info('Sending %s to %s' % (command, destination))
        m.message(message=command, routing_key=destination)


