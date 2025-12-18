"""
Benchmark script comparing Hamming and BCH McEliece variants.
"""
import time
import numpy as np
from code.hamming_mceliece import keygen as hamming_keygen
from code.hamming_mceliece import encrypt as hamming_encrypt
from code.hamming_mceliece import decrypt as hamming_decrypt
from code.bch_mceliece import keygen as bch_keygen
from code.bch_mceliece import encrypt as bch_encrypt
from code.bch_mceliece import decrypt as bch_decrypt


def benchmark_hamming(L, num_trials=3):
    """Benchmark Hamming variant."""
    times = {
        'keygen': [],
        'encrypt': [],
        'decrypt': []
    }
    
    for _ in range(num_trials):
        # Key generation
        start = time.time()
        public_key, private_key = hamming_keygen.generate_keys(L)
        times['keygen'].append(time.time() - start)
        
        G_pub, t = public_key
        S, P, G_total, hamming_code = private_key
        
        # Generate random message
        msg_length = 11 * L
        message = np.random.randint(0, 2, msg_length)
        
        # Encryption
        start = time.time()
        ciphertext = hamming_encrypt.encrypt(message, G_pub, t, S, G_total, P)
        times['encrypt'].append(time.time() - start)
        
        # Decryption
        start = time.time()
        decrypted = hamming_decrypt.decrypt(ciphertext, S, P, G_total, hamming_code)
        times['decrypt'].append(time.time() - start)
    
    # Calculate averages
    avg_times = {k: np.mean(v) for k, v in times.items()}
    
    # Calculate metrics
    msg_bits = 11 * L
    cipher_bits = 15 * L
    expansion_rate = cipher_bits / msg_bits
    pub_key_size = G_pub.shape[0] * G_pub.shape[1] / 8  # bytes
    
    return {
        'keygen_time': avg_times['keygen'],
        'encrypt_time': avg_times['encrypt'],
        'decrypt_time': avg_times['decrypt'],
        'expansion_rate': expansion_rate,
        'pub_key_size': pub_key_size
    }


def benchmark_bch(L, num_trials=3):
    """Benchmark BCH variant."""
    times = {
        'keygen': [],
        'encrypt': [],
        'decrypt': []
    }
    
    for _ in range(num_trials):
        # Key generation
        start = time.time()
        public_key, private_key = bch_keygen.generate_keys(L)
        times['keygen'].append(time.time() - start)
        
        G_pub, t = public_key
        S, P, G_total, bch_code = private_key
        
        # Generate random message
        msg_length = 7 * L
        message = np.random.randint(0, 2, msg_length)
        
        # Encryption
        start = time.time()
        ciphertext = bch_encrypt.encrypt(message, G_pub, t, S, G_total, P)
        times['encrypt'].append(time.time() - start)
        
        # Decryption
        start = time.time()
        decrypted = bch_decrypt.decrypt(ciphertext, S, P, G_total, bch_code)
        times['decrypt'].append(time.time() - start)
    
    # Calculate averages
    avg_times = {k: np.mean(v) for k, v in times.items()}
    
    # Calculate metrics
    msg_bits = 7 * L
    cipher_bits = 15 * L
    expansion_rate = cipher_bits / msg_bits
    pub_key_size = G_pub.shape[0] * G_pub.shape[1] / 8  # bytes
    
    return {
        'keygen_time': avg_times['keygen'],
        'encrypt_time': avg_times['encrypt'],
        'decrypt_time': avg_times['decrypt'],
        'expansion_rate': expansion_rate,
        'pub_key_size': pub_key_size
    }


def main():
    print("=" * 80)
    print("McEliece Cryptosystem Benchmark")
    print("=" * 80)
    
    L_values = [5, 10, 20]
    
    print("\n" + "=" * 80)
    print("HAMMING VARIANT")
    print("=" * 80)
    print(f"\n{'L':<5} {'KeyGen(s)':<12} {'Encrypt(s)':<12} {'Decrypt(s)':<12} {'Expansion':<12} {'PubKey(KB)':<12}")
    print("-" * 80)
    
    for L in L_values:
        print(f"Running benchmark for L={L}...", end=" ", flush=True)
        results = benchmark_hamming(L)
        print("Done!")
        print(f"{L:<5} {results['keygen_time']:<12.6f} {results['encrypt_time']:<12.6f} "
              f"{results['decrypt_time']:<12.6f} {results['expansion_rate']:<12.2f} "
              f"{results['pub_key_size']/1024:<12.2f}")
    
    print("\n" + "=" * 80)
    print("BCH VARIANT")
    print("=" * 80)
    print(f"\n{'L':<5} {'KeyGen(s)':<12} {'Encrypt(s)':<12} {'Decrypt(s)':<12} {'Expansion':<12} {'PubKey(KB)':<12}")
    print("-" * 80)
    
    for L in L_values:
        print(f"Running benchmark for L={L}...", end=" ", flush=True)
        results = benchmark_bch(L)
        print("Done!")
        print(f"{L:<5} {results['keygen_time']:<12.6f} {results['encrypt_time']:<12.6f} "
              f"{results['decrypt_time']:<12.6f} {results['expansion_rate']:<12.2f} "
              f"{results['pub_key_size']/1024:<12.2f}")
    
    print("\n" + "=" * 80)
    print("\nNotes:")
    print("  - Expansion: Ciphertext length / Message length")
    print("  - PubKey: Size of public key matrix in KB")
    print("  - Times are averaged over 3 trials")
    print("=" * 80)


if __name__ == "__main__":
    main()
