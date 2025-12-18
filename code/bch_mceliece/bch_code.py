"""
BCH (15, 7) code implementation using galois library.
"""
import numpy as np
import galois


class BCHCode:
    """
    Implementation of the (15, 7) BCH code.
    This code can correct 2 errors.
    """
    
    def __init__(self):
        """Initialize the (15, 7) BCH code."""
        self.n = 15  # Codeword length
        self.k = 7   # Message length
        self.t = 2   # Error correction capability
        
        # Create BCH code using galois library
        self.bch = galois.BCH(15, 7)
        
    def encode(self, msg_bits):
        """
        Encode a message using the BCH code.
        
        Args:
            msg_bits: Array of k=7 message bits
            
        Returns:
            galois.FieldArray: Codeword of length n=15
        """
        GF2 = galois.GF(2)
        msg = GF2(np.array(msg_bits))
        codeword = self.bch.encode(msg)
        return codeword
    
    def decode(self, codeword):
        """
        Decode a received codeword.
        Corrects up to 2 errors.
        
        Args:
            codeword: Received codeword of length n=15
            
        Returns:
            galois.FieldArray: Decoded message of length k=7
        """
        GF2 = galois.GF(2)
        received = GF2(np.array(codeword))
        decoded = self.bch.decode(received)
        return decoded
