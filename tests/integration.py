from unittest import TestCase, main
import re

from vaultssh.keygen import ssh_keygen


class TestKeyGen(TestCase):
    def test_generate_pub_key_generates_an_open_ssh_key(self):
        self.assertTrue(re.match('^ssh-rsa.+', ssh_keygen()))


if __name__ == '__main__':
    main()
