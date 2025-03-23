from decimal import Decimal
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time
import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

def connect_to_bitcoin_rpc():
    rpc_user = "Jetha"
    rpc_password = "tapu_ke_papa"
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443", timeout=120)
    print("\nConnected to Bitcoin Core RPC\n")
    return rpc_connection

def main():
    p = connect_to_bitcoin_rpc()
    try:
        p.loadwallet("mywallet")
        print("\nWallet 'mywallet' loaded successfully\n")
    except JSONRPCException as e:
        if "Wallet file verification failed" in str(e) or "Wallet not found" in str(e):
            p.createwallet("mywallet")
            print("\nWallet 'mywallet' created successfully\n")
    balance = p.getbalance()
    if balance < 50:
        mining_address = p.getnewaddress()
        print(f"\nMining to address: {mining_address}\n")
        p.generatetoaddress(101, mining_address)
    addr_A_prime = p.getnewaddress("", "p2sh-segwit")
    addr_B_prime = p.getnewaddress("", "p2sh-segwit")
    addr_C_prime = p.getnewaddress("", "p2sh-segwit")
    print(f"\nSegWit Address A': {addr_A_prime}")
    print(f"SegWit Address B': {addr_B_prime}")
    print(f"SegWit Address C': {addr_C_prime}\n")
    txid_funding = p.sendtoaddress(addr_A_prime, 1.0)
    print(f"\nFunding transaction: {txid_funding}\n")
    p.generatetoaddress(1, p.getnewaddress())
    unspent = p.listunspent(1, 9999999, [addr_A_prime])
    if not unspent:
        print("\nNo UTXOs found for address A'\n")
        return
    utxo = unspent[0]
    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_B_prime: 0.5}
    change_amount = utxo["amount"] - Decimal('0.5') - Decimal('0.0001')
    if change_amount > 0:
        outputs[addr_A_prime] = change_amount
    raw_tx_A_to_B = p.createrawtransaction(inputs, outputs)
    decoded_tx = p.decoderawtransaction(raw_tx_A_to_B)
    challenge_script_A_to_B = decoded_tx["vout"][0]["scriptPubKey"]
    print("\nScriptPubKey (Challenge) for Address B':")
    print(challenge_script_A_to_B, "\n")
    signed_tx = p.signrawtransactionwithwallet(raw_tx_A_to_B)
    if signed_tx["complete"]:
        print("\nTransaction successfully signed\n")
    else:
        print("\nTransaction signing failed\n")
        return
    txid_A_to_B = p.sendrawtransaction(signed_tx["hex"])
    print(f"\nTransaction A' to B': {txid_A_to_B}\n")
    p.generatetoaddress(1, p.getnewaddress())
    complete_tx_A_to_B = p.getrawtransaction(txid_A_to_B, True)
    response_script_A_to_B = complete_tx_A_to_B["vin"][0].get("scriptSig", {})
    print("\nScriptSig (Response) from Address A' to Address B':")
    print(response_script_A_to_B, "\n")
    unspent = p.listunspent(1, 9999999, [addr_B_prime])
    if not unspent:
        print("\nNo UTXOs found for address B'\n")
        return
    utxo = unspent[0]
    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_C_prime: 0.25}
    change_amount = utxo["amount"] - Decimal('0.25') - Decimal('0.0001')
    if change_amount > 0:
        outputs[addr_B_prime] = change_amount
    raw_tx_B_to_C = p.createrawtransaction(inputs, outputs)
    decoded_tx = p.decoderawtransaction(raw_tx_B_to_C)
    challenge_script_B_to_C = decoded_tx["vout"][0]["scriptPubKey"]
    print("\nScriptPubKey (Challenge) for Address C':")
    print(challenge_script_B_to_C, "\n")
    signed_tx = p.signrawtransactionwithwallet(raw_tx_B_to_C)
    if signed_tx["complete"]:
        print("\nTransaction successfully signed\n")
    else:
        print("\nTransaction signing failed\n")
        return
    txid_B_to_C = p.sendrawtransaction(signed_tx["hex"])
    print(f"\nTransaction B' to C': {txid_B_to_C}\n")
    p.generatetoaddress(1, p.getnewaddress())
    complete_tx_B_to_C = p.getrawtransaction(txid_B_to_C, True)
    response_script_B_to_C = complete_tx_B_to_C["vin"][0].get("scriptSig", {})
    print("\nScriptSig (Response) from Address B' to Address C':")
    print(response_script_B_to_C, "\n")
    print("\nAnalysis:")
    print(f"Transaction ID from A' to B': {txid_A_to_B}")
    print(f"Transaction ID from B' to C': {txid_B_to_C}\n")
    print(f"\nFinal Transaction Size (A' to B'): {complete_tx_A_to_B['size']} bytes")
    print(f"Final Virtual Transaction Size (A' to B'): {complete_tx_A_to_B['vsize']} bytes\n")
    print(f"\nFinal Transaction Size (B' to C'): {complete_tx_B_to_C['size']} bytes")
    print(f"Final Virtual Transaction Size (B' to C'): {complete_tx_B_to_C['vsize']} bytes\n")
    print("\nChallenge and Response Scripts:")
    print(f"ScriptPubKey (Challenge) for Address B': {challenge_script_A_to_B}")
    print(f"ScriptSig (Response) from Address A' to Address B': {response_script_A_to_B}\n")
    print(f"ScriptPubKey (Challenge) for Address C': {challenge_script_B_to_C}")
    print(f"ScriptSig (Response) from Address B' to Address C': {response_script_B_to_C}\n")
    print("Use Bitcoin Debugger to validate these scripts.\n")
    mempool_info = p.getmempoolinfo()
    print(f"\nMempool info: {mempool_info}\n")
    blockchain_info = p.getblockchaininfo()
    print(f"\nBlockchain info: {blockchain_info}\n")

if __name__ == "__main__":
    main()
