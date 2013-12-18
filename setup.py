from distutils.core import setup

setup(
    name='appacitive-python-sdk',
    version='1.0',
    packages=['pyappacitive', 'pyappacitive.src', 'pyappacitive.src.query', 'pyappacitive.src.cloudcode',
              'pyappacitive.src.utilities', 'pyappacitive.tests'],
    url='www.appacitive.com',
    license='',
    author='sathley',
    author_email='sathley@appacitive.com',
    description='Python SDK for Appacitive'
)
