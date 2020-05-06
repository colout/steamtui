
from setuptools import setup, find_packages

setup (
    name='steamtui',
    version='0.1',
    packages=['steamtui'],
    python_requires='>=3.8',
    install_requires=[
        'npyscreen',
        'requests',
        'activesoup',
        'bs4',
        'pycryptodome'
    ],
    entry_points={
        'console_scripts': [
            'steamtui=steamtui.__main__:main'
        ]
    },
    package_dir={'': 'src'},
)



