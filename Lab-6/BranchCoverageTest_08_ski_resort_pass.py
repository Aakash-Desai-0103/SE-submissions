import pytest

from ski_resort_pass import (
    process_resort_bookings,
    check_chairlift_anemometer,
)


# Branch-coverage tests for process_resort_bookings


def test_invalid_groups_type_takes_error_branch():
    with pytest.raises(ValueError):
        process_resort_bookings("invalid", 15.0)


def test_negative_facility_fee_takes_error_branch():
    with pytest.raises(ValueError):
        process_resort_bookings([], -1.0)


def test_inactive_group_is_skipped():
    result = process_resort_bookings(
        [{
            "is_active": False,
            "duration": "full_day",
            "skiers": [{"age": 30}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_season_pass_child_senior_adult_and_gear_rental():
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


def test_unknown_duration_increments_rejected_passes():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "weekend",
            "skiers": [{"age": 30}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_nonpositive_ages_are_rejected():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "full_day",
            "skiers": [{"age": 0}, {"age": -5}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_full_day_blackout_override_charges_half_rate():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "full_day",
            "skiers": [{"age": 30, "blackout_override": True}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 40.0, "status": "COMPLETED"}


def test_half_day_blackout_override_zeroes_group_total():
    result = process_resort_bookings(
        [{
            "is_active": True,
            "duration": "half_day",
            "skiers": [{"age": 30, "blackout_override": True}],
        }],
        15.0,
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_lodge_locker_adds_facility_fee():
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


def test_more_than_four_rejections_triggers_audit_review():
    result = process_resort_bookings(
        [
            {"is_active": True, "duration": "unknown", "skiers": []}
            for _ in range(5)
        ],
        15.0,
    )
    assert result == {
        "total_revenue": 0.0,
        "status": "AUDIT_REVIEW",
    }


# Branch-coverage tests for check_chairlift_anemometer


def test_empty_wind_streams_return_no_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_wind_at_or_below_threshold_is_safe():
    assert check_chairlift_anemometer([[20, 35, 45, 30]]) == "SAFE_OPERATION"


def test_single_high_gust_does_not_suspend_lift():
    assert check_chairlift_anemometer([[46, 30, 47]]) == "SAFE_OPERATION"


def test_two_consecutive_high_gusts_suspend_lift():
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"


def test_safe_reading_resets_high_gust_streak():
    assert check_chairlift_anemometer([[46, 30, 46]]) == "SAFE_OPERATION"


def test_gust_streak_can_reach_threshold_on_another_lift():
    assert check_chairlift_anemometer([[46], [47, 48]]) == "SUSPEND_LIFT"
