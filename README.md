# Caution!!!
This project is mainly used on my internal projects and in `early developing stage`. So use it at you own risk.

Bug reports / Fix PRs are welcomed.


# Installation

```sh
pip install django-mini-fastapi
```

# Live demo provided by Gitpod

Click the button below and launch a free live demo server via Gitpod

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/tokikanno/django-mini-fastapi)

If the button doesn't show up, you clould also use below link directly

[https://gitpod.io/#https://github.com/tokikanno/django-mini-fastapi](https://gitpod.io/#https://github.com/tokikanno/django-mini-fastapi)

After Gitpod launched, wait a while for the auto execution of `make intro` command
Then you could using VScode remote explorer for opening the intro demo server in your browser.

![image](https://raw.githubusercontent.com/tokikanno/django-mini-fastapi/master/docs/images/gitpod-remote-explorer.png) 



# What is `django-mini-fastapi` ?
A minimal FastAPI implementation for Django !

This project reused more than 95% codes from [FastAPI](https://fastapi.tiangolo.com/). I just did minimal necessary modifications for making it working under Django.

So basicly you can read documents from FastAPI for knowing how to use this module. (Except features metioned in `Features currently not work` section)
The difference between django-mini-fastapi and FastAPI is how you import and mount it.


```python
# This is how you declear OpenAPI endpoint in FastAPI
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

Above is the quick start sample in FastAPI document, which should be re-written like below


```python
# This is how you do the same thing in django-mini-fastapi
from typing import Optional
from django_mini_fastapi import OpenAPI

app = OpenAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

And you should mount the API endpoint via Django url pattern mechanism by calling `app.as_django_url_pattern()`

```python
urlpatterns = [
    # use as_django_url_pattern() for mounting API endpoint into Django url parser
    app.as_django_url_pattern(),
]
```

And usually you won't want to mount API endpoint in `/` for a Django project. You could pass the `root_path` parameter to OpenAPI init function for changing the mount point.

```python
app = OpenAPI(root_path='/api')
```

For fully working example script, please see [demo/intro.py](https://github.com/tokikanno/django-mini-fastapi/blob/master/demo/intro.py)

You can also type

```sh
make intro
```

for starting test intro server.


# Why do you make this? Can't you just use FastAPI directly?
I'm a big fan of FastAPI. It's elegant and saves lots of doc maintaince & API spec communication costs for me.

But I'm maintaing huge legacy projects built by Django framework. It will take massive resources for porting it onto FastAPI.

So I decided to modifiy FastAPI for making it working under Django, then I could instantly get the benefits from FastAPI without  doing migrations for my legacy projects.

# Who should use this?
People who like the way FastAPI works but don't want to do full system rewrite from Django to FastAPI

# Features currently work
* Auto OpenAPI schema/document generation from Python function declaration
* Auto request parameter validation
* Dependencies system

# Features currently not work
* Auto OpenAPI parameters parsing & processing
  * Callback function delcearation (WIP)
  * Security scopes (Evaluating/Planning)
* WebSocket endpoints (Not in priority)
* Backgournd tasks (Not in priority)
