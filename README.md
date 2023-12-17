# Rule-Based Expert System using Forward Chaining

Welcome to the Rule-Based Expert System program! This Python application implements a forward chaining reasoning method to process facts and rules and generate new facts based on the provided rules.

## Introduction
The project consists of two main modules:

1. **main.py**:
   This module provides a user interface to input facts and rules, display existing facts, and generate new facts based on the rules. The program utilizes the forward chaining reasoning method.

2. **exprt_func.py**:
   This module includes functions related to the generation and validation of facts, loading and saving facts from/to a JSON file, and other helper functions.

## How to Use

1. **Run the Program**: Execute `main.py` to start the program. Follow the on-screen instructions to input facts and rules, display existing facts, and generate new facts.

2. **Input Facts**: Press 'a' to input new facts. The program will prompt you to provide a fact, and it will be added to the database.

3. **Input Rules**: Press 'b' to input new rules. Follow the specified format for rules (e.g., If (statement 1) and (statement 2) then (statement n)).

4. **Generate Facts**: Press 'c' to generate new facts based on the inputted rules. The program will validate the rules and generate facts accordingly.

5. **Exit**: Press 'q' to exit the program.

## File Structure

- `main.py`: Main program file for user interaction.
- `exprt_func.py`: Module containing functions for generating, validating, and saving facts.
- `db.json`: JSON file storing existing facts.
