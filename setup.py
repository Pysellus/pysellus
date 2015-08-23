from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name='pysellus',
    version=version,
    description='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='stream streaming api test testing quality',
    author='',
    author_email='',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        i.strip() for i in open('requirements.txt').readlines()
    ],
    entry_points={
        'console_scripts': [
            'pysellus = pysellus.core:main'
        ],
    },
)
