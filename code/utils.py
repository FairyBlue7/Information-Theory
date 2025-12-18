"""
Shared utility functions for McEliece cryptosystem implementation.
"""
import numpy as np
import galois


def generate_invertible_matrix(n):
    """
    Generate a random n x n invertible matrix over GF(2).
    
    Args:
        n: Size of the square matrix
        
    Returns:
        galois.FieldArray: An n x n invertible matrix over GF(2)
    """
    GF2 = galois.GF(2)
    
    while True:
        # Generate random matrix over GF(2)
        matrix = GF2(np.random.randint(0, 2, (n, n)))
        
        # Check if matrix is invertible using GF(2) rank
        try:
            _ = np.linalg.inv(matrix)
            return matrix
        except np.linalg.LinAlgError:
            # Matrix is singular, try again
            continue


def generate_permutation_matrix(n):
    """
    Generate a random n x n permutation matrix.
    
    Args:
        n: Size of the square matrix
        
    Returns:
        galois.FieldArray: An n x n permutation matrix over GF(2)
    """
    GF2 = galois.GF(2)
    
    # Create identity matrix and shuffle rows
    perm = np.random.permutation(n)
    identity = np.eye(n, dtype=int)
    perm_matrix = identity[perm]
    
    return GF2(perm_matrix)


def str_to_bits(s):
    """
    Convert a string to a list of bits.
    
    Args:
        s: Input string
        
    Returns:
        list: List of bits (0s and 1s)
    """
    bits = []
    for char in s:
        byte_val = ord(char)
        for i in range(8):
            bits.append((byte_val >> (7 - i)) & 1)
    return bits


def bits_to_str(bits):
    """
    Convert a list of bits to a string.
    
    Args:
        bits: List of bits (0s and 1s)
        
    Returns:
        str: Decoded string
    """
    # Pad bits to multiple of 8
    bits = list(bits)
    while len(bits) % 8 != 0:
        bits.append(0)
    
    chars = []
    for i in range(0, len(bits), 8):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | int(bits[i + j])
        if byte_val != 0:  # Skip null characters
            chars.append(chr(byte_val))
    
    return ''.join(chars)
