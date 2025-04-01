# Phylactery

A secure file encryption system using Shamir's Secret Sharing and AES-256-GCM.

## Features

- File encryption using AES-256-GCM
- Key management using Shamir's Secret Sharing
- Command-line interface for easy use
- Secure key generation and storage

## Installation

```bash
pip install -e .
```

## Usage

### Encrypting a File

To encrypt a file, you'll need to specify:
- The input file to encrypt
- The output file where the encrypted data will be stored
- The number of shards required to reconstruct the key (quorum)
- The total number of shards to generate

```bash
phylactery encrypt input.txt output.enc -q 3 -t 5
```

This will:
1. Generate a new Data Encryption Key (DEK)
2. Create 5 shards, requiring 3 to reconstruct the key
3. Save the shards in numbered files (1.shard, 2.shard, etc.)
4. Encrypt the input file using the DEK

### Decrypting a File

To decrypt a file, you'll need:
- The encrypted input file
- The output file where the decrypted data will be stored
- The required number of shard files to reconstruct the key

```bash
phylactery decrypt output.enc decrypted.txt 1.shard 2.shard 3.shard
```

This will:
1. Read the shard files
2. Reconstruct the DEK using Shamir's Secret Sharing
3. Decrypt the file using the reconstructed DEK

## Security Notes

- Keep your shard files secure and separate
- Never share all shards with a single party
- The quorum should be less than the total number of shards
- Store shards in different secure locations

## License

MIT License
