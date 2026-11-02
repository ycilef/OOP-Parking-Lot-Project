# Author: Gian Sicat (module: ticket)
"""Ticket module for the Parking Lot Management System.

Depends only on the shared contracts, so it works with any vehicle
and slot that follow IVehicle and ISlot.
"""

from datetime import datetime

from contracts import ITicket, IVehicle, ISlot, ParkingLotError


def _is_int(value) -> bool:
    """Return True for real integers (bool is excluded)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _same_awareness(a: datetime, b: datetime) -> bool:
    """Return True if both datetimes are naive or both are aware."""
    return (a.tzinfo is None) == (b.tzinfo is None)


class Ticket(ITicket):
    """Concrete parking ticket implementing the ITicket contract.

    Records which vehicle is parked in which slot, when it entered,
    and when it left (None while the ticket is open).
    """

    def __init__(self, ticket_number: int, vehicle: IVehicle,
                 slot: ISlot, entry_time: datetime | None = None):
        """Create an open ticket.

        If entry_time is None, the current time is used.

        Raises ValueError if ticket_number is not a positive int,
        vehicle/slot do not follow their contracts, or entry_time is
        not a datetime.
        Raises ParkingLotError if the slot is not assigned to this
        vehicle (the vehicle must be parked before a ticket is issued).
        """
        if not _is_int(ticket_number) or ticket_number <= 0:
            raise ValueError("Ticket number must be a positive integer.")
        if not isinstance(vehicle, IVehicle):
            raise ValueError("Vehicle must implement IVehicle contract.")
        if not isinstance(slot, ISlot):
            raise ValueError("Slot must implement ISlot contract.")
        if entry_time is not None and not isinstance(entry_time, datetime):
            raise ValueError("Entry time must be a datetime object.")

        # Business rule 1: the slot must actually hold this vehicle.
        if slot.assigned_vehicle is not vehicle:
            raise ParkingLotError(
                "Cannot issue ticket: slot is not assigned to this vehicle.")

        self._ticket_number = ticket_number
        self._vehicle = vehicle
        self._slot = slot
        self._entry_time = entry_time if entry_time is not None else datetime.now()
        self._exit_time = None

    @property
    def ticket_number(self) -> int:
        """Return the unique positive ticket number."""
        return self._ticket_number

    @property
    def vehicle(self) -> IVehicle:
        """Return the vehicle this ticket was issued to."""
        return self._vehicle

    @property
    def slot(self) -> ISlot:
        """Return the slot assigned to this ticket."""
        return self._slot

    @property
    def entry_time(self) -> datetime:
        """Return when the vehicle entered."""
        return self._entry_time

    @property
    def exit_time(self) -> datetime | None:
        """Return when the vehicle exited, or None if still open."""
        return self._exit_time

    def close(self, exit_time: datetime) -> None:
        """Record the exit time and close the ticket.

        Raises ParkingLotError if the ticket is already closed.
        Raises ValueError if exit_time is not a datetime, mixes naive
        and timezone-aware values with the entry time, or is earlier
        than the entry time.
        """
        # Business rule 2: a closed ticket cannot be closed again.
        if self._exit_time is not None:
            raise ParkingLotError("This ticket is already closed.")
        if not isinstance(exit_time, datetime):
            raise ValueError("Exit time must be a datetime object.")
        if not _same_awareness(exit_time, self._entry_time):
            raise ValueError(
                "Exit and entry times must both be naive or both timezone-aware.")
        if exit_time < self._entry_time:
            raise ValueError("Exit time cannot be earlier than the entry time.")
        self._exit_time = exit_time

    def __str__(self) -> str:
        """Return a readable description of the ticket."""
        status = "Closed" if self._exit_time is not None else "Open"
        return (f"Ticket #{self._ticket_number} for "
                f"{self._vehicle.vehicle_plate} ({status})")

    def __eq__(self, other) -> bool:
        """Tickets are equal when their ticket numbers match."""
        if not isinstance(other, ITicket):
            return NotImplemented
        return self._ticket_number == other.ticket_number

    def __hash__(self) -> int:
        """Hash by ticket number, consistent with __eq__."""
        return hash(self._ticket_number)
