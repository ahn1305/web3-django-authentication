from setuptools import setup, find_packages

setup(
    name='web3-django-authentication',
    version='0.0.1',
    install_requires=['ethereum==2.3.2', 'rlp<=2.0.0', 'eth_utils>=1.0.3', 'Django>=2.0'],
    packages=[
        '.',
    ],
    author='Ashwin B',
    author_email='ahnashwin1305@gmail.com',
    description='Integrate metamask with django' 	 	,
    url='https://github.com/ahn1305/web3-django-authentication',
)
