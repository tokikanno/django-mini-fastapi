import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="django-mini-fastapi",
    version="0.1",
    author="toki kanno",
    author_email="toki.kanno@gmail.com",
    description="A minimal FastAPI implementation for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tokikanno/django_mini_fastapi",
    packages=setuptools.find_packages(
        ".",
        include=(
            "django_mini_fastapi",
            "django_mini_fastapi.*",
        ),
    ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    setup_requires=["wheel"],
    install_requires=["django", "pydantic"],
)
