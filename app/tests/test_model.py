"""Tests for the Booking model."""

from datetime import date

import pytest

from booking.model import Booking, InvalidBookingDates


@pytest.mark.parametrize(
    "test_dates",
    [
        ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05"],
        ["2023-10-01", "2023-10-02", "2023-10-03"],
        ["2023-10-01"],
        ["2023-02-28", "2023-03-01"],
        ["2022-12-30", "2022-12-31", "2023-01-01", "2023-01-02"],
    ],
)
def test_booking_accept_valid_dates(test_dates: list[str]) -> None:
    """Test that a Booking object can be created with valid dates."""
    expected_dates = [date.fromisoformat(str(d)) for d in test_dates]

    assert Booking("123", test_dates, "").dates == expected_dates


@pytest.mark.parametrize(
    "test_dates",
    [
        # Non-consecutive dates:
        ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-06"],
        ["2023-10-01", "2023-10-03"],
        # Non-unique dates:
        ["2023-10-01", "2023-10-02", "2023-10-02"],
        # Non ISO 8601/invalid format:
        ["2023/10/01", "2023/10/02"],
        [1, 2],
        [None, None],
        # Invalid dates:
        ["2023-02-29", "2023-13-01"],
        # Invalid length:
        [
            "2023-10-01",
            "2023-10-02",
            "2023-10-03",
            "2023-10-04",
            "2023-10-05",
            "2023-10-06",
        ],
        [],
    ],
)
def test_booking_fails_with_invalid_dates(test_dates: list[str]) -> None:
    """Test that a Booking object cannot be created with invalid dates."""
    with pytest.raises(InvalidBookingDates):
        Booking("123", test_dates, "")


def test_booking_dates_returns_dates_in_iso_format() -> None:
    """Test that the dates can be returned in ISO 8601 format."""
    booking = Booking("123", ["2023-10-24", "2023-10-25"], "")
    expected = ["2023-10-24", "2023-10-25"]

    assert booking.dates_iso == expected


def test_booking_representation() -> None:
    """Test that the Booking object can be represented as a string."""
    booking = Booking("123", ["2023-10-24", "2023-10-25"], "Paul")
    expected = (
        "Booking(id_=123, dates=['2023-10-24', '2023-10-25'], customer_name=Paul)"
    )

    assert str(booking) == expected


@pytest.mark.parametrize(
    "test_bookings, expected",
    [
        (
            (
                Booking("123", ["2025-01-01"], "John"),
                Booking("123", ["2025-01-01"], "John"),
            ),
            True,
        ),
        (
            (Booking("123", ["2025-01-01"], ""), Booking("124", ["2025-01-01"], "")),
            False,
        ),
        (
            (Booking("123", ["2025-01-01"], ""), Booking("123", ["2025-01-02"], "")),
            False,
        ),
        ((Booking("123", ["2025-01-01"], ""), 123), False),
        (
            (
                Booking("123", ["2025-01-01"], "Mark"),
                Booking("123", ["2025-01-01"], "Paul"),
            ),
            False,
        ),
    ],
)
def test_booking_equality(test_bookings: tuple[Booking], expected: bool) -> None:
    """Test that two Booking objects can be compared for equality."""
    assert (test_bookings[0] == test_bookings[1]) == expected
