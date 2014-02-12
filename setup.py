from distutils.core import setup

setup(
    name='hyp',
    version='0.1.0',
    packages=['hyp', 'hyp.adapters'],
    license='MIT',
    author='Joakim Ekberg',
    author_email='jocke.ekberg@gmail.com',
    url='https://github.com/kalasjocke/hyp',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().split(),
)
