TESTS=./tests
SOURCE=./spaceship

all: test lint clean

.PHONY: clean
clean:
	rm -rf *.orig
	rm -rf *.pyc
	rm -rf $(SOURCE)\*.orig
	rm -rf $(SOURCE)\*.pyc
	rm -rf $(SOURCE)\__pycache__
	rm -rf $(TESTS)\*.orig
	rm -rf $(TESTS)\*.pyc
	rm -rf $(TESTS)\__pycache__

lint-flake-tests:
	python2.7.exe -m flake8 $(TESTS)

lint-flake-source:
	python2.7.exe -m flake8 $(SOURCE)

lint-flake: lint-flake-source lint-flake-tests

lint-pep8-tests:
	pep8 $(TESTS)

lint-pep8-source:
	pep8 $(SOURCE)

lint-pep8: lint-pep8-source lint-pep8-tests

lint: lint-flake lint-pep8
	@echo "Done checking"

test: clean
	py.test --verbose --color=yes --cov=spaceship $(TESTS)
	if [ -a picturfy-img.png ] ; then rm picturfy-img.png; fi;

test-clean: test clean

help:
	@echo "    clean-pyc:"
	@echo "        Clean directory of .pyc files and __pycache__ folders"
	@echo "    lint:"
	@echo "        Checks formatting style with flake8 and pep8"
	@echo "     test:"
	@echo "        Runs pytest in tests folder"