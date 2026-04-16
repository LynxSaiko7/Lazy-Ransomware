import os
from os import path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

def generate_rsa_keys_if_not_exist():
    """Generate RSA key pair jika private.pem atau public.pem belum ada"""
    if path.exists("private.pem") and path.exists("public.pem"):
        print("[✓] RSA keys already exist.")
        return
    
    print("[+] Generating RSA key pair...")
    
    key = RSA.generate(2048)                    # 2048-bit RSA
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    with open("private.pem", "wb") as f:
        f.write(private_key)
    
    with open("public.pem", "wb") as f:
        f.write(public_key)
    
    print("[✓] RSA keys saved as private.pem and public.pem")


def generate_aes_key_and_encrypt_with_rsa():
    """Generate AES key lalu enkripsi dengan RSA public key"""
    try:
        if not path.exists("public.pem"):
            print("[!] public.pem not found.")
            raise FileNotFoundError("public.pem not found.")
        
        # Generate AES-256 key (32 bytes)
        aes_key = get_random_bytes(32)
        print("[+] AES Key (hex):", aes_key.hex())
        
        # Simpan AES key dalam bentuk plaintext dulu (opsional)
        with open("aes_key.txt", "w") as f:
            f.write(aes_key.hex())
        
        # Baca public key
        with open("public.pem", "rb") as f:
            public_key = RSA.import_key(f.read())
        
        # Enkripsi AES key pakai RSA
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_key = cipher_rsa.encrypt(aes_key)
        
        # Simpan hasil enkripsi ke aes_key.bin
        with open("aes_key.bin", "wb") as f:
            f.write(encrypted_key)
        
        print(f"[✓] AES key encrypted and saved to aes_key.bin ({len(encrypted_key)} bytes)")
        
    except FileNotFoundError:
        print("[!] public.pem not found.")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    generate_rsa_keys_if_not_exist()
    generate_aes_key_and_encrypt_with_rsa()
