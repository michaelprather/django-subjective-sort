from typing import List
from unittest import TestCase

from django.db import models

from django_subjective_sort.models import Sortable


class SortableWithDescription(Sortable):
    description = models.CharField(max_length=255)

    class Meta:
        app_label = 'tests'

    def __str__(self):
        return f'{self.description}: position {self.position}'


class TestSorting(TestCase):
    def setUp(self):
        self.sortable1 = SortableWithDescription(
            description='Sortable A',
        )
        self.sortable2 = SortableWithDescription(
            description='Sortable B',
        )
        self.sortable3 = SortableWithDescription(
            description='Sortable C',
        )
        self.sortable4 = SortableWithDescription(
            description='Sortable D',
        )

        self.list = [
            self.sortable1,
            self.sortable2,
            self.sortable3,
            self.sortable4,
        ]

    def collection_without(self,
                           index: int) -> List['SortableWithDescription']:
        collection = self.list.copy()
        collection.pop(index)
        return collection

    def test_sorts_by_position(self):
        """
        An item can be made more prominent
        """
        self.sortable3.position = 1
        self.sortable2.position = 2
        SortableWithDescription.sort_by_position(self.list)
        self.assertListEqual(self.list, [
            self.sortable3,
            self.sortable2,
            self.sortable1,
            self.sortable4,
        ])

    def test_sortable_can_be_promoted(self):
        """
        An item can be made more prominent
        """
        peers = self.collection_without(2)
        self.sortable3.reposition(peers, 1)
        self.assertEqual(self.sortable3.position, 1)

    def test_sortable_can_be_demoted(self):
        """
        An item can be made more prominent
        """
        self.sortable3.position = 1
        self.sortable2.position = 2

        peers = self.collection_without(2)
        self.sortable3.reposition(peers, 2)
        self.assertEqual(self.sortable3.position, 2)

    def test_promote_among_nullish_peers(self):
        """An item can be promoted among nullish peers"""
        self.assertIsNone(self.sortable1.position)
        self.assertIsNone(self.sortable2.position)
        self.assertIsNone(self.sortable3.position)
        self.assertIsNone(self.sortable4.position)

        peers = self.collection_without(1)
        self.sortable2.reposition(peers, 1)

        self.assertEqual(self.sortable2.position, 1)
        self.assertIsNone(self.sortable1.position)
        self.assertIsNone(self.sortable3.position)
        self.assertIsNone(self.sortable4.position)

    def test_demote_among_nullish_peers(self):
        """An item can be demoted among nullish peers"""
        peers = self.collection_without(1)
        self.sortable2.reposition(peers, 2)
        self.assertEqual(self.sortable2.position, 2)

    def test_reorders_list_after_promotion(self):
        """
        Other items are correctly automatically
        re-sorted when one is promoted
        """
        self.sortable4.position = 1
        self.sortable3.position = 2
        self.sortable1.position = 3

        peers = self.collection_without(0)
        peers_affected = self.sortable1.reposition(peers, 2)
        self.assertEqual(len(peers_affected), 2)

        self.assertEqual(self.sortable4.position, 1)
        self.assertEqual(self.sortable1.position, 2)
        self.assertEqual(self.sortable3.position, 3)
        self.assertEqual(self.sortable2.position, None)

    def test_reorders_list_after_demotion(self):
        """
        Other items are correctly automatically
        re-sorted when one is demoted
        """
        self.sortable4.position = 1
        self.sortable2.position = 2
        self.sortable3.position = 3

        peers = self.collection_without(3)
        peers_affected = self.sortable4.reposition(peers, 2)
        self.assertEqual(len(peers_affected), 2)

        self.assertEqual(self.sortable2.position, 1)
        self.assertEqual(self.sortable4.position, 2)
        self.assertEqual(self.sortable3.position, 3)
        self.assertEqual(self.sortable1.position, None)

    def test_position_must_be_at_least_one(self):
        """
        The Sortable's position must be at least one
        """
        peers = self.collection_without(2)
        with self.assertRaises(ValueError):
            self.sortable3.reposition(peers, -1)

    def test_position_cannot_exceed_list_length(self):
        """
        The Sortable's position cannot exceed
        the total number of sortables with a defined position
        """
        self.sortable4.position = 1
        self.sortable2.position = 2

        peers = self.collection_without(2)
        self.sortable3.reposition(peers, 8)
        self.assertEqual(self.sortable3.position, 4)

    def test_can_clear_position(self):
        """
        A Sortable's position can be cleared
        """
        self.sortable4.position = 1
        self.sortable3.position = 2
        self.sortable2.position = 3

        peers = self.collection_without(2)
        self.sortable3.reposition(peers)

        self.assertEqual(self.sortable4.position, 1)
        self.assertEqual(self.sortable2.position, 2)
        self.assertIsNone(self.sortable1.position)
        self.assertIsNone(self.sortable3.position)
