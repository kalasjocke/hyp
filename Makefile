clean-pyc:
	$(shell find * -name "*.pyc" | xargs rm -rf)

clean: clean-pyc

test: clean
	coverage run --source hyp -m py.test tests/ -s
	coverage report -m

dist: clean
	python setup.py sdist upload
