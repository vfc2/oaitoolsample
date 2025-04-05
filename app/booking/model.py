"""Models"""

from datetime import date


class InvalidBookingDates(ValueError):
    """Custom exception for invalid booking dates."""


class Booking:
    """Booking model"""

    def __init__(self, id_: str, dates: list[str], customer_name: str) -> None:
        """Initialize the Booking model.

        Args:
            dates (list[str]): List of dates to check in ISO 8601 format (YYYY-MM-DD).
        """
        self.id_ = id_
        self._dates = []
        self.dates = self.validate_dates(dates)
        self.customer_name = customer_name

    @property
    def dates_iso(self) -> list[str]:
        """Get the list of dates in ISO 8601 format."""
        return [d.isoformat() for d in self._dates]

    @property
    def dates(self) -> list[date]:
        """Get the list of dates."""
        return self._dates

    @dates.setter
    def dates(self, new_dates: list[date]) -> None:
        """Set the list of dates."""
        self._dates = self.validate_dates(new_dates)

    def validate_dates(self, dates: list[str]) -> list[date]:
        """Ensure that the dates are in valid format, consecutive,
            and within the allowed range (5 days max).

        Args:
            dates (list[str]): A list of dates to validate. The expected format is YYYY-MM-DD.

        Raises:
            InvalidBookingDates: If the dates are invalid, non-consecutive, not unique or
                in invalid format.

        Returns:
            list[date]: A list of validated dates.
        """
        validated_dates = []

        if not dates:
            raise InvalidBookingDates("Dates list cannot be empty.")

        if len(dates) > 5:
            raise InvalidBookingDates("No more than 5 dates can be booked at a time.")

        if len(dates) != len(set(dates)):
            raise InvalidBookingDates("Dates must be unique.")

        try:
            validated_dates = [date.fromisoformat(str(d)) for d in dates]
        except ValueError as e:
            raise InvalidBookingDates(
                f"Invalid date format. Expected format is (YYYY-MM-DD): {e}"
            ) from e

        if len(dates) > 1:
            dates_int = [d.toordinal() for d in validated_dates]
            if max(dates_int) - min(dates_int) != len(dates_int) - 1:
                raise InvalidBookingDates("Dates must be consecutive.")

        return validated_dates

    def __repr__(self) -> str:
        """Return a string representation of the Booking model."""
        return (
            f"Booking(id_={self.id_}, dates={self.dates_iso}, "
            f"customer_name={self.customer_name})"
        )

    def __eq__(self, other: object) -> bool:
        """Check if two Booking models are equal."""
        if not isinstance(other, Booking):
            return False
        return (
            self.id_ == other.id_
            and self.dates == other.dates
            and self.customer_name == other.customer_name
        )

    def __hash__(self) -> int:
        """Return a hash of the Booking model."""
        return hash(self.id_)
