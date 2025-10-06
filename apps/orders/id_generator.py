import secrets

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ1234567890"
ORDER_ID_LENGTH = 10

def make_order_id(length=ORDER_ID_LENGTH):
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))
