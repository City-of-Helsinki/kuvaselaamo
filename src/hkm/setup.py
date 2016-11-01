#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = open('README.rst').read()

def get_version():
    try:
        import subprocess
        p = subprocess.Popen('hg id -t', shell=True, stdout=subprocess.PIPE)
        tag = p.stdout.read()[1:].strip()
        return tag
    except:
        return 'dev'

setup(
    name='hkm',
    version=get_version(),
    description="""Helsingin kaupunginmuseon kuvapalvelu""",
    long_description=readme,
    author='Haltu',
    packages=find_packages(),
    include_package_data=True,
    license="Haltu",
    zip_safe=False,
    keywords='hkm-kuvapalvelu',
    install_requires=[
      'django-ordered-model==1.3.0',
      'django-phonenumber-field==1.1.0',
    ],
)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
