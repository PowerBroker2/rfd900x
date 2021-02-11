from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name             = 'rfd900x',
    packages         = ['rfd900x'],
    version          = '0.0.5',
    description      = 'Python module for configuring RFD900x series radios',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author           = 'Power_Broker',
    author_email     = 'gitstuff2@gmail.com',
    url              = 'https://github.com/PowerBroker2/rfd900x',
    download_url     = 'https://github.com/PowerBroker2/rfd900x/archive/0.0.5.tar.gz',
    keywords         = ['RFD', 'RFD-900', 'RFD-900x', 'RFD-900+', 'RFD 900', 'RFD 900x', 'RFD 900+'],
    classifiers      = [],
    install_requires = ['pyserial']
)
