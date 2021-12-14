from fastapi import FastAPI
from blockchain import Blockchain

blockchain = Blockchain()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/get_chain')
def get_chain():
    response = {'Chain Length': len(blockchain.chain),
                'Chain': blockchain.chain}
    return response

# Mining new block
@app.get('/mine_block')
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
    
    return response

# Checking if the blockchain is valid
@app.get('/is_valid')
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid: 
        response = {'Message': 'The blockchain is valid'}
    else:
        response = {'Message': 'Saim, We have a problem. The blockchain is not valid'}
        
    return response