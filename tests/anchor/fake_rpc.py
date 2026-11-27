# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S1, S2, S7
# contract: -
# depends:  -
# status:   stable
"""Testler için sahte Bitcoin node'u.

Gerçek bitcoind olmadan daily.py akışını denemek için, kullandığımız RPC
komutlarının basit bir taklidi. Her poll'da bir blok "üretir"; işlem
confirm_after kadar blok sonra onaylanır. stuck=True ise ilk işlem hiç
onaylanmaz, böylece fee bump yolu test edilir.
"""

import hashlib
import json


class FakeRPC:
    def __init__(self, chain="regtest", confirm_after=1, stuck_first=False):
        self.chain = chain
        self.confirm_after = confirm_after
        self.stuck_first = stuck_first
        self.height = 200
        self.txs = {}          # txid -> {"hex", "sent_at", "outputs"}
        self.sent = []         # gönderim sırası
        self.calls = []

    def mine(self):
        self.height += 1

    def _block_hash(self, height):
        return hashlib.sha256(f"block-{height}".encode()).hexdigest()

    def call(self, method, *params):
        self.calls.append(method)
        return getattr(self, "_" + method)(*params)

    def _getblockchaininfo(self):
        return {"chain": self.chain}

    def _getblockcount(self):
        return self.height

    def _createrawtransaction(self, inputs, outputs):
        return json.dumps({"outputs": outputs})

    def _fundrawtransaction(self, raw, options):
        assert options.get("replaceable") is True
        tx = json.loads(raw)
        tx["outputs"].append({"change": 1})
        return {"hex": json.dumps(tx)}

    def _signrawtransactionwithwallet(self, raw):
        return {"hex": raw, "complete": True}

    def _decoderawtransaction(self, raw):
        vout = []
        for out in json.loads(raw)["outputs"]:
            if "data" in out:
                data = bytes.fromhex(out["data"])
                vout.append({"scriptPubKey": {"hex": (bytes([0x6A, len(data)]) + data).hex()}})
            else:
                vout.append({"scriptPubKey": {"hex": "0014" + "11" * 20}})
        return {"vout": vout}

    def _sendrawtransaction(self, raw):
        txid = hashlib.sha256(raw.encode() + str(len(self.sent)).encode()).hexdigest()
        self.txs[txid] = {"hex": raw, "sent_at": self.height, "block": None}
        self.sent.append(txid)
        return txid

    def _bumpfee(self, txid):
        new = self._sendrawtransaction(self.txs[txid]["hex"])
        return {"txid": new}

    def _gettransaction(self, txid):
        tx = self.txs[txid]
        stuck = self.stuck_first and txid == self.sent[0]
        if tx["block"] is None and not stuck and self.height - tx["sent_at"] >= self.confirm_after:
            tx["block"] = self.height
        if tx["block"] is None:
            return {"confirmations": 0}
        return {
            "confirmations": self.height - tx["block"] + 1,
            "blockheight": tx["block"],
            "blockhash": self._block_hash(tx["block"]),
            "blocktime": 1_700_000_000 + tx["block"] * 600,
        }

    def _getrawtransaction(self, txid, verbose, blockhash=None):
        tx = self.txs[txid]
        if tx["block"] is None or blockhash != self._block_hash(tx["block"]):
            raise KeyError("No such transaction found in the provided block")
        decoded = self._decoderawtransaction(tx["hex"])
        decoded.update(in_active_chain=True, confirmations=self.height - tx["block"] + 1)
        return decoded
