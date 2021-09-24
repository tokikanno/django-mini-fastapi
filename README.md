# django-mini-fastapi
A minimal FastAPI implementation for Django !

This project reused more than 95% codes from [FastAPI](https://fastapi.tiangolo.com/)

I just did minimal necessary modifications for letting it works on Django.

# Why do you make this? Can't you just use FastAPI directly?
I'm a big fan of FastAPI. It's elegant and saves lots of doc maintaince & API spec communication costs for me.

But I'm maintaing huge legacy projects built by Django framework. It will take massive resources for porting it onto FastAPI.

So I decided to modifiy FastAPI for letting it works in Django, that I could instantly get the benefits from FastAPI without  migrations on legacy projects.

# Who should use this?
People who like the way FastAPI works but don't want to do full system rewrite from Django to FastAPI

# Features currently works
* Auto OpenAPI schema/document generation from Python function declaration
* Auto request parameter validation

# Features currently not work / untested / or porting
* Dependencies system (porting)
* Security check (porting)
* Callback function delcearation (porting)
* WebSocket endpoints (not work)
* Backgournd tasks (not work)
