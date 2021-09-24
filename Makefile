.PHONY: clean build demo upload-test py3 intro test-intro

clean:
	rm -rf build dist django_openapi.egg-info

build:
	python setup.py sdist bdist_wheel

demo:
	django-admin runserver --pythonpath=. --settings=demo.app

intro:
	django-admin runserver --pythonpath=. --settings=demo.intro

py3:
	django-admin runserver --pythonpath=. --settings=demo.py3

test-intro:
	django-admin test --pythonpath=. --settings=demo.intro tests.test_intro

upload-prod:
	twine upload -u __token__ dist/*

upload-test:
	twine upload -u __token__ --repository testpypi dist/*
