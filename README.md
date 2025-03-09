# Operating-Systems-Assignment 1 Readers-Writers Problem with Load Balancing

## Overview
This project implements the Readers-Writers synchronization problem in Python. The solution provides:
- **Writer Priority:** When a writer signals its intent to write, no new readers are allowed to start until the writer has finished
- **Load Balancing:** Readers are distributed evenly across three file replicas by selecting the replica with the fewest active readers

## Requirements
- Python 3.13.2 (3.x)
- No additional packages are needed, only Python’s standard libraries are used

## How to Run the Program
1. **Install Python:** Download and install Python 3.x from [python.org](https://www.python.org/downloads/).,ensure Python is added to your system PATH
2. **Clone or Extract the Project:** Place all files, including "readers_writers.py" and "log.txt" in a single folder
3. **Open the Project in Visual Studio Code (or your preferred IDE):**
   - Open VS Code
   - Choose "File -> Open Folder..." and select your project folder
4. **Run the Program:**
   - Open the integrated terminal in VS Code (press " Ctrl+` ")
   - Run the command:
     ```
     python readers_writers.py
     ```
   - The program will continuously spawn reader threads and periodically perform writer updates. Logs are appended to `log.txt`.
5. **Stop the Program:** Press `Ctrl+C` in the terminal to exit the simulation.

## Configuration Options
- **Sleep Durations:** You can modify the sleep durations in the code (for both readers and the writer) by adjusting the values in the `time.sleep()` calls

