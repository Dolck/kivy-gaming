#Kivy + Box2d test
#Not working...

from Box2D import *

from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string('''
<PongBall>:
    canvas:
        Color:
            hsv: self.hue, 1, 1
        Ellipse:
            pos: self.x - self.radius, self.y - self.radius
            size: self.radius * 2, self.radius * 2

<PongPaddle>:
    size: 25, 200
    canvas:
        Rectangle:
            pos:self.pos
            size:self.size
''')


class PongPaddle(Widget):
	score = NumericProperty(0)

	def __init__(self, **kwargs):
		super(PongPaddle,self).__init__(**kwargs)



class PongBall(Widget):
	radius = NumericProperty(20)
	hue = NumericProperty(0)

	# for physics
	world = ObjectProperty(None)
	_body = ObjectProperty(None)
	speed = 100
	def __init__(self, **kwargs):
		super(PongBall, self).__init__(**kwargs)
		
		self._body = body = self.world.CreateDynamicBody(
			position = self.pos,
			linearDamping=0
			)
		fix = body.CreateCircleFixture(
			radius = self.radius,
			density = 0,
			restitution = 1,
			friction=0
			)
		self.hue = random()

	def update_from_body(self):
		#constant speed
		vel = self._body.linearVelocity
		if(vel.length > 0  and (vel.length > 1.05 or vel.length < 0.95)):
			t = self.speed/vel.length
			vel.x = vel.x*t
			vel.y = vel.y*t
			self._body.linearVelocity = vel
		self.pos = self._body.position.x, self._body.position.y


class PongGame(App):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	def touchdown(self, instance, touch):
		self.serve_ball()

	def serve_ball(self):
		vel = self.ball._body.linearVelocity
		vel.x = random()-0.5
		vel.y = random()-0.5
		self.ball._body.linearVelocity = vel

		#self.ball._body.SetPosition(b2Vec2(200,200))
		self.ball._body.SetTransform(b2Vec2(200,200),0)
		#self.ball._body.position.x = 200
		#self.ball._body.position.y = 200

	def build(self):
		canvas = Widget()
		canvas.bind(on_touch_down=self.touchdown)
		self.world = world = b2World((0,-10), True)

		edges = self.world.CreateStaticBody(
			shapes=b2EdgeShape(vertices=[(-4000,0),(0,4000)]) 
			)
		edges.position.Set(0,0)

		self.ball = ball = PongBall(y=200,x=200,world=world)
		canvas.add_widget(ball)

		self.serve_ball()

		Clock.schedule_interval(self.update, 1/60)
		return canvas

	def update(self, dt):
		self.world.Step(dt, 10, 8)
		self.ball.update_from_body()
		

PongGame().run()