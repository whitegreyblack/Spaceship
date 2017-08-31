TESTS=./tests
SOURCE=./spaceship
clean:
	rm -rf $(SOURCE)\*.pyc
	rm -rf $(SOURCE)\__pycache__
	rm -rf $(TESTS)\*.pyc
	rm -rf $(TESTS)\__pycache__

lint-flake:
	python2.7 -m flake8 spaceship\
	python2.7 -m flake8 tests\

lint-pep8:
	pep8 spaceship\
	pep8 tests\

lint: lint-flake lint-pep8
	@echo "Done checking"

test: clean
	py.test --verbose --color=yes --cov=spaceship $(TESTS)
	clean
	
help:
	@echo "    clean-pyc:"
	@echo "        Clean directory of .pyc files and __pycache__ folders"
	@echo "    lint:"
	@echo "        Checks formatting style with flake8 and pep8"
	@echo "     test:"
	@echo "        Runs pytest in tests folder"