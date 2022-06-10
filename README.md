# Django Subjective Sort

![PyPI - License](https://img.shields.io/pypi/l/django-subjective-sort)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/builtbykrit/django-subjective-sort/Publish)
![PyPI](https://img.shields.io/pypi/v/django-subjective-sort)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-subjective-sort)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-subjective-sort)
![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-subjective-sort)

This library enables subjective sorting of a list of objects. Imagine you are building a task management app, and 
the UI allows a user to manually sort his or her daily tasks via drag-and-drop. Django Subjective Sort makes it easy to 
handle re-positioning, both of the task that moved but also the other tasks that were affected by the move.

## How it works

An abstract Django model class establishes an integer field named `position` for storing the position of an object in a 
list. Objects have no position by default (e.g. `position = None`). Positioning is one-indexed with the object assigned 
the `1` position having the highest prominence and objects without a position the lowest prominence. Objects cannot have
a position less than one, and cannot have a position greater than the number of objects in the list. If an object is 
assigned a position greater than the number of objects with an assigned position, list objects without a position will
inherit one until the desired list position is reached.

**Important: Never modify the value of the `position` field directly. Only manage object positioning using the
`reposition` method.**

By design, Django Subjective Sort cannot influence list membership. It's only responsibility is managing the positioning
of objects in the list it is provided. Since only a single position value is stored, each object can belong to only one
subjectively sortable list. Using the task management example above, a task could be manually sorted among peers 
assigned to the same day, but not also among peers assigned to the same week or month.

Both for flexibility and because the Sortable model class is abstract, positioning changes are not automatically saved. 
The example below demonstrates how to extend the `reposition` method to save positioning changes for all objects 
affected by re-positioning in a single transaction.

The Sortable model class contains two methods: `reposition` and `sort_by_position`. The `reposition` method updates the
position of the object it is called on, as well as any of its list peers affected by the change. The `sort_by_position`
method is a convenience method for sorting a list of objects by their position. 

## Installation

```shell
    $ pip install django-subjective-sort
```

## Usage

1. Extend the `Sortable` class to add custom sorting logic to any Django model.

```python
# food/models.py
from django_subjective_sort.models import Sortable


class Food(Sortable):
    pass

```

2. Apply migrations.

```shell
    $ python manage.py makemigrations
    $ python manage.py migrate
```

3. Extend the `reposition` method to save positioning changes for all objects affected by re-positioning in a single
transaction.

```python
# food/models.py
from typing import List

from src.django_subjective_sort.models import Sortable


class Food(Sortable):
    # Extend the `Sortable` class to save sorting order.
    # This allows flexibility to save other changes simultaneously.
    def reposition(self,
                   peers: List['Food'],
                   position: int = None) -> List['Food']:
        sortables_affected = super().reposition(peers, position) + [self]
        # Save the changes
        return Food.objects.bulk_update(sortables_affected, ['position'])

```
