import hashlib
# Generator to read bytes from filename on a chunk of 1024 bytes
def bytes_from_file(filename, chunksize=1024) -> bytes:
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk: yield chunk
            else: break

def get_chunks(filename) -> list:
    # List which will have all 1024-bytes sized chunks
    blocks = []
    # Getting chunks
    for chunk in bytes_from_file(filename):
        blocks.append(chunk)
    # Reverting list to start with last block
    return blocks

def calculate_hashes(blocks) -> list:
    aux_blocks = blocks.copy()
    aux_blocks.reverse()
    hashes = []
    hash_block = b''
    for block in aux_blocks:
        m = hashlib.sha256()
        block_with_hash = block + hash_block
        m.update(block_with_hash)
        hash_block = m.digest()
        hashes.append(hash_block.hex())
    hashes.reverse()
    return hashes

def check_block(hashes, block, block_index) -> bytes:
    m = hashlib.sha256()
    next_block_hash = bytes.fromhex(hashes[block_index+1])
    block_plus_hash = block+next_block_hash
    m.update(block_plus_hash)
    hash_acquired = m.digest().hex()
    return hash_acquired

# SETUP
filename = input('Type path of file:')
blocks = get_chunks(filename)
hashes = calculate_hashes(blocks)

print(f'H0: {hashes[0]}')
iterative = "Z"
while iterative.upper() != "Y" and iterative.upper() != "N":
    iterative = input("Do you want to parse the hashes iteratively? Y or N\n")
    if iterative.upper() != "Y" and iterative.upper() != "N":
        print('Invalid output, I only understand Y or N, try again?')

for i, block in enumerate(blocks):
    if iterative.upper() == "Y":
        input("next>")
    if len(hashes) == i+1:
        m = hashlib.sha256()
        m.update(block)
        last_hash = m.digest()
        print(f'Hash from block {i+1} provided: {last_hash.hex()}')
        print(f'Hash {i+1} from hashes list:    {hashes[-1]}')
        break
    print(f'Hash from block {i+1} provided: {check_block(hashes, block, i)}')
    print(f'Hash {i+1} from hashes list:    {hashes[i]}\n')