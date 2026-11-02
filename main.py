# Author: Whole group (shared file: main.py)

"""Demo script for the Parking Lot Management System.

This is the only file that imports concrete classes from the five
modules (vehicle, slot, ticket, fees, lot_manager). It wires them
together and tells a short story about one busy morning at the lot,
including several business rules being broken and handled.

Run with:  python main.py
"""

from datetime import timedelta

from contracts import ParkingLotError
from vehicle import Car, Motorcycle, VehicleRegistry
from slot import ParkingSlot
from ticket import Ticket
from fees import StandardFees
from lot_manager import LotManager


def heading(title: str) -> None:
    """Print a section heading."""
    print(f"\n=== {title} ===")


def show_slots(lot: LotManager) -> None:
    """Print every slot (works with any ISlot) and the lot summary."""
    for slot in lot.slots:
        occupant = slot.assigned_vehicle
        suffix = f" -> {occupant}" if occupant is not None else ""
        print(f"  {slot}{suffix}")
    print(f"  {lot}")


def main() -> None:
    """Run the parking lot story."""

    # ------------------------------------------------------------
    # Chapter 1: Build the lot (this is where modules are wired up)
    # ------------------------------------------------------------
    heading("Chapter 1: Opening the lot")

    slots = [
        ParkingSlot(1, "small", 1),
        ParkingSlot(2, "small", 1),
        ParkingSlot(3, "regular", 1),
        ParkingSlot(4, "regular", 2),
    ]
    fees = StandardFees(car_hourly_rate=50.0,
                        motorcycle_hourly_rate=20.0,
                        grace_minutes=15)
    lot = LotManager(slots=slots, fee_calculator=fees, ticket_factory=Ticket)
    registry = VehicleRegistry()

    print(f"Fee schedule: {fees}")
    show_slots(lot)

    # Invalid input is rejected by constructors (ValueError).
    try:
        ParkingSlot(0, "small", 1)
    except ValueError as error:
        print(f"Rejected a bad slot -> {error}")

    # ------------------------------------------------------------
    # Chapter 2: Vehicles arrive and are registered
    # ------------------------------------------------------------
    heading("Chapter 2: Registering vehicles")

    moto_a = Motorcycle("mca-101")   # plates are normalized to upper case
    moto_b = Motorcycle("MCB-202")
    car_1 = Car("CAR-111")
    car_2 = Car("CAR-222")
    car_3 = Car("CAR-333")

    for vehicle in (moto_a, moto_b, car_1, car_2, car_3):
        registry.register(vehicle)
        print(f"  Registered {vehicle}")
    print(f"  Total registered: {len(registry)}")

    # Rule broken: duplicate plate numbers are not allowed.
    try:
        registry.register(Car("car-111"))
    except ParkingLotError as error:
        print(f"Rule broken (handled) -> {error}")

    # ------------------------------------------------------------
    # Chapter 3: Parking
    # ------------------------------------------------------------
    heading("Chapter 3: Morning rush")

    tickets = {}
    for vehicle in (moto_a, moto_b, car_1, car_2):
        ticket = lot.park_vehicle(vehicle)
        tickets[vehicle.vehicle_plate] = ticket
        print(f"  {ticket} in {ticket.slot}")
    show_slots(lot)

    # Rule broken: a vehicle cannot be parked twice.
    try:
        lot.park_vehicle(moto_a)
    except ParkingLotError as error:
        print(f"Rule broken (handled) -> {error}")

    # Rule broken: no suitable slot left for another car.
    try:
        lot.park_vehicle(car_3)
    except ParkingLotError as error:
        print(f"Rule broken (handled) -> {error}")

    print(f"  Active tickets: {lot.active_ticket_count}")

    # ------------------------------------------------------------
    # Chapter 4: Leaving and paying
    # ------------------------------------------------------------
    heading("Chapter 4: Vehicles leave")

    # (plate, time stayed) - exit times are based on each ticket's entry time.
    departures = [
        ("MCA-101", timedelta(minutes=10)),   # within grace -> free
        ("CAR-222", timedelta(minutes=61)),   # 61 min -> 2 hours charged
        ("CAR-111", timedelta(hours=2, minutes=30)),  # 3 hours charged
    ]
    for plate, stay in departures:
        ticket = tickets[plate]
        vehicle = registry.find(plate)
        fee = lot.release_vehicle(ticket.ticket_number,
                                  ticket.entry_time + stay)
        print(f"  {vehicle} stayed {stay} and paid P{fee:.2f}")

    # Rule broken: a ticket that was already released cannot be reused.
    used = tickets["CAR-111"]
    try:
        lot.release_vehicle(used.ticket_number,
                            used.entry_time + timedelta(hours=3))
    except ParkingLotError as error:
        print(f"Rule broken (handled) -> {error}")

    # Rule broken: unknown ticket number.
    try:
        lot.release_vehicle(999, used.entry_time + timedelta(hours=3))
    except ParkingLotError as error:
        print(f"Rule broken (handled) -> {error}")

    # Invalid input: exit time earlier than entry time (ValueError).
    open_ticket = tickets["MCB-202"]
    try:
        lot.release_vehicle(open_ticket.ticket_number,
                            open_ticket.entry_time - timedelta(minutes=5))
    except ValueError as error:
        print(f"Bad exit time rejected (handled) -> {error}")

    # ------------------------------------------------------------
    # Chapter 5: The waiting car finally gets in
    # ------------------------------------------------------------
    heading("Chapter 5: A slot opens up")

    ticket = lot.park_vehicle(car_3)
    tickets[car_3.vehicle_plate] = ticket
    print(f"  {ticket} in {ticket.slot}")

    # ------------------------------------------------------------
    # Chapter 6: Closing time
    # ------------------------------------------------------------
    heading("Chapter 6: Closing time")

    total = 0.0
    for ticket in lot.active_tickets:
        fee = lot.release_vehicle(ticket.ticket_number,
                                  ticket.entry_time + timedelta(hours=1))
        total += fee
        print(f"  {ticket.vehicle} paid P{fee:.2f}")
    print(f"  Collected at closing: P{total:.2f}")
    show_slots(lot)

    # Clean up the registry as vehicles leave for the day.
    for vehicle in registry.vehicles:
        registry.unregister(vehicle.vehicle_plate)
    print(f"  Vehicles still registered: {len(registry)}")


if __name__ == "__main__":
    main()
