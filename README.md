# Django Subjective Sort

## Installation

```shell
    $ pip install django-subjective-sort
```

## Usage

1. Extend the `Sortable` class to add custom sorting logic to any Django model.

```python
# food/models.py
from typing import List

from django.db import models

from src.django_subjective_sort.models import Sortable


class Food(Sortable):
    name = models.CharField(max_length=255)

    # Extend the `Sortable` class to save sorting order.
    # This allows flexibility to save other changes simultaneously.
    def reposition(self,
                   peers: List['Food'],
                   position: int = None) -> List['Food']:
        sortables_affected = super().reposition(peers, position) + [self]
        # Save the changes
        return Food.objects.bulk_update(sortables_affected, ['position'])
```

2. Apply migrations.

```shell
    $ python manage.py makemigrations
    $ python manage.py migrate
```
