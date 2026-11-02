"""Run a short parking-lot demo using all five project modules."""

from datetime import timedelta

from fees import StandardFees
from lot_manager import LotManager
from slot import ParkingSlot
from ticket import Ticket
from vehicle import Car, Motorcycle


def main() -> None:
    """Simulate two vehicles parking and leaving the lot."""
    slots = [
        ParkingSlot(1, "small", 0),
        ParkingSlot(2, "regular", 0),
        ParkingSlot(3, "regular", 1),
    ]
    fees = StandardFees(
        car_hourly_rate=50,
        motorcycle_hourly_rate=20,
        grace_minutes=15,
    )
    lot = LotManager(slots, fees, Ticket)

    motorcycle = Motorcycle("MOTO-123")
    car = Car("CAR-456")

    print("A motorcycle and a car arrive at the parking lot.")
    motorcycle_ticket = lot.park_vehicle(motorcycle)
    print(f"  {motorcycle} parks in {motorcycle_ticket.slot}.")
    car_ticket = lot.park_vehicle(car)
    print(f"  {car} parks in {car_ticket.slot}.")
    print(f"  {lot}")

    motorcycle_exit = motorcycle_ticket.entry_time + timedelta(minutes=45)
    motorcycle_fee = lot.release_vehicle(
        motorcycle_ticket.ticket_number,
        motorcycle_exit,
    )
    print(
        f"\n{motorcycle.vehicle_plate} leaves after 45 minutes "
        f"and pays P{motorcycle_fee:.2f}."
    )

    car_exit = car_ticket.entry_time + timedelta(hours=2, minutes=25)
    car_fee = lot.release_vehicle(car_ticket.ticket_number, car_exit)
    print(
        f"{car.vehicle_plate} leaves after 2 hours 25 minutes "
        f"and pays P{car_fee:.2f}."
    )

    print(f"\nAfter both vehicles leave: {lot}")


if __name__ == "__main__":
    main()
