from setuptools import setup, find_packages

readme = '''
Python wrapper for NetworkManager-CLI(nmcli)

To manipulate network configuration from python code on Linux, 
you can use this module as a wrapper to nmcli.
'''

setup(
    name='python_nmcli_wrapper',
    version='0.1.0',
    description='Python wrapper for NetworkManager-CLI(nmcli)',
    long_description=readme,
    author='Satoshi HOSHINO',
    author_email='s-hoshino@ib-sol.co.jp',
    install_requires=['os', 'shlex', 'subprocess', 'enum'],
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
)
