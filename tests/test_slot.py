"""Tests for the slot module, using a fake vehicle (no real Car/Motorcycle)."""

import unittest

from contracts import IVehicle, ParkingLotError
from slot import ParkingSlot


class FakeVehicle(IVehicle):
    """Minimal vehicle that follows the IVehicle contract."""

    def __init__(self, plate: str, vtype: str):
        self._plate = plate
        self._type = vtype

    @property
    def vehicle_plate(self) -> str:
        return self._plate

    @property
    def vehicle_type(self) -> str:
        return self._type


class TestParkingSlot(unittest.TestCase):

    def setUp(self):
        self.car = FakeVehicle("CAR-111", "car")
        self.moto = FakeVehicle("MOTO-22", "motorcycle")
        self.small = ParkingSlot(1, "small", 1)
        self.regular = ParkingSlot(2, "regular", 1)

    def test_properties_and_read_only(self):
        self.assertEqual(self.small.slot_number, 1)
        self.assertEqual(self.small.slot_type, "small")
        self.assertEqual(self.small.level, 1)
        with self.assertRaises(AttributeError):
            self.small.slot_number = 5

    def test_car_does_not_fit_small_slot(self):
        self.assertFalse(self.small.can_fit(self.car))
        with self.assertRaises(ParkingLotError):
            self.small.assign_vehicle(self.car)
        self.assertTrue(self.small.is_available)

    def test_motorcycle_fits_both_slot_types(self):
        self.assertTrue(self.small.can_fit(self.moto))
        self.assertTrue(self.regular.can_fit(self.moto))

    def test_unknown_type_and_none_do_not_fit(self):
        self.assertFalse(self.regular.can_fit(FakeVehicle("X", "truck")))
        self.assertFalse(self.regular.can_fit(None))

    def test_assign_and_remove_flip_availability(self):
        self.regular.assign_vehicle(self.car)
        self.assertFalse(self.regular.is_available)
        self.assertIs(self.regular.assigned_vehicle, self.car)
        removed = self.regular.remove_vehicle()
        self.assertIs(removed, self.car)
        self.assertTrue(self.regular.is_available)
        self.assertIsNone(self.regular.assigned_vehicle)

    def test_assign_to_occupied_slot_raises(self):
        self.regular.assign_vehicle(self.car)
        with self.assertRaises(ParkingLotError):
            self.regular.assign_vehicle(self.moto)
        self.assertIs(self.regular.assigned_vehicle, self.car)

    def test_remove_from_empty_slot_raises(self):
        with self.assertRaises(ParkingLotError):
            self.regular.remove_vehicle()

    def test_constructor_rejects_bad_input(self):
        bad_args = [
            (0, "small", 1), (-1, "small", 1), ("a", "small", 1),
            (True, "small", 1), (1.5, "small", 1),
            (1, "large", 1), (1, None, 1), (1, "small", -1),
            (1, "small", "1"), (1, "small", True),
        ]
        for args in bad_args:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    ParkingSlot(*args)

    def test_str_eq_and_hash(self):
        self.assertIn("Slot 1", str(self.small))
        self.assertIn("free", str(self.small))
        self.assertEqual(ParkingSlot(1, "regular", 3), self.small)
        self.assertEqual(len({self.small, ParkingSlot(1, "small", 1)}), 1)
        self.assertNotEqual(self.small, self.regular)


if __name__ == "__main__":
    unittest.main()
