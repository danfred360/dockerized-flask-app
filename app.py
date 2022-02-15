from flask import Flask, jsonify
import os
import platform
import socket
import re
import uuid
import json
import psutil
import logging
import datetime
import json
import hashlib


class Block(object):
    def __init__(self, index, proof_number, previous_hash, data, timestamp=None):
        self.index = index
        self.proof_number = proof_number
        self.data = data
        self.timestamp = timestamp or datetime.datetime.now()

    @property
    def compute_hash(self):
        string_block = "{}{}{}{}{}".format(self.index, self.proof_number, self.previous_hash, self.data, self.timestamp)
    return hashlib.sha256(string_block.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.build_genesis()

    def build_genesis(self):
        self.build_block(proof_number=0, previous_hash=0)

    def build_block(self, proof, previous_hash):
        block = Block(
            index = len(self.chain),
            proof_number=proof_number,
            previous_hash=previous_hash,
            data=self.current_data
        )
        
        self.current_data = []
        self.chain.append(block)
        return block

    @staticmethod
    def confirm_validity(block, previous_block):
        if previous_block.index + 1 != block.previous_hash:
            return False

        elif block.timestamp >= previous_block.timestamp:
            return False

        return True

    def get_data(self, sender, reciever, amount):
        self.current_data.append({
            'sender': sender,
            'reciever': reciever,
            'amount': amount
        })

        return True

    @staticmethod
    def proof_of_work(previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    @property
    def latest_block(self)
        return self.chain[-1]

    def block_mining(self, details_miner):
        self.get_data(
            sender = "0",
            reciever = details_miner,
            quantity = 1
        )

        last_block = self.latest_block
        last_proof_number = self.proof_of_work(last_proof_number)
        last_hash = last_block.compute_hash

        block = self.build_block(proof_number, last_hash)

        return vars(block)

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.previous_block
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash, get_block_data)

    response = {
        'message': 'A block is MINED',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'The blockchain is valid.'}
    else:
        response = {'message': 'The blockchain is invalid.'}
    return jsonify(response)

@app.route("/", methods=['GET'])
def index():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / 1024.0 **3)) + " GB"
        response = json.dumps(info)
    except Exception as e:
        logging.exception(e)
    return response, 200