from setuptools import setup, find_packages


setup(
    name='autoextract-poet',
    version='0.1.0',
    description='web-poet definitions for AutoExtract API',
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    author='Scrapinghub',
    author_email='info@scrapinghub.com',
    url='https://github.com/scrapinghub/autoextract-poet',
    packages=find_packages(exclude=['tests',]),
    install_requires=[
        'attrs',
        'web-poet',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
