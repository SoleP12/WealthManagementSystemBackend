from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
fake_hash = password_hash.hash("fakehash")