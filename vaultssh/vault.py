import requests
import json

from vaultssh.keygen import generate_pub_key


class Client(object):
    def __init__(
            self,
            host: str,
            port: (str, int)=8200,
            api_version: str='v1',
            use_ssl: bool=True,
            verify: bool=True,
    ):
        """
        Create a client that can communicate with the Vault API.
        :param host:
        :param port:
        :param api_version:
        :param use_ssl:
        :param verify:
        """
        self.host = host
        self.port = port
        self.api_version = api_version
        self.use_ssl = use_ssl
        self.verify = verify

    def get_token(self, username: str, password: str) -> str:
        """
        Use the username and password auth backend to obtain a client token.  The clien token can be used to sign
        a key for direct SSH access.

        Vault Documentation Reference: https://www.vaultproject.io/docs/auth/userpass.html
        :param username:
        :param password:
        :return: client token
        """
        url = '{protocol}://{host}:{port}/{api_version}/auth/userpass/login/{user}'.format(
            protocol='https' if self.use_ssl else 'http',
            host=self.host,
            port=self.port,
            api_version=self.api_version,
            user=username,
        )
        payload = json.dumps({'password': '{}'.format(password)})
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers, verify=self.verify)
        client_token = response.json()['auth']['client_token']
        return client_token

    def sign_key(
            self,
            token: str,
            backend: str='ssh-client-signer',
            client_role: str='clientrole',
            auto_gen_key=True,
            public_key: str=None,
    ) -> str:
        """
        Sign an SSH key
        :param token: client token used to authenticate with Vault
        :param backend: vault backend to use
        :param client_role: name of the Vault client role
        :param auto_gen_key: automatically generate an OpenSSH RSA public key to sign
               not compatible with public_key parameter
        :param public_key: public key string to sign
               not compatible with auto_gen_key parameter
        :return: signed private key
        """
        if auto_gen_key:
            public_key = generate_pub_key().decode()

        url = '{protocol}://{host}:{port}/{api_version}/{backend}/sign/{client_role}'.format(
            protocol='https' if self.use_ssl else 'http',
            host=self.host,
            port=self.port,
            api_version=self.api_version,
            backend=backend,
            client_role=client_role
        )
        payload = json.dumps({
            'public_key': public_key
        })
        headers = {
            'X-Vault-Token': token,
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers, verify=self.verify)
        signed_key = response.json()['data']['signed_key']
        return signed_key
