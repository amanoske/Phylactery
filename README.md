# Phylactery

Phylactery is a secure file encryption system using Shamir's Secret Sharing and AES-256-GCM.

Using Phylactery, you can store highly sensitive data in semi-untrusted and untrusted locations such as cloud storage protected by the same cryptography used to protect US/NATO TOP SECRET military information. 

The keys for this data are split into **shards** that must be re-assembled within a set quorum to unlock the file's contents. 

## Cryptography

Phylactery uses a two-key system for secure file encryption:

- **Data Encryption Key (DEK)**: A 256-bit key used with [AES-256-GCM](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) to encrypt and decrypt the actual file contents. The DEK is randomly generated for each encryption operation and is never stored in its complete form.

- **Key Encryption Key (KEK)**: A 256-bit key used to protect the DEK. The KEK is split into multiple shards using [Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing), which allows the key to be reconstructed only when a sufficient number of shards (the quorum) are combined. This provides distributed security, as no single party needs to possess the complete key.


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
