import pygame
import random 
from tkinter import *
from tkinter import messagebox
import time



# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 500x500 sized screen
screen = pygame.display.set_mode([500, 500])
 
# Set the title of the window
pygame.display.set_caption('Snake Example')
 
allspriteslist = pygame.sprite.Group()



# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
red = (255,0,0)
yellow =(255,255,0) 

#list of coordinats to choose from
list1= list(range (20,460,20))
list2= list(range (40,460,20))

# Set the width and height of each snake segment
segment_width = 20
segment_height = 20

 
#snake length
snake_length=1

# Create an initial snake
snake_segments = []

#load  images for background
sand= pygame.image.load('./images/sand.png')

#load image for snakes skin
skin = pygame.image.load('./images/skin.png')

#load fruit images
orange = pygame.image.load('./images/orange.png')
plum = pygame.image.load('./images/plum.png')
apple = pygame.image.load('./images/apple.png')
strawberry = pygame.image.load('./images/strawberry.png')
fruit=[orange,plum,apple,strawberry]

#add sounds
eat= pygame.mixer.Sound('./sounds/eat.wav')
music= pygame.mixer.music.load('./sounds/music.mp3')
pygame.mixer.music.play(-1)

#load clock to change frame rate
clock = pygame.time.Clock()

		
class Segment(pygame.sprite.Sprite):
	""" Class to represent one segment of the snake. """
	# -- Methods
	# Constructor function
	
	def __init__(self, x, y):
		# Call the parent's constructor
		super().__init__()
		
		# Set height, width
		self.image = skin

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		#list to store snakes head coords
		self.snake=[x,y]


		
#class to hold the food
class Food():
	# ~ x= random.choice(list1)
	# ~ y= random.choice(list2)
	x=220
	y= 200
	def __init__(self):
		# initiate x,y
		self.fcoords=[self.x,self.y]
	
		#add image
		self.fruits = random.choice(fruit)
	
	def updateFood(self):
		"""function to update the position after food has been eaten"""
		Food.x= random.choice(list1) 
		Food.y=random.choice(list2)
		self.fruits = random.choice(fruit)
		self.fcoords=[Food.x,Food.y]
		
		
#score_total=0
class Score():
	score_total=0
	def __init__(self):
		#Font style
		self.font = pygame.font.Font('freesansbold.ttf', 20)  
		self.text = self.font.render('Score '+str(self.score_total), True, (0,255,0), (0,0,0)) 
		self.textRect = self.text.get_rect() 
		self.textRect.center = (250,20)

	def update_score(self): 
		Score.score_total+=1
				
def game():
	"""Function to contain game logic"""
	
	# Set initial speed
	x_change = segment_width
	y_change = 0

	
		
	
	#initialise snake 
	for i in range(2):
		x = 200 
		y = 200
		segment = Segment(x, y)
		snake_segments.append(segment)
		allspriteslist.add(segment)
			


	#initialise food 
	food = Food()
	done = False
	 
	while not done:
		#initialise score
		score= Score()	
	 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				
				done = True
	 
			# ~ # Set the speed based on the key pressed
			# ~ # We want the speed to be enough that we move a full
			# ~ # segment, plus the margin.
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:			 
					x_change = (segment_width) * -1
					y_change = 0
				if event.key == pygame.K_RIGHT:				
					x_change = (segment_width)
					y_change = 0
				if event.key == pygame.K_UP:				
					x_change = 0
					y_change = (segment_height) * -1
				if event.key == pygame.K_DOWN: 				
					x_change = 0
					y_change = (segment_height)
					
		#uncomment this to allow 
		#snakes head to leave screen re-appear at far side of screen
		#if segment.rect.x == 480:segment.rect.x =0
		#elif segment.rect.x == 0:segment.rect.x =480				
		#if segment.rect.y == 480:segment.rect.y =40
		#elif segment.rect.y == 40:segment.rect.y =480
		
		#uncomment this to allow 
		#snakes head to leave screen re-appear at far side of screen
		if segment.rect.x == 480:segment.rect.x =0
		elif segment.rect.x == 0:segment.rect.x =480				
		if segment.rect.y == 480:segment.rect.y =40
		elif segment.rect.y == 40:segment.rect.y =480
			
		# ~ # if snake head touches side die
		# ~ if segment.rect.x == 480 or segment.rect.x== 0:done= True			
		# ~ if segment.rect.y == 480 or segment.rect.y== 60:done= True
		
		#test to see if snake eats food					
		if segment.snake == food.fcoords:
			eat.play()
				
			#Remove old food and add new food
			allspriteslist.remove(food)
			food.updateFood()
			
			# add new segment to snake  by invoking Segment class again
			segment=Segment(segment.rect.x,segment.rect.y)
			snake_segments.append(segment)
			#allspriteslist.add(body)
							  
			#update score
			score.update_score()
						
		#Test to see if snake bites its tail
		coords=[]		
		length_s= len(snake_segments)
		for i in range(1,length_s):
			coords.append(snake_segments[i].snake)	   
			if coords[0] in coords[1:]:
				done = True
				endGame()
						
		#remove last segement of the snake		 		
		old_segment = snake_segments.pop()
		allspriteslist.remove(old_segment)
	 
		# Figure out where new segment will be
		x = snake_segments[0].rect.x + x_change
		y = snake_segments[0].rect.y + y_change
		segment = Segment(x, y)
	 
		# Insert new segment into the list
		snake_segments.insert(0, segment)
		allspriteslist.add(segment)
		
		# -- Draw everything
		# Clear screen
		screen.fill(BLACK)
		
		#Draw background
		screen.blit(sand,(0,0))
		
		#Create box at the top of screen t
		pygame.draw.rect(screen,BLACK,(0,0, 500,40))
		
		#Draw fruit
		screen.blit(food.fruits,(food.x,food.y))
		
		#Draw Score
		screen.blit(score.text, score.textRect)		 
		allspriteslist.draw(screen)
		
		# Flip screen
		pygame.display.flip()
	 
		# Adjust number to increase frame rate
		clock.tick(10)
	
	pygame.quit()

game()


