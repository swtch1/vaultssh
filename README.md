# vaultssh
Sign SSH keys with Hashicorp Vault that can then be used to SSH into a
server.

## Summary
If multiple applications need to access compute resources through Vault
there's no reason for each of them to re-implement the process.  This
library makes it easy to get a token from Vault using a username and
password, and sign a public SSH key using a Vault generated token.

# Installation
Install directly from the Build.GE Github.
```bash
pip3 install git+git://github.build.ge.com/CoreTechAutomation/vaultssh.git
```

On linux you will likely need to get python34-devel or something similar
for pip3 to install the software successfully.

# Usage
Please read the examples from top to bottom.  They build on each other
so no one snippet of code may work without context from the code above.

Start by importint the Client class.
```python3
from vaultssh import Client
```

Let's run through the most standard setup.  Using a username and
password, get a token and the token to return a signed private key.
```python3
client = Client(host='10.20.30.40', verify=False)  # no verify since we're using a self signed certificate
token = client.get_token(username='me', password='p@55w0rd')
signed_key = client.sign_key(token)
```

If you have a public key already you can use that instead of having one
automatically generated.
```python3
with open('/path/to/mykey.pub', 'r') as k:
    pubkey = k.read()

signed_key = client.sign_key(token, public_key=pubkey)
```

Now let's use paramiko to SSH to the server with the key we created.
```python3
import paramiko


```

Otherwise the libraries methods have build in documentation that can be
referenced directly through the source code or any modern IDE.

# Contributing
This library is pretty bare bones as it was created for a very specific
use case.  If you want to add on just follow PEP8 styling as well as the
general style of the existing code, and include tests.  Submit a pull
request and we'll try to get your feature merged in.
