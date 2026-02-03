import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Clock to control frame rate
clock = pygame.time.Clock()

# 3D Point class
class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotateX(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        self.y = y
        self.z = z

    def rotateY(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        self.z = z
        self.x = x

    def rotateZ(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        self.x = x
        self.y = y

    def project(self, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return int(x), int(y)

# Define cube vertices
vertices = [
    Point3D(-1, 1, -1), Point3D(1, 1, -1),
    Point3D(1, -1, -1), Point3D(-1, -1, -1),
    Point3D(-1, 1, 1), Point3D(1, 1, 1),
    Point3D(1, -1, 1), Point3D(-1, -1, 1)
]

# Main loop
running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for vertex in vertices:
        vertex.rotateX(1)
        vertex.rotateY(1)
        vertex.rotateZ(1)
    
    projected_points = [
        vertex.project(width, height, 256, 4)
        for vertex in vertices
    ]

    # Draw vertices
    for point in projected_points:
        pygame.draw.circle(screen, (255, 255, 255), point, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
