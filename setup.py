import setuptools
import sys

tests_require = ['nose', 'mock']
if sys.version_info < (2, 7, 0):
    tests_require.append('unittest2')

requirements = []
if sys.version_info < (3, 0, 0):
    requirements.append('dnspython>=1.12.0,<2.0')
else:
    requirements.append('dnspython3>=1.12.0,<2.0')

classifiers = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: BSD License',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.3',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: Implementation :: CPython',
               'Programming Language :: Python :: Implementation :: PyPy',
               'Topic :: Communications', 'Topic :: Internet',
               'Topic :: Software Development :: Libraries']

setuptools.setup(name='email-normalize',
                 version='0.1.0',
                 description=('Normalize email addresses, removing ISP '
                              'specific markup'),
                 long_description=open('README.rst').read(),
                 author='Gavin M. Roy',
                 author_email='gavinmroy@gmail.com',
                 url='http://github.com/gmr/email-normalize',
                 py_modules=['email_normalize'],
                 package_data={'': ['LICENSE', 'README.rst']},
                 include_package_data=True,
                 install_requires=requirements,
                 tests_require=tests_require,
                 license=open('LICENSE').read(),
                 classifiers=classifiers)
