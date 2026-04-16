"""Standard randomness provider backed by ``random.Random``."""

import random
from collections.abc import Sequence

from tg_devices.random.protocols import IRandomProvider, T


class StandardRandomProvider(IRandomProvider):
    """Weighted random selection using Python's ``random.Random``.

    Args:
        seed: Optional seed for reproducible results.

    """

    def __init__(self, seed: str | int | None = None) -> None:
        """Initialize the StandardRandomProvider with an optional seed.

        Args:
            seed: A string, integer, or None to seed the random generator.
                If None, the generator is initialized with system time or
                entropy source for non-deterministic behavior.

        """
        self._random = random.Random(seed)

    def choice(
        self,
        population: Sequence[T],
        weights: Sequence[int | float] | None = None,
    ) -> T:
        """Select a single element from *population*.

        Args:
            population: Non-empty sequence to choose from.
            weights: Optional relative weights for each element.

        Returns:
            A single selected element.

        Raises:
            ValueError: If *population* is empty.

        """
        chosen = self.choices(population=population, weights=weights, k=1)
        return chosen[0]

    def choices(
        self,
        population: Sequence[T],
        weights: Sequence[int | float] | None = None,
        k: int = 1,
    ) -> list[T]:
        """Select *k* elements from *population* with replacement.

        Args:
            population: Non-empty sequence to choose from.
            weights: Optional relative weights for each element.
            k: Number of elements to select.

        Returns:
            List of *k* selected elements.

        Raises:
            ValueError: If *population* is empty.

        """
        if not population:
            raise ValueError("Population is empty")
        return self._random.choices(
            population=population, weights=weights, k=k
        )
