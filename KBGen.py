import pygame
import math
pygame.init() #hello

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("9 Torus Orbit")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("comicsans", 16)

square_width = 400
square_height =400
square_x = 230
square_y = 150


class Body:
    AU = 1.496e11
    G = 6.67428e-11
    SCALE = 100 / AU
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

        if not self.star:
            distance_text = FONT.render(f"{round(self.distance_to_star/1000, 1)}km", 1, WHITE)
            #win.blit(distance_text, (x, y + distance_text.get_height()/2))

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
        center = ((square_x + (square_width / 2)) - (WIDTH / 2)) / (Body.AU * Body.SCALE) * Body.AU
        hasChanged = False

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

                if self.y > ((square_y + square_height) - (HEIGHT / 2)) / (Body.AU * Body.SCALE) * Body.AU:
                    self.y = (square_y - (HEIGHT / 2)) / (Body.AU * Body.SCALE) * Body.AU
                    self.x_vel = -self.x_vel


                    if self.x > center:
                        self.x = center - (self.x - center)
                        hasChanged = True

                    if (self.x < center) & hasChanged == False:
                        self.x = center + (center - self.x)

                if self.y < (square_y - (HEIGHT / 2)) / (Body.AU * Body.SCALE) * Body.AU:
                    self.y = ((square_y + square_height) - (HEIGHT / 2)) / (Body.AU * Body.SCALE) * Body.AU
                    self.x_vel = -self.x_vel


                    if self.x > center:
                        self.x = center - (self.x - center)
                        hasChanged = True
                    if (self.x < center) & hasChanged == False:
                        self.x = center + (center - self.x)

                if self.x > ((square_x + square_width) - (WIDTH / 2)) / (Body.AU * Body.SCALE) * Body.AU:
                    self.x = (square_x - (WIDTH / 2)) / (Body.AU * Body.SCALE) * Body.AU
                if self.x < (square_x - (WIDTH / 2)) / (Body.AU * Body.SCALE) * Body.AU:
                    self.x = ((square_x + square_width) - (WIDTH / 2)) / (Body.AU * Body.SCALE) * Body.AU



def main():
    run = True
    clock = pygame.time.Clock()

    number = 27
    xnum = math.floor(number/2)

    satellite = Body(-1 * Body.AU, 0 * Body.AU, 10, WHITE, 5.9742e24)
    satellite.y_vel = 29.783e3
    satellite.x_vel = 3e3
    bodies = [satellite]

    a = square_width - (400 - square_x)
    b = (400 - square_x) - a

    suns = []
    for i in range(0, number):
        suns.append([])
        for j in range(0, number):
            if (j % 2) == 1:
                suns[i].append(Body((((((square_width/Body.SCALE)/Body.AU)*i) - (((number -1)/2)*((square_width/Body.SCALE)/Body.AU))) - ((b / Body.SCALE) / Body.AU))* Body.AU,
                                ((((square_height/Body.SCALE)/Body.AU)*j) - (((number -1)/2)*((square_height/Body.SCALE)/Body.AU))) * Body.AU,
                                20, WHITE, 1.98892e30))
                suns[i][j].star = True
                bodies.append(suns[i][j])
            else:
                suns[i].append(Body(((((square_width/Body.SCALE)/Body.AU)*i) - (((number -1)/2)*((square_width/Body.SCALE)/Body.AU))) * Body.AU,
                                ((((square_height/Body.SCALE)/Body.AU)*j) - (((number -1)/2)*((square_height/Body.SCALE)/Body.AU))) * Body.AU,
                                20, WHITE, 1.98892e30))
                suns[i][j].star = True
                bodies.append(suns[i][j])

    clock_value = 45
    elapsed_time = 0

    while run:
        clock.tick(clock_value)
        WIN.fill((0, 0, 0))
        elapsed_time += (Body.TIMESTEP / (3600 * 24)) / 365
        time_text = FONT.render(f"{round(elapsed_time, 5)} normal yrs", 1, WHITE)
        #WIN.blit(time_text, (100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for n in bodies:
            n.update_position(bodies)
            n.draw(WIN)
            #n.draw(WIN)
        #satellite.draw(WIN)
        #suns[xnum][xnum].draw(WIN)

        pygame.display.update()

    pygame.quit()

main()