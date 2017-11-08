from Crypto.PublicKey import RSA
from Crypto import Random


def ssh_keygen(bits: int=2048) -> (str, str):
    """
    Generate a public OpenSSH key pair using the RSA algorithm.

    :param bits: number of bits in the key
    :return: priavte_key, public_key

    private_key, public_key = keygen(2048)
    """
    randgen = Random.new().read
    key = RSA.generate(bits=bits, randfunc=randgen)
    private = key.exportKey('PEM').decode()
    public = key.exportKey('OpenSSH').decode()
    return private, public
