"""
Hamming (15, 11) code implementation.
"""
import numpy as np
import galois


class HammingCode:
    """
    Implementation of the (15, 11) Hamming code.
    This code can correct 1 error and has parameters [n=15, k=11, d=3].
    """
    
    def __init__(self):
        """Initialize the (15, 11) Hamming code matrices."""
        self.n = 15  # Codeword length
        self.k = 11  # Message length
        self.t = 1   # Error correction capability
        self.r = 4   # Number of parity bits
        
        GF2 = galois.GF(2)
        
        # Standard Hamming code: H matrix has columns that are all distinct non-zero r-bit patterns
        # Build H with column i having binary representation i+1
        H_standard = GF2(np.zeros((self.r, self.n), dtype=int))
        for i in range(self.n):
            for j in range(self.r):
                H_standard[j, i] = ((i + 1) >> j) & 1
        
        # Now we need to find a systematic form [I_k | P] for G
        # such that H @ G.T = 0
        
        # Approach: rearrange H into form [A | I_r], then G = [I_k | -A^T] = [I_k | A^T] in GF(2)
        
        # Find r columns of H that form an identity matrix
        # These will be columns at positions that are powers of 2 minus 1: 0, 1, 3, 7 (positions 1, 2, 4, 8 in 1-indexed)
        # In our H: column i has value i+1, so we need columns with values 1, 2, 4, 8 
        # which are at indices 0, 1, 3, 7
        
        parity_positions = [0, 1, 3, 7]  # positions 1, 2, 4, 8 (1-indexed)
        data_positions = [i for i in range(self.n) if i not in parity_positions]
        
        # Rearrange H: [data columns | parity columns]
        H_data = H_standard[:, data_positions]
        H_parity = H_standard[:, parity_positions]
        
        # For standard Hamming code with parity at positions 1, 2, 4, 8 (1-indexed):
        # Data bit at position i affects parity bits based on binary representation of i
        
        # Build G directly:
        # Codeword positions: 1-15 (1-indexed)
        # Parity positions: 1,2,4,8 (powers of 2)
        # Data positions: 3,5,6,7,9,10,11,12,13,14,15 (11 positions)
        
        # For each data bit at position i, determine which parity bits it affects
        # This is determined by the binary representation of i
        
        G = GF2(np.zeros((self.k, self.n), dtype=int))
        
        # Parity bit positions: 1,2,4,8 (powers of 2 in 1-indexed positions)
        # Data bit positions: 3,5,6,7,9,10,11,12,13,14,15 (remaining 11 positions)
        # In 0-indexed: parity at 0,1,3,7 and data at 2,4,5,6,8,9,10,11,12,13,14
        data_pos_list = [2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14]  # 0-indexed: 3,5,6,7,9,10,11,12,13,14,15 in 1-indexed
        
        for msg_bit_idx in range(self.k):
            codeword_pos = data_pos_list[msg_bit_idx]  # 0-indexed position in codeword
            codeword_pos_1idx = codeword_pos + 1  # 1-indexed
            
            # Set the data bit itself
            G[msg_bit_idx, codeword_pos] = 1
            
            # Set parity bits based on binary representation
            if codeword_pos_1idx & 1:  # bit 0 set
                G[msg_bit_idx, 0] = 1  # parity position 1 (0-indexed: 0)
            if codeword_pos_1idx & 2:  # bit 1 set
                G[msg_bit_idx, 1] = 1  # parity position 2 (0-indexed: 1)
            if codeword_pos_1idx & 4:  # bit 2 set
                G[msg_bit_idx, 3] = 1  # parity position 4 (0-indexed: 3)
            if codeword_pos_1idx & 8:  # bit 3 set
                G[msg_bit_idx, 7] = 1  # parity position 8 (0-indexed: 7)
        
        self.G = G
        self.H = H_standard
        self.data_positions = data_pos_list
        
    def encode(self, msg_bits):
        """
        Encode a message using the Hamming code.
        
        Args:
            msg_bits: Array of k=11 message bits
            
        Returns:
            galois.FieldArray: Codeword of length n=15
        """
        GF2 = galois.GF(2)
        msg = GF2(np.array(msg_bits).reshape(1, -1))
        codeword = msg @ self.G
        return codeword.flatten()
    
    def decode(self, codeword):
        """
        Decode a received codeword with syndrome decoding.
        Corrects up to 1 error.
        
        Args:
            codeword: Received codeword of length n=15
            
        Returns:
            galois.FieldArray: Decoded message of length k=11
        """
        GF2 = galois.GF(2)
        received = GF2(np.array(codeword).copy())
        
        # Compute syndrome
        syndrome = (self.H @ received.reshape(-1, 1)).flatten()
        
        # If syndrome is non-zero, correct error
        if np.any(syndrome != 0):
            # Syndrome value indicates error position (1-indexed)
            syndrome_val = 0
            for i in range(len(syndrome)):
                syndrome_val += int(syndrome[i]) * (2 ** i)
            
            # Error position is syndrome_val - 1 (0-indexed)
            if 1 <= syndrome_val <= self.n:
                error_pos = syndrome_val - 1
                received[error_pos] = received[error_pos] + GF2(1)
        
        # Extract message bits from data positions
        msg = GF2(np.zeros(self.k, dtype=int))
        for i, pos in enumerate(self.data_positions):
            msg[i] = received[pos]
        
        return msg

