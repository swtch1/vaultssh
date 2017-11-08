import requests
import json


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
        :param host: vault host IP or DNS name
        :param port: vault listening port
        :param api_version: vault API version
        :param use_ssl: use HTTPS
        :param verify: verify certificate
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
            public_key: str,
            backend: str='ssh-client-signer',
            client_role: str='clientrole',
    ) -> str:
        """
        Sign an SSH key.
        :param token: client token used to authenticate with Vault
        :param public_key: public key string to sign
        :param backend: vault backend to use
        :param client_role: name of the Vault client role
        :return: signed private key
        """
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
        try:
            signed_key = response.json()['data']['signed_key'].rstrip('\n')
        except KeyError as e:
            print('error retrieving key from request response: {}'.format(e))
            raise
        return signed_key
