from vpython import *
import random

wallThickness = .1
widthRoom = 15
heightRoom = 10
depthRoom = 1.5
mRadius = .75
side = widthRoom/2-wallThickness-mRadius
height = heightRoom/2-wallThickness-mRadius
v_ball = .01

scene = canvas(title='Games!!', width=1600, height=800, center=vector(0,0,0))

def get_random_ball(n):
  colors = [color.green, color.blue, color.red, color.cyan, color.magenta, color.orange, color.yellow, color.white, color.black]
  if n > len(colors):
    raise ValueError("Jumlah colors yang diminta melebihi jumlah colors yang tersedia.")
  # list warna, velocity, pos
  return [[i, vec(random.choice([random.uniform(-1, -0.2), random.uniform(0.2, 1)]), random.choice([random.uniform(-1, -0.2), random.uniform(0.2, 1)]), 0), vec(random.uniform(-side, side), random.uniform(-height, height), 0)] for i in random.sample(colors, n)] 


floor = box(pos=vector(0, -heightRoom/2, 0), size=vector(widthRoom, wallThickness, depthRoom), color=color.red)
ceiling = box(pos=vector(0, heightRoom/2, 0), size=vector(widthRoom, wallThickness, depthRoom), color=color.red)
backWall = box(pos=vector(0, 0, -depthRoom/2), size=vector(widthRoom, heightRoom, wallThickness), color=color.yellow)
leftWall = box(pos=vector(-widthRoom/2, 0, 0), size=vector(wallThickness, heightRoom, depthRoom), color=color.blue)
rightWall = box(pos=vector(widthRoom/2, 0, 0), size=vector(wallThickness, heightRoom, depthRoom), color=color.blue)

main_ball = sphere(pos=vec(random.uniform(-side, side), random.uniform(-height, height), 0), radius=mRadius, color=color.purple)

def move_green_ball(evt):
  direction = {
    'left': vec(-.1, 0, 0),
    'right': vec(.1, 0, 0),
    'up': vec(0, .1, 0),
    'down': vec(0, -.1, 0),
  }
  if evt.key in direction:
    main_ball.pos += direction[evt.key]

scene.bind('keydown', move_green_ball)

bola = []
random_ball = get_random_ball(5)
for warna, vel, pos in random_ball:
  bola.append(sphere(velocity=vel ,pos=pos, radius=mRadius, color=warna))


collision_mode = 'bounce'  # 'bounce' or 'stop'
collision_count = 0
collision_text = label(text=f'Collisions: {collision_count}', pos=vector(-side, height, mRadius), color=color.white)


def change_mode(x):
    global collision_mode
    global collision_count
    global collision_text
    global bola
    global main_ball
    if x.checked == True:
      if collision_mode != 'bounce':
        collision_count = 0
        collision_mode = 'bounce'
        collision_text.text = f'Collisions: {collision_count}'
        for i in bola:
          i.velocity = vec(random.choice([random.uniform(-1, -0.2), random.uniform(0.2, 1)]), random.choice([random.uniform(-1, -0.2), random.uniform(0.2, 1)]), 0)
          
    elif x.checked == False:
      if collision_mode != 'stop':
        collision_count = 0
        collision_mode = 'stop'
        collision_text.text = f'Collisions: {collision_count}'




# menu(bind=change_mode, choices=['bounce', 'stop'])

def bigBall(x):
    global mRadius
    if x.checked == True:
        mRadius = mRadius * 2
        marble.radius = mRadius
    if x.checked == False:
        mRadius = mRadius / 2
        marble.radius = mRadius

scene.append_to_caption('\n\n')

    
checkbox(bind=change_mode, text='Bounce / Stop', checked=True)

while True:
  rate(200)
  
  if main_ball.pos.x >= side:
    main_ball.pos.x -= .1
  if main_ball.pos.x <= -side:
    main_ball.pos.x += .1
  if main_ball.pos.y >= height:
    main_ball.pos.y -= .1
  if main_ball.pos.y <= -height:
    main_ball.pos.y += .1

  for ball in bola:
    ball.pos += ball.velocity * v_ball
    if abs(ball.pos.x) >= side:
      ball.velocity.x *= -1
    if abs(ball.pos.y) >= height:
      ball.velocity.y *= -1
    if mag(ball.pos - main_ball.pos) <= 2*mRadius:
      # collision_count += 1
      # print(collision_count)
      # collision_text.text = f'Collisions: {collision_count}'
      # print(collision_count)
      # print(collision_mode)
      if collision_mode == 'bounce':
        if ball.pos.x > main_ball.pos.x:
          ball.velocity.x = abs(ball.velocity.x)
          main_ball.pos.x -= .1
        else:
          ball.velocity.x = -abs(ball.velocity.x)
          main_ball.pos.x += .1

        if ball.pos.y > main_ball.pos.y:
          ball.velocity.y = abs(ball.velocity.y)
          main_ball.pos.y -= .1
        else:
          ball.velocity.y = -abs(ball.velocity.y)
          main_ball.pos.y += .1
        collision_count += 1
        collision_text.text = f'Collisions: {collision_count}'
      else:
        if not (ball.velocity.x == 0 and ball.velocity.y == 0):
          collision_count += 1
          collision_text.text = f'Collisions: {collision_count}'
        ball.velocity.x = 0
        ball.velocity.y = 0

        if ball.pos.x > main_ball.pos.x:
          # ball.velocity.x = abs(ball.velocity.x)
          main_ball.pos.x -= .1
        else:
          # ball.velocity.x = -abs(ball.velocity.x)
          main_ball.pos.x += .1

        if ball.pos.y > main_ball.pos.y:
          # ball.velocity.y = abs(ball.velocity.y)
          main_ball.pos.y -= .1
        else:
          # ball.velocity.y = -abs(ball.velocity.y)
          main_ball.pos.y += .1

    for ball2 in bola:
      if ball != ball2:
        if mag(ball.pos - ball2.pos) <= 2*mRadius:
          if ball.pos.x > ball2.pos.x:
            ball.velocity.x = abs(ball.velocity.x)
            ball2.velocity.x = -abs(ball2.velocity.x)
          else:
            ball2.velocity.x = abs(ball2.velocity.x)
            ball.velocity.x = -abs(ball.velocity.x)
          if ball.pos.y > ball2.pos.y:
            ball.velocity.y = abs(ball.velocity.y)
            ball2.velocity.y = -abs(ball2.velocity.y)
          else:
            ball2.velocity.y = abs(ball2.velocity.y)
            ball.velocity.y = -abs(ball.velocity.y)
      

          
          
          # ball.velocity *= -1


