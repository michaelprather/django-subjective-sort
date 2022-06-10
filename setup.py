import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-subjective-sort",
    version="1.0.0",
    author="Michael Prather",
    author_email="michael@krit.com",
    description="Allows items of a collection to be manually sorted"
                "(such as for use with drag-and-drop).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/builtbykrit/django-subjective-sort",
    project_urls={
        "Bug Tracker": "https://github.com/builtbykrit/django-subjective-sort/issues",  # noqa: E501
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django :: 4.1"
        "Framework :: Django :: 4.0"
        "Framework :: Django :: 3.2"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
