# Import all libraries
from blockchain import Blockchain
from flask import Flask, jsonify, request
import requests 
from urllib.parse import urlparse
from uuid import uuid4


blockchain = Blockchain()
# Create a web app
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-','')

@app.route('/')
def hello_world():
    return {'message': 'Hello world!'}


# Mining new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Saim', amount = 1) # miner will get this transaction
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulation, you just mine a block!', 
                'index': block['index'], 
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    
    return jsonify(response), 200
    
# Getting full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'length': len(blockchain.chain),
                'chain': blockchain.chain}
    return jsonify(response), 200 

# Checking if the blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid: 
        response = {'Message': 'The blockchain is valid'}
    else:
        response = {'Message': 'Saim, We have a problem. The blockchain is not valid'}
        
    return jsonify(response), 200

# Add transaction to the blockchain
@app.route('/add_transaction', methods=['POST']) 
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201


# Decentralizing our blockchain
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected✓. The SadCoin blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200


app.run(host='localhost', port=5001)
        
        
        
        
        
        
        
        
        
        
        
        
    
            
        