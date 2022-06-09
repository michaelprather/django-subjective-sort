from typing import List

import pytest as pytest
from django.db import models

from src.django_subjective_sort.models import Sortable


class SortableWithDescription(Sortable):
    description = models.CharField(max_length=255)

    class Meta:
        app_label = 'tests'

    def __str__(self):
        return f'{self.description}: position {self.position}'


@pytest.fixture()
def sortables() -> List[SortableWithDescription]:
    return [
        SortableWithDescription(description='Sortable A'),
        SortableWithDescription(description='Sortable B'),
        SortableWithDescription(description='Sortable C'),
        SortableWithDescription(description='Sortable D')
    ]


def test_sorts_by_position(sortables):
    """An sortable can be made more prominent"""
    sortables[2].position = 1
    sortables[1].position = 2
    SortableWithDescription.sort_by_position(sortables)
    assert sortables[0].description == 'Sortable C'
    assert sortables[1].description == 'Sortable B'
    assert sortables[2].description == 'Sortable A'
    assert sortables[3].description == 'Sortable D'


def test_sortable_can_be_promoted(sortables):
    """A sortable can be promoted"""
    promoted_sortable = sortables[2]
    sortables.pop(2)
    promoted_sortable.reposition(sortables, 1)
    assert promoted_sortable.position == 1
    assert promoted_sortable.description == 'Sortable C'


def test_sortable_can_be_demoted(sortables):
    """A sortable can be demoted"""
    sortables[2].position = 1
    sortables[1].position = 2

    demoted_sortable = sortables[2]
    sortables.pop(2)
    demoted_sortable.reposition(sortables, 2)
    assert demoted_sortable.position == 2
    assert demoted_sortable.description == 'Sortable C'


def test_promote_among_nullish_peers(sortables):
    """A sortable can be promoted among nullish peers"""
    for sortable in sortables:
        assert sortable.position is None

    promoted_sortable = sortables[1]
    sortables.pop(1)
    promoted_sortable.reposition(sortables, 1)

    assert promoted_sortable.position == 1
    assert promoted_sortable.description == 'Sortable B'
    assert sortables[0].position is None
    assert sortables[1].position is None
    assert sortables[2].position is None


def test_demote_among_nullish_peers(sortables):
    """A sortable can be demoted among nullish peers"""
    for sortable in sortables:
        assert sortable.position is None

    demoted_sortable = sortables[1]
    sortables.pop(1)
    demoted_sortable.reposition(sortables, 2)

    assert demoted_sortable.position == 2
    assert demoted_sortable.description == 'Sortable B'
    assert sortables[0].position == 1
    assert sortables[1].position is None
    assert sortables[2].position is None


def test_reorders_list_after_promotion(sortables):
    """Sortables are re-sorted when one is promoted"""
    sortables[3].position = 1
    sortables[2].position = 2
    sortables[0].position = 3

    promoted_sortable = sortables[0]
    sortables.pop(0)
    peers_affected = promoted_sortable.reposition(sortables, 2)

    assert len(peers_affected) == 2
    assert promoted_sortable.position == 2
    assert promoted_sortable.description == 'Sortable A'
    assert sortables[0].description == 'Sortable D'
    assert sortables[1].description == 'Sortable C'
    assert sortables[2].description == 'Sortable B'


def test_reorders_list_after_demotion(sortables):
    """Sortables are re-sorted when one is demoted"""
    sortables[3].position = 1  # D
    sortables[1].position = 2  # B
    sortables[2].position = 3  # C

    demoted_sortable = sortables[3]
    sortables.pop(3)
    peers_affected = demoted_sortable.reposition(sortables, 2)

    assert len(peers_affected) == 2
    assert demoted_sortable.position == 2
    assert demoted_sortable.description == 'Sortable D'
    assert sortables[0].description == 'Sortable B'
    assert sortables[1].description == 'Sortable C'
    assert sortables[2].description == 'Sortable A'


def test_position_must_be_at_least_one(sortables):
    """A sortable's position must be at least one"""
    repositioned_sortable = sortables[2]
    sortables.pop(2)

    with pytest.raises(ValueError):
        repositioned_sortable.reposition(sortables, -1)


def test_position_cannot_exceed_list_length(sortables):
    """A sortable's position cannot exceed the length of the list"""
    sortables[3].position = 1
    sortables[1].position = 2

    repositioned_sortable = sortables[2]
    sortables.pop(2)

    repositioned_sortable.reposition(sortables, 8)
    assert repositioned_sortable.position == 4


def test_can_clear_position(sortables):
    """A sortable's position can be cleared"""
    sortables[3].position = 1
    sortables[2].position = 2
    sortables[1].position = 3

    repositioned_sortable = sortables[2]
    sortables.pop(2)
    repositioned_sortable.reposition(sortables)

    assert repositioned_sortable.position is None
    assert sortables[0].description == 'Sortable D'
    assert sortables[1].description == 'Sortable B'
    assert sortables[2].description == 'Sortable A'
