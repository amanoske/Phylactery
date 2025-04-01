"""
Command-line interface for Phylactery
"""

import click
from .file_locker import FileLocker
from .dek_generator import DEKGenerator
import os
import glob

@click.group()
def cli():
    """Phylactery - Secure file encryption using Shamir's Secret Sharing"""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--quorum', '-q', type=int, required=True,
              help='Number of shards required to reconstruct the key')
@click.option('--total-shards', '-t', type=int, required=True,
              help='Total number of shards to generate')
def encrypt(input_file, output_file, quorum, total_shards):
    """Encrypt a file using Shamir's Secret Sharing"""
    # Generate DEK and shards
    dek_gen = DEKGenerator()
    if not dek_gen.create_new_dek(quorum, total_shards):
        click.echo("Failed to generate DEK", err=True)
        return

    # Save shards to files
    for i, shard in enumerate(dek_gen.shards):
        shard_file = f"{i+1}.shard"
        with open(shard_file, 'w') as f:
            f.write(shard)
        click.echo(f"Generated shard {i+1} in {shard_file}")

    # Encrypt the file
    locker = FileLocker()
    try:
        locker.encrypt_file(input_file, output_file, dek_gen.dek)
        click.echo(f"Successfully encrypted {input_file} to {output_file}")
    except Exception as e:
        click.echo(f"Error encrypting file: {str(e)}", err=True)

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.argument('shard_files', nargs=-1, type=click.Path(exists=True))
def decrypt(input_file, output_file, shard_files):
    """Decrypt a file using Shamir's Secret Sharing shards"""
    # Read shards from files
    shards = []
    for shard_file in shard_files:
        with open(shard_file, 'r') as f:
            shards.append(f.read().strip())

    # Regenerate DEK from shards
    dek_gen = DEKGenerator()
    if not dek_gen.regenerate_dek(shards):
        click.echo("Failed to regenerate DEK from shards", err=True)
        return

    # Decrypt the file
    locker = FileLocker()
    try:
        locker.decrypt_file(input_file, output_file, dek_gen.dek)
        click.echo(f"Successfully decrypted {input_file} to {output_file}")
    except Exception as e:
        click.echo(f"Error decrypting file: {str(e)}", err=True)

if __name__ == '__main__':
    cli() 