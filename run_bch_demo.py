"""
Demo script for BCH-based McEliece cryptosystem.
"""
import numpy as np
from code.bch_mceliece import keygen, encrypt, decrypt


def main():
    print("=" * 60)
    print("BCH-based McEliece Cryptosystem Demo")
    print("=" * 60)
    
    # Parameters
    L = 5
    print(f"\nParameters:")
    print(f"  Number of blocks (L): {L}")
    print(f"  BCH code: (15, 7)")
    print(f"  Message length: {7 * L} bits")
    print(f"  Ciphertext length: {15 * L} bits")
    
    # Generate keys
    print("\n[1] Generating keys...")
    public_key, private_key = keygen.generate_keys(L)
    G_pub, t = public_key
    S, P, G_total, bch_code = private_key
    
    print(f"  Public key size: {G_pub.shape}")
    print(f"  Error correction capability: {t} errors (2 per block)")
    print(f"  Key generation complete!")
    
    # Generate random message
    msg_length = 7 * L
    message = np.random.randint(0, 2, msg_length)
    
    print(f"\n[2] Original message ({len(message)} bits):")
    print(f"  {message[:20]}... (showing first 20 bits)")
    
    # Encrypt
    print("\n[3] Encrypting message...")
    ciphertext = encrypt.encrypt(message, G_pub, t, S, G_total, P)
    print(f"  Ciphertext ({len(ciphertext)} bits):")
    print(f"  {ciphertext[:20]}... (showing first 20 bits)")
    print(f"  Encryption complete!")
    
    # Decrypt
    print("\n[4] Decrypting ciphertext...")
    decrypted = decrypt.decrypt(ciphertext, S, P, G_total, bch_code)
    print(f"  Decrypted message ({len(decrypted)} bits):")
    print(f"  {decrypted[:20]}... (showing first 20 bits)")
    
    # Verify
    print("\n[5] Verification:")
    if np.array_equal(message, decrypted):
        print("  ✓ SUCCESS: Decrypted message matches original!")
    else:
        print("  ✗ FAILURE: Decrypted message does not match!")
        # Count differences
        diff = np.sum(message != decrypted)
        print(f"  Number of bit errors: {diff}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
