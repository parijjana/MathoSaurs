import pygame
from pygame.math import Vector2 as vector
import sys
from os import walk,environ
from random import choice, randint
from entity import Entity, AllSprites, AssetLoader, TreesAndBushes, MagicTree, Floor, MsgBox, StatusBar,SmokeEffects
from interaction_page import TextPage

from settings import *




class Main:
	def __init__(self):
		# environ['SDL_VIDEO_CENTERED'] = '1'

		pygame.init()
		# info = pygame.display.Info()
		# print(info)
		self.display_surface=pygame.display.set_mode(WINDOW_SIZE)
		self.game_screen = pygame.Surface(WINDOW_SIZE)
		self.interaction_screen= pygame.Surface(WINDOW_SIZE)
		self.window_size=WINDOW_SIZE
		self.scaling_factor=1
		pygame.display.set_caption("MathoSaurs")
		self.clock=pygame.time.Clock()
		self.window_middle=(map_tiles[0]*TILE_SIZE/2,map_tiles[1]*TILE_SIZE/2)
		self.font=pygame.font.Font("KodeMono-Medium.ttf",24)
		self.font_big=pygame.font.Font("KodeMono-Medium.ttf",32)
		self.font_huge=pygame.font.Font("KodeMono-Medium.ttf",128)
		self.setup_groups()

		self.layout=[]
		self.make_startup_page()

		self.level_map=[]
		self.setup_map()
		self.setup_sprites()
		self.setup_statusbar()
		self.setup_closebutton()
		self.state='Startup' # possible states : Startup, Game, Interaction, Won, Paused
		self.state_old=None
		self.fruits_found=0


	def setup_closebutton(self):
		close_button_image=pygame.image.load(close_button).convert_alpha()
		self.close_button=StatusBar(close_button_image,close_button_image,1,(WINDOW_SIZE[0]-close_button_image.get_width()-5,5),self.ui_sprites)

	def setup_statusbar(self):
		default_statusbar_image=pygame.image.load(statusbar_default).convert_alpha()
		alternate_statusbar_image=pygame.image.load(statusbar_alternate).convert_alpha()
		self.statusbar=StatusBar(default_statusbar_image,alternate_statusbar_image,self.total_magic_trees,(10,5),self.ui_sprites)


	def setup_map(self)	:
		flr_images=AssetLoader(floor_images)
		self.floor_images=flr_images.get_assets()
		tree_img=AssetLoader(tree_images)
		self.trees=tree_img.get_assets()

		self.tile_size=self.floor_images[0].get_width()
		self.floor_max_x=self.tile_size*map_tiles[0]
		self.floor_max_y=self.tile_size*map_tiles[1]

		for y in range(map_tiles[0]):
			for x in range(map_tiles[1]):
				x_pos = self.tile_size*x
				y_pos= self.tile_size*y

				self.level_map.append([[x_pos,y_pos],choice(self.floor_images)])

				#make the base layer
		self.floor = pygame.Surface((map_tiles[0]*self.tile_size,map_tiles[1]*self.tile_size))
		for tile in self.level_map:
			if tile[0][0]<= WINDOW_SIZE[0] and tile[0][1] <=WINDOW_SIZE[1]:
				self.floor.blit(tile[1],(tile[0][0],tile[0][1]))


	def setup_groups(self):
		self.all_sprites=AllSprites()
		self.obstacles=pygame.sprite.Group()
		self.floor_sprites=AllSprites()
		self.msg_boxes=pygame.sprite.Group()
		self.interaction_msg=pygame.sprite.Group()
		self.interaction_sprites=pygame.sprite.Group()
		self.ui_sprites=pygame.sprite.Group()

	def setup_sprites(self):
		self.player=Entity(player_images,self.window_middle,[self.all_sprites],self.obstacles,(self.floor_max_x,self.floor_max_y),self.font,self.msg_boxes)
		self.total_magic_trees=0
		sprite_id=0
		for tile in self.level_map:
			Floor(tile[1],(tile[0][0],tile[0][1]),[self.floor_sprites])
			if tile[0][0] ==0  or tile[0][0] == self.floor_max_x-self.tile_size  or tile[0][1] ==0  or tile[0][1] == self.floor_max_y-self.tile_size  :

				TreesAndBushes(choice(self.trees),(tile[0][0],tile[0][1]),[self.all_sprites,self.obstacles],sprite_id)
				sprite_id+=1
			else:
				if randint(1,4) == 1:
					TreesAndBushes(choice(self.trees),(tile[0][0],tile[0][1]),[self.all_sprites,self.obstacles],sprite_id)
					sprite_id+=1
				else:
					if randint(1,50) == 1 and self.total_magic_trees < MAX_MAGIC_TREES:
						MagicTree(magictree_images,(tile[0][0],tile[0][1]),[self.all_sprites,self.obstacles])
						self.total_magic_trees+=1

	def make_startup_page(self):
		self.layout.clear()
		self.interaction_sprites.empty()
		self.layout.append({'Groups':self.interaction_sprites,'Text':f'Help the MathoSaurs find the fruits'+' '*10,'Dimensions':((20,WINDOW_SIZE[1]/4),(WINDOW_SIZE[0]*1.12,30)),'Can_display':True,'Name':'Header','Features':[None]})
		self.layout.append({'Groups':self.interaction_sprites,'Text':f'Press ENTER to play game'+' '*10,'Dimensions':((10,WINDOW_SIZE[1]/2),(WINDOW_SIZE[0],30)),'Can_display':True,'Name':'Header','Features':[None]})
		self.startup=TextPage(self.layout,self.font_big)

	def make_interaction_page(self):
		self.layout.clear()
		self.interaction_sprites.empty()

		num_1,num_2,result,operand=self.interaction_sprite.get_problem_details()
		self.result=result

		self.layout= [{'Groups':self.interaction_sprites,'Text':f'To get a fruit, answer the following:'+' '*10,'Dimensions':((10,10),(WINDOW_SIZE[0]-20,30)),'Can_display':True,'Name':'Header','Features':[None]}]
		self.layout.append({'Groups':self.interaction_sprites,'Text':f'{num_1 :>11}','Dimensions':((280,250),(200,30)),'Can_display':True,'Name':'num_1','Features':[None]})
		self.layout.append({'Groups':self.interaction_sprites,'Text':f'{operand:<}{num_2:>10}','Dimensions':((280,280),(200,30)),'Can_display':True,'Name':'num_2','Features':[None]})
		self.layout.append({'Groups':self.interaction_sprites,'Text':f'_'*12,'Dimensions':((280,300),(200,30)),'Can_display':True,'Name':'uc','Features':[None]})
		self.layout.append({'Groups':self.interaction_sprites,'Text':f'','Dimensions':((280,330),(200,30)),'Can_display':True,'Name':'player_input','Features':['Updatable','Text Updatable','Cursor']})
		self.layout.append({'Groups':self.interaction_sprites,'Text':f'Correct Answer!','Dimensions':((280,430),(200,30)),'Can_display':False,'Name':'success_message','Features':['Updatable']})

		self.interaction_page=TextPage(self.layout,self.font)
		self.player_input_field=self.interaction_page.get_updatable_items('player_input')
		self.success_message=self.interaction_page.get_updatable_items('success_message')


	def game_processes(self,dt):
		self.all_sprites.update(dt)
		self.game_screen.fill(BG_COLOUR)
		self.floor_sprites.customize_draw(self.game_screen,self.player)
		self.all_sprites.customize_draw(self.game_screen,self.player)
		self.msg_boxes.draw(self.game_screen)
		self.ui_sprites.update(dt)
		self.ui_sprites.draw(self.game_screen)
		# self.display_surface.blit(self.game_screen,(0,0))
		self.display_surface.blit(pygame.transform.smoothscale(self.game_screen,(WINDOW_SIZE[0]*self.scaling_factor,WINDOW_SIZE[1]*self.scaling_factor)),(0,0))

		if self.fruits_found == self.total_magic_trees:
			self.first_run=True
			self.state ='Won'


	def startup_process(self,dt):
		self.interaction_screen.fill(BG_COLOUR)
		self.interaction_sprites.update(dt,self.events)
		self.interaction_sprites.draw(self.interaction_screen)
		self.display_surface.blit(pygame.transform.smoothscale(self.interaction_screen,(WINDOW_SIZE[0]*self.scaling_factor,WINDOW_SIZE[1]*self.scaling_factor)),(0,0))


	def interaction_process(self,dt):

		if self.first_run:
			MsgBox(f'Press ESC to go back',self.font,self.interaction_msg)
			self.make_interaction_page()
			self.first_run=False
			self.check_for_input=True


		self.interaction_screen.fill(BG_COLOUR)
		self.interaction_msg.draw(self.interaction_screen)

		if self.check_for_input:

			try: #find a way to do this more elegantly !!
				if int(self.player_input_field.get_text()) == int(self.result):
					self.success_message.toggle_display()
					self.player_input_field.change_text_colour((17, 245, 237))
					self.player_input_field.toggle_text_updateable()
					self.check_for_input=False
					self.interaction_sprite.toggle_interactable()
					self.statusbar.add_block()
					self.fruits_found+=1

			except:
				pass

		self.interaction_sprites.update(dt,self.events)
		self.interaction_sprites.draw(self.interaction_screen)

		self.display_surface.blit(pygame.transform.smoothscale(self.interaction_screen,(WINDOW_SIZE[0]*self.scaling_factor,WINDOW_SIZE[1]*self.scaling_factor)),(0,0))



	def show_pause_messgae(self,dt):
		if self.first_run:
			self.screen_rect=self.display_surface.get_rect()
			self.curr_screen=pygame.Surface((WINDOW_SIZE[0],WINDOW_SIZE[1]))
			self.curr_screen.blit(self.display_surface,(0,0))
			self.curr_screen.set_alpha(127)
			self.first_run=False
			self.scaling_factor=1
			self.message=self.font_big.render(' Game Pasued ',True,(255,255,255))
			pygame.draw.rect(self.message,(255,255,255),self.message.get_rect(),1,10)

		self.display_surface.fill((0,0,0))
		self.display_surface.blit(pygame.transform.smoothscale(self.curr_screen,(WINDOW_SIZE[0]*self.scaling_factor,WINDOW_SIZE[1]*self.scaling_factor)),(0,0))
		self.display_surface.blit(self.message,(WINDOW_SIZE[0]/2-self.message.get_width()/2,WINDOW_SIZE[1]/2-self.message.get_height()/2))

	def show_win_messgae(self,dt):
		if self.first_run:
			self.screen_rect=self.display_surface.get_rect()
			self.curr_screen=pygame.Surface((WINDOW_SIZE[0],WINDOW_SIZE[1]))
			self.curr_screen.blit(self.display_surface,(0,0))
			self.curr_screen.set_alpha(127)
			self.first_run=False
			self.scaling_factor=1
			self.win_message=self.font_huge.render(' You Won! ',True,(255,255,255))
			pygame.draw.rect(self.win_message,(255,255,255),self.win_message.get_rect(),1,10)
			# self.smoke=[]
			self.smokestack_left=SmokeEffects([WINDOW_SIZE[0]/4,WINDOW_SIZE[1]],self.display_surface)
			self.smokestack_right=SmokeEffects([WINDOW_SIZE[0]/4*3,WINDOW_SIZE[1]],self.display_surface)


		self.display_surface.fill((0,0,0))

		self.smokestack_left.update(dt)
		self.smokestack_right.update(dt)


		self.display_surface.blit(pygame.transform.smoothscale(self.curr_screen,(WINDOW_SIZE[0]*self.scaling_factor,WINDOW_SIZE[1]*self.scaling_factor)),(0,0))
		self.display_surface.blit(self.win_message,(WINDOW_SIZE[0]/2-self.win_message.get_width()/2,WINDOW_SIZE[1]/2-self.win_message.get_height()/2))


	def run(self):
		start_ticks=pygame.time.get_ticks()

		while True:
			self.events=pygame.event.get()
			for event in self.events:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.VIDEORESIZE:
					self.window_size = event.size
					self.scaling_factor=self.window_size[1]/WINDOW_SIZE[1]

				elif event.type == pygame.MOUSEBUTTONDOWN:
					print(event.pos)
					if self.close_button.check_click(event.pos):
						pygame.quit()
						sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						if self.state=='Paused':
							self.state=self.state_old
						else:
							self.first_run=True
							self.state_old=self.state
							self.state='Paused'

					if self.state=='Game':
						if event.key == pygame.K_RETURN  and self.player.is_interacting():
							self.state='Interaction'
							self.interaction_sprite=self.player.interacting_sprite()
							self.first_run=True


					elif self.state=='Interaction':
						if event.key == pygame.K_ESCAPE :
							self.state='Game'
							self.player.end_interaction()
							self.interaction_msg.empty()
							self.first_run=False

					elif self.state == 'Startup':
						if event.key == pygame.K_RETURN :
							self.state='Game'




			dt=self.clock.tick()/1000

			if ( pygame.time.get_ticks()- start_ticks)/1000 > fps_delay:
				pygame.display.set_caption(f'MathoSaurs Running at {int(self.clock.get_fps())} FPS')
				start_ticks = pygame.time.get_ticks()



			if self.state=='Game':
				self.game_processes(dt)
			elif self.state == 'Interaction':
				self.interaction_process(dt)
			elif self.state == 'Startup':
				self.startup_process(dt)
			elif self.state =='Won':
				self.show_win_messgae(dt)
			elif self.state =='Paused':
				self.show_pause_messgae(dt)




			pygame.display.update()

if __name__=='__main__':
	main=Main()
	main.run()
