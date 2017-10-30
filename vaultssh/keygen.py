from Crypto.PublicKey import RSA, DSA


class GeneratePublicKey(object):
    def __init__(self, algorithm: str='RSA', bits: int=2048):
        """
        Generate a public key.
        :param algorithm: algorithm to use for key encryption.
                          RSA is recommended.
                          Ref: https://en.wikipedia.org/wiki/Public-key_cryptography
        :param bits: number of bits in the key.
                     2048 bits is generally considered sufficient.
                     Ref: https://en.wikipedia.org/wiki/Key_size
        """
        self.algorithm = algorithm
        self.bits = bits

    def public_key(self):
        try:
            return getattr(GeneratePublicKey, '_{}'.format(self.algorithm.lower()))(self)
        except AttributeError:
            raise ValueError('{} is not a supported algorithm'.format(self.algorithm))

    def _rsa(self):
        return RSA.generate(bits=self.bits).publickey().exportKey()

    def _dsa(self):
        return DSA.generate(bits=self.bits).publickey().exportKey()
