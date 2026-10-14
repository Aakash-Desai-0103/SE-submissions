
"""Warehouse asset maintenance registry.

Register warehouse equipment, track service dates, identify overdue
inspections, and export maintenance records to JSON.
"""

import json
import tempfile
from datetime import datetime, timedelta

# Global state
assets = {}
CONFIG = {"service_interval_days": 90}


def register_asset(asset_id, machine_type, logs=None):
    """Register a warehouse asset."""
    if logs is None:
        logs = []

    if not asset_id or not asset_id.strip():
        print("Could not register an asset with an empty ID")
        return

    if asset_id in assets:
        print("Asset already registered:", asset_id)
        return

    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime("%Y-%m-%d"),
    }
    logs.append(asset_id)
    print(
        "Registered", asset_id,
        "- total registrations this run:", len(logs)
    )


def update_service_date(asset_id, service_date):
    """Update an asset's last service date after validating the input."""
    if asset_id not in assets:
        print("Could not update", asset_id)
        return

    try:
        parsed_date = datetime.strptime(service_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        print("Invalid service date:", service_date)
        return

    if parsed_date.date() > datetime.now().date():
        print("Service date cannot be in the future:", service_date)
        return

    assets[asset_id]["last_service"] = parsed_date.strftime("%Y-%m-%d")


def due_for_inspection():
    """Return asset IDs whose last service exceeds the inspection interval."""
    due = []
    current_date = datetime.now()
    interval = CONFIG["service_interval_days"]

    for asset_id, asset in assets.items():
        last_service = datetime.strptime(
            asset["last_service"], "%Y-%m-%d"
        )
        if current_date - last_service > timedelta(days=interval):
            due.append(asset_id)

    return due


def change_interval(days):
    """Set the inspection interval to a positive number of days."""
    if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
        raise ValueError("Inspection interval must be a positive integer")

    CONFIG["service_interval_days"] = days


def export_service_report(file="maintenance.json"):
    """Export asset records to a JSON report."""
    with open(file, "w", encoding="utf-8") as report_file:
        json.dump(assets, report_file, indent=2)

    print("Report written to " + file)


def write_scratch_copy():
    """Write asset data to a securely created temporary JSON file."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    ) as scratch_file:
        json.dump(assets, scratch_file, indent=2)
        path = scratch_file.name

    print("Scratch copy at", path)


def print_alerts():
    """Print an alert for each asset overdue for inspection."""
    for asset_id in due_for_inspection():
        print(
            "ALERT: inspection overdue for",
            asset_id,
            assets[asset_id]["type"],
        )


def main():
    """Run the warehouse asset maintenance registry."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")

    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")

    change_interval(90)

    service_date = input(
        "Last service date for CV-07 (YYYY-MM-DD, Enter to skip): "
    )
    if service_date:
        update_service_date("CV-07", service_date)

    if not assets:
        raise ValueError("No assets registered")

    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
