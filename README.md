# Quality assesment and Isobus to ROS2 communication

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Spraying Module](#spraying-module)
  - [Weeding Module](#weeding-module)
- [License](#license)

---

## Overview

This project is a robotic agricultural management system designed to facilitate tasks like spraying and weeding. It includes modules for CAN communication, ROS bridge integration, and GUI-based controls for managing robotic processes.

---

## Project Structure

```plaintext
├── LICENSE.md            # Licensing information
├── environment.yml       # Conda environment configuration
├── spraying              # Spraying module
│   ├── kinematics.py       # Kinematics logic for spraying
│   ├── kinematics_test.py  # Unit tests for spraying kinematics
│   └── trigger.py          # Trigger logic for spraying operations
├── weeding               # Weeding module
│   ├── bridge.py           # ROS-CAN bridge for weeding
│   ├── control.kv          # GUI layout for weeding control
│   ├── emergency_db_flash.py # Emergency flash system
│   ├── emergency_db_tim.py   # Emergency TIM messages
│   ├── emergency_raw.py      # Raw CAN message handling for emergencies
│   ├── ip.py                # IP retrieval for devices
│   ├── kinematics.py        # Kinematics logic for weeding
│   ├── q_dbc_to_fc.py       # DBC to functional components bridge
│   ├── q_raw_to_fc.py       # Raw message processing for functional components
│   └── trigger.py           # Trigger logic for weeding operations
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url
   cd your-repo
   ```

2. Create a conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate <your-environment-name>
   ```

3. Install any additional dependencies via pip if required.

---

## Usage

### Spraying Module
- **Kinematics**:
  Handles spraying operations by interfacing with CAN bus and ROS topics.
  ```bash
  python spraying/kinematics.py
  ```
- **Trigger**:
  Sends trigger signals to initiate spraying.
  ```bash
  python spraying/trigger.py
  ```

### Weeding Module
- **Bridge**:
  Connects ROS topics and CAN messages for real-time updates.
  ```bash
  python weeding/bridge.py
  ```
- **Emergency Control**:
  - `emergency_db_flash.py` manages emergency signals for flash.
  - `emergency_db_tim.py` manages TIM-based emergency messages.
  ```bash
  python weeding/emergency_db_flash.py
  python weeding/emergency_db_tim.py
  ```
- **GUI**:
  Launches the GUI for controlling weeding operations.
  ```bash
  python weeding/bridge.py
  ```

---

## License

This project is licensed under the MIT License. See [LICENSE.md](./LICENSE.md) for more details.
