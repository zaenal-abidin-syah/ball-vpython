from vpython import *
import random

box_size = 20
scene = canvas(title = "Bola Ungu Vpython", size= box_size, center = vector(0,0,0))
scene.userzoom = False
killer = False


wall_left = box(pos=vector(-box_size*1.15, 0, 0), size=vector(0.2, box_size*2.3, box_size*2.3), color=color.gray(0.5))
wall_right = box(pos=vector(box_size*1.15, 0, 0), size=vector(0.2, box_size*2.3, box_size*2.3), color=color.gray(0.5))
wall_top = box(pos=vector(0, box_size*1.15, 0), size=vector(box_size*2.3, 0.2, box_size*2.3), color=color.gray(0.5))
wall_bottom = box(pos=vector(0, -box_size*1.15, 0), size=vector(box_size*2.3, 0.2, box_size*2.3), color=color.gray(0.5))
wall_back = box(pos=vector(0, 0, -box_size*1.15), size=vector(box_size*2.3, box_size*2.3, 0.2), color=color.gray(0.5))


def makeBall(jumlahBola, box_size, ball_radius):
    result = []
    for ball in range(jumlahBola):
        if ball>0 :
            random_position = None
            for ball_position in result:
                while random_position == None or mag(ball_position.pos - random_position) <= ball_radius*2:                             
                    random_position = vector(random.uniform(-box_size, box_size), random.uniform(-box_size, box_size), 0)
        else:
            random_position = vector(random.uniform(-box_size, box_size), random.uniform(-box_size, box_size), 0)
        result.append(sphere(pos=random_position, radius = ball_radius, velocity = vector(0.1, 0.1, 0), state="alive", kill = 0))
    return result

def coloring_ball(ball_vault):
    for i in range(len(ball_vault)):
        color = vector(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        color = check_color_existence(ball_vault, color)
        balls[i].color = color
        if i == 0:
            balls[i].color = vector(200, 0 , 255)
            balls[i].velocity = vector(0, 0, 0)
            balls[i].tujuan = vector(0, 0, 0)
    return ball_vault

def check_color_existence(ball_vault, color):
    for ball in ball_vault:
        while color == ball.color:
            color = vector(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color

def check_collision(ball1, ball2, iteration):
    dist = mag(ball1.pos - ball2.pos)
    if dist <= ball1.radius + ball2.radius:
        m1 = ball1.radius**3
        v1 = ball1.velocity
        if iteration == 0:
            if balls[0].tujuan == vector(0, 0, 0):
                ball2.velocity *= -1
                return None
            else:
                v1 = balls[0].tujuan
        v2 = ball2.velocity
        m2 = ball2.radius**3
        new_v1 = v1 - 2 * m2 / (m1 + m2) * dot(v1 - v2, ball1.pos - ball2.pos) / mag(ball1.pos - ball2.pos)**2 * (ball1.pos - ball2.pos)
        new_v2 = v2 - 2 * m1 / (m1 + m2) * dot(v2 - v1, ball2.pos - ball1.pos) / mag(ball2.pos - ball1.pos)**2 * (ball2.pos - ball1.pos)
        if ball1.state == "alive" and ball2.state == "alive":
            ball1.velocity = new_v1
            ball2.velocity = new_v2

def dead_trigger(current_ball, deadly_ball, iteration, killer):
    poin = 1
    ketidakpastian = 0.1
    if killer:
        if iteration == 0:
            return None
        if mag(current_ball.pos - deadly_ball.pos) <= (current_ball.radius*2) + ketidakpastian:
            current_ball.velocity = vector(0, 0, 0)
            if current_ball.state == "alive":
                deadly_ball.kill += poin
            current_ball.state = "die"

def Keyboard(key_event):
    key = key_event.key
    speed = 0.1 * 7.25
    if key == 'up' and balls[0].pos.y <= box_size:
        balls[0].pos.y += speed
        balls[0].tujuan.y = 0 + speed
    if key == 'down' and balls[0].pos.y >= -box_size:
        balls[0].pos.y -= speed
        balls[0].tujuan.y = 0 - speed
    if key == 'right' and balls[0].pos.x <= box_size:
        balls[0].pos.x += speed
        balls[0].tujuan.x = 0 + speed
    if key == 'left' and balls[0].pos.x >= -box_size:
        balls[0].pos.x -= speed
        balls[0].tujuan.x = 0 - speed

def safeball():
    global killer
    killer = False

def deathball():
    global killer
    killer = True


scene.bind('keydown',Keyboard)
scene.append_to_caption('\n\n')

button(bind = safeball, text = "menabrak memantul", background=color.green)
scene.append_to_caption('             ')
button(bind = deathball, text = "menabrak berhenti", background=color.red)

scene.append_to_caption('\n\n')

balls = makeBall(5, box_size, 2)
balls = coloring_ball(balls)

kecepatan = 1
while True:
    rate(100)
    for i in range(len(balls)):
        if i != 0:
            balls[i].pos += (balls[i].velocity * kecepatan)
        if abs(balls[i].pos.x) >= box_size:
            balls[i].velocity.x *= -1
        if abs(balls[i].pos.y) >= box_size:
            balls[i].velocity.y *= -1
        # Hit DeadlyBall Condition
        dead_trigger(balls[i], balls[0], i, killer)
        # Cek Collision
        for j in range(i + 1, len(balls)):
            check_collision(balls[i], balls[j], i)
        
    label(text = f"Points = {balls[0].kill}", pos=vector(box_size, box_size, 0))
    balls[0].tujuan = vector(0, 0, 0)