# Author: James Ryan Cagas (module: ticket)

# Author: <Your Classmate's Name> (module: slot)
"""Slot module for the Parking Lot Management System.

Depends only on the shared contracts; it never imports a concrete
vehicle class, so it works with any object that follows IVehicle.
"""

from contracts import ISlot, IVehicle, ParkingLotError

SMALL = "small"
REGULAR = "regular"
VALID_SLOT_TYPES = (SMALL, REGULAR)

CAR = "car"
MOTORCYCLE = "motorcycle"

# Assumption: ground floor is level 0. Change to 1 if the group's
# contract says levels start at 1.
MIN_LEVEL = 0


def _is_int(value) -> bool:
    """Return True for real integers (bool is excluded)."""
    return isinstance(value, int) and not isinstance(value, bool)


class ParkingSlot(ISlot):
    """Concrete parking slot implementing the ISlot contract.

    Small slots fit motorcycles only; regular slots fit cars and
    motorcycles. Tracks which vehicle (if any) occupies the slot.
    """

    def __init__(self, slot_number: int, slot_type: str, level: int):
        """Create an empty slot.

        Raises ValueError if slot_number is not a positive int,
        slot_type is not 'small' or 'regular', or level is not an
        int >= MIN_LEVEL.
        """
        if not _is_int(slot_number) or slot_number <= 0:
            raise ValueError("Slot number must be a positive integer.")
        if not isinstance(slot_type, str) or slot_type not in VALID_SLOT_TYPES:
            raise ValueError("Slot type must be 'small' or 'regular'.")
        if not _is_int(level) or level < MIN_LEVEL:
            raise ValueError(f"Level must be an integer >= {MIN_LEVEL}.")

        self._slot_number = slot_number
        self._slot_type = slot_type
        self._level = level
        self._assigned_vehicle = None

    @property
    def slot_number(self) -> int:
        """Return the unique positive number of the slot."""
        return self._slot_number

    @property
    def slot_type(self) -> str:
        """Return 'small' or 'regular'."""
        return self._slot_type

    @property
    def level(self) -> int:
        """Return the level where the slot is located."""
        return self._level

    @property
    def is_available(self) -> bool:
        """Return True if no vehicle occupies the slot."""
        return self._assigned_vehicle is None

    @property
    def assigned_vehicle(self) -> IVehicle | None:
        """Return the parked vehicle, or None if the slot is empty."""
        return self._assigned_vehicle

    def can_fit(self, vehicle: IVehicle) -> bool:
        """Return True if the vehicle fits this slot's size.

        Motorcycles fit any slot; cars fit regular slots only.
        None or an unknown vehicle type returns False.
        """
        if vehicle is None:
            return False
        if vehicle.vehicle_type == MOTORCYCLE:
            return True
        if vehicle.vehicle_type == CAR:
            return self._slot_type == REGULAR
        return False

    def assign_vehicle(self, vehicle: IVehicle) -> None:
        """Park a vehicle in this slot.

        Raises ParkingLotError if the slot is occupied or the
        vehicle does not fit.
        """
        if not self.is_available:
            raise ParkingLotError(f"Slot {self._slot_number} is already occupied.")
        if not self.can_fit(vehicle):
            raise ParkingLotError(f"Vehicle cannot fit in slot {self._slot_number}.")
        self._assigned_vehicle = vehicle

    def remove_vehicle(self) -> IVehicle:
        """Remove and return the parked vehicle.

        Raises ParkingLotError if the slot is already empty.
        """
        if self.is_available:
            raise ParkingLotError(f"Slot {self._slot_number} is already empty.")
        vehicle = self._assigned_vehicle
        self._assigned_vehicle = None
        return vehicle

    def __str__(self) -> str:
        """Return a readable description of the slot."""
        status = "free" if self.is_available else "occupied"
        return (f"Slot {self._slot_number} "
                f"({self._slot_type}, level {self._level}, {status})")

    def __eq__(self, other) -> bool:
        """Slots are equal when their slot numbers match."""
        if not isinstance(other, ISlot):
            return NotImplemented
        return self._slot_number == other.slot_number

    def __hash__(self) -> int:
        """Hash by slot number, consistent with __eq__."""
        return hash(self._slot_number)
