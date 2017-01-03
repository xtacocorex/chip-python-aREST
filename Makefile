pckage: clean
	python setup.py sdist

publish: package
	twine upload dist/*

clean:
	rm -rf CHIP_aREST.* build dist
	rm -f *.pyo *.pyc
	rm -f *.egg

build:
	python setup.py build --force

install: build
	python setup.py install --force
