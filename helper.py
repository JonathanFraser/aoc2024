from dataclasses import dataclass

@dataclass(frozen=True)
class Point():
    x : int
    y : int

    def double(self):
        return Point(2*self.x,self.y)
    
    def right(self):
        return Point(self.x+1,self.y)

    def left(self):
        return Point(self.x-1,self.y)

    def up(self):
        return Point(self.x,self.y-1)

    def down(self):
        return Point(self.x,self.y+1)
    
    def l1dist(self,other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def move(self,d):
        if d == "<":
            return self.left()
        if d == ">":
            return self.right()
        if d == "^":
            return self.up()
        if d == "v":
            return self.down()
    
    def within(self,grid):
        return self.x >= 0 and self.x < grid[0] and self.y >= 0 and self.y < grid[1]