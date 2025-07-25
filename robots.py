class Robot:
    def __init__(self, x=0, y=0, direction='N'):
        self.x = x
        self.y = y
        self.directions = ['N', 'E', 'S', 'W']
        self.direction = direction
        self.direction_index = self.directions.index(direction)
    
    def turn_left(self):
        self.direction_index = (self.direction_index - 1) % 4
        self.direction = self.directions[self.direction_index]
    
    def turn_right(self):
        self.direction_index = (self.direction_index + 1) % 4
        self.direction = self.directions[self.direction_index]

    def move(self):
        if self.direction == 'N':
            self.y += 1
        elif self.direction == 'E':
            self.x += 1
        elif self.direction == 'S':
            self.y -= 1
        elif self.direction == 'W':
            self.x -= 1
    
    def get_status(self):
        return f"Position: ({self.x}, {self.y}), Direction: {self.direction}"
    
def main():
    robot = Robot()
    command = input("< ").strip().upper()
    while True:
        if command == "Q":
            break
        elif command == "L":
            robot.turn_left()
            robot.get_status()
        elif command == "R":
            robot.turn_right()
            robot.get_status
        elif command == "M":
            robot.move()
            robot.get_status()

if __name__ == "__main__":
    main()

