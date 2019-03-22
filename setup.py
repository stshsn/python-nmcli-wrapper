setup(
    name='python_nmcli_wrapper',
    version='0.1.0',
    description='Simple wrapper for Network Manager CLI',
    long_description=readme,
    author='Satoshi HOSHINO',
    author_email='s-hoshino@ib-sol.co.jp',
    install_requires=['os', 'shlex', 'subprocess', 'enum']
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))

