import pygame
from pygame.math import Vector2 as vector
from settings import * 
from random import randint
from os import walk, path,listdir
import sys 
from randommaths import RandomMathsProblems

class AssetLoader():
	def __init__(self,path) -> None:
		self.path=self.resource_path(path)
		self.assets=[]
		self.import_images()
		

	def resource_path(self,relative_path):
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except Exception:
			base_path = path.abspath(".")

		return path.join(base_path, relative_path) 
	
	def import_images(self):
		
		for filename in listdir(self.path):
			
			if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
				self.assets.append(pygame.image.load(path.join(self.path, filename)).convert_alpha())

	def get_assets(self):
		return(self.assets)


class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset=vector()
		self.screen_rect=pygame.Rect(0,0,WINDOW_SIZE[0],WINDOW_SIZE[1]) #make a rect the size of the window

	def customize_draw(self,display_surface, player):
		self.offset.x=player.rect.centerx - WINDOW_SIZE[0]/2
		self.offset.y=player.rect.centery - WINDOW_SIZE[1]/2

		self.screen_rect.center=player.rect.center # move the window rect to have the same center as the player
		on_screen_sprites=[]

		for sprite in self.sprites(): #check which sprites "collide" with window rect
			if sprite.rect.colliderect(self.screen_rect):
				on_screen_sprites.append(sprite)

		for sprite in sorted(on_screen_sprites, key=lambda sprite: sprite.rect.centery): # draw only the sprites that collide with the window rect			 
			offset_rect=sprite.image.get_rect(center=sprite.rect.center)
			offset_rect.center-=self.offset
			display_surface.blit(sprite.image,offset_rect)
		


class Floor(pygame.sprite.Sprite):
	def __init__(self,surf,pos,groups):	
		super().__init__(groups)
		self.image=surf
		self.rect=self.image.get_rect(topleft=pos)

class TreesAndBushes(pygame.sprite.Sprite):
	def __init__(self,surf,pos,groups,sprite_id):
		super().__init__(groups)
		self.image=surf
		self.rect=self.image.get_rect(topleft=pos)
		# self.rect=self.rect.inflate(self.rect.width*rect_scale,self.rect.height*rect_scale)
		self.hitbox=self.rect.inflate(-self.rect.width*0.5,-self.rect.height*0.5)

		self.old_rect=self.rect.copy()
		self.name='Tree'
		self.can_interact=False
		self.sprite_id=sprite_id
	
	def get_name(self):
		return(self.name)
	
	def interaction_possible(self):
		return(self.can_interact)
	

class SmokeEffects():
	def __init__(self,pos,screen) -> None:
		self.pos=pos
		self.screen=screen
		self.smoke=[]

	def circle_surf(self,radius, color):
		surf = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surf, color, (radius, radius), radius,5)
		surf.set_colorkey((0, 0, 0))
		surf.set_alpha(127)
		return surf		

	def update(self,dt):
	
		if len(self.smoke) < MAX_PARTICLES:
			self.smoke.append(self.pos.copy())

			
		for i in self.smoke:
			i[1]-=dt*200
			i[0]+=randint(-3, 3)
			if i[1] < 0 :
				self.smoke.remove(i)
			else:
				# pygame.draw.circle(self.display_surface, (255,255,255), (i[0], i[1]), 5)
				self.screen.blit(self.circle_surf(5,(189, 66, 47)),(i[0], i[1]))
				self.screen.blit(self.circle_surf(5*2,(20, 20, 60)),(i[0], i[1]),special_flags=pygame.BLEND_RGB_ADD)
		

#todo : Consolidate all the various sprite classes into one super class and subclasses inhetiting from it for teh varous different objects

class StatusBar(pygame.sprite.Sprite):
	def __init__(self,default_image,alternate_image,number_of_blocks,pos,groups):	
		super().__init__(groups)
		self.default_image=default_image
		self.alternate_image=alternate_image
		self.number_of_blocks=number_of_blocks
		self.image=pygame.Surface((self.default_image.get_width()*self.number_of_blocks, self.default_image.get_height()))
		self.rect=self.image.get_rect(topleft=pos)
		self.current_blocks=0
		self.build_image()
		
		
	
	def build_image(self):
		for i in range(self.number_of_blocks):
			if i < self.current_blocks:
				self.image.blit(self.alternate_image,(i*self.default_image.get_width(),0))
			else:
				self.image.blit(self.default_image,(i*self.default_image.get_width(),0))
		
		# pygame.draw.rect(self.image,(255,255,255),self.rect,1,5)
		self.image.set_colorkey((0,0,0))

	def check_click(self, mouse):
		return(self.rect.collidepoint(mouse))
			

	def add_block(self):
		self.current_blocks+=1

	def remove_block(self):
		self.current_blocks-=1

	def set_blocks(self,num_of_blocks):
		if num_of_blocks > self.number_of_blocks:
			num_of_blocks = self.number_of_blocks 
		if num_of_blocks < 0 :
			num_of_blocks = 0 
		self.current_blocks=num_of_blocks

	def animate(self,dt):
		self.build_image()

	def update(self, dt):
		self.animate(dt)

	



class MsgBox(pygame.sprite.Sprite):
		def __init__(self,msg,font,groups):	
			super().__init__(groups)
			text_surf=font.render(msg,True,(255,255,255))
			self.image=pygame.Surface(( WINDOW_SIZE[0]*.6, WINDOW_SIZE[1]/4),pygame.SRCALPHA, 32).convert_alpha()
			self.image.fill((127,127,127))
			self.image.set_colorkey((127,127,127))
			self.image.blit(text_surf,(self.image.get_width()/2-text_surf.get_width()/2,self.image.get_height()/2-text_surf.get_height()/2))
			pygame.draw.rect(self.image,(255,255,255),(self.image.get_width()/2-text_surf.get_width()/2-5,self.image.get_height()/2-text_surf.get_height()/2-2 , text_surf.get_width()+10,text_surf.get_height()+5),1,5)
			self.rect=self.image.get_rect(topleft=(WINDOW_SIZE[0]/2-self.image.get_width()/2,WINDOW_SIZE[1]*3/4-10))  #-10 to offset it 10 pixels from the bottom 

class MagicTree(pygame.sprite.Sprite):
	def __init__(self,path,pos,groups):
		super().__init__(groups)
		self.name='MagicTree'
		self.import_assets(path)
		self.frame_index=0
		self.status='magictree'

		self.image=self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox=self.rect.inflate(-self.rect.width*0.5,-self.rect.height/2)
		self.old_rect=self.rect.copy()
		
		self.interaction_messages=[f'Press ENTER to speak',f'Let me rest for now']
		self.can_interact=False

		self.toggle_interactable() # convulated way to set the interaction message

		self.math_problems=RandomMathsProblems(NUM_DIGITS)

	def get_name(self):
		return(self.name)
	
	def get_problem_details(self):
		return(self.math_problems.summation())
	
	def interaction_possible(self):
		return(self.can_interact)
	
	def get_interaction_msg(self):
		return(self.interaction_msg)

	def toggle_interactable(self):
		self.can_interact = not self.can_interact
		if self.can_interact:
			self.interaction_msg=self.interaction_messages[0]
		else:
			self.interaction_msg=self.interaction_messages[1] # doesn't really work at the moment as the self.can_interact check preceeds it !!
		#as of now this doesn't work on the image. Replace this method call and handle it by changing the images displayed. i.e. store another set of animations and switch to them 
  
		# for i in range(len(self.animations)):
		# 	self.animations[i]= self.change_img_colour(self.animations[i],pygame.Color((89, 97, 97)))



	def change_img_colour(self,img,colour):  #colour has to be in the format-->  pygame.Color((R,G,B)) 
		for x in range(img.get_width()):
			for y in range(img.get_height()):
				colour.a = img.get_at((x, y)).a  # Preserve the alpha value.
				img.set_at((x, y), colour)  # Set the color of the pixel.s
		return(img)
	
	def import_assets(self,path):
		self.animations={}
		for index,folder in enumerate(walk(path)):

			if index==0:
				for name in folder[1]:
					self.animations[name]=[]
			else:
				for file_name in sorted(folder[2],key = lambda string:int(string.split('.')[0])):
					path=folder[0].replace('\\','/')+'/'+file_name
					surf=pygame.image.load(path).convert_alpha()
					surf.set_colorkey((0,0,0))
					key=folder[0].split('\\')[-1]

					self.animations[key].append(surf)
		
	def animate(self,dt):
		current_animation=self.animations[self.status]
 
		self.frame_index+=7*dt

		if self.frame_index>= len(current_animation):
			self.frame_index=0

		self.image=current_animation[int(self.frame_index)]
		self.mask=pygame.mask.from_surface(self.image)

	def update(self, dt):
		self.animate(dt)

class Entity(pygame.sprite.Sprite):
	def __init__(self,path,pos,groups,collision_sprites,bounds,msg_font,msg_group):
		super().__init__(groups)
		self.collision_sprites=collision_sprites
		self.import_assets(path)
		self.frame_index=0
		self.status='player_idle'
		self.floor_max_x,self.floor_max_y=bounds

		self.image=self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(topleft=pos)
		#self.z=LAYERS['Level']
		self.mask=pygame.mask.from_surface(self.image)
		self.pos=vector(self.rect.topleft)
		
		self.direction=vector()
		# self.gravity = 15
		self.speed=400
		# self.collision=None
		self.player_flip=False
		self.hitbox=self.rect.inflate(-self.rect.width*0.5,-self.rect.height*0.5)
		self.start_ticks=0
		self.interacting=False
		self.interacting_with=None
		self.font=msg_font
		self.msg_group=msg_group



	def import_assets(self,path):
		self.animations={}
		for index,folder in enumerate(walk(path)):

			if index==0:
				for name in folder[1]:
					self.animations[name]=[]
			else:
				for file_name in sorted(folder[2],key = lambda string:int(string.split('.')[0])):
					path=folder[0].replace('\\','/')+'/'+file_name
					surf=pygame.image.load(path).convert_alpha()
					key=folder[0].split('\\')[-1]

					self.animations[key].append(surf)

		

	def input(self):

		keys=pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.direction.x=1
			self.player_flip=False
			self.status='player_running'
		elif keys[pygame.K_LEFT]:
			self.direction.x=-1
			self.player_flip=True
			self.status='player_running'
		else:
			self.direction.x=0
		if keys[pygame.K_UP]:
			self.direction.y=-1
			self.status='player_running'
		elif keys[pygame.K_DOWN]:
			self.direction.y=1
			self.status='player_running'
		else:
			self.direction.y=0
	

		if self.direction == (0,0):
			self.status="player_idle"

	def collision(self,direction):
		

		colliding=False
		for sprite in self.collision_sprites.sprites():
			if sprite.hitbox.colliderect(self.hitbox):
				colliding=True
				if sprite.interaction_possible():
					self.interacting=True
					self.interacting_with=sprite
				else:
					self.interacting=False
					self.interacting_with=None

				if direction == 'horizontal':
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left 
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right  
					self.rect.centerx=self.hitbox.centerx
					self.pos.x=self.hitbox.centerx
				else:
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery=self.hitbox.centery
					self.pos.y=self.hitbox.centery

	def move(self,dt):
		if self.direction.magnitude() !=0:
			self.direction=self.direction.normalize()

		self.pos.x += self.direction.x* self.speed * dt 
		self.hitbox.centerx=round(self.pos.x)
		self.rect.centerx=self.hitbox.centerx
		self.collision('horizontal')
	
		self.pos.y += self.direction.y*self.speed*dt 
		
		self.hitbox.centery=round(self.pos.y)
		self.rect.centery=self.hitbox.centery
		self.collision('vertical')	

		#make sure player doesn't leave the play area

		if self.pos.x <= TILE_SIZE:
			self.pos.x=TILE_SIZE+1
		elif self.pos.x >=self.floor_max_x  - TILE_SIZE:
			self.pos.x=self.floor_max_x  - TILE_SIZE -1 
			
		if self.pos.y <= TILE_SIZE:
			self.pos.y=TILE_SIZE+1
		elif self.pos.y >=self.floor_max_y  - TILE_SIZE :
			self.pos.y=self.floor_max_y  - TILE_SIZE -1 

			

	def animate(self,dt):
		current_animation=self.animations[self.status]
 
		self.frame_index+=7*dt


		if self.frame_index>= len(current_animation):
			self.frame_index=0

		self.image=pygame.transform.flip(current_animation[int(self.frame_index)],self.player_flip,False)
		self.mask=pygame.mask.from_surface(self.image)


	def is_interacting(self):
		return(self.interacting)
	
	def interacting_sprite(self):
		return(self.interacting_with)
	
	def end_interaction(self):
		self.interacting=False
		self.interacting_with=None

	def check_for_interaction(self):
		
		if self.interacting and len(self.msg_group) == 0 :
			if ( pygame.time.get_ticks()- self.start_ticks)/1000 > GREETING_DELAY:  # show the greeting after a delay, now delay set to 1 sec
				self.start_ticks = pygame.time.get_ticks()
			
				MsgBox(self.interacting_with.get_interaction_msg(),self.font,self.msg_group)

		else:
			if not self.status=="player_idle":
				if len(self.msg_group) >0 :
					self.msg_group.empty()
				

			
	def update(self, dt):
		self.old_rect=self.rect.copy()
		self.input()
		self.animate(dt)		
		self.move(dt)
		self.check_for_interaction()
