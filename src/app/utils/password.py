import bcrypt


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def db_str_to_bytes(db_hex_hash: str) -> bytes:
    return bytes.fromhex(db_hex_hash[2:])


def verify_password(password: str, hashed_password: str | bytes, db: bool = False) -> bool:
    if db:
        return bcrypt.checkpw(password.encode("utf-8"), db_str_to_bytes(hashed_password))
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
