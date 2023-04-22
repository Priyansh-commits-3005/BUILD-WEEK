from web3 import Web3 
import info as i

infura_link = "https://mainnet.infura.io/v3/81565f63460d4d609dd8253caba4ac4f"
web3 = Web3(Web3.HTTPProvider(infura_link))


acc_1 = i.account_1 #input
acc_2 = i.account_2

private_key = i.private_key

nonce = web3.eth.get_transaction_count(account=acc_1)


tx = {
    'nonce':nonce,
    'to':acc_2,
    'value':web3.to_wei(1,'ether'),
    'gas':20000,
    'gasPrice':web3.to_wei('50','gwei')
}

signed_tx = web3.eth.sign_transaction(tx,private_key)

tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)