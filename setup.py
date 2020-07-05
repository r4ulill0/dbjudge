from setuptools import setup, find_packages

setup(
    name='dbjudge',
    version='1.0.0a2',
    description='A SQL judge for postgresql',
    author='Raúl Medina González',
    author_email='raulmgcontact@gmail.com',
    packages=find_packages(),
    install_requires=[
        'psycopg2',
        'xeger',
        'sqlparse',
    ],
)
