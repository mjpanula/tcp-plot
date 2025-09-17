import threading
import time
import socket
import pygame
import random
import struct

points = []  # tämä on globaali lista johon socketti kirjoittaa
             # ja jota käyttöliittymä lukee
             # tästä aiheutuu nyt lukitus eli deadlock
             # tai jonkunlainen race-condition
             # tämä pitäisi nyt korjata jonon avulla

def socket_thread(name):
    HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received {data!r}")
                now = time.time()
                for i in range(0, len(data), 4):
                    if i + 4 <= len(data):
                        value = struct.unpack('!f', data[i:i+4])[0]
                        points.append((now, value))                

if __name__ == "__main__":
    # käynnistä socketkommunikaatiosäie
    s = threading.Thread(target=socket_thread, args=(1,))
    s.start()

    # käynnistä graafinen käyttöliittymä
    WIDTH, HEIGHT = 800, 400
    PLOT_MARGIN = 50
    PLOT_WIDTH = WIDTH - 2 * PLOT_MARGIN
    PLOT_HEIGHT = HEIGHT - 2 * PLOT_MARGIN
    ROLLING_SECONDS = 10  # seconds to show on x-axis
    FPS = 60

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Rolling X,Y Plot')
    clock = pygame.time.Clock()

    start_time = time.time()

    running = True
    while running:

        # Remove points outside rolling window
        now = time.time()
        points = [(t, y) for (t, y) in points if t >= now - ROLLING_SECONDS]

        # Draw background
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (200, 200, 200), (PLOT_MARGIN, PLOT_MARGIN, PLOT_WIDTH, PLOT_HEIGHT), 2)

        # Draw points
        if points:
            min_y, max_y = -1, 1  # fixed for proof of concept
            min_x = now - ROLLING_SECONDS
            max_x = now
            plot_points = []
            for t, y in points:
                px = PLOT_MARGIN + int((t - min_x) / (max_x - min_x) * PLOT_WIDTH)
                py = PLOT_MARGIN + int((1 - (y - min_y) / (max_y - min_y)) * PLOT_HEIGHT)
                plot_points.append((px, py))
            if len(plot_points) > 1:
                pygame.draw.lines(screen, (0, 255, 0), False, plot_points, 2)
            for pt in plot_points:
                pygame.draw.circle(screen, (255, 0, 0), pt, 3)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


