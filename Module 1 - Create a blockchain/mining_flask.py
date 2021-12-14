# Import all libraries
from blockchain import Blockchain
from flask import Flask, jsonify

# Create a web app
app = Flask(__name__)
blockchain = Blockchain()

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
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulation, you just mine a block!', 
                'index': block['index'], 
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    
    return jsonify(response), 200
    
# Getting full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'Chain Length': len(blockchain.chain),
                'Chain': blockchain.chain}
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


app.run(host='localhost', port=5000)
        
        
        
        
        
        
        
        
        
        
        
        
    
            
        