Q36 – Basic Block Identification and CFG Generation

Requirements

Python 3 installed. No external libraries required.

How to Run

1. Open the project folder in VS Code.
2. Open the terminal.
3. Run:

python q36_basic_blockes.py

4. Enter Three-Address Code instructions.
5. Type "END" to finish.

Sample Input

a = b + c
if a < d goto L1
x = y * z
goto L2
L1: x = y - z
L2: print x
END

Sample Output

CFG Edges:
B1 -> B2
B1 -> B3
B2 -> B4
B3 -> B4

Description

This program identifies leaders, divides Three-Address Code into basic blocks and generates Control Flow Graph (CFG) edges.