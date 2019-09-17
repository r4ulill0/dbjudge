from setuptools import setup, find_packages

setup(
    name='dbjudge',
    version='0.5.0a',
    description='A SQL judge for postgresql',
    author='Raúl Medina',
    author_email='raulmgcontact@gmail.com',
    packages=find_packages(),
    install_requires=[
        'psycopg2',
        'xeger',
    ],
)
