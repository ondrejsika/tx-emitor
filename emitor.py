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
parser.add_argument('-sw', '--emit-segwit', action='store_true')

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


def emit_segwit():
    address = xcoind_conn.getnewaddress()
    address2 = xcoind_conn.getnewaddress()
    segwit_address = xcoind_conn.addwitnessaddress(address)
    segwit_address2 = xcoind_conn.addwitnessaddress(address2)
    amount = random.randint(1, 10)/10.
    print('segwit', segwit_address2, amount*0.9)
    try:
        tx_id = xcoind_conn.sendtoaddress(segwit_address, amount)
        segwit_tx = xcoind_conn.createrawtransaction([{'txid': tx_id, 'vout': 1}],
                                                     {segwit_address2: amount*0.9})
        segwit_tx = xcoind_conn.fundrawtransaction(segwit_tx)['hex']
        signed_segwit_tx = xcoind_conn.signrawtransaction(segwit_tx)['hex']
        segwit_tx_id = xcoind_conn.sendrawtransaction(signed_segwit_tx)
        print segwit_tx_id
    except Exception, e:
        print(e.message, e.args)
    time.sleep(0.01)


while True:
    if args.emit_v1:
        emit_v1()
    if args.emit_segwit:
        emit_segwit()
