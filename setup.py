from setuptools import setup

DESCRIPTION = 'Sign SSH keys with Hashicorp Vault that can then be used to SSH into a server.'

setup(
    name='vaultssh',
    version='0.1',
    description=DESCRIPTION,
    url='https://github.build.ge.com/CoreTechAutomation/vaultssh',
    author='Joshua Thornton',
    author_email='joshua.thornton@ge.com',
    packages=['vaultssh'],
    install_requires=[
        'pycryptodomex',  # more secure implementation of PyCrypto
        'requests',
        'requests-mock',
    ],
    zip_safe=False,
)
