import signal
import server
import logging
import argparse
import yaml


from server import Server
from worker import Worker   



logger = logging.getLogger(__name__)
server = Server()
worker = Worker()



def get_args():
    parser = argparse.ArgumentParser(description='Serve your WSGI app')
    parser.add_argument('-c', '--config', dest='config', help='location of the config file', required=True)
    return parser.parse_args()





def run():
    listener= server.run()
    worker.run(listener)
def setup():
    
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGHUP, shutdown)

    args = get_args()

    with open(args.config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    print(config)

    logger.info("Running server with following config: %s", str(config))

    server.setup(config)
    worker.setup(config)

def shutdown(signum, _):
    worker.shutdown()
    server.shutdown()
    exit(0)

if __name__ == "__main__":
    setup()
    run()

