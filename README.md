**Parking Lot Management System**

**Project description**

The Parking Lot Management System is a Python package that manages vehicles entering and leaving a parking lot facility. It supports cars and motorcycles and assigns them to suitable parking slots based on slot type and availability across different parking levels. The system creates parking tickets to record vehicle entry and exit times and calculates parking fees according to vehicle type and parking duration. It also manages parking slot availability and handles business-rule violations, such as attempting to park a vehicle in an incompatible or occupied slot.

**Group members and Module Assignments**

| Module | Member | Contract ABC |
|--------|--------|-------------|
|vehicle|Aranjuez|IVehicle|
|slot|Cagas|ISlot|
|ticket|Sicat|ITicket|
|fees|Ferolino|IFees|
|lot_manager|Mier|ILotManager|

The shared contracts package defines the abstract base classes (ABCs) used by the five modules and the custom ParkingLotError exception.

Each module implements its assigned contract. Modules depend on the shared contracts and Python standard library rather than importing other modules' concrete implementations. Dependencies are passed through constructor or method parameters using the appropriate contract types.

The main.py file is responsible for importing the concrete classes and connecting all five modules to demonstrate the complete system.

**Project Structure**

The project is organized into packages and test files as follows:

parking-lot-project/
│
├── contracts/
│   └── __init__.py
│
├── fees/
│   └── __init__.py
│
├── lot_manager/
│   └── __init__.py
│
├── slot/
│   └── __init__.py
│
├── tests/
│   ├── test_fees.py
│   ├── test_lot_manager.py
│   ├── test_slot.py
│   ├── test_ticket.py
│   └── test_vehicle.py
│
├── ticket/
│   └── __init__.py
│
├── vehicle/
│   └── __init__.py
│
├── main.py
└── README.md

**Requirements**
- Python 3.10 or newer
- Python standard library only
- No third-party packages are required

**Contract and Design**

The project uses five abstract base classes defined in contracts/__init__.py:

**IVehicle** – Defines the required vehicle information, including its plate number and vehicle type.

**ISlot** – Defines parking slot information, checks whether a vehicle can fit, and supports assigning and removing vehicles.

**ITicket** – Defines a parking ticket that records the vehicle, assigned slot, entry time, and exit time.

**IFees** – Defines hourly parking rates for cars and motorcycles and calculates fees for completed parking tickets.

**ILotManager** – Defines the operations for parking and releasing vehicles and provides information about parking slots and active tickets.

ParkingLotError is the shared custom exception used for parking-related business-rule violations.

**Object-Oriented Programming Principles**

The project applies the following object-oriented programming principles:

Abstraction: Abstract base classes define the required interfaces for each module.

Encapsulation: Internal data is protected through private or protected-style attributes and controlled access through properties and methods.

Inheritance and Polymorphism: Concrete classes implement the shared contracts, allowing modules to work with different objects that follow the same interface.

Validation and Business Rules: Constructors validate input, while invalid parking operations raise the shared ParkingLotError exception.

**How to run the tests**

Open a terminal in the project root folder, where main.py and README.md are located.

Run the demonstration program: python main.py

The program demonstrates a realistic parking lot scenario using all five modules. It includes vehicle creation, parking slot assignment, ticket creation, fee calculation, and vehicle release. It also demonstrates at least one invalid operation and handles the resulting business-rule exception.

Run all unit tests: python -m unittest discover tests -v

The tests are organized in the tests/ folder, with a separate test file for each module.

**AI Assistance and References Disclosure**

AI-assisted tools and references were used during the development and preparation of this project.

The tools and resources used include:

Google Colab: Used as a Python development and experimentation environment, including AI-assisted help during the development process.

ChatGPT (OpenAI): Used for assistance in understanding the assignment requirements, reviewing project organization, troubleshooting Python and Git commands, improving documentation, and understanding testing and module integration.

The team members reviewed and worked with the project materials and remain responsible for understanding their respective modules, the shared contract, and the complete system. AI assistance does not replace each member's responsibility to explain their own code and design decisions during the project demonstration.


