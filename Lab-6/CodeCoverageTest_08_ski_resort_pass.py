import pytest

from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


# Tests focused on line/code coverage: execute application statements across
# the normal and exceptional scenarios without specifically organizing tests
# around every True/False branch.


def test_invalid_groups_input():
    with pytest.raises(ValueError):
        process_resort_bookings("invalid", 15.0)


def test_negative_facility_fee():
    with pytest.raises(ValueError):
        process_resort_bookings([], -1.0)


def test_inactive_group_returns_zero_sales():
    result = process_resort_bookings(
        [{"is_active": False, "duration": "full_day",
          "skiers": [{"age": 30}]}],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_season_pass_pricing_and_gear_rental():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "season",
            "skiers": [
                {"age": 10, "gear_rental": True},
                {"age": 70},
                {"age": 30},
            ],
        }],
        15.0,
    )
    assert result == {"total_revenue": 725.0, "status": "COMPLETED"}


def test_half_day_pass_pricing():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "half_day",
            "skiers": [{"age": 30}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 50.0, "status": "COMPLETED"}


def test_unknown_duration():
    result = process_resort_bookings(
        [{"is_active": True, "duration": "weekend",
          "skiers": [{"age": 30}]}],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_invalid_ages():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "full_day",
            "skiers": [{"age": 0}, {"age": -5}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_blackout_override_on_full_day_pass():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "full_day",
            "skiers": [{"age": 30, "blackout_override": True}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 40.0, "status": "COMPLETED"}


def test_blackout_override_on_half_day_pass():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "half_day",
            "skiers": [{"age": 30, "blackout_override": True}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_lodge_locker_fee_is_added():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "full_day",
            "includes_lodge_locker": True,
            "skiers": [{"age": 30}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 95.0, "status": "COMPLETED"}


def test_audit_review_after_many_rejections():
    result = process_resort_bookings(
        [
            {"is_active": True, "duration": "unknown", "skiers": []}
            for _ in range(5)
        ],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "AUDIT_REVIEW"}


def test_empty_wind_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_safe_wind_data():
    assert check_chairlift_anemometer([[20, 35, 45, 30]]) == "SAFE_OPERATION"


def test_high_gusts_separated_by_safe_reading():
    assert check_chairlift_anemometer([[46, 30, 47]]) == "SAFE_OPERATION"


def test_two_consecutive_high_gusts():
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"


def test_wind_gust_streak_resets():
    assert check_chairlift_anemometer([[46, 30, 46]]) == "SAFE_OPERATION"


def test_wind_gusts_across_lifts():
    assert check_chairlift_anemometer([[46], [47, 48]]) == "SUSPEND_LIFT"
