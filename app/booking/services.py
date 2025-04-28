"""Services module for managing bookings."""

from datetime import date
from uuid import uuid4

from booking.model import Booking
from booking.repository import AbstractRepository


def check_availability(dates: list[str], repo: AbstractRepository) -> dict[str, bool]:
    """Check availability of dates.

    Args:
        dates (list[str]): A list of dates to check availability for. Expected format is YYYY-MM-DD.
        repo (AbstractRepository): A repository instance to check against.

    Returns:
        dict[str, bool]: A dictionary with dates as keys and availability as values.
            True if available, False if booked.

    Example:
        >>> check_availability(["2023-10-01", "2023-10-02"], repo)
        {'2023-10-01': False, '2023-10-02': True}
    """
    availabilities = {}

    try:
        input_dates = [date.fromisoformat(str(d)) for d in dates]
    except ValueError as e:
        raise ValueError(
            f"Invalid date format. Expected format is (YYYY-MM-DD): {e}"
        ) from e

    booked_dates = repo.get_booked_dates()

    for date_ in input_dates:
        availabilities[date_.isoformat()] = date_ not in booked_dates

    return availabilities


def create_booking(
    dates: list[str], customer_name: str, repo: AbstractRepository
) -> str:
    """Create a new booking for the specified dates and customer.

    Args:
        dates (list[str]): List of dates to book in ISO format (YYYY-MM-DD).
        customer_name (str): Name of the customer making the booking.
        repo (AbstractRepository): Repository to store the booking.

    Returns:
        str: The ID of the newly created booking.
    """
    booking_id = str(uuid4())

    booking = Booking(booking_id, dates, customer_name)
    repo.add(booking)

    return booking_id
