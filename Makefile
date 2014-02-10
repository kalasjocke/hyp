clean-pyc:
	$(shell find * -name "*.pyc" | xargs rm -rf)

clean: clean-pyc

test: clean
	coverage run --source hy -m py.test tests/ -s
	coverage report -m
