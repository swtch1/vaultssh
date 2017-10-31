from Crypto.PublicKey import RSA


def generate_pub_key(bits: int=2048) -> str:
    """
    Generate a public OpenSSH key using the RSA algorithm.
    :param bits: number of bits in the key
    :return: ssh publick key: str
    """
    return RSA.generate(bits=bits).publickey().exportKey('OpenSSH').decode()
