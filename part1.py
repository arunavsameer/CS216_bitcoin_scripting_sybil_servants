from decimal import Decimal
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
import time

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

def connect_to_bitcoin_rpc():
    rpc_user = "Jetha"
    rpc_password = "tapu_ke_papa"
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443", timeout=120)
    print("Connected to Bitcoin Core RPC")
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
    addr_A = p.getnewaddress("", "legacy")
    addr_B = p.getnewaddress("", "legacy")
    addr_C = p.getnewaddress("", "legacy")
    print(f"Address A: {addr_A}")
    print(f"Address B: {addr_B}")
    print(f"Address C: {addr_C}\n")
    txid_funding = p.sendtoaddress(addr_A, 1.0)
    print(f"Funding transaction: {txid_funding}\n")
    p.generatetoaddress(1, p.getnewaddress())
    unspent = p.listunspent(1, 9999999, [addr_A])
    if not unspent:
        print("No UTXOs found for Address A")
        return
    utxo = unspent[0]
    print(f"UTXO for Address A: {utxo}\n")
    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_B: 0.5}
    change_amount = utxo["amount"] - Decimal('0.5') - Decimal('0.0001')
    if change_amount > 0:
        outputs[addr_A] = change_amount
    raw_tx_A_to_B = p.createrawtransaction(inputs, outputs)
    decoded_tx_A_to_B = p.decoderawtransaction(raw_tx_A_to_B)
    print("Decoded transaction from A to B:")
    print(decoded_tx_A_to_B, "\n")
    vout_B = decoded_tx_A_to_B["vout"][0]
    script_pubkey_B = vout_B["scriptPubKey"]["hex"]
    print(f"ScriptPubKey for Address B: {script_pubkey_B}\n")
    signed_tx_A_to_B = p.signrawtransactionwithwallet(raw_tx_A_to_B)
    if signed_tx_A_to_B["complete"]:
        print("Transaction successfully signed\n")
    else:
        print("Transaction signing failed\n")
        return
    txid_A_to_B = p.sendrawtransaction(signed_tx_A_to_B["hex"])
    print(f"Transaction A to B: {txid_A_to_B}\n")
    p.generatetoaddress(1, p.getnewaddress())
    unspent = p.listunspent(1, 9999999, [addr_B])
    if not unspent:
        print("No UTXOs found for Address B\n")
        return
    utxo = unspent[0]
    print(f"UTXO for Address B: {utxo}\n")
    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_C: 0.25}
    change_amount = utxo["amount"] - Decimal('0.25') - Decimal('0.0001')
    if change_amount > 0:
        outputs[addr_B] = change_amount
    raw_tx_B_to_C = p.createrawtransaction(inputs, outputs)
    decoded_tx_B_to_C = p.decoderawtransaction(raw_tx_B_to_C)
    print("Decoded transaction from B to C:")
    print(decoded_tx_B_to_C, "\n")
    signed_tx_B_to_C = p.signrawtransactionwithwallet(raw_tx_B_to_C)
    if signed_tx_B_to_C["complete"]:
        print("Transaction successfully signed\n")
    else:
        print("Transaction signing failed\n")
        return
    decoded_signed_tx_B_to_C = p.decoderawtransaction(signed_tx_B_to_C["hex"])
    print("Decoded signed transaction from B to C:")
    print(decoded_signed_tx_B_to_C, "\n")
    vin_B_to_C = decoded_signed_tx_B_to_C["vin"][0]
    script_sig_B_to_C = vin_B_to_C.get("scriptSig", {}).get("hex", "No ScriptSig found")
    print(f"ScriptSig for Address B to C: {script_sig_B_to_C}\n")
    txid_B_to_C = p.sendrawtransaction(signed_tx_B_to_C["hex"])
    print(f"Transaction B to C: {txid_B_to_C}\n")
    p.generatetoaddress(1, p.getnewaddress())
    complete_tx_B_to_C = p.getrawtransaction(txid_B_to_C, True)
    print("Complete transaction from B to C:")
    print(complete_tx_B_to_C, "\n")
    print("Analysis:")
    print(f"Transaction ID from A to B: {txid_A_to_B}")
    print(f"Transaction ID from B to C: {txid_B_to_C}")
    print(f"Raw Transaction Hex A to B: {raw_tx_A_to_B}")
    print(f"Raw Transaction Hex B to C: {raw_tx_B_to_C}")
    print(f"ScriptPubKey (locking script) from A to B: {script_pubkey_B}")
    print(f"ScriptSig (unlocking script) from B to C: {script_sig_B_to_C}")
    print("Use Bitcoin Debugger to validate these scripts.\n")

if __name__ == "__main__":
    main()
