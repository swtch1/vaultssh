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
##### Basic Implementation:
```python3
from vaultssh import Client

vault = Client(host='my.vault.server')
token = vault.get_token('vaultuser', 'P@$$wurd')

with open('my/publc/key.pub', 'r') as f:
    pkey = f.read()

signed_key = vault.sign_key(token, pkey)
```

##### Full Implementation:
NOTE: I understand this to be a naive implementation as
generating keys in memory and calling directly to paramiko would be more
efficient but as of this point I haven't gotten that working.
PRs welcomed :)
```python3
import os
from vaultssh import Client
from tempfile import mkdtemp
from subprocess import Popen, PIPE
import shlex
import sys

# define vault server settings
VAULT_SERVER = 'vault.example.com'
VAULT_USER = 'vaultuser'
VAULT_PASS = 'P@$$wurd'

# host to connect to
HOST = 'my.vault.enabled.host'

# setup location for all keys
KEYS_DIR = mkdtemp(dir='/run')
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, 'id_rsa')
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, 'id_rsa.pub')
SIGNED_KEY_PATH = os.path.join(KEYS_DIR, 'signed_key.pub')

# generate key pair with ssh-keygen
cmd = "ssh-keygen -t rsa -f {} -N ''".format(os.path.join(KEYS_DIR, 'id_rsa'))
keygen = Popen(shlex.split(cmd))

# obtain a token from vault
vault = Client(host=VAULT_SERVER, verify=False)
token = vault.get_token(VAULT_USER, VAULT_PASS)

# wait for key generation process to complete, read public key, write signed key
keygen.wait()
with open(PUBLIC_KEY_PATH, 'r') as f:
    signed_key = vault.sign_key(token=token, public_key=f.read())
with open(SIGNED_KEY_PATH, 'w') as f:
    f.write(signed_key)
os.chmod(SIGNED_KEY_PATH, 0o600)

# build a command and execute on the remote host using the generated and signed key pair
remote_command = 'hostname'
cmd = 'ssh -i {signed} -i {private} {user}@{host} {command}'.format(
    signed=SIGNED_KEY_PATH,
    private=PRIVATE_KEY_PATH,
    user='gecloud',
    host=HOST,
    command=remote_command)
r = Popen(shlex.split(cmd), stdout=PIPE)
stdout, stderr = r.communicate()
if stdout is not None:
    sys.stdout.write(str(stdout, 'UTF-8').rstrip('\n'))
if stderr is not None:
    sys.stderr.write(str(stderr, 'UTF-8').rstrip('\n'))
```

# Special Considerations
##### Key Location:
Although not what I expected, in my testing I found that a key must be
used where it is generated.  If a key is moved or renamed it will very
likely not work in the authentication phase.  The first sign that a key
is failing for formattion or location reasons is the request of a
password during the sign on attempt.  Unless a passphrase was created on
the key file it is very unlikely this error means what it says.  Check
your process and try again.

##### OpenSSH Version:
In testing Byron Pezan noticed that the version os OpenSSH can at
times cause a false error asking for a passphrase when one is not
necessary.  Make sure that your version of OpenSSH and associated
libraries are up to date if you are receiving errors.

# More Information
For more informatin the methods in this library have build in
documentation that can be referenced directly through the source code
or any modern IDE.

# Contributing
This library is pretty bare bones as it was created for a very specific
use case.  If you want to add on just follow PEP8 styling as well as the
general style of the existing code, and include tests.  Submit a pull
request and we'll try to get your feature merged in.
