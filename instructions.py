class Bytecode:

    def __init__(self):
        self.stack = []
        self.locals = [0] * 10
        self.pc = 0
        self.instructions = []

    def push(self, value):

        if len(self.stack) >= 10:
            raise Exception("Error: Operand stack overflow")

        self.stack.append(value)

    def pop(self):

        if len(self.stack) == 0:
            raise Exception("Error: Operand stack underflow")

        return self.stack.pop()

    def load_file(self, filename):
        with open(filename, "r") as file:
            self.instructions = [
                line.strip()
                for line in file
                if line.strip()
            ]

    def run_code(self):

        print("----- simulator started -----")

        while self.pc < len(self.instructions):

            instruction = self.instructions[self.pc]

            
            parts = instruction.split()
            opcode = parts[0]

            # Push constant
            if opcode == "ldc":
                operand = int(parts[1])
                self.push(operand)
                self.pc += 1

            # Read integer
            elif opcode == "read":
                value = int(input("Enter integer: "))
                self.push(value)
                self.pc += 1

            # Store in local variable
            elif opcode == "istore":
                index = int(parts[1])

                if len(self.stack) == 0:
                    print("Error: stack is empty")
                    break

                value = self.stack.pop()
                self.locals[index] = value
                self.pc += 1

            # Load local variable
            elif opcode == "iload":
                index = int(parts[1])
                value = self.locals[index]
                self.push(value)
                self.pc += 1

            # Addition
            elif opcode == "iadd":
                if len(self.stack) < 2:
                    print("Error: not enough values for iadd")
                    break

                right = self.pop()
                left = self.pop()

                self.push(left + right)
                self.pc += 1

            # Subtraction
            elif opcode == "isub":
                if len(self.stack) < 2:
                    print("Error: not enough values for isub")
                    break

                right = self.pop()
                left = self.pop()

                self.push(left - right)
                self.pc += 1

            # Multiplication
            elif opcode == "imul":
                if len(self.stack) < 2:
                    print("Error: not enough values for imul")
                    break

                right = self.pop()
                left = self.pop()

                self.push(left * right)
                self.pc += 1

            # Division
            elif opcode == "idiv":
                if len(self.stack) < 2:
                    print("Error: not enough values for idiv")
                    break

                right = self.pop()
                left = self.pop()

                if right == 0:
                    print("Error: division by zero")
                    break

                self.push(left / right)
                self.pc += 1

            # Jump if equal to zero
            elif opcode == "ifeq":
                target = int(parts[1])

                if len(self.stack) == 0:
                    print("Error: stack is empty for ifeq")
                    break

                value = self.pop()

                if value == 0:
                    self.pc = target
                else:
                    self.pc += 1

            # Jump if less than zero
            elif opcode == "iflt":
                target = int(parts[1])

                if len(self.stack) == 0:
                    print("Error: stack is empty for iflt")
                    break

                value = self.pop()

                if value < 0:
                    self.pc = target
                else:
                    self.pc += 1

            # Jump if greater than zero
            elif opcode == "ifgt":
                target = int(parts[1])

                if len(self.stack) == 0:
                    print("Error: stack is empty for ifgt")
                    break

                value = self.pop()

                if value > 0:
                    self.pc = target
                else:
                    self.pc += 1

            # Print
            elif opcode == "print":

                if len(self.stack) == 0:
                    print("Error: nothing to print")
                    break

                print("OUTPUT:", self.stack[-1])
                self.pc += 1

            # Unknown instruction
            else:
                print("Unknown opcode:", opcode)
                break

           

        print("-----------------------------")
       
        print("----- simulator ended ------")


vm = Bytecode()

file=input("enter your filename:")
vm.load_file(file)

vm.run_code()