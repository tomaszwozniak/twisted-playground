# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='playground',
    version='0.1.0',
    author=u'Michał Rostecki',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points='''
[console_scripts]
    deferred_html = playground.deferred_html:main
    deferred = playground.deferred:main
    echo = playground.echo:main
    cmd = playground.cmd:main
    http = playground.http:main
    http_jinja = playground.http_jinja:main
    ftp = playground.ftp:main
    manhole = playground.manhole:main
    ssh = playground.ssh:main
    irc_bot = playground.irc_bot:main
    irc_server = playground.irc_server:main
''',
    install_requires=[
        'Twisted',
        'pycrypto',
        'pyasn1',
        'Jinja2'
    ]
)
