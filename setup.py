from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))


setup(
    name="typst-sympy-calculator",
    version="0.4.2",
    description='Convert typst math expressions to sympy form with ANTLR and support matrix, calculous and custom functions.',
    long_description_content_type='text/markdown',
    long_description=open(path.join(here, "README.md"), encoding='utf-8').read(),
    # The project's main homepage.
    url='https://github.com/OrangeX4/typst-sympy-calculator',
    # Author details
    author='OrangeX4',
    author_email='orangex4@qq.com',
    # Choose your license
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Compilers',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Text Processing :: Markup :: Markdown',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(exclude=('tests')),
    py_modules=['TypstCalculator', 'TypstCalculatorServer', 'TypstConverter', 'TypstParser', 'DefaultTypstCalculator'],
    install_requires=[
        'sympy>=1.4',
        'antlr4-python3-runtime==4.7.2'
    ],
)
