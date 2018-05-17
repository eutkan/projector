import bcrypt


def hash(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_hash(password, hash):
    return bcrypt.checkpw(password, hash)
