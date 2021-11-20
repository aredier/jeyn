from setuptools import setup, find_packages


with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.readlines()


setup(
 author='Antoine Redier',
 author_email='antoine.redier2@gmail.com',
 classifiers=[
     'Development Status :: 3 - Alpha',
     'Intended Audience :: Developers',
     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
     'Natural Language :: English',
     'Programming Language :: Python :: 3',
     'Programming Language :: Python :: 3.7',
 ],
 description='python sdk of the jeyn project',
 install_requires=[],
 license='GNU General Public License v3',
 long_description=[],
 include_package_data=True,
 keywords='jeyn',
 name='jeyn',
 packages=find_packages(),
 setup_requires=requirements,
)
