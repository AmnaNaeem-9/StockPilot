
from app.auth.password_manager import PasswordManager


# Test password
password = "StockPilot@123"


# 1. Generate password hash
hashed_password = PasswordManager.hash_password(password)

print("Original password:", password)
print("Generated hash:", hashed_password)


# 2. Verify correct password
result = PasswordManager.verify_password(
    password,
    hashed_password,
)

print("Correct password verification:", result)


# 3. Verify incorrect password
result = PasswordManager.verify_password(
    "WrongPassword123",
    hashed_password,
)

print("Incorrect password verification:", result)


# 4. Check whether hash needs updating
result = PasswordManager.needs_rehash(hashed_password)

print("Hash needs rehashing:", result)
