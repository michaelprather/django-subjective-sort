import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-subject-sort",
    version="0.2.0",
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
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
