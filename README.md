# 💰 Bitcoin Scripting Project

## 👨‍💼 Team

- **Arunav Sameer** | Roll No: **230001010**
- **Abhitulya Mishra** | Roll No: **230002002**
- **Anmol Joshi** | Roll No: **230001007**

## 📌 Introduction

This project demonstrates **Bitcoin transaction scripting** using **Legacy (P2PKH)** and **SegWit (P2SH-P2WPKH)** formats. The scripts interact with `bitcoind` via **Bitcoin Core RPC**, covering:

- Address creation 🏦
- Funding and spending transactions 💰
- Raw transaction analysis 🔍
- Script verification using **Bitcoin Debugger** ✅
- Broadcasting transactions on a private **Regtest** blockchain 🚀

## 🎯 Tasks

✅ **Legacy (P2PKH) Transactions**\
✅ **SegWit (P2SH-P2WPKH) Transactions**\
✅ **ScriptPubKey & ScriptSig Extraction**\
✅ **Transaction Verification using Bitcoin Debugger**\
✅ **Mempool & Blockchain State Analysis**

## 🛠 Prerequisites

Ensure you have the following installed:

- **Bitcoin Core** (`bitcoind`) running in **regtest mode**
- **Python 3**
- Required dependencies:
  ```sh
  pip install python-bitcoinrpc
  ```

## 🚀 Installation

Clone this repository and navigate into the project directory:

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/Bitcoin-Scripting.git
cd Bitcoin-Scripting
```

## ⚡ Usage

### 1️⃣ Start Bitcoin Core in Regtest Mode

```sh
bitcoind -regtest -daemon
```

### 2️⃣ Run the Scripts

#### 🔹 Legacy Transactions (P2PKH)

```sh
python code1.py
```

#### 🔹 SegWit Transactions (P2SH-P2WPKH)

```sh
python code2.py
```

## 🔍 How It Works

### 🏦 1. Wallet Setup

- Loads an existing wallet or creates a new one.
- Generates Bitcoin addresses for transactions.

### 💰 2. Funding Transactions

- Mints Bitcoin using `generatetoaddress`.
- Funds addresses using `sendtoaddress`.

### 🔄 3. Transaction Creation & Analysis

- Creates raw transactions.
- Extracts **locking scripts** (ScriptPubKey) and **unlocking scripts** (ScriptSig).
- Decodes and signs transactions.

### 📱 4. Broadcasting & Verification

- Sends signed transactions to the Bitcoin network.
- Confirms transactions by generating new blocks.
- Verifies transactions using **Bitcoin Debugger**.

## 🛠 Debugging & Verification

After running the scripts, you can manually inspect transactions using `bitcoin-cli`:

```sh
bitcoin-cli -regtest getrawtransaction <txid> 1
```

For deeper analysis, use the **Bitcoin Debugger** to verify:

- **ScriptPubKey (Locking Script)**
- **ScriptSig (Unlocking Script)**
- **Transaction Validation**

## 💜 Example Output

```
Connected to Bitcoin Core RPC
Wallet 'mywallet' loaded successfully

Generating addresses...
Legacy Address A: <address>
Legacy Address B: <address>
Funding transaction: <txid>
...
Transaction successfully signed
Transaction broadcasted: <txid>
Decoded transaction details: { ... }
Verifying transaction using Bitcoin Debugger...
✅ Transaction verified successfully!
```

## 🏆 Results & Analysis

### ✅ Legacy Transactions (P2PKH)

- **Sent BTC from A ➞ B ➞ C**
- **Signed transaction using private key**
- **Extracted ScriptPubKey & ScriptSig**
- **Verified the transaction with Bitcoin Debugger**

### ✅ SegWit Transactions (P2SH-P2WPKH)

- **Sent BTC from A' ➞ B' ➞ C'**
- **Used SegWit-compatible addresses**
- **Reduced transaction size & fees**
- **Verified unlocking scripts in Bitcoin Debugger**

## 📌 Additional Blockchain Info

```sh
bitcoin-cli -regtest getmempoolinfo
bitcoin-cli -regtest getblockchaininfo
```

