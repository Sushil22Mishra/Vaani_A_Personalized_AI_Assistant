from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT= '-e .'
def get_requirements(file_path:str)->List[str]:
    """This function returns a list of requirements from a file."""

    requirements=[]
    with open('requirements.txt') as file_obj:
        requirements= file_obj.readlines()
        requirements= [req.replace("\n", "") for req in requirements ]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name='vaani',
    version='0.0.1',
    author_name= 'Sushil Mishra',
    author_email= 'sushil22mishra@gmail.com',
    packages= find_packages(),
    install_requires= get_requirements('requirements.txt')
)