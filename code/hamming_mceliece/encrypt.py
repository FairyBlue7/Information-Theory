"""
Encryption for Hamming-based McEliece cryptosystem.
"""
import numpy as np
import galois


def encrypt(msg_bits, G_pub, t, S=None, G_total=None, P=None):
    """
    Encrypt a message using the McEliece public key.
    
    Args:
        msg_bits: Message bits (length must match G_pub rows)
        G_pub: Public generator matrix (S @ G_total @ P)
        t: Number of errors to add (corresponds to L, one error per block)
        S: Optional scrambling matrix (if provided, uses internal encryption)
        G_total: Optional block-diagonal generator (if provided, uses internal encryption)
        P: Optional permutation matrix (if provided, uses internal encryption)
        
    Returns:
        galois.FieldArray: Ciphertext
    """
    GF2 = galois.GF(2)
    
    # Convert message to GF(2) array
    msg = GF2(np.array(msg_bits))
    
    if S is not None and G_total is not None and P is not None:
        # Internal encryption with controlled error placement
        # Step 1: m @ S
        m_S = msg.reshape(1, -1) @ S
        
        # Step 2: (m @ S) @ G_total
        m_S_G = m_S @ G_total
        m_S_G = m_S_G.flatten()
        
        # Step 3: Add errors (one per block)
        n_total = len(m_S_G)
        block_size = 15
        L = t
        
        error = GF2(np.zeros(n_total, dtype=int))
        
        # Add exactly one error per block
        for i in range(L):
            block_start = i * block_size
            block_end = (i + 1) * block_size
            # Randomly choose one position in this block
            error_pos = np.random.randint(block_start, block_end)
            error[error_pos] = 1
        
        m_S_G_with_error = m_S_G + error
        
        # Step 4: Apply permutation
        ciphertext = m_S_G_with_error.reshape(1, -1) @ P
        ciphertext = ciphertext.flatten()
    else:
        # Standard public-key encryption (no error control)
        # c = m @ G_pub + e (random errors)
        c = msg.reshape(1, -1) @ G_pub
        c = c.flatten()
        
        n_total = len(c)
        error = GF2(np.zeros(n_total, dtype=int))
        
        # Add t random errors
        error_positions = np.random.choice(n_total, size=t, replace=False)
        for pos in error_positions:
            error[pos] = 1
        
        ciphertext = c + error
    
    return ciphertext
