import random


class TechburgGrid:
    def __init__(self, size):
        self.size = size
        self.grid = [[[] for _ in range(size)] for _ in range(size)]
        self.entities = []

    def wrap_coordinates(self, x, y):
        return x % self.size, y % self.size

    def place_entity(self, entity, x, y):
        x, y = self.wrap_coordinates(x, y)
        self.grid[x][y].append(entity)
        entity.x, entity.y = x, y
        if hasattr(entity, "act"):
            self.entities.append(entity)

    def move_entity(self, entity, new_x, new_y):
        self.grid[entity.x][entity.y].remove(entity)
        new_x, new_y = self.wrap_coordinates(new_x, new_y)
        self.grid[new_x][new_y].append(entity)
        entity.x, entity.y = new_x, new_y

    def update(self):
        for entity in self.entities:
            entity.act(self)


class SparePart:
    def __init__(self, size):
        self.size = size
        self.enhancement = {"small": 3, "medium": 5, "large": 7}[size]
        self.decay_rate = 0.1
        self.x = self.y = None

    def decay(self):
        self.enhancement = max(0, self.enhancement - self.decay_rate)


class SurvivorBot:
    def __init__(self, bot_type, energy=100):
        self.bot_type = bot_type
        self.energy = energy
        self.carrying = None
        self.speed = 1
        self.vision = 1
        self.x = self.y = None

    def act(self, grid):
        self.energy -= 5
        if self.energy <= 0:
            print(f"Bot at ({self.x}, {self.y}) is deactivated.")
            grid.entities.remove(self)
            grid.grid[self.x][self.y].remove(self)
            return

        for dx in range(-self.vision, self.vision + 1):
            for dy in range(-self.vision, self.vision + 1):
                x, y = grid.wrap_coordinates(self.x + dx, self.y + dy)
                for entity in grid.grid[x][y]:
                    if isinstance(entity, SparePart):
                        self.move_to(grid, x, y)
                        return

        self.move_randomly(grid)

    def move_to(self, grid, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)
        grid.move_entity(self, self.x + dx, self.y + dy)

    def move_randomly(self, grid):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        grid.move_entity(self, self.x + dx, self.y + dy)


class RechargeStation:
    def __init__(self):
        self.parts = []
        self.bots = []
        self.x = self.y = None

    def store_part(self, part):
        self.parts.append(part)

    def recharge_bot(self, bot):
        if self.parts and bot.energy < 100:
            part = self.parts.pop(0)
            bot.energy = min(100, bot.energy + part.enhancement)
