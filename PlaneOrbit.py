#Final program for simulating motion in infinite, flat plane

import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Orbit")

WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("calibri", 16)


class Body:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24 * 1

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
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []

            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.star:
            distance_text = FONT.render(f"{round(self.distance_to_star / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x, y + distance_text.get_height()))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.star:
            self.distance_to_star = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, bodies):
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


def main():
    run = True
    clock = pygame.time.Clock()
    star = Body(0, 0, 30, WHITE, 1.98892e30)
    star.star = True
    satellite = Body(-1 * Body.AU, 0, 15, WHITE, 5.9742e24)
    satellite.y_vel = 29.783e3

    bodies = [star, satellite]

    clock_value = 45
    elapsed_time = 0

    while run:
        clock.tick(clock_value)
        WIN.fill((0, 0, 0))
        elapsed_time += (Body.TIMESTEP / (3600 * 24)) / 365
        time_text = FONT.render(f"{round(elapsed_time, 5)}yrs", 1, WHITE)
        #WIN.blit(time_text, (100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for n in bodies:
            n.update_position(bodies)
            n.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
