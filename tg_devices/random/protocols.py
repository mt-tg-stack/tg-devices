"""Protocol definition for randomness providers."""

from collections.abc import Sequence
from typing import Protocol, TypeVar

T = TypeVar("T")


class IRandomProvider(Protocol):
    """Interface for providing randomness during profile generation.

    This protocol allows swapping the randomness source (e.g., for
    deterministic testing or using a different probability library).
    """

    def choice(
        self,
        population: Sequence[T],
        weights: Sequence[int | float] | None = None,
    ) -> T:
        """Select a single element from a population based on weights.

        Args:
            population: A non-empty sequence to choose from.
            weights: An optional sequence of relative weights.

        Returns:
            The single element selected from the population.

        """
        ...

    def choices(
        self,
        population: Sequence[T],
        weights: Sequence[int | float] | None = None,
        k: int = 1,
    ) -> list[T]:
        """Select multiple elements with replacement from a population.

        Args:
            population: A non-empty sequence to choose from.
            weights: An optional sequence of relative weights.
            k: The number of elements to select.

        Returns:
            A list containing the selected elements.

        """
        ...
