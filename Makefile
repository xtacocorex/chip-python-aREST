# PyPi Packaging
package: clean
	@echo " ** PACKAGING FOR PYPI **"
	python setup.py sdist bdist_wheel
	python3 setup.py bdist_wheel

# PyPi Packaging
package3: package
	@echo " ** PACKAGING FOR PYPI **"
	python3 setup.py bdist_wheel

# PyPi Publishing
publish: package package3
	@echo " ** UPLOADING TO PYPI **"
	twine upload dist/*

# Clean all the things
clean:
	@echo " ** CLEANING CHIP PYTHON AREST **"
	rm -rf CHIP_aREST.* build dist
	rm -f *.pyo *.pyc
	rm -f *.egg
	rm -rf __pycache__
	rm -rf debian/python-chip-python-arest*
	rm -rf debian/python3-chip-python-arest*

# Build all the things
build:
	@echo " ** BUILDING CHIP PYTHON AREST: PYTHON 2 **"
	python setup.py build --force

# Install all the things
install: build
	@echo " ** INSTALLING CHIP PYTHON AREST: PYTHON 2 **"
	python setup.py install --force

# Build for Python 3
build3:
	@echo " ** BUILDING CHIP PYTHON AREST: PYTHON 3 **"
	python3 setup.py build --force

# Install for Python 3
install3: build3
	@echo " ** INSTALLING CHIP PYTHON AREST: PYTHON 3 **"
	python3 setup.py install --force

# Install for both Python 2 and 3
all: install install3

# Create a deb file
debfile:
	@echo " ** BUILDING DEBIAN PACKAGES **"
	dpkg-buildpackage -rfakeroot -uc -b
