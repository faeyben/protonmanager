from setuptools import setup, find_packages

setup(
    name='protonmanager',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'protonmanager = protonmanager:cli',
        ]
    }
)
