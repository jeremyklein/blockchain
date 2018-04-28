
from blockchain import Blockchain
from uuid import uuid4
import requests as r


from flask import Flask, jsonify, request

# Instantiate our node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # we run proof of work algorithm to get next proof..
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must recieve a reward for finding the proof
    # The sender is "0" to signify that this node has mined new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,

    )

    #Forge new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof,previous_hash)


    response = {
        "messsage": "New Block Forged",
        "index": block['index'],
        "transactions": block['transactions'],
        "proof": block['proof'],
        "previous_hash": block['previous_hash'],

    }
    return jsonify(response),200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check that we get the correct parameters
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values", 400

    # create a new transaction
    index = blockchain.new_transaction(values["sender"],values["recipient"], values["amount"])
    response = {'message': f'Transaction will be added to Block{index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
       return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
       blockchain.register_node(node)

    response = {
        'message':'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def censensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain was authoritative',
            'chain': blockchain.chain
        }


    return jsonify(response), 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
