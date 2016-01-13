from setuptools import setup

setup(name='pyBSRP',
    version='0.1',
    description='Bike share research\'s data feed parser',
    url='http://github.com/serialc/BSR_parsers',
    author='Cyrille Medard de Chardon',
    author_email='cyrille.mdc@gmail.com',
    license='MIT',
    packages=['pyBSRP'],
    package_data = { 'pyBSRP': [ 'protocols/*.py' ] },
    install_requires=[ 'beautifulsoup4' ],
    zip_safe=False)
