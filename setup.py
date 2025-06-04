
from setuptools import setup, find_packages

setup(
    name='zra_smart_invoice',
    version='1.0.0',
    description='ERPNext integration with ZRA Smart Invoice (e-Invoicing Zambia)',
    author='Miyanda Hakooma',
    author_email='mh@antares.co.zm',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['frappe'],
)
