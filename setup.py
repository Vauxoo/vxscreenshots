#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

install_requires = []
try:
    with open('requirements.txt', 'rb') as req_file:
        install_requires = [r.strip() for r in req_file.readlines()]
except Exception, e:
    print 'Are you testing? %s' % e

test_requirements = []
try:
    with open('requirements_dev.txt', 'rb') as req_file:
        test_requirements = [r.strip() for r in req_file.readlines()]
except Exception, e:
    print 'Are you testing? %s ' % e

setup(
    name='vxscreenshots',
    version='2.3.18',
    description="Basic Screenshots manager pushing and sharing automatically "
                "to Amazon S3",
    long_description=readme + '\n\n' + history,
    author="Vauxoo OpenSource Specialists",
    author_email='nhomar@vauxoo.com',
    url='https://github.com/vauxoo/vxscreenshots',
    packages=[
        'vxscreenshots',
    ],
    package_dir={'vxscreenshots':
                 'vxscreenshots'},
    include_package_data=True,
    license="ISCL",
    zip_safe=False,
    keywords='vxscreenshots',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    install_requires=install_requires,
    tests_requirements=test_requirements,
    scripts=['bin/screenshot.sh'],
    entry_points='''
        [console_scripts]
        vxsswatcher=vxscreenshots.watch:cli
        vxssicon=vxscreenshots.vxscreenshots:cli
    '''
)
