from dataclasses import dataclass

@dataclass
class Command:
    count: int            # Repeat count
    type: str             # 'h', 'l', or 'r'
    arg: str = None       # Only for 'r' commands
    
class CommandParser:
    def __init__(self, command_str: str):
        self.command_str = command_str
        self.index = 0

    def parse(self):
        while self.index < len(self.command_str):
            count = self._read_number()
            cmd = self._next_char()

            if cmd == 'r':
                arg = self._next_char()
                yield Command(count if count is not None else 1, 'r', arg)
            else:
                yield Command(count if count is not None else 1, cmd)

    def _read_number(self):
        start = self.index
        while self.index < len(self.command_str) and self.command_str[self.index].isdigit():
            self.index += 1
        return int(self.command_str[start:self.index]) if self.index > start else None

    def _next_char(self):
        char = self.command_str[self.index]
        self.index += 1
        return char


class TextManipulator:
    def __init__(self, text: str):
        self.text = list(text)      # Mutable character buffer
        self.cursor = 0             # Current cursor position

    def apply_commands(self, command_str: str):
        parser = CommandParser(command_str)
        for cmd in parser.parse():
            self._execute(cmd)

    def _execute(self, command: Command):
        # Pattern match or use if-else chain
        if command.type == 'h':
            self.cursor = max(0, self.cursor - command.count)
        elif command.type == 'l':
            self.cursor = min(len(self.text), self.cursor + command.count)
        elif command.type == 'r':
            for i in range(command.count):
                pos = self.cursor + i
                if pos < len(self.text):
                    self.text[pos] = command.arg
            self.cursor = min(len(self.text), self.cursor + command.count)

    def get_output(self):
        return ''.join(self.text), self.cursor
    

def main():
    tm = TextManipulator("Hello World")
    tm.apply_commands("rh6l9l4hrw")
    text, cursor = tm.get_output()
    print(text)
    print(" " * cursor + "_")



if __name__ == "__main__":
    main()