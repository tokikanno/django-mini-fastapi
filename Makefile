.PHONY: clean build demo upload-test py3 intro test-intro

clean:
	rm -rf build dist django_mini_fastapi.egg-info

# build:
# 	python setup.py sdist bdist_wheel

# demo:
# 	django-admin runserver --pythonpath=. --settings=demo.app

intro:
	django-admin runserver --pythonpath=. --settings=demo.intro

# py3:
# 	django-admin runserver --pythonpath=. --settings=demo.py3

test-intro:
	django-admin test --pythonpath=. --settings=demo.intro tests.test_intro

upload-prod:
	flit publish --repository real-pypi

upload-test:
	flit publish --repository pypi
