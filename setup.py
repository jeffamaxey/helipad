import setuptools

with open('README.md', 'r', encoding='UTF-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name="helipad",
	version="1.4.1",
	author="C Harwick",
	author_email="cameron@cameronharwick.com",
	description="An agent-based modeling framework for Python with a shallow learning curve and powerful visualization capabilities.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://helipad.dev",
	project_urls = {
		'Homepage': 'https://helipad.dev',
		'Documentation': 'https://helipad.dev/functions/',
		'Source Code': 'https://github.com/charwick/helipad'
	},
	packages=setuptools.find_packages(),
	package_dir={'helipad': 'helipad'},
	include_package_data=True,
	package_data={'': ['*.css', '*.mo', '*.po', '*.pot', '*.png']},
	license='MIT',
	install_requires=[
		'matplotlib',
		'pandas',
		'networkx'
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Science/Research",
		"Topic :: Scientific/Engineering :: Visualization"
	],
	python_requires='>=3.7',
)