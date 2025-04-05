"""Tests for the services module."""

from datetime import date

import pyodbc
import pytest

from booking.repository import SqlRepository
from booking.model import Booking
from booking.services import check_availability, create_booking
from tests.shared import FakeRepository


@pytest.mark.parametrize(
    "test_dates, expected",
    [
        (
            [date(2023, 10, 1), date(2023, 10, 2)],
            {"2023-10-01": False, "2023-10-02": False},
        ),
        ([date(2023, 10, 3)], {"2023-10-03": True}),
        (
            [date(2023, 10, 2), date(2023, 10, 3)],
            {"2023-10-02": False, "2023-10-03": True},
        ),
        ([], {}),
    ],
)
def test_check_availability_returns_correct_availability(
    test_dates: list[str], expected: dict[str, bool]
):
    """Test that check_availability returns correct availability."""
    bookings = [
        Booking("123", ["2023-10-01", "2023-10-02"], ""),
    ]
    repo = FakeRepository(bookings)

    test_availability = check_availability(test_dates, repo)

    assert test_availability == expected


@pytest.mark.parametrize(
    "test_dates",
    [["12/10/2023"], ["2023-10-01", "2023-13-02"], ["invalid_date"], [None]],
)
def test_check_availability_raises_exception_on_invalid_date_format(
    test_dates: list[str],
):
    """Test that check_availability raises a Value Error exception on invalid date format."""
    repo = FakeRepository()

    with pytest.raises(ValueError):
        check_availability(test_dates, repo)


@pytest.mark.usefixtures("clear_db")
def test_booking_is_created_correctly(db_session):
    """Test that a booking is created correctly."""
    repo = SqlRepository(db_session)

    test_dates = ["2025-10-01", "2025-10-02"]
    test_customer_name = "John Dory"

    test_booking_id = create_booking(test_dates, test_customer_name, repo)

    test_booking = repo.get(test_booking_id)

    assert (
        test_booking.id_ == test_booking_id
        and test_booking.dates_iso == test_dates
        and test_booking.customer_name == test_customer_name
    )


@pytest.mark.usefixtures("clear_db")
def test_booking_cannot_be_created_with_existing_dates(db_session):
    """Test that a booking can't be created if the dates already exist."""
    repo = SqlRepository(db_session)

    test_dates = ["2025-10-01", "2025-10-02"]
    test_customer_name = "John Dory"

    _ = create_booking(test_dates, test_customer_name, repo)

    with pytest.raises(pyodbc.IntegrityError):
        _ = create_booking(test_dates, test_customer_name, repo)
