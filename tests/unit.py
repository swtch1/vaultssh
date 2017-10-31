from unittest import TestCase, main, skip

import requests_mock

from vaultssh import vault


@requests_mock.mock()
class TestVaultSSH(TestCase):
    def test_get_token_returns_token(self, m):
        client = vault.Client(
            host='somehost',
            port=1234,
            api_version='v0',
            use_ssl=True,
            verify=False,
        )

        response = {
            'request_id': 'rid1',
            'lease_id': '',
            'renewable': False,
            'lease_duration': 0,
            'data': None,
            'wrap_info': None,
            'warnings': None,
            'auth': {
                'client_token': '12-34-56-78',
                'accessor': '12-12-12-12',
                'policies': ['default', 'ssh_client_token_create'],
                'metadata': {'username': 'rundeck'},
                'lease_duration': 123456789,
                'renewable': True
            }}
        m.post('https://somehost:1234/v0/auth/userpass/login/user1', json=response)
        token = client.get_token(username='user1', password='doesntmatter')
        self.assertEqual(token, '12-34-56-78')

    def test_sign_key_returns_correct_string(self, m):
        client = vault.Client(
            host='somehost',
            port=1234,
            api_version='v1',
            use_ssl=False,
            verify=False,
        )
        response = {
            "request_id": "f5f35ee8-41a7-78a9-327a-57285324e20a",
            "lease_id": "",
            "renewable": False,
            "lease_duration": 0,
            "data": {
                "serial_number": "613da3d55c0de6b8",
                "signed_key": "ssh-rsa-cert-v01@openssh.com AAA==\n"
            },
            "wrap_info": None,
            "warnings": None,
            "auth": None
        }
        m.post('http://somehost:1234/v1/ssh-client-signer/sign/clientrole', json=response)
        signed_key = client.sign_key(token='1234')
        self.assertEqual(signed_key, 'ssh-rsa-cert-v01@openssh.com AAA==\n')


if __name__ == '__main__':
    main()
