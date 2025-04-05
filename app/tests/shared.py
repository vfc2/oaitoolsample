"""Shared testing utilities."""

from datetime import date

from booking.model import Booking


class FakeRepository:
    """In-memory fake repository for bookings."""

    def __init__(self, data: set[Booking] | None = None) -> None:
        self.data = set(data or [])

    def get(self, id_: str) -> Booking | None:
        """Get a booking by ID."""
        return next((booking for booking in self.data if booking.id_ == id_), None)

    def get_booked_dates(self) -> list[date]:
        """Get all booked dates."""
        return sorted({date_ for booking in self.data for date_ in booking.dates})

    def add(self, booking: Booking) -> None:
        """Add a new booking."""
        self.data.add(booking)
