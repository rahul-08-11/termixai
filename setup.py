from setuptools import setup, find_packages
# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
setup(
    name='termixai',
    version='0.1',
    packages=find_packages(exclude=['tests*', 'venv*', '__pycache__']),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'termixai = termixai.cli:main', 
        ],
    },
    include_package_data=True,
    description='🤖 AI Shell Assistant - Terminal-based AI helper for Linux users.',
    author='Rahul Kumar',
    author_email='rahul.work.programming@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ],
)
