**Parking Lot Management System**

**Project description**

The Parking Lot Management System is a Python package that manages vehicles entering and leaving a parking facility. It supports cars and motorcycles, assigns vehicles to suitable parking slots across different levels, and creates tickets to record entry and exit times. The system calculates parking fees based on the vehicle type and the duration of the parking session. It also manages slot availability and handles parking-related rule violations, such as trying to park when no suitable slot is available.

**Group members and Module Assignments**

| Module | Member | Contract ABC |
|--------|--------|-------------|
|vehicle.py|Aranjuez|IVehicle|
|slot.py|Cagas|ISlot|
|ticket.py|Sicat|ITicket|
|fees.py|Ferolino|IFees|
|lot_manager.py|Mier|ILotManager|

The shared contracts.py file defines the abstract base classes (ABCs) used by the five modules, along with the shared ParkingLotError exception. Each module should depend on the contracts and the Python standard library rather than importing another member's concrete module. The main.py file connects the concrete classes and demonstrates how the complete system works.

**Project Structure**

parking-lot-project/

├── contracts.py

├── vehicle.py

├── slot.py

├── ticket.py

├── fees.py

├── lot_manager.py

├── main.py

├── tests/

│   ├── test_vehicle.py

│   ├── test_slot.py

│   ├── test_ticket.py

│   ├── test_fees.py

│   └── test_lot_manager.py

└── README.md

**Requirements**
- Python 3.10 or newer
- Python standard library only
- No third-party packages are required

**How to run the tests**

Open a terminal in the parking-lot-project folder. The tests are organized in the tests/ folder, with a separate test file for each module.

Run the demonstration program: python main.py

Run all unit tests: python -m unittest discover tests -v

**Contract and Design**

The project uses these abstract base classes from contracts.py:
- IVehicle: provides a vehicle's plate number and type.
- ISlot: describes a parking slot, checks whether a vehicle fits, and supports assigning and removing a vehicle.
- ITicket: records the vehicle, assigned slot, entry time, and exit time for a parking session.
- IFees: provides hourly rates for cars and motorcycles and calculates the fee for a completed ticket.
- ILotManager: parks and releases vehicles and provides information about parking slots and active tickets.

ParkingLotError is the shared exception for parking business-rule violations. The program should handle expected rule violations in main.py and display an understandable message rather than terminating unexpectedly.

**Reference Disclosure**
