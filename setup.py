from setuptools import find_packages, setup

setup(
    name='fencegate',
    version='0.0.1 - ALPHA',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-babel2',
        'markdown',
        'flask-sqlalchemy',
    ],
)
