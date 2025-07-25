from collections import deque

class Solution:
    def __init__(self, rooms):
        self.rooms = rooms

    def wallsAndGates(self):
        if not self.rooms or not self.rooms[0]:
            return
        
        rows, cols = len(self.rooms), len(self.rooms[0])
        queue = deque([])

        for row in rows:
            for col in cols:
                if self.rooms[row][col] == 0:
                    queue.append((row, col))
            
        # BFS
        while queue:
            x, y = queue.popleft()
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx = x + dx
                ny = y + dy
                
                if 0 <= nx < rows and 0 <= ny < cols and self.rooms[nx][ny]==2147483647:
                    self.rooms[nx][ny] = self.rooms[x][y] + 1
                    queue.append((nx, ny))