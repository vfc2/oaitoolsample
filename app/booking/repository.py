"""Repository module for managing bookings."""

from datetime import date
from typing import Protocol

import pyodbc

from booking.model import Booking


class AbstractRepository(Protocol):
    """Repository interface for bookings."""

    def get(self, id_: str) -> Booking | None:
        """Get a booking by ID."""

    def get_booked_dates(self) -> list[date]:
        """Get all bookings."""

    def add(self, booking: Booking) -> None:
        """Add a new booking."""


class SqlRepository:
    """SQL repository for bookings."""

    def __init__(self, connection: pyodbc.Connection) -> None:
        self.connection = connection

    def get(self, id_: str) -> Booking | None:
        """Get a booking by ID.

        Args:
            id_ (str): The ID of the booking to retrieve.

        Returns:
            Booking | None: The retrived booking object or None if not found.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, customer_name FROM dbo.booking WHERE id = ?", id_
            )
            row = cursor.fetchone()
            if not row:
                return None

            cursor.execute(
                "SELECT [date] FROM dbo.booking_dates WHERE booking_id = ?", id_
            )
            rows = cursor.fetchall()
            dates = [r.date for r in rows]

            return Booking(row.id, dates, row.customer_name)

    def get_booked_dates(self) -> list[date]:
        """Get all booked dates.

        Returns:
            list[date]: A list of booked dates.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT [date] FROM dbo.booking_dates")
            rows = cursor.fetchall()
            dates = [r.date for r in rows]

        return sorted(dates)

    def add(self, booking: Booking) -> None:
        """Add a new booking.

        Args:
            booking (Booking): A booking object to add.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO dbo.booking (id, customer_name) VALUES (?, ?)",
                booking.id_,
                booking.customer_name,
            )
            cursor.executemany(
                "INSERT INTO dbo.booking_dates (booking_id, [date]) VALUES (?, ?)",
                [(booking.id_, str(date)) for date in booking.dates],
            )
