import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='ar_sudoku',
     version='1.0',
     author='Tristan Bester',
     author_email='tristanbester@gmail.com',
     description='An augmented reality sudoku solver.',
     license='MIT',
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     include_package_data=True,
     packages=setuptools.find_packages(),
     install_requires=[
     'opencv-python',
     'keras'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
