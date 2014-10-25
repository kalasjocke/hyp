from setuptools import setup

setup(
    name='hyp',
    version='0.6.0',
    packages=['hyp'],
    license='MIT',
    author='Joakim Ekberg',
    author_email='jocke.ekberg@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    url='https://github.com/kalasjocke/hyp',
    description='Partial JSON API implementation in Python on top of Schematics',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().split(),
)
