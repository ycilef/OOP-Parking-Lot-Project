"""Tests for the ticket module, using fake vehicle and slot classes."""

import unittest
from datetime import datetime, timedelta, timezone

from contracts import IVehicle, ISlot, ParkingLotError
from ticket import Ticket


class FakeVehicle(IVehicle):
    """Minimal vehicle following the IVehicle contract."""

    def __init__(self, plate="ABC-123", vtype="car"):
        self._plate, self._type = plate, vtype

    @property
    def vehicle_plate(self):
        return self._plate

    @property
    def vehicle_type(self):
        return self._type


class FakeSlot(ISlot):
    """Minimal slot following the ISlot contract."""

    def __init__(self, number=1, vehicle=None):
        self._number, self._vehicle = number, vehicle

    slot_number = property(lambda self: self._number)
    slot_type = property(lambda self: "regular")
    level = property(lambda self: 1)
    is_available = property(lambda self: self._vehicle is None)
    assigned_vehicle = property(lambda self: self._vehicle)

    def can_fit(self, vehicle):
        return True

    def assign_vehicle(self, vehicle):
        self._vehicle = vehicle

    def remove_vehicle(self):
        v, self._vehicle = self._vehicle, None
        return v


class TestTicket(unittest.TestCase):

    def setUp(self):
        self.vehicle = FakeVehicle()
        self.slot = FakeSlot(1, self.vehicle)
        self.entry = datetime(2026, 11, 2, 8, 0)
        self.ticket = Ticket(1, self.vehicle, self.slot, self.entry)

    def test_properties_and_read_only(self):
        self.assertEqual(self.ticket.ticket_number, 1)
        self.assertIs(self.ticket.vehicle, self.vehicle)
        self.assertIs(self.ticket.slot, self.slot)
        self.assertEqual(self.ticket.entry_time, self.entry)
        self.assertIsNone(self.ticket.exit_time)
        with self.assertRaises(AttributeError):
            self.ticket.entry_time = datetime.now()

    def test_default_entry_time_is_now(self):
        t = Ticket(2, self.vehicle, self.slot)
        self.assertLess(abs(datetime.now() - t.entry_time), timedelta(seconds=5))

    def test_constructor_rejects_bad_input(self):
        bad = [
            (0, self.vehicle, self.slot), (-1, self.vehicle, self.slot),
            ("1", self.vehicle, self.slot), (True, self.vehicle, self.slot),
            (1, "car", self.slot), (1, self.vehicle, "slot"),
            (1, self.vehicle, self.slot, "2026-01-01"),
        ]
        for args in bad:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    Ticket(*args)

    def test_slot_not_holding_vehicle_raises(self):
        empty = FakeSlot(2)
        with self.assertRaises(ParkingLotError):
            Ticket(3, self.vehicle, empty, self.entry)
        other = FakeSlot(3, FakeVehicle("XYZ-999"))
        with self.assertRaises(ParkingLotError):
            Ticket(3, self.vehicle, other, self.entry)

    def test_close_records_exit_time(self):
        exit_time = self.entry + timedelta(hours=2)
        self.ticket.close(exit_time)
        self.assertEqual(self.ticket.exit_time, exit_time)

    def test_close_twice_raises(self):
        self.ticket.close(self.entry + timedelta(hours=1))
        with self.assertRaises(ParkingLotError):
            self.ticket.close(self.entry + timedelta(hours=2))

    def test_close_with_bad_time_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.ticket.close(self.entry - timedelta(minutes=1))
        with self.assertRaises(ValueError):
            self.ticket.close("noon")
        with self.assertRaises(ValueError):
            self.ticket.close(datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc))
        self.assertIsNone(self.ticket.exit_time)  # still open after failures

    def test_str_shows_status(self):
        self.assertIn("Open", str(self.ticket))
        self.assertIn("ABC-123", str(self.ticket))
        self.ticket.close(self.entry + timedelta(hours=1))
        self.assertIn("Closed", str(self.ticket))

    def test_eq_and_hash(self):
        same = Ticket(1, self.vehicle, self.slot, self.entry)
        self.assertEqual(self.ticket, same)
        self.assertEqual(len({self.ticket, same}), 1)
        self.assertNotEqual(self.ticket, Ticket(2, self.vehicle, self.slot, self.entry))
        self.assertNotEqual(self.ticket, "ticket 1")


if __name__ == "__main__":
    unittest.main()
