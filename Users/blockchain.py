import hashlib
import json
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Stable AES-256 key derived from a fixed secret.
# IMPORTANT: Change this secret in production and keep it private.
_SECRET = b'blockchain-chat-aes-secret-key-2025'
STABLE_AES_KEY = hashlib.sha256(_SECRET).digest()  # 32 bytes

class Block:
    def __init__(self, index, sender, recipient, message, timestamp, previous_hash, key):
        self.index = index
        self.sender = sender
        self.recipient = recipient
        self.message = self.encrypt_message(message, key)
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'sender': self.sender,
            'recipient': self.recipient,
            'message': self.message,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty=4):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

    def encrypt_message(self, message, key):
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return json.dumps({'iv': iv, 'ciphertext': ct})

    @staticmethod
    def decrypt_message(encrypted_message, key):
        try:
            data = json.loads(encrypted_message)
            iv = base64.b64decode(data['iv'])
            ct = base64.b64decode(data['ciphertext'])
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except:
            return "Decryption failed"

class Blockchain:
    def __init__(self):
        self.difficulty = 4
        self.encryption_key = STABLE_AES_KEY  # Persistent AES-256 key
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "system", "system", "Genesis Block", time.time(), "0", self.encryption_key)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, sender, recipient, message):
        if not message:
            raise ValueError("Message cannot be empty")
        block = Block(
            len(self.chain),
            sender,
            recipient,
            message,
            time.time(),
            self.get_latest_block().hash,
            self.encryption_key
        )
        block.mine_block(self.difficulty)
        self.chain.append(block)
        return block