TESTS=./tests
SOURCE=./spaceship

all: test lint clean

.PHONY: clean
clean: clean-logs
	rm -rf *.orig~
	rm -rf *.pyc
	rm -rf */__pycache__
	rm -rf *.stackdump~

clean-logs:
	rm -rf logs/*.txt

clean-saves:
	rm -rf saves/*

lint-flake: lint-flake-source lint-flake-tests

lint-pep8-tests:
	pep8 $(TESTS)

lint-pep8-source:
	pep8 $(SOURCE)

lint-pep8: lint-pep8-source lint-pep8-tests

lint: lint-flake lint-pep8
	@echo "Done checking"

test:
	py.test --verbose --color=yes --cov=$(SOURCE) $(TESTS)
	if [ -a picturfy-img.png ] ; then rm picturfy-img.png ; fi;
	if [ -a assets/picturfy-img.png ] ; then rm assets/picturfy-img.png ; fi
	
test-clean: test clean

# profile:
# 	python -m cProfile -s time -m spaceship.start > profiler.txt

profile-dungeon:
	python -m cProfile -s time spaceship/dungeon.py > profiler.txt

help:
	@echo "    clean-pyc:"
	@echo "        Clean directory of .pyc files and __pycache__ folders"
	@echo "    lint:"
	@echo "        Checks formatting style with flake8 and pep8"
	@echo "     test:"
	@echo "        Runs pytest in tests folder"

run:
	python -m spaceship.start

check-classes:
	python -m spaceship.classes.color
	python -m spaceship.classes.tile
	python -m spaceship.classes.object
	python -m spaceship.classes.unit
	python -m spaceship.classes.neutrals
	python -m spaceship.classes.monsters
	python -m spaceship.classes.bat
	python -m spaceship.classes.player
	python -m spaceship.classes.item
	python -m spaceship.classes.charmap	
	python -m spaceship.classes.map
	python -m spaceship.classes.world
	python -m spaceship.classes.cave
	python -m spaceship.classes.city
	python -m spaceship.classes.wild grass
	python -m spaceship.classes.wild forest
	python -m spaceship.classes.wild plains
	python -m spaceship.classes.wild woods


