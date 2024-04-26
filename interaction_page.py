import pygame
from settings import * 

class TextPage():
	def __init__(self,layout,font): #layout= [{'Groups'=groups,'Image'=src_image,'Pos'=pos,'Can_display'=can_display}]
		self.font=font
		self.items=[]
		self.updatable_items=[]
		for item in layout:
			self.items.append(ClickableSprites(item['Groups'],item['Text'],item['Dimensions'],item['Can_display'],item['Name'],item['Features'],self.font))
			if 'Updatable' in item['Features'] or 'Text Updatable' in item['Features']:
				self.updatable_items.append(self.items[-1])

	def get_updatable_items(self,item_name=None):
		if item_name:
			for sprite in self.updatable_items :
				if sprite.get_name()==item_name:
					return(sprite)
		else:
			return(self.updatable_items)

class ClickableSprites(pygame.sprite.Sprite):
	def __init__(self, groups,text,dimesions,can_display,name,features,font) -> None:
		super().__init__(groups)
		self.groups=groups
		self.font=font
		self.box_rect=pygame.Rect(dimesions)
		self.text=text
		self.colour=(43, 35, 34)
		self.can_display=can_display
		if self.can_display:
			self.image=self.text_to_img(self.text)
		else:
			self.image=self.text_to_img(f'')
		self.dimensions=dimesions
		self.rect=self.image.get_rect(topright=self.box_rect.topright)
		self.name=name
		
		
		#check for features that this box can have :

		self.text_updateable=False
		self.cursor=False
		if	'Text Updatable' in features:
			self.text_updateable=True
		if 'Cursor' in features:
			self.cursor=True

		self.occur_once=0
		


	# def rescale_image(self):

	# 	if self.src_image.get_height() > self.dimensions[1]:
	# 		width=

	def text_to_img(self,txt):
		return(self.font.render(txt,True,self.colour))
	
	def change_text_colour(self,colour=None):
		if colour:
			self.colour=colour
		
	def toggle_display(self):
		self.can_display= not self.can_display

	def toggle_text_updateable(self):
		self.text_updateable = not self.text_updateable

	def update_display(self,src_image):
		self.image=src_image

	def get_name(self):
		return(self.name)
	
	def get_text(self):
		return(self.text)
	
	def check_click(self, mouse):
		if self.rect.collidepoint(mouse):
			return(self)    

	def input(self,events):
		for event in events:
			if event.type == pygame.KEYDOWN and event.unicode.isdigit():
				self.text=str(int(event.unicode))+self.text
				
			elif event.type == pygame.KEYDOWN and (event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE) :
				self.text=self.text[1:]
		
	def animate(self,dt):

		if self.can_display:
			self.image=self.text_to_img(self.text)
		else:
			self.image=self.text_to_img(f'')
		
		self.rect=self.image.get_rect(topright=self.box_rect.topright)

	def blink_cursor(self,dt):
		pass
	def update(self, dt,events):
		if self.text_updateable:
			self.input(events)
			if self.cursor:
				self.blink_cursor(dt)
		
		self.animate(dt)

