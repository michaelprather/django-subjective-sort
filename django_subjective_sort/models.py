import math
from typing import List

from django.db import models


class Sortable(models.Model):
    """
    Makes objects manually sortable
    """
    position = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True

    @staticmethod
    def sort_by_position(sortables: List['Sortable']) -> None:
        """
        Sorts a list of sortables by position
        """
        sortables.sort(key=lambda s: s.position or math.inf)

    def reposition(self,
                   peers: List['Sortable'],
                   position: int = None) -> List['Sortable']:
        """
        Updates manual list sorting based on a one-indexed position.
        Returns a filtered list of peers that were changed.
        """
        max_position = len(peers) + 1
        if position and position < 1:
            raise ValueError(
                'Position must be at least one.'
            )

        if position and position > max_position:
            position = max_position

        self.position = position
        self.sort_by_position(peers)

        affected_peers = []
        for index, sortable in enumerate(peers):
            index_position = index + 1

            if not position:
                if not sortable.position:
                    continue
                # if this one has a position, retain it
                sortable.position = index_position

            elif not sortable.position:
                if position <= index_position:
                    continue
                # if the position is gt than the indexed position,
                # we have to declare this one's position
                sortable.position = index_position

            elif index_position < position:
                sortable.position = index_position

            else:
                sortable.position = index_position + 1

            affected_peers.append(sortable)

        return affected_peers
