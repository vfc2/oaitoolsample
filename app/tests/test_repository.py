"""Tests for the repository module."""

import pytest

from booking.model import Booking
from booking.repository import AbstractRepository, SqlRepository


def create_test_bookings(repo: AbstractRepository) -> list[Booking]:
    """Create test bookings."""
    bookings = [
        Booking("123", ["2023-10-01", "2023-10-02"], ""),
        Booking("456", ["2023-10-03", "2023-10-04"], ""),
        Booking("789", ["2023-10-05", "2023-10-06"], ""),
    ]
    for booking in bookings:
        repo.add(booking)

    return bookings


@pytest.mark.usefixtures("clear_db")
def test_repository_can_retrieve_specific_booking(db_session) -> None:
    """Test that the repository can retrieve bookings."""
    repo = SqlRepository(db_session)

    create_test_bookings(repo)

    expected_booking = Booking("123", ["2023-10-01", "2023-10-02"], "")
    retrieved_booking = repo.get("123")

    assert retrieved_booking == expected_booking


@pytest.mark.usefixtures("clear_db")
def test_repository_returns_none_when_no_booking_is_found(db_session) -> None:
    """Test that the repository returns None when no booking is found."""
    repo = SqlRepository(db_session)

    test_booking = repo.get("999999")

    assert test_booking is None


@pytest.mark.usefixtures("clear_db")
def test_repository_can_create_bookings(db_session) -> None:
    """Test that the repository can create bookings."""
    repo = SqlRepository(db_session)

    expected_bookings = [
        Booking("123", ["2024-11-02", "2024-11-03"], "John Dory"),
        Booking("456", ["2023-10-03", "2023-10-04"], "Peter"),
        Booking("789", ["2023-10-05", "2023-10-06"], "Matthew"),
        Booking("451", ["2023-02-20", "2023-02-21"], "Mark"),
    ]

    for booking in expected_bookings:
        repo.add(booking)

    actual_bookings = [repo.get(b.id_) for b in expected_bookings]

    assert actual_bookings == expected_bookings


@pytest.mark.usefixtures("clear_db")
def test_repository_can_retrieve_all_booked_dates(db_session) -> None:
    """Test that the repository can retrieve all booked dates."""
    repo = SqlRepository(db_session)

    bookings = create_test_bookings(repo)
    expected_dates = [b for booking in bookings for b in booking.dates]

    test_dates = repo.get_booked_dates()

    assert test_dates == sorted(expected_dates)
