from distutils.core import setup

setup(
    name='hy-py',
    version='0.1.0',
    packages=['hy', 'hy.adapters'],
    license='MIT',
    author='Joakim Ekberg',
    author_email='jocke.ekberg@gmail.com',
    url='https://github.com/kalasjocke/hy',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().split(),
)
