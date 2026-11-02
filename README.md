# Fees Module (`fees/`)

**Owner:** Ana Lynica B. Ferolino
**Contract ABC implemented:** `IFees` (from `contracts`)
**Concrete class:** `StandardFees`
**Part of:** Parking Lot Management System

## What this module does

The `fees` module calculates how much a vehicle owes when it leaves the parking lot. It takes a closed parking ticket, looks at the vehicle type and how long the vehicle stayed, and returns the fee in pesos. Cars and motorcycles have separate hourly rates, and every stay has a free grace period at the start.

The module imports only from `contracts` and the Python standard library. It never imports a teammate's module, so it works with **any** ticket and vehicle that follow `ITicket` and `IVehicle`.

## Fee rules

| Rule | Behavior |
|---|---|
| Grace period | A stay up to and including `grace_minutes` is free (`0.0`). Default: 15 minutes. |
| Billing | Beyond the grace period, every started hour is charged. Default rates: car P50.00/h, motorcycle P20.00/h. |
| Minimum | At least 1 hour is charged once the grace period is exceeded. |
| Rounding | The result is rounded to 2 decimal places. |
| Charged time | The whole stay is billed, not only the time after the grace period. |

Examples with the default settings:

| Vehicle | Time parked | Hours charged | Fee |
|---|---|---|---|
| car | 15 min | 0 (grace) | P0.00 |
| car | 16 min | 1 | P50.00 |
| car | 60 min | 1 | P50.00 |
| car | 61 min | 2 | P100.00 |
| motorcycle | 120 min | 2 | P40.00 |

## Public interface

### `StandardFees(car_hourly_rate=50.0, motorcycle_hourly_rate=20.0, grace_minutes=15)`

| Member | Kind | Description |
|---|---|---|
| `car_hourly_rate` | read-only property (`IFees`) | Hourly rate for cars, in pesos. |
| `motorcycle_hourly_rate` | read-only property (`IFees`) | Hourly rate for motorcycles, in pesos. |
| `grace_minutes` | read-only property (extra) | Free minutes at the start of every stay. |
| `compute_fee(ticket)` | method (`IFees`) | Returns the fee in pesos for a closed ticket. |
| `rate_for(vehicle_type)` | method (extra) | Returns the hourly rate for `'car'` or `'motorcycle'`. |
| `__str__`, `__eq__`, `__hash__` | dunder methods | Readable text; two schedules are equal if rates and grace match. |

`grace_minutes` and `rate_for` are not part of `IFees`. Code that is typed against `IFees` should not depend on them.

## Validation and business rules

**Constructor (raises `ValueError`):**
- A rate that is not a number, is a `bool`, is negative, or is NaN or infinite.
- `grace_minutes` that is not an `int`, is a `bool`, or is negative.

**`compute_fee` and `rate_for`:**

| Situation | Error |
|---|---|
| `ticket` does not implement `ITicket` | `ValueError` |
| Ticket is still open (`exit_time is None`) | `ParkingLotError` |
| Vehicle type is not `'car'` or `'motorcycle'` | `ParkingLotError` |

## Design notes

- **Encapsulation:** all data is stored in underscore attributes (`_car_rate`, `_motorcycle_rate`, `_grace_minutes`) and exposed through three read-only properties. The module holds no mutable collections.
- **Polymorphism:** `compute_fee` uses only the `ITicket` and `IVehicle` contracts (`exit_time`, `entry_time`, `vehicle.vehicle_type`), so any ticket from any teammate works.
- **Dunder methods:** `__eq__` and `__hash__` use the same three values, so equal schedules always have equal hashes. `__eq__` returns `NotImplemented` for other types.
- **Time handling:** the duration is computed in seconds, so 15 minutes + 1 second is already charged.
- **Datetimes:** `entry_time` and `exit_time` must both be naive or both be timezone-aware. Mixing them raises `TypeError` in Python.

## Usage

Only `main.py` imports the concrete class and passes it to other modules:

```python
from fees import StandardFees

fees = StandardFees()                      # P50/h car, P20/h motorcycle, 15 min grace
fees = StandardFees(60, 25, grace_minutes=10)   # custom schedule

amount = fees.compute_fee(closed_ticket)   # closed_ticket is any ITicket
```

A lot manager should receive it as `IFees` (constructor injection) and call `compute_fee(ticket)`.

## Running the tests

From the project root:

```
python -m unittest discover tests -v
```

The tests are in `tests/test_fees.py`. They use small fake classes (`FakeVehicle`, `FakeTicket`) that inherit from `IVehicle` and `ITicket`, so they never use a teammate's real code. They cover the grace boundary, hour rounding, per-type rates, 2-decimal rounding, open tickets, unknown vehicle types, constructor validation, read-only properties, and `__eq__`, `__hash__` and `__str__`.

## Contract notes for the group

These are proposals for the contract keeper. They are not final until the group agrees and the change is logged in the main README.

- Add the grace period, the "every started hour" rule, and the `ValueError` for a non-ticket argument to the `IFees.compute_fee` docstring.
- State in `contracts/` whether `entry_time` and `exit_time` are naive or timezone-aware.
- Decide whether `grace_minutes` belongs in `IFees` or stays a `StandardFees` extra.

## Row for the main README's module table

| Module | Owner | Contract ABC |
|---|---|---|
| `fees` | Ana Lynica B. Ferolino | `IFees` |

## AI tools and references

> Edit this section so it is true. The assignment requires listing every AI tool or reference used and what it was used for.

- Claude (Anthropic) was used to review the module and test file against the assignment checklist and the contract, and to suggest extra test cases and README wording.
- I wrote and can explain the code in `fees/__init__.py` and `tests/test_fees.py`.
