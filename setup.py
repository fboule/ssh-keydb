from setuptools import setup, find_packages
setup(
    name="ssh-keydb",
    version="0.1",
    packages=find_packages(),

    # Dependencies
    install_requires=['SQLAlchemy==0.7.8', 'elixir>=0.7.1', 'pysqlite>=2.5', 'skeletool>=0.1dev'],

    package_data={
        '': ['COPYING', "*.txt"],
    },

    entry_points={
        'console_scripts': [
            'ssh-keydb = ssh_keydb.ssh_keydb:run',
        ],
    },

    # Metadata
    author='Fabien Bouleau',
    author_email='fabien.bouleau@gmail.com',
    description='OpenSSH public key management tool',
    license='GPLv3',
    keywords='openssh public key management tool',
    url='http://code.google.com/p/ssh-keydb/',
)
