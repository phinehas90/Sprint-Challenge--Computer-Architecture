"""CPU functionality."""

import sys
import re


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0
        self.SP = self.reg[7] = 0xF3

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0
        pattern = "[0-1]{8}"
        if len(sys.argv) >= 2:
            try:
                with open(sys.argv[1], 'r') as f:
                    lines = f.readlines()

                    for line in lines:
                        match = re.match(pattern, line)
                        if match:
                            self.ram[address] = int(line[0:8], base=2)
                            address += 1
            except FileNotFoundError:
                print("File not found, check the name given")
                sys.exit(2)
        else:
            print("No argument provided to sys")
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            print(self.reg[reg_a] + self.reg[reg_b])
        elif op == "MUL":
            mul = self.reg[reg_a] * self.reg[reg_b]
            print(mul)
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def push(self, operand_a):
        #decrement the SP
        self.SP = (self.SP-1) % 255
        self.ram[self.SP] = self.reg[operand_a]

    def pop(self, operand):
        self.reg[operand] = self.ram[self.SP]
        self.SP = (self.SP + 1) % 255

        return self.SP

    def run(self):
        """Run the CPU."""
        self.trace()
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        print("LDI",
              LDI,
              "PRN",
              PRN,
              "HLT",
              HLT,
              "MUL",
              MUL,
              "PUSH",
              PUSH,
              "POP",
              POP,
              "CALL",
              CALL,
              "RET",
              RET,
              "WTF",
              0x00011000)

        running = True

        while running:

            IR = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == ADD:
                self.alu("ADD", operand_a, operand_b)
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                self.push(operand_a)
                self.pc += 2
            elif IR == POP:
                self.pop(operand_a)
                self.pc += 2
            elif IR == CALL:
                print('working in CALL')
                self.push(operand_a)
                self.ram[self.SP] = self.pc+2
                self.pc = self.reg[operand_a]

            elif IR == RET:
                self.pc = self.ram[self.SP]
            elif IR == HLT:
                running = False
            else:
                print("command not recoginized")
                running = False