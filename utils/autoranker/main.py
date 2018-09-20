#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import time
import argparse
from queue import Queue
from urllib.request import urlopen, Request
import re
import json

import hashlib

import os.path

import web3
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract
from web3.middleware import geth_poa_middleware

import sha3
from ecdsa import SigningKey, SECP256k1

import logging
logger = logging.getLogger('autoranker')

from autoranker import Autoranker


def get_config():
    config = {
        "eth_http_node": "https://rinkeby.infura.io/v3/1474ceef2da44edbac41a2efd66ee882",
        "tcrank_address": "0xa2adc9a11b232e03840601ec219e2e3d551e3dc2",
        "faucet_address": "0x417f86bdcb99264b54f8492644bd4f3d93dbb3ee",
    }
    with open("../../solidity/smartz/ranking.abi") as json_data:
        config['tcrank_abi'] = json.load(json_data)
    return config


def main(arguments):

    logger = logging.getLogger('autoranker')
    fh = logging.FileHandler('/tmp/autoranker.log')
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    fh.setFormatter(formatter)


    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-k', '--private-key-file', required=True, help="File with private key", type=argparse.FileType('r'))
    args = parser.parse_args(arguments)
    private_key = args.private_key_file.read().strip()
    
    config = get_config()

    # now create autoranker object and pass contract and account to it. Any further logic must be implemented in Autoranker class
    autoranker = Autoranker(config, private_key)

    dapps = {}
    with open("./dapps.json") as f:
        dapps = json.load(f)

    # dapps = autoranker.get_dapps_from_contract(dapps)

    autoranker.load_dapps_info_to_contract(dapps)



def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))



if __name__ == '__main__':
    start = time.time()
    sys.exit(main(sys.argv[1:]))

