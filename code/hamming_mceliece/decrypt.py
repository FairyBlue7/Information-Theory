"""
Decryption for Hamming-based McEliece cryptosystem.
"""
import numpy as np
import galois


def decrypt(ciphertext, S, P, G_total, hamming_code):
    """
    Decrypt a ciphertext using the McEliece private key.
    
    Args:
        ciphertext: Encrypted message
        S: Scrambling matrix
        P: Permutation matrix
        G_total: Block-diagonal generator matrix
        hamming_code: HammingCode instance
        
    Returns:
        galois.FieldArray: Decrypted message bits
    """
    GF2 = galois.GF(2)
    
    # Compute P inverse
    P_inv = np.linalg.inv(P)
    
    # Apply inverse permutation: c' = ciphertext @ P^-1
    c_prime = GF2(ciphertext).reshape(1, -1) @ P_inv
    c_prime = c_prime.flatten()
    
    # Decode block by block
    n = hamming_code.n  # 15
    k = hamming_code.k  # 11
    L = len(c_prime) // n
    
    decoded_blocks = []
    for i in range(L):
        block_start = i * n
        block_end = (i + 1) * n
        block = c_prime[block_start:block_end]
        
        # Decode this block
        decoded_msg = hamming_code.decode(block)
        decoded_blocks.append(decoded_msg)
    
    # Concatenate all decoded blocks
    m_prime = GF2(np.concatenate(decoded_blocks))
    
    # Compute S inverse
    S_inv = np.linalg.inv(S)
    
    # Apply inverse scrambling: m = m' @ S^-1
    m = m_prime.reshape(1, -1) @ S_inv
    
    return m.flatten()
