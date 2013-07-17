from setuptools import setup, find_packages
setup(
    name="ssh-keydb-server",
    version="1.0",
    packages=find_packages(),

    # Dependencies
    install_requires=['SQLAlchemy==0.7.9', 'elixir>=0.7.1', 'pysqlite>=2.5', 'skeletool>=1.0'],

    package_data={
        '': ['GPL', 'COPYING', "*.txt", 'ssh-keydb-www', 'ssh-keydb.conf' ],
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
