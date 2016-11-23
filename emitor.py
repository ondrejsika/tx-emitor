import time
import argparse
import random
import jsonrpc_requests

parser = argparse.ArgumentParser('TX Emitor')
parser.add_argument('XCOIND_HOST', type=str)
parser.add_argument('XCOIND_PORT', type=int)
parser.add_argument('XCOIND_USER', type=str)
parser.add_argument('XCOIND_PASSWORD', type=str)
parser.add_argument('-v1', '--emit-v1', action='store_true')

args = parser.parse_args()

XCOIND_URL = 'http://%s:%s@%s:%s' % (args.XCOIND_USER, args.XCOIND_PASSWORD, args.XCOIND_HOST, args.XCOIND_PORT)

xcoind_conn = jsonrpc_requests.Server(XCOIND_URL)


def emit_v1():
    address = xcoind_conn.getnewaddress()
    amount = random.randint(1, 10)/10.
    print('v1', address, amount)
    try:
        xcoind_conn.sendtoaddress(address, amount)
    except Exception, e:
        print(e.message, e.args)
    time.sleep(0.01)


while True:
    if args.emit_v1:
        emit_v1()
