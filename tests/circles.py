#Kivy + Box2d test

from Box2D import *

from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string('''
<Circle>:
    canvas:
        Color:
            hsv: self.hue, 1, 1
        Ellipse:
            pos: self.x - self.radius, self.y - self.radius
            size: self.radius * 2, self.radius * 2
''')

class Circle(Widget):
	radius = NumericProperty(20)
	hue = NumericProperty(0)

	# for physics
	world = ObjectProperty(None)
	_body = ObjectProperty(None)
	def __init__(self, **kwargs):
		super(Circle, self).__init__(**kwargs)
		self.hue = random()

		self._body = body=self.world.CreateDynamicBody(
            position=self.pos,
            fixtures=b2FixtureDef(
                        shape=b2CircleShape(radius=self.radius),
                        density=0.2,
                        )
                )

	def update_from_body(self):
		self.pos = self._body.position.x, self._body.position.y


class TestApp(App):
	def generate(self, instance, touch):
		c = Circle(pos=touch.pos, world=self.world)
		self.circles.append(c)
		self.root.add_widget(c)

	def build(self):
		canvas = Widget()
		canvas.bind(on_touch_move=self.generate)
		self.world = world = b2World((0,-10), True)

		ground = self.world.CreateStaticBody(
			shapes=b2EdgeShape(vertices=[(-4000,0),(40000,0)]) 
			)

		ground.position.Set(0,0)
		self.circles = []
		for x in range(0,5):
			c = Circle(y=500 + x*5, x=500+x, world=world)
			self.circles.append(c)
			canvas.add_widget(c)

		Clock.schedule_interval(self._update_world,1/60.)

		return canvas

	def _update_world(self, dt):
		self.world.Step(dt, 10, 8)
		for child in self.circles:
			child.update_from_body()

TestApp().run()