"""
Key generation for BCH-based McEliece cryptosystem.
"""
import numpy as np
import galois
from .bch_code import BCHCode
from ..utils import generate_invertible_matrix, generate_permutation_matrix


def generate_keys(L):
    """
    Generate public and private keys for McEliece cryptosystem using BCH codes.
    
    Args:
        L: Number of BCH code blocks
        
    Returns:
        tuple: (public_key, private_key)
            public_key: (G_pub, t) where G_pub is the public generator matrix and t is error count
            private_key: (S, P, G_total, bch_code) where S is scrambling matrix, P is permutation matrix
    """
    GF2 = galois.GF(2)
    bch = BCHCode()
    
    # Get generator matrix from BCH code
    G_bch = bch.bch.G
    
    n = bch.n  # 15
    k = bch.k  # 7
    
    # Total dimensions
    n_total = n * L  # 15L
    k_total = k * L  # 7L
    
    # Create block-diagonal generator matrix G_total
    G_total = GF2(np.zeros((k_total, n_total), dtype=int))
    
    for i in range(L):
        row_start = i * k
        row_end = (i + 1) * k
        col_start = i * n
        col_end = (i + 1) * n
        G_total[row_start:row_end, col_start:col_end] = G_bch
    
    # Generate scrambling matrix S (k_total x k_total)
    S = generate_invertible_matrix(k_total)
    
    # Generate permutation matrix P (n_total x n_total)
    P = generate_permutation_matrix(n_total)
    
    # Compute public key G_pub = S @ G_total @ P
    G_pub = S @ G_total @ P
    
    # Public key includes the error correction capability
    # t = 2 * L (two errors per block)
    public_key = (G_pub, 2 * L)
    
    # Private key now includes G_total
    private_key = (S, P, G_total, bch)
    
    return public_key, private_key
