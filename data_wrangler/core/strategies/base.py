from abc import ABC, abstractmethod

class ColumnNormalizer(ABC):
    """
    Abstract base class for column-specific normalizers.
    """

    @abstractmethod
    def normalize(self, value):
        """
        Normalize the given value.

        Args:
            value: The value to normalize.

        Returns:
            The normalized value.
        """
        pass