.venv/venv.timestamp:
	virtualenv .venv
	touch $@


.venv/requirements.timestamp: .venv/venv.timestamp setup.py requirements.txt
	.venv/bin/pip install --upgrade -r requirements.txt
	touch $@


.PHONY: git-attributes
git-attributes:
	git --no-pager diff --check `git log --oneline | tail -1 | cut --fields=1 --delimiter=' '`


.PHONY: lint
lint: .venv/requirements.timestamp
	.venv/bin/flake8


.PHONY: test
test: .venv/requirements.timestamp
	.venv/bin/py.test -vv --cov=geolink_formatter --cov-report term-missing:skip-covered \
		geolink_formatter/tests


.PHONY: check
check: git-attributes lint test


.PHONY: clean
clean:
	rm -rf .venv


.PHONY: build
build:
	awk 'FNR==1{print ""}1' README.md CHANGELOG | pandoc -f markdown -t rst -o description.rst
	.venv/bin/python setup.py clean sdist bdist_wheel
	git checkout -- description.rst


.PHONY: doc
doc:
	.venv/bin/sphinx-build -b html doc/source/ doc/build/html/