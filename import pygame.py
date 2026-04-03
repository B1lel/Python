import pygame
import serial
import math
import re

# ---------------- CONFIG ----------------

PORT = "COM4"      # à adapter
BAUD = 115200

MAX_DISTANCE = 50  # cm affichés max
ANGLE_SPEED = 1.5   # vitesse balayage

WIDTH = 900
HEIGHT = 700

CENTER = (WIDTH//2, HEIGHT//2 + 150)
RADIUS = 300

# ----------------------------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultrasonic Radar")
3
clock = pygame.time.Clock()

green = (0,255,0)
dark_green = (0,80,0)
black = (0,0,0)

font = pygame.font.SysFont("consolas",20)

# serial
ser = serial.Serial(PORT, BAUD, timeout=0.05)

angle = 0
blips = []

def draw_radar_background():

    pygame.draw.circle(screen, dark_green, CENTER, RADIUS, 2)

    for i in range(1,5):
        pygame.draw.circle(screen, dark_green, CENTER, int(RADIUS*i/5),1)

    for a in range(0,181,30):

        x = CENTER[0] + RADIUS*math.cos(math.radians(a))
        y = CENTER[1] - RADIUS*math.sin(math.radians(a))

        pygame.draw.line(screen,dark_green,CENTER,(x,y),1)


def draw_sweep():

    global angle

    x = CENTER[0] + RADIUS*math.cos(math.radians(angle))
    y = CENTER[1] - RADIUS*math.sin(math.radians(angle))

    pygame.draw.line(screen,green,CENTER,(x,y),3)

    angle += ANGLE_SPEED
    if angle > 180:
        angle = 0


def draw_blips():

    for b in blips:

        x,y,strength = b

        color = (0, int(255*strength),0)

        pygame.draw.circle(screen,color,(int(x),int(y)),5)

        b[2] -= 0.02

    blips[:] = [b for b in blips if b[2] > 0]


def add_blip(distance):

    if distance > MAX_DISTANCE or distance <=0:
        return

    d = distance/MAX_DISTANCE

    r = d * RADIUS

    x = CENTER[0] + r*math.cos(math.radians(angle))
    y = CENTER[1] - r*math.sin(math.radians(angle))

    blips.append([x,y,1])


def read_serial():

    try:

        line = ser.readline().decode(errors="ignore")

        match = re.search(r'\d+', line)

        if match:
            return int(match.group())

    except:
        pass

    return None


# ---------------- MAIN LOOP ----------------

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    draw_radar_background()

    distance = read_serial()

    if distance:
        add_blip(distance)

    draw_blips()

    draw_sweep()

    txt = font.render("Radar HC-SR04",True,green)
    screen.blit(txt,(20,20))

    pygame.display.update()

    clock.tick(60)

pygame.quit()