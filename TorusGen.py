import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("9 Torus Orbit")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("comicsans", 16)

square_width = 400
square_height = 400
square_x = 130
square_y = 130

class Body:
    AU = 1.496e11
    G = 6.67428e-11
    SCALE = 80 / AU
    TIMESTEP = 3600*24*1

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.star = False
        self.distance_to_star = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        global point
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
            updated_points = []
            for i, point in enumerate(self.orbit):
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

                if i > 0:
                    prev_x, prev_y = updated_points[i - 1]
                    distance = ((x - prev_x) ** 2 + (y - prev_y) ** 2) ** 0.5
                    if distance < 50:
                        pygame.draw.line(win, self.color, (prev_x, prev_y), (x, y), 2)

        pygame.draw.rect(WIN, WHITE, (square_x, square_y, square_width, square_height), 2)
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.star:
            self.distance_to_star = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, bodies):
        if not self.star:
            total_fx = total_fy = 0
            for n in bodies:
                if self == n:
                    continue

                fx, fy = self.attraction(n)
                total_fx += fx
                total_fy += fy

            self.x_vel += total_fx / self.mass * self.TIMESTEP
            self.y_vel += total_fy / self.mass * self.TIMESTEP

            self.x += self.x_vel * self.TIMESTEP
            self.y += self.y_vel * self.TIMESTEP
            self.orbit.append((self.x, self.y))

            if not self.star:
                if self.y > ((square_y + square_height) - (HEIGHT/2)) / (Body.AU * Body.SCALE) * Body.AU:
                    self.y = (square_y - (HEIGHT/2)) / (Body.AU * Body.SCALE) * Body.AU
                if self.y < (square_y - (HEIGHT/2)) / (Body.AU * Body.SCALE) * Body.AU:
                    self.y = ((square_y + square_height) - (HEIGHT/2)) / (Body.AU * Body.SCALE) * Body.AU
                if self.x > ((square_x + square_width) - (WIDTH/2)) / (Body.AU * Body.SCALE) * Body.AU:
                    self.x = (square_x - (WIDTH/2)) / (Body.AU * Body.SCALE) * Body.AU
                if self.x < (square_x - (WIDTH/2)) / (Body.AU * Body.SCALE) * Body.AU:
                    self.x = ((square_x + square_width) - (WIDTH/2)) / (Body.AU * Body.SCALE) * Body.AU

def main():
    run = True
    clock = pygame.time.Clock()
    number = 701
    xnum = math.floor(number/2)

    satellite = Body(-1 * Body.AU, 0 * Body.AU, 10, WHITE, 5.9742e24)
    satellite.y_vel = 49.783e3
    satellite.x_vel = 3e3
    bodies = [satellite]

    suns = []
    for i in range(0, number):
        suns.append([])
        for j in range(0, number):
            suns[i].append(Body(((((square_width/Body.SCALE)/Body.AU)*i) - (((number -1)/2)*((square_width/Body.SCALE)/Body.AU))) * Body.AU,
                                ((((square_height/Body.SCALE)/Body.AU)*j) - (((number -1)/2)*((square_height/Body.SCALE)/Body.AU))) * Body.AU,
                                20, WHITE, 1.98892e30))
            suns[i][j].star = True
            bodies.append(suns[i][j])

    clock_value = 45
    elapsed_time = 0

    paused = False
    while run:
        clock.tick(clock_value)
        WIN.fill((0, 0, 0))
        elapsed_time += (Body.TIMESTEP / (3600 * 24)) / 365
        time_text = FONT.render(f"{round(elapsed_time, 5)} normal yrs", 1, WHITE)
        #WIN.blit(time_text, (100, 100))

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_SPACE]:
                paused = True
            if keys[pygame.K_EQUALS]:
                paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for n in bodies:
            n.update_position(bodies)
            n.draw(WIN)

        if not paused:
            pygame.display.update()
        #satellite.draw(WIN)
        #suns[xnum][xnum].draw(WIN)

    pygame.quit()

main()