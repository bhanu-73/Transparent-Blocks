import json
import random
from web3 import *
from variables import abi, contract_address


class Chain:

    def __init__(self):
        self.chain = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
        self.contract = self.chain.eth.contract(address=contract_address, abi=abi)

    def get_balance(self, address):
        return self.contract.caller().balanceOf(address)

    def transfer(self, from_address, to_address, amount):
        self.chain.eth.default_account = from_address
        return self.contract.functions.transfer(to=to_address, tokens=int(amount)).transact()

    def get_latest_block(self):
        latest_block_no = self.chain.eth.get_block_number()
        block_data = self.chain.eth.get_block(latest_block_no)
        transaction = self.chain.eth.get_transaction(block_data['transactions'][0])
        return latest_block_no, transaction['from']

    def get_accounts(self):
        return set(self.chain.eth.accounts)

    def assign_account(self, name):
        accounts = self.get_accounts()
        with open("./data/accounts.json") as file:
            assigned = json.load(file)
            assigned_accounts = set(assigned.keys())
            free_accounts = accounts - assigned_accounts
            to_assign_account = random.choice(list(free_accounts))
            assigned[to_assign_account] = name
        with open("./data/accounts.json", 'w+') as file:
            json.dump(assigned, file)
        return to_assign_account


chain = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract = chain.eth.contract(address=contract_address, abi=abi)

block_data = chain.eth.get_block(1)
transaction = chain.eth.get_transaction(block_data['transactions'][0])
print(dict(transaction))
print(1 , transaction['from'], transaction['input'])
