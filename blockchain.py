import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []

        # Create genesis block
        self.new_block(previous_hash = 1, proof = 100)

    def new_block(self, previous_hash, proof):
        """
        :param previous_hash: <int> The proof given by the Proof of Work algorithm
        :param proof: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        #Creates a new block and adds it to the chain

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block
        :param block: <dict> Block
        :return: <str>
        """
        # We have to make sure that the dictionaries or ordered otherwise the hashes will be inconsistent
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns last block in the chain
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transaction.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount
            }
        )
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        A simple proof of work algorithm
        -Find a number p' such that hash(pp') contains leading 4 zeros, where p is the previous p'
        - p is the previous proof of work p' is the new one
        :param last_proof: <int>
        :return:<int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof,proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"




