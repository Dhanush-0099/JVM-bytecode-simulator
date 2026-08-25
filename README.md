# Bytecode Simulator

A simple **stack-based bytecode virtual machine (VM)** implemented in Python.

This project demonstrates how a small virtual machine can read instructions from text files, execute them one by one, maintain an operand stack and local variables, perform arithmetic operations, make conditional jumps, and print results.

The project contains:

- `instructions.py` — the Python bytecode simulator/interpreter
- `matrix.txt` — bytecode program for adding pairs of input values
- `minmax.txt` — bytecode program for finding the minimum and maximum among three integers
- `sort.txt` — bytecode program for sorting three integers in ascending order

---

## 1. Project Overview

A **bytecode simulator** is a program that executes a sequence of low-level instructions.

Instead of directly writing Python code such as:

```python
a = int(input())
b = int(input())
print(a + b)
```

this project represents the logic using custom bytecode instructions such as:

```text
read
istore 0
iload 0
iload 1
iadd
print
```

The Python program acts as the **virtual machine** that understands these instructions.

The overall execution flow is:

```text
Text Bytecode File
       |
       v
instructions.py
       |
       v
Read instructions
       |
       v
Program Counter (PC)
       |
       v
Execute instruction
       |
       +----> Operand Stack
       |
       +----> Local Variables
       |
       v
Conditional / Arithmetic Operations
       |
       v
Output
```

---

# 2. Files in the Project

## `instructions.py`

This is the main program.

It implements a class called `Bytecode`, which behaves like a small virtual machine.

The simulator maintains:

- an operand stack
- local variables
- a program counter
- a list of bytecode instructions

The constructor initializes these components:

```python
self.stack = []
self.locals = [0] * 10
self.pc = 0
self.instructions = []
```

The simulator therefore has **10 local variable slots**, indexed from `0` to `9`.

The program counter (`pc`) tells the VM which instruction should execute next.

---

# 3. Bytecode VM Architecture

The simulator uses three important pieces of runtime state.

## 3.1 Operand Stack

The operand stack temporarily stores values used by instructions.

For example:

```text
ldc 10
ldc 20
iadd
```

Execution:

```text
ldc 10

Stack:
[10]
```

Then:

```text
ldc 20
```

Stack:

```text
[10, 20]
```

Then:

```text
iadd
```

The VM removes the two top values:

```text
20 -> right
10 -> left
```

and pushes:

```text
10 + 20 = 30
```

Final stack:

```text
[30]
```

This is called **stack-based execution**.

---

## 3.2 Local Variables

The VM also has:

```python
self.locals = [0] * 10
```

This creates ten local storage locations:

```text
locals[0]
locals[1]
locals[2]
...
locals[9]
```

For example:

```text
read
istore 0
```

means:

1. Read an integer from the user.
2. Put the value on the operand stack.
3. `istore 0` removes the value from the stack.
4. Store it in local variable `0`.

If the user enters `25`:

```text
locals[0] = 25
```

The value can later be retrieved using:

```text
iload 0
```

---

## 3.3 Program Counter

The program counter is:

```python
self.pc = 0
```

It represents the index of the instruction currently being executed.

For normal instructions, the VM advances using:

```python
self.pc += 1
```

For conditional instructions such as `ifeq`, `iflt`, and `ifgt`, the PC may jump to another instruction:

```python
self.pc = target
```

This is what allows the bytecode programs to implement:

- `if`
- `else`
- comparisons
- branching
- sorting logic

---

# 4. Loading a Bytecode File

The method:

```python
def load_file(self, filename):
```

opens the supplied text file and loads its instructions.

The important logic is:

```python
with open(filename, "r") as file:
    self.instructions = [
        line.strip()
        for line in file
        if line.strip()
    ]
```

This does three things:

1. Opens the file.
2. Removes unnecessary whitespace using `strip()`.
3. Ignores empty lines.

For example, a file containing:

```text
read

istore 0

read
```

becomes:

```python
[
    "read",
    "istore 0",
    "read"
]
```

The simulator then executes these strings one by one.

---

# 5. Running the Program

The main execution method is:

```python
def run_code(self):
```

It starts by displaying:

```text
----- simulator started -----
```

Then it repeatedly executes instructions while:

```python
self.pc < len(self.instructions)
```

The current instruction is obtained with:

```python
instruction = self.instructions[self.pc]
```

The instruction is split into parts:

```python
parts = instruction.split()
opcode = parts[0]
```

For example:

```text
istore 3
```

becomes:

```python
parts = ["istore", "3"]
opcode = "istore"
```

The VM then checks which opcode it has received.

---

# 6. Supported Instructions

The simulator currently supports these instructions:

| Instruction | Purpose |
|---|---|
| `ldc value` | Push a constant onto the stack |
| `read` | Read an integer from the user |
| `istore index` | Store a stack value in a local variable |
| `iload index` | Load a local variable onto the stack |
| `iadd` | Add two stack values |
| `isub` | Subtract two stack values |
| `imul` | Multiply two stack values |
| `idiv` | Divide two stack values |
| `ifeq target` | Jump if the stack value is zero |
| `iflt target` | Jump if the stack value is negative |
| `ifgt target` | Jump if the stack value is positive |
| `print` | Print the top stack value |

---

# 7. Instruction-by-Instruction Explanation

## `ldc`

Example:

```text
ldc 10
```

`ldc` means **load constant**.

The simulator converts the operand into an integer:

```python
operand = int(parts[1])
```

and pushes it onto the stack:

```python
self.push(operand)
```

Example:

```text
Before:
[]

ldc 10

After:
[10]
```

---

# 8. `read`

Example:

```text
read
```

The VM asks the user:

```text
Enter integer:
```

The input is converted to an integer and pushed onto the operand stack.

For example, if the user enters `25`:

```text
Stack:
[25]
```

This allows the bytecode programs to accept runtime input.

---

# 9. `istore`

Example:

```text
istore 0
```

This stores the top value of the operand stack into local variable `0`.

Suppose:

```text
Stack:
[25]
```

After:

```text
istore 0
```

the state becomes:

```text
Stack:
[]

locals[0] = 25
```

The simulator directly removes the value from the stack using:

```python
value = self.stack.pop()
```

and stores it:

```python
self.locals[index] = value
```

---

# 10. `iload`

Example:

```text
iload 0
```

This retrieves the value from local variable `0` and pushes it onto the operand stack.

If:

```text
locals[0] = 25
```

then:

```text
iload 0
```

produces:

```text
Stack:
[25]
```

The implementation is:

```python
value = self.locals[index]
self.push(value)
```

---

# 11. Arithmetic Instructions

## `iadd`

Example:

```text
iload 0
iload 1
iadd
```

Suppose:

```text
locals[0] = 10
locals[1] = 20
```

Execution:

```text
iload 0
Stack: [10]

iload 1
Stack: [10, 20]

iadd
Stack: [30]
```

The VM pops the right and left operands:

```python
right = self.pop()
left = self.pop()
```

and pushes:

```python
self.push(left + right)
```

---

## `isub`

Example:

```text
iload 0
iload 1
isub
```

The operation is:

```text
left - right
```

For:

```text
left = 20
right = 5
```

the result is:

```text
15
```

The order is important because subtraction is not commutative.

---

## `imul`

Example:

```text
iload 0
iload 1
imul
```

It calculates:

```text
left * right
```

For example:

```text
10 * 5 = 50
```

---

## `idiv`

Example:

```text
iload 0
iload 1
idiv
```

It calculates:

```text
left / right
```

The simulator also checks for division by zero:

```python
if right == 0:
    print("Error: division by zero")
    break
```

This prevents an invalid division operation.

Note: the implementation uses Python's `/`, so the result can be a floating-point value.

---

# 12. Conditional Branch Instructions

The most important part of this project is the branching system.

The VM supports:

```text
ifeq
iflt
ifgt
```

These instructions use the program counter to jump to another instruction.

---

## `ifeq`

Example:

```text
ifeq 16
```

This means:

> Pop a value from the stack. If it is equal to zero, jump to instruction 16. Otherwise continue with the next instruction.

Conceptually:

```python
value = self.pop()

if value == 0:
    self.pc = target
else:
    self.pc += 1
```

This allows bytecode to represent a condition such as:

```python
if condition == 0:
    ...
```

---

## `iflt`

Example:

```text
iflt 14
```

This means:

> Pop a value. If the value is less than zero, jump to instruction 14.

The VM performs:

```python
if value < 0:
    self.pc = target
else:
    self.pc += 1
```

This is useful for comparisons.

For example:

```text
iload 0
iload 1
isub
iflt 18
```

calculates:

```text
value0 - value1
```

If the result is negative:

```text
value0 < value1
```

and the VM jumps to the target.

---

## `ifgt`

Example:

```text
ifgt 32
```

This means:

> Pop a value. If the value is greater than zero, jump to instruction 32.

For:

```text
iload 0
iload 1
isub
ifgt 32
```

the condition is effectively:

```text
value0 > value1
```

because:

```text
value0 - value1 > 0
```

---

# 13. `print`

The `print` instruction displays the value at the top of the stack.

Example:

```text
iload 3
print
```

If:

```text
locals[3] = 40
```

the output is:

```text
OUTPUT: 40
```

The implementation uses:

```python
print("OUTPUT:", self.stack[-1])
```

Notice that `print` does **not** pop the value. It only reads the top value.

---

# 14. Error Handling

The simulator contains several safety checks.

## Stack Overflow

The `push()` method checks:

```python
if len(self.stack) >= 10:
    raise Exception("Error: Operand stack overflow")
```

This limits the operand stack to 10 values.

---

## Stack Underflow

The `pop()` method checks:

```python
if len(self.stack) == 0:
    raise Exception("Error: Operand stack underflow")
```

This prevents attempting to pop from an empty stack.

---

## Empty Stack for Store

Before `istore`, the VM checks whether the stack contains a value.

If it does not:

```text
Error: stack is empty
```

---

## Arithmetic Operand Validation

The arithmetic operations check that at least two values are available.

For example, `iadd` checks:

```python
if len(self.stack) < 2:
```

If there are not enough operands, execution stops with an error.

---

## Division by Zero

`idiv` checks:

```python
if right == 0:
```

and reports:

```text
Error: division by zero
```

---

## Empty Stack for Conditional Instructions

`ifeq`, `iflt`, and `ifgt` verify that a value exists before popping it.

This prevents invalid conditional execution.

---

## Unknown Opcode

If the bytecode contains an unsupported instruction, the VM reports:

```text
Unknown opcode: <opcode>
```

and stops.

---

# 15. `matrix.txt`

`matrix.txt` contains a bytecode program that reads **eight integers** and stores them in local variables `0` through `7`.

The first part repeatedly performs:

```text
read
istore 0

read
istore 1

...

read
istore 7
```

So the input values are stored as:

```text
locals[0]
locals[1]
locals[2]
locals[3]
locals[4]
locals[5]
locals[6]
locals[7]
```

The program then adds the values in pairs.

For example:

```text
iload 0
iload 4
iadd
print
```

calculates:

```text
locals[0] + locals[4]
```

and prints the result.

The next sections calculate:

```text
locals[1] + locals[5]
locals[2] + locals[6]
locals[3] + locals[7]
```

The uploaded bytecode confirms these four pairwise additions. fileciteturn0file1L17-L30

### Logical meaning

The bytecode is equivalent to the following high-level idea:

```text
Read A
Read B
Read C
Read D
Read E
Read F
Read G
Read H

Print A + E
Print B + F
Print C + G
Print D + H
```

This resembles adding corresponding elements from two groups of four values.

The file itself does not explicitly define these values as matrices, so the safest interpretation is that it performs **four pairwise additions between the first four and last four stored values**.

---

# 16. `minmax.txt`

`minmax.txt` reads three integers and determines the minimum and maximum.

The input values are stored as:

```text
locals[0]
locals[1]
locals[2]
```

The program uses:

```text
iload 0
iload 1
isub
iflt 14
```

This calculates:

```text
locals[0] - locals[1]
```

and checks whether it is less than zero.

That is equivalent to checking:

```text
locals[0] < locals[1]
```

The bytecode then stores the smaller value in:

```text
locals[3]
```

The next comparison checks the third input against the current minimum.

The resulting minimum is printed with:

```text
iload 3
print
```

The same general strategy is then used for the maximum, stored in:

```text
locals[4]
```

and printed with:

```text
iload 4
print
```

The uploaded file shows the complete comparison flow for both the minimum and maximum. fileciteturn0file2L7-L41

### Logical algorithm

Conceptually:

```text
Read a
Read b
Read c

if a < b:
    min = a
else:
    min = b

if min < c:
    keep min
else:
    min = c

print min

if a > b:
    max = a
else:
    max = b

if max > c:
    keep max
else:
    max = c

print max
```

For example, with:

```text
25
10
40
```

the expected output is:

```text
OUTPUT: 10
OUTPUT: 40
```

---

# 17. `sort.txt`

`sort.txt` reads three integers:

```text
locals[0]
locals[1]
locals[2]
```

and sorts them in ascending order.

It uses subtraction and `iflt` to determine whether two values are in the correct order.

For example:

```text
iload 1
iload 2
isub
iflt 18
```

checks whether:

```text
locals[1] < locals[2]
```

If the condition is false, the program swaps the values using temporary local variable `4`.

The swap pattern is:

```text
iload 1
istore 4

iload 2
istore 1

iload 4
istore 2
```

This is equivalent to:

```python
temp = b
b = c
c = temp
```

The same type of comparison and swapping is performed for the other pairs.

The uploaded bytecode contains the three comparison/swap stages and finally prints locals `1`, `2`, and `3`. fileciteturn0file3L9-L43

### Important observation

The source file stores the three inputs in:

```text
locals[0]
locals[1]
locals[2]
```

but the final output uses:

```text
iload 1
print

iload 2
print

iload 3
print
```

Therefore, when describing or modifying this program, pay attention to the exact local-variable indexes used by the bytecode. The README intentionally describes what the uploaded file actually contains rather than silently changing its instructions.

---

# 18. Example Execution

Run the simulator:

```bash
python instructions.py
```

The program asks:

```text
enter your filename:
```

Enter:

```text
minmax.txt
```

The VM then asks for integers:

```text
Enter integer: 25
Enter integer: 10
Enter integer: 40
```

The bytecode instructions are executed sequentially.

The simulator maintains:

```text
PC
Stack
Locals
```

during execution.

For example, when the program executes:

```text
iload 0
iload 1
isub
```

the values are loaded from local variables, placed on the stack, and subtracted.

Then:

```text
iflt 14
```

uses the result to decide whether execution should continue normally or jump to instruction `14`.

---

# 19. How to Run the Project

## Step 1 — Install Python

Make sure Python is installed:

```bash
python --version
```

or:

```bash
py --version
```

---

## Step 2 — Put all files in one folder

Recommended structure:

```text
bytecode-simulator/
│
├── instructions.py
├── matrix.txt
├── minmax.txt
├── sort.txt
└── README.md
```

---

## Step 3 — Open the terminal

Navigate to the project directory:

```bash
cd path/to/bytecode-simulator
```

---

## Step 4 — Run the simulator

```bash
python instructions.py
```

---

## Step 5 — Select a bytecode program

When prompted:

```text
enter your filename:
```

enter one of:

```text
matrix.txt
```

or:

```text
minmax.txt
```

or:

```text
sort.txt
```

---

# 20. How Execution Works Internally

The complete VM execution cycle can be understood as:

```text
1. Create VM
       |
       v
2. Ask for bytecode filename
       |
       v
3. Load file
       |
       v
4. Store instructions in self.instructions
       |
       v
5. Set PC = 0
       |
       v
6. Fetch instruction
       |
       v
7. Split opcode and operand
       |
       v
8. Execute opcode
       |
       +--> Stack operation
       |
       +--> Local variable operation
       |
       +--> Arithmetic operation
       |
       +--> Conditional jump
       |
       +--> Print
       |
       v
9. Update PC
       |
       v
10. Repeat until program ends
```

This is essentially a simplified version of how a real bytecode interpreter works.

---

# 21. Why the Program Counter Is Important

The `pc` is especially important for conditional instructions.

Without jumps, execution would always be:

```text
0 -> 1 -> 2 -> 3 -> 4 -> ...
```

Conditional instructions change this behavior.

For example:

```text
ifeq 16
```

can cause:

```text
10 -> 16
```

instead of:

```text
10 -> 11
```

Therefore, the program counter provides **control flow**.

This is the foundation for implementing:

- conditional statements
- loops
- branching
- decision-making algorithms

in bytecode.

---

# 22. Stack-Based vs Normal Python Execution

A normal Python program might write:

```python
result = a + b
```

The bytecode simulator represents the same operation as:

```text
iload 0
iload 1
iadd
```

The VM performs the work using its operand stack.

This teaches an important programming concept:

```text
High-level code
      ↓
Lower-level instructions
      ↓
Virtual machine
      ↓
Execution
```

---

# 23. Concepts Demonstrated by This Project

This project is useful for learning several important computer science concepts.

### Virtual Machines

The Python program acts as a simple VM that interprets another instruction set.

### Bytecode

The `.txt` files contain low-level instructions rather than normal Python statements.

### Stack Machines

Arithmetic operations use an operand stack.

### Local Variable Storage

The VM provides ten local variable slots.

### Program Counter

`pc` controls instruction execution.

### Instruction Fetch and Decode

The VM fetches an instruction and extracts its opcode:

```python
instruction = self.instructions[self.pc]
parts = instruction.split()
opcode = parts[0]
```

### Arithmetic Operations

The VM implements addition, subtraction, multiplication, and division.

### Conditional Branching

`ifeq`, `iflt`, and `ifgt` provide control flow.

### Error Handling

The VM checks for stack errors, invalid arithmetic situations, and unknown instructions.

---

# 24. Project Limitations

This is an educational bytecode simulator, not a complete production virtual machine.

Current limitations include:

- Only a small set of instructions is supported.
- The operand stack is limited to 10 values.
- Only 10 local variables are available.
- The bytecode format is plain text.
- There is no assembler or compiler.
- There are no labels; jump targets are numeric instruction indexes.
- There is no type system.
- `read` accepts integers only.
- `idiv` uses Python `/`, so division can produce a floating-point result.
- Invalid local-variable indexes are not explicitly validated.
- The bytecode programs depend on carefully calculated instruction indexes for jumps.

These limitations make the project small enough to understand while still demonstrating the core ideas behind an interpreter.

---

# 25. Possible Future Improvements

The simulator could be extended with:

### More Arithmetic Instructions

```text
imod
ineg
```

### More Comparison Instructions

```text
ifeq
ifne
iflt
ifle
ifgt
ifge
```

### Unconditional Jump

```text
goto target
```

### Better Output

Add instructions such as:

```text
print
println
```

### Labels

Instead of:

```text
iflt 18
```

use:

```text
iflt LESS
```

This would make programs easier to write and understand.

### Better Error Messages

The VM could report:

- current instruction
- program counter
- stack state
- local variables
- source line

when an error occurs.

### Debug Mode

A debug mode could display:

```text
PC: 10
Instruction: iadd
Stack: [25, 40]
Locals: [25, 10, 40, 0, 0, ...]
```

after every instruction.

### More Data Types

The VM could eventually support:

```text
int
float
boolean
string
```

### Loops

With `goto` and conditional jumps, the VM could support loops.

---

# 26. Learning Value

The main purpose of this project is not simply to perform addition, sorting, or minimum/maximum calculations.

The important learning is understanding **how programs are executed at a lower level**.

For example:

```text
High-level logic:

if a < b:
    min = a
else:
    min = b
```

can be represented using:

```text
iload 0
iload 1
isub
iflt ...
```

The VM turns these low-level instructions into actual execution.

This creates a useful connection between:

```text
Algorithms
   ↓
Programming Languages
   ↓
Bytecode
   ↓
Virtual Machines
   ↓
CPU-style execution concepts
```

---

# 27. Project Structure

```text
bytecode-simulator/
│
├── instructions.py    # Bytecode virtual machine/interpreter
│
├── matrix.txt         # Bytecode for pairwise addition
│
├── minmax.txt         # Bytecode for minimum and maximum
│
├── sort.txt           # Bytecode for sorting three values
│
└── README.md          # Project documentation
```

---

# 28. Summary

This project implements a small stack-based bytecode virtual machine in Python.

`instructions.py` provides the execution engine. It loads bytecode from text files, maintains an operand stack and local variables, processes instructions using a program counter, performs arithmetic, handles conditional jumps, and prints results.

The three bytecode programs demonstrate how algorithms can be expressed using low-level instructions:

- `matrix.txt` performs four pairwise additions.
- `minmax.txt` compares three integers to determine minimum and maximum values.
- `sort.txt` uses comparisons and swaps to order three values.

Overall, the project provides a practical introduction to:

**bytecode → instruction execution → stack → local variables → program counter → branching → algorithms.**

---

## Author

**Dhanush**

Educational project for learning:

- Python
- Data Structures and Algorithms
- Virtual Machines
- Bytecode Interpreters
- Programming Language Concepts
- Low-level Program Execution
