from setuptools import setup, find_packages

def get_requirements_from_file():
    with open("./requirements.txt") as f_in:
        requirements = f_in.read().splitlines()
    return requirements


setup(
    name="ColorTextOCR",
    version="0.5.0",
    author="Aosin",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    install_requires=get_requirements_from_file()
)
