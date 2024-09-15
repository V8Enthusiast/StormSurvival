import math
import random
import time

import pygame

import settings_values
from classes import GameObject, particles, hotbar, weapon

from Assets import mixer
import images

class Game:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.main_text_rect_center = (self.app.width//2, 150 * self.app.scale)
        self.font = "fonts/second.ttf"
        self.helpText = ""
        self.font_color = (255, 255, 255)
        self.screen = self.app.screen
        self.buttons = []
        self.chests = []
        self.enemies = []
        self.selected_chest = None
        self.chest_ui = None
        self.pay_for_chest = settings_values.pay_for_chest
        self.speed = 3
        self.dx = 0
        self.dy = 0



        self.player = GameObject.Player(self, self.app.width // 2 - 50, self.app.height // 2 - 50, 100, 100,
                                        images.player, True)
        self.storm_counter=0
        self.storm = GameObject.Storm(self, -1000, 0, 500, self.app.height, images.storm,True)
        self.storm2=GameObject.Storm(self, -1000, -self.app.height, 500, self.app.height, images.storm,True)
        #chest = GameObject.Chest(self, 600, 600, 100, 100, images.chest, True)
        #self.chests.append(chest)
        #self.objects.append(chest)
        #self.objects.append(GameObject.Chest(self, 600, 600, 100, 100, images.chest, True))

        self.tiles = {}
        self.tile_size = 96

        self.waters=['water']
        self.trees = ['tree1','tree2','tree3']
        self.init_tiles()

        self.environmentparticlesystem = particles.ParticleSystem(self)

        self.weaponparticlesystem = particles.ParticleSystem(self, movable=True)
        self.current_max_x=0
        self.current_max_y=0
        self.current_min_x=0
        self.current_min_y=0
        self.tile_width=96

        self.hotbar = hotbar.Hotbar(self, self.app.width//2 - ((50 + 10) * 5 -50)//2, self.app.height-75, 5)
        self.hotbar.add_item(weapon.Glock17(self, self.player), 0)

        self.sound_mixer = mixer.Mixer()
        self.sound_mixer.change_volume(self.app.mixer.get_volume())

        self.time_of_last_shot = time.time_ns()
        self.burst_shots = 0

        self.resource_manager=GameObject.Resource_Manager(0,0,self,[['gems',0],['wood',50]],[images.gem,images.wood])
        self.resources = {}
        self.e=False
        self.bar_speed=2
        self.move_x =0#self.app.width//2%self.tile_size
        self.move_y =0 #self.app.height//2%self.tile_size

        self.day_night_cycle_duration = 120  # Duration of a full day-night cycle in seconds
        self.cycle_start_time = time.time()
        self.time_of_day = None
        self.overlay_alpha = 0
        self.overlay_surface = pygame.Surface((self.app.width, self.app.height))
        self.overlay_surface.fill((0, 0, 0))

        self.is_raining = False
        self.next_weather_change = time.time() + random.uniform(30, 180)
        self.last_hunger_update = time.time()
        self.last_fps_time = time.time()
        self.current_fps = 0

        self.wave = 0
        self.enemy_spawns_left = 20 + self.wave * 5
        self.delay_between_spawns = self.day_night_cycle_duration / self.enemy_spawns_left
        self.enemies_per_spawn = 2
        self.delay_between_spawns = self.enemies_per_spawn * self.day_night_cycle_duration / (self.enemy_spawns_left * 2)
        self.spawn_delay_clock = time.time_ns()
        self.enemy_spawn_offset = 350
        self.score = 0

        self.place_block_radius = 3 * 96
        self.place_mode = False

        self.weapon_selection_ui = None

    def init_tiles(self):
        for y in range(-96, self.app.height+96, self.tile_size):
            for x in range(-96, self.app.width+96, self.tile_size):
                self.choose_tile(x,y)
                # print(x,y)

    def surround_by_sand(self,x,y):
        for dx in range(-1,2):
            for dy in range(-1,2):
                if abs(dx)!=abs(dy):
                    if (x + dx * self.tile_size, y + dy * self.tile_size) in self.tiles:
                        if self.tiles[(x + dx * self.tile_size,y + dy * self.tile_size)] not in self.waters:
                            self.tiles[(x + dx * self.tile_size,y + dy * self.tile_size)]='sand'




    def build(self):
        try:
            self.bar.value+=self.bar_speed
            if self.bar.value>self.bar.max_value:
                self.bar.value = self.bar.max_value
                self.build_success()
                self.end_building()
                self.e=False

        except:
            pass

    def build_success(self):
        if self.tiles[(self.current_tile_x,self.current_tile_y)] in self.trees:
            self.tiles[(self.current_tile_x, self.current_tile_y)]=self.tiles[(self.current_tile_x, self.current_tile_y)]+'_farm'
            GameObject.Resource(self,self.current_tile_x,self.current_tile_y-self.tile_size//6,'wood',images.wood,50,10)
            GameObject.Resource(self, self.current_tile_x, self.current_tile_y +self.tile_size//6, 'food', images.food, 120, 10)
        elif self.tiles[(self.current_tile_x,self.current_tile_y)] =='mine' and self.resource_manager.resources[1][1]>=100:
            self.tiles[(self.current_tile_x, self.current_tile_y)] = self.tiles[(
            self.current_tile_x, self.current_tile_y)] + '_farm'
            self.resource_manager.resources[1][1]-=100
            GameObject.Resource(self, self.current_tile_x, self.current_tile_y, 'gems', images.gem, 50, 10)
        elif self.tiles[(self.current_tile_x,self.current_tile_y)] =='water' :
            self.player.thirst+=5
            if self.player.thirst>100:
                self.player.thirst=100

    def start_building(self):

        #for a in self.tiles.items():
            # print(a)

        try:
            if self.app.resolution_number==0:
                self.current_tile_x = (2 * self.player.relative_position[
                    0]  + self.app.width // 2 // self.tile_size * self.tile_size) // 96 * 96
                self.current_tile_y = (2 * self.player.relative_position[
                    1]  + self.app.height // 2 // self.tile_size * self.tile_size) // 96 * 96
            elif self.app.resolution_number==1 :
                self.current_tile_x = (2 * self.player.relative_position[
                    0] + self.tile_size // 3 + self.app.width // 2 // self.tile_size * self.tile_size) // 96 * 96
                self.current_tile_y = (2 * self.player.relative_position[
                    1] + self.tile_size // 2 + self.app.height // 2 // self.tile_size * self.tile_size) // 96 * 96
            # print(self.tiles[(2*self.player.relative_position[0]+5*self.tile_size-self.move_x,2*self.player.relative_position[1]-self.move_y+4*self.tile_size)])
            elif self.app.resolution_number==2:
                self.current_tile_x = (2 * self.player.relative_position[
                    0]  + self.app.width // 2 // self.tile_size * self.tile_size) // 96 * 96
                self.current_tile_y = (2 * self.player.relative_position[
                    1] + self.tile_size // 2 + self.app.height // 2 // self.tile_size * self.tile_size) // 96 * 96
            elif self.app.resolution_number==3:
                self.current_tile_x = (2 * self.player.relative_position[
                    0] + self.tile_size // 3 + self.app.width // 2 // self.tile_size * self.tile_size) // 96 * 96
                self.current_tile_y = (2 * self.player.relative_position[
                    1] + self.tile_size  //3 + self.app.height // 2 // self.tile_size * self.tile_size) // 96 * 96

            if self.tiles[(self.current_tile_x,self.current_tile_y)] !='grass' and self.tiles[(self.current_tile_x,self.current_tile_y)] !='sand':


                self.bar = GameObject.Bar(self, (self.app.width // 2) // 96 * 96 - 50, (self.app.height // 2 // 96 * 96) - 10,
                                  100, 20, (255, 255, 0), 0, 100)
                # print('is')
            else:
                self.e=False
                # print('not')
        except:
            pass
    def end_building(self):
        try:
            self.objects.remove(self.bar)
            self.bar=None
        except:
            pass
    def collect(self):

        if self.app.resolution_number == 0:
            self.current_tile_x = (2 * self.player.relative_position[
                0] + self.app.width // 2 // self.tile_size * self.tile_size) // 96 * 96
            self.current_tile_y = (2 * self.player.relative_position[
                1] + self.app.height // 2 // self.tile_size * self.tile_size) // 96 * 96
        elif self.app.resolution_number == 1:
            self.current_tile_x = (2 * self.player.relative_position[
                0] + self.tile_size // 3 + self.app.width // 2 // self.tile_size * self.tile_size) // 96 * 96
            self.current_tile_y = (2 * self.player.relative_position[
                1] + self.tile_size // 2 + self.app.height // 2 // self.tile_size * self.tile_size) // 96 * 96
        # print(self.tiles[(2*self.player.relative_position[0]+5*self.tile_size-self.move_x,2*self.player.relative_position[1]-self.move_y+4*self.tile_size)])
        elif self.app.resolution_number == 2:
            self.current_tile_x = (2 * self.player.relative_position[
                0] + self.app.width // 2 // self.tile_size * self.tile_size) // 96 * 96
            self.current_tile_y = (2 * self.player.relative_position[
                1] + self.tile_size // 2 + self.app.height // 2 // self.tile_size * self.tile_size) // 96 * 96
        elif self.app.resolution_number == 3:
            self.current_tile_x = (2 * self.player.relative_position[
                0] + self.tile_size // 3 + self.app.width // 2 // self.tile_size * self.tile_size) // 96 * 96
            self.current_tile_y = (2 * self.player.relative_position[
                1] + self.tile_size // 3 + self.app.height // 2 // self.tile_size * self.tile_size) // 96 * 96


        try:
            if self.resources[(self.current_tile_x, self.current_tile_y - self.tile_size // 6)].resource == 'wood':
                # print('x')
                # print(self.resource_manager.resources[1][1],
                #       self.resources[(self.current_tile_x, self.current_tile_y)].value)
                self.resource_manager.resources[1][1] += self.resources[
                    (self.current_tile_x, self.current_tile_y - self.tile_size // 6)].value
                self.resources[(self.current_tile_x, self.current_tile_y - self.tile_size // 6)].value = 0
                print('ymu yum yum',
                      self.resources[(self.current_tile_x, self.current_tile_y + self.tile_size // 6)].value)
                self.player.hunger += self.resources[
                    (self.current_tile_x, self.current_tile_y + self.tile_size // 6)].value
                self.resources[(self.current_tile_x, self.current_tile_y + self.tile_size // 6)].value = 0
                # print('y')
        except:
            if self.resources[(self.current_tile_x, self.current_tile_y)].resource == 'gems':
                self.resource_manager.resources[0][1] += self.resources[
                    (self.current_tile_x, self.current_tile_y)].value
                self.resources[(self.current_tile_x, self.current_tile_y)].value = 0





    def choose_tile(self, x, y):
        tree_probability = 100
        mine_probability = 50
        chest_probability = 50
        tile_image = 'grass'

        for n in self.check_neighbours(x, y):
            # print(n)
            # print(n)
            if n in self.trees:
                if random.randint(0, 10) > 6:
                    self.add_tile(x, y, random.choice(self.trees))
                    return
            elif n in self.waters:
                if random.randint(0, 10) > 6:
                    self.add_tile(x, y, random.choice(self.waters))
                    self.surround_by_sand(x,y)
                else:
                    self.add_tile(x, y, 'sand')



        if random.randint(1, tree_probability) == 1:
            self.add_tile(x, y, random.choice(self.waters))
            self.surround_by_sand(x, y)

        elif random.randint(1, tree_probability) == 1:
            self.add_tile(x, y, random.choice(self.trees))

        elif random.randint(1,mine_probability)==1:
            self.add_tile(x, y, 'mine')
        else:
            if random.randint(1, chest_probability) == 1:
                chest = GameObject.Chest(self, y, x, 96, 96, images.chest_closed, True)
                self.objects.append(chest)
                self.chests.append(chest)
                print('aa')

            self.add_tile(x, y, tile_image)




    def check_neighbours(self,x,y):
        neighs=[]
        for dx in range(-1,2):
            for dy in range(-1,2):
                if abs(dx)!=abs(dy):
                    try:
                        # print(self.tiles[(x + dx * self.tile_size, y + dy * self.tile_size)], self.trees)

                        if self.tiles[(x + dx * self.tile_size, y + dy * self.tile_size)] in self.trees or self.tiles[
                            (x + dx * self.tile_size, y + dy * self.tile_size)] in self.waters :
                            neighs.append(self.tiles[(x + dx * self.tile_size, y + dy * self.tile_size)])




                    except:
                        pass

        if len(neighs)!=0:

            pass
        return neighs

    def add_tile(self, x, y, tile_image, force=False):
        if force or (x, y) not in self.tiles.keys():
            self.tiles[(x, y)] = tile_image

    def update_day_night_cycle(self):
        current_time = time.time()
        elapsed_time = (current_time - self.cycle_start_time) % self.day_night_cycle_duration
        cycle_progress = elapsed_time / self.day_night_cycle_duration

        if cycle_progress < 0.25:  #Dawn
            self.overlay_alpha = int(255 * (0.25 - cycle_progress) / 0.25)//2
        elif cycle_progress < 0.75:  #Day
            self.overlay_alpha = 0
        elif cycle_progress < 1.0:  #Tusk
            self.overlay_alpha = int(255 * (cycle_progress - 0.75) / 0.25)//2
        else:  #Night
            self.overlay_alpha = 255//2

    def render_day_info(self):
        font = pygame.font.Font(self.font, 24)
        text_color = (255, 255, 255)

        current_time = time.time()
        elapsed_time = (current_time - self.cycle_start_time) % self.day_night_cycle_duration
        cycle_progress = elapsed_time / self.day_night_cycle_duration

        if cycle_progress < 0.25:
            if self.time_of_day != "Dawn" and self.score != 0:
                self.score += 2500
            time_of_day = "Dawn"
            time_to_next = int((0.25 - cycle_progress) * self.day_night_cycle_duration)
        elif cycle_progress < 0.75:
            time_of_day = "Noon"
            time_to_next = int((0.75 - cycle_progress) * self.day_night_cycle_duration)
        elif cycle_progress < 1.0:
            if self.time_of_day != "Evening":
                self.wave += 1
                self.delay_between_spawns = self.enemies_per_spawn * self.day_night_cycle_duration / (self.enemy_spawns_left * 2)
            time_of_day = "Evening"
            time_to_next = int((1.0 - cycle_progress) * self.day_night_cycle_duration)
        else:
            time_of_day = "Night"
            time_to_next = int((1.25 - cycle_progress) * self.day_night_cycle_duration)

        day_info_text = font.render(f"Time of Day: {time_of_day}", True, text_color)
        self.screen.blit(day_info_text, (10, 40))

        time_to_next_text = font.render(f"Time to Next: {time_to_next}s", True, text_color)
        self.screen.blit(time_to_next_text, (10, 70))

        score = font.render(f"Score: {self.score}", True, (min(255, self.score //255), min(255, 255//(self.score + 1)),255))
        self.screen.blit(score, (10, 100))

        self.time_of_day = time_of_day

    def render_player_info(self):
        ui_surface = pygame.Surface((self.app.width, 100), pygame.SRCALPHA)
        ui_surface.fill((0, 0, 0, 150))  # RGBA, where A is the alpha value for transparency

        font = pygame.font.Font(self.font, 24)
        text_color = (255, 255, 255)

        health_text = font.render(f"Health: {round(self.player.health)}", True, text_color)
        ui_surface.blit(health_text, (10, 10))

        hunger_text = font.render(f"Hunger: {self.player.hunger}", True, text_color)
        ui_surface.blit(hunger_text, (10, 40))

        drink_text = font.render(f"Thirst: {self.player.thirst}", True, text_color)
        ui_surface.blit(drink_text, (10, 70))

        gem_icon = pygame.transform.scale(images.gem, (24, 24))
        wood_icon = pygame.transform.scale(images.wood, (24, 24))

        ui_surface.blit(gem_icon, (200, 10))
        gem_text = font.render(f"{self.resource_manager.resources[0][1]} Gems", True, text_color)
        ui_surface.blit(gem_text, (230, 10))

        ui_surface.blit(wood_icon, (200, 40))
        wood_text = font.render(f"{self.resource_manager.resources[1][1]} Wood", True, text_color)
        ui_surface.blit(wood_text, (230, 40))

        self.screen.blit(ui_surface, (0, self.app.height - 100))

    def render_weather_info(self):
        font = pygame.font.Font(self.font, 24)
        text_color = (255, 255, 255)
        current_time = time.time()
        time_remaining = int(self.next_weather_change - current_time)
        weather_status = "Raining" if self.is_raining else "Not Raining"
        weather_text = font.render(f"Weather: {weather_status} | Next change in: {time_remaining}s", True, text_color)
        self.screen.blit(weather_text, (10, 10))

    def render(self):
        t1=time.time()
        if time.time() > self.storm.clock + self.storm.wait_time and self.storm.is_moving is False:
            self.storm.is_moving=True
            self.storm2.is_moving=True
            self.storm.clock = time.time()
        if time.time() > self.storm.clock + self.storm.move_time and self.storm.is_moving:
            self.storm.is_moving=False
            self.storm2.is_moving=False
            self.storm.clock = time.time()
        # if self.trees[0]==self.trees[1]:
        #     print('a')

        # print(self.dx)
        self.app.screen.fill((45, 149, 34))

        player_x, player_y = self.player.relative_position

        max_x = max(x for x, y in self.tiles.keys())
        min_x = min(x for x, y in self.tiles.keys())
        max_y = max(y for x, y in self.tiles.keys())
        min_y = min(y for x, y in self.tiles.keys())

        player_x2 = player_x * 2
        player_y2 = player_y * 2
        self.player_x2=player_x2
        self.player_y2 = player_y2

        #right
        if player_x2 + self.app.width >= max_x:
            for y in range(min_y, max_y + self.tile_size, self.tile_size):
                self.choose_tile(max_x + self.tile_size, y)
                # self.add_tile(max_x + self.tile_size, y, random.choice([images.grass, images.grass, images.water]))
        #left
        if player_x2 <= min_x:
            for y in range(min_y, max_y + self.tile_size, self.tile_size):
                self.choose_tile(min_x- self.tile_size, y)
                # self.add_tile(min_x - self.tile_size, y, random.choice([images.grass, images.grass, images.water]))
        #down
        if player_y2 + self.app.height >= max_y:
            for x in range(min_x, max_x + self.tile_size, self.tile_size):
                self.choose_tile(x, max_y + self.tile_size)
                # self.add_tile(x, max_y + self.tile_size, random.choice([images.grass, images.grass, images.water]))
        #up
        if player_y2 <= min_y:
            for x in range(min_x, max_x + self.tile_size, self.tile_size):
                self.choose_tile(x, min_y - self.tile_size)
                # self.add_tile(x, min_y - self.tile_size, random.choice([images.grass, images.grass, images.water]))

        visible_area = pygame.Rect(player_x2 - self.app.width // 2, player_y2 - self.app.height // 2,
                                   self.app.width * 2, self.app.height * 2)
        # print(self.tiles.items())
        player_x = int((self.player.relative_position[0]+self.player.gameObjectPos[0]))
        player_y = int((self.player.relative_position[1]+self.player.gameObjectPos[1]))
        for x in range(((player_x-self.app.width//2)//self.tile_size)*self.tile_size,((player_x+self.app.width//2)//self.tile_size)*self.tile_size+2*self.tile_size,self.tile_size):
            for y in range(((player_y - self.app.height//2) // self.tile_size) * self.tile_size,
                           ((player_y + self.app.height//2) // self.tile_size) * self.tile_size + 2*self.tile_size,
                           self.tile_size):
                try:
                    image=None
                    tile_image=self.tiles[(x,y)]
                    if tile_image=='tree1':
                        image=images.tree1
                    if tile_image=='tree1_farm':
                        image=images.tree_farm
                    if tile_image=='tree2':
                        image=images.tree2
                    if tile_image=='tree2_farm':
                        image=images.tree_farm
                    if tile_image=='tree3':
                        image=images.tree3
                    if tile_image=='tree3_farm':
                        image=images.tree_farm
                    if tile_image=='water':
                        image=images.water
                    if tile_image=='grass':
                        image=images.grass
                    if tile_image=='mine':
                        image=images.mine
                    if tile_image=='mine_farm':
                        image=images.mine_farm
                    if tile_image=='sand':
                        image=images.sand
                    self.screen.blit(image, (x - player_x2, y - player_y2))
                except:
                    pass

        # Render other game objects
        for obj in self.objects:
            if not isinstance(obj, (GameObject.Tile, GameObject.Player, GameObject.Storm, GameObject.Resource_Manager)):
                obj.render()
            elif isinstance(obj, GameObject.Player):
                obj.rotate_towards_cursor()
                obj.render()
            elif isinstance(obj, GameObject.Storm):
                obj.move()
                obj.render()
        for obj in self.resources.values():
            obj.render()
            # if isinstance(obj, GameObject.Chest):
            #     if obj.rect.colliderect(self.player.rect) and self.chest_ui is None:
            #         self.helpText = "Press E to open"
            #         self.selected_chest = obj
            #     elif self.helpText == "Press E to open" or (self.chest_ui is not None and obj.rect.colliderect(self.player.rect) is False):
            #         self.helpText = ""
            #         self.selected_chest = None
            #         self.chest_ui = None

        for chest in self.chests:
            if chest.rect.colliderect(self.player.rect) and self.chest_ui is None:
                self.selected_chest = chest
                # print(chest)
                if settings_values.pay_for_chest == True:
                    if self.resource_manager.resources[0][1]>=50:
                        if self.selected_chest.opened == False:
                            self.helpText = "Pay 50 gems to be able to open"
                            self.selected_chest = chest
                        else:
                            self.helpText = "Press E to open"
                            self.selected_chest = chest
                    else:
                        self.helpText = "Not enough gems"
                        self.selected_chest = None
                        self.chest_ui = None
                    break
                else:
                    self.helpText = "Press E to open"
                    self.selected_chest = chest
                    break

            elif self.helpText in ["Press E to open", "Pay 50 gems to be able to open", "Not enough gems"] or (
                    self.chest_ui is not None and self.selected_chest.rect.colliderect(self.player.rect) is False):
                self.helpText = ""
                self.selected_chest = None
                self.chest_ui = None

        for enemy in self.enemies:
            # if self.player.x - enemy.x > 0:
            #     enemy.angle = math.atan((self.player.y - enemy.y)/(self.player.x - enemy.x))
            # if self.player.x - enemy.x < 0:
            #     enemy.angle = math.atan((self.player.y - enemy.y)/(self.player.x - enemy.x)) + math.radians(180)

            # Calculate the distance between the player and the enemy
            distance_x = self.player.x - enemy.x
            distance_y = self.player.y - enemy.y

            # Calculate the total distance to move (5 blocks in this case)
            total_distance = enemy.speed

            # Calculate the angle towards the player
            angle = math.atan2(distance_y, distance_x)

            enemy.angle = angle

            zombie_x = enemy.x
            zombie_y = enemy.y

            collidesWithAnything = False
            canMoveRight = True
            canMoveLeft = True
            canMoveUp = True
            canMoveDown = True

            for obj in self.objects:
                if obj.collision is True:
                    obj_x = obj.x
                    obj_y = obj.y
                    if obj_x <= zombie_x + enemy.w <= obj_x + obj.w and ((zombie_y >= obj_y and zombie_y <= obj_y + obj.h) or (zombie_y + enemy.h >= obj_y and zombie_y + enemy.h <= obj_y + obj.h)):  # Left
                        collidesWithAnything = True
                        canMoveRight = False
                        # print(self.player.gameObjectPos[0], self.player.gameObjectPos[1], obj.x, obj.y)
                    elif obj_x <= zombie_x <= obj_x + obj.w and ((zombie_y >= obj_y and zombie_y <= obj_y + obj.h) or (zombie_y + enemy.h >= obj_y and zombie_y + enemy.h <= obj_y + obj.h)):  # Right
                        collidesWithAnything = True
                        canMoveLeft = False
                    if ((obj_x <= zombie_x <= obj_x + obj.w) or (obj_x <= zombie_x + enemy.w <= obj_x + obj.w)) and zombie_y >= obj_y and zombie_y <= obj_y + obj.h:  # Up
                        collidesWithAnything = True
                        canMoveUp = False
                    elif ((obj_x <= zombie_x <= obj_x + obj.w) or (obj_x <= zombie_x + enemy.w <= obj_x + obj.w)) and zombie_y + enemy.h >= obj_y and zombie_y + enemy.h <= obj_y + obj.h:  # Down
                        collidesWithAnything = True
                        canMoveDown = False

            move_x = min(total_distance, abs(distance_x)) * math.cos(angle)
            move_y = min(total_distance, abs(distance_y)) * math.sin(angle)

            if collidesWithAnything:
                # Calculate the movement in x and y directions
                if not canMoveDown and move_y > 0:
                    move_y = 0
                if not canMoveRight and move_x > 0:
                    move_x = 0
                if not canMoveUp and move_y < 0:
                    move_y = 0
                if not canMoveLeft and move_x < 0:
                    move_x = 0

                if time.time() > enemy.break_clock + enemy.break_cooldown and type(obj) == GameObject.Block:
                    print(obj.durability)
                    obj.durability -= enemy.break_damage
                    enemy.break_clock = time.time()


            # Update the enemy's position
            enemy.x += move_x
            enemy.y += move_y

            enemy.distance_to_player = math.sqrt(distance_x**2 + distance_y**2)


        self.generate_rain()

        self.environmentparticlesystem.update(self)
        self.environmentparticlesystem.draw(self.screen)
        if self.weapon_selection_ui:
            self.weapon_selection_ui.render()
        self.weaponparticlesystem.update(self)
        self.weaponparticlesystem.draw(self.screen)

        self.update_day_night_cycle()
        self.overlay_surface.set_alpha(self.overlay_alpha)
        self.screen.blit(self.overlay_surface, (0, 0))

        self.render_weather_info()
        self.render_day_info()

        if self.time_of_day in ["Night", "Evening"]:
            if self.enemy_spawns_left - self.enemies_per_spawn >= 0 and time.time_ns() > self.spawn_delay_clock + self.delay_between_spawns * 1_000_000_000:
                for _ in range(self.enemies_per_spawn):
                    if random.randint(0, 100) < 50:
                        x_offset = random.randint(-self.app.width//2 - self.enemy_spawn_offset, self.player.x - self.enemy_spawn_offset)
                    else:
                        x_offset = random.randint(self.player.x + self.enemy_spawn_offset, self.app.width//2 + self.enemy_spawn_offset)

                    if random.randint(0, 100) < 50:
                        y_offset = random.randint(-self.app.height//2 - self.enemy_spawn_offset, self.player.y - self.enemy_spawn_offset)
                    else:
                        y_offset = random.randint(self.player.y + self.enemy_spawn_offset, self.app.height//2 + self.enemy_spawn_offset)

                    zombie = GameObject.Zombie(self, self.player.x + x_offset, self.player.y + y_offset, 100, 100, images.player, True)

                    if random.randint(0, 100) > 75:
                        zombie.health = 100
                    if random.randint(0, 100) > 85:
                        zombie.speed = 6

                    self.enemies.append(zombie)
                    self.objects.append(zombie)
                    self.enemy_spawns_left -= 1
                    self.spawn_delay_clock = time.time_ns()


        if self.chest_ui is not None:
            self.chest_ui.render()

        font = pygame.font.Font(self.font, int(48 * self.app.scale))
        display_text = font.render(self.helpText, True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)

        if self.player.isShooting and isinstance(self.hotbar.items[self.hotbar.selected_slot], weapon.Weapon):
            if self.hotbar.items[self.hotbar.selected_slot].firemode == 1 and time.time_ns() > self.time_of_last_shot + 1_000_000_000 /self.hotbar.items[self.hotbar.selected_slot].fire_rate: # Full Auto
                self.hotbar.items[self.hotbar.selected_slot].shoot()
                self.time_of_last_shot = time.time_ns()
                #time.sleep(1/self.hotbar.items[self.hotbar.selected_slot].fire_rate)
            if self.hotbar.items[self.hotbar.selected_slot].firemode == 2 and self.burst_shots < 3: # Burst
                if time.time_ns() > self.time_of_last_shot + 70_000_000:
                    self.hotbar.items[self.hotbar.selected_slot].shoot()
                    self.burst_shots += 1
                    self.time_of_last_shot = time.time_ns()

        self.render_player_info()
        self.hotbar.render()

        if isinstance(self.hotbar.items[self.hotbar.selected_slot], weapon.Weapon):
            firemode_text = self.hotbar.items[self.hotbar.selected_slot].get_firemode_text()
            font = pygame.font.Font(self.font, int(24 * self.app.scale))
            firemode_display = font.render(f"Fire Mode: {firemode_text}", True, self.font_color)
            firemode_display_rect = firemode_display.get_rect()
            firemode_display_rect.topright = (self.app.width - 30, self.app.height - 75+ firemode_display_rect.height//2)
            self.app.screen.blit(firemode_display, firemode_display_rect)

        current_time = time.time()
        if current_time >= self.next_weather_change:
            if self.is_raining:
                self.is_raining = False
                self.next_weather_change = current_time + random.uniform(60, 180)
            else:
                self.is_raining = True
                self.next_weather_change = current_time + random.uniform(30, 180)


        if current_time - self.last_fps_time >= 1:
            self.current_fps = int(1 / (current_time - t1))
            self.last_fps_time = current_time

        font = pygame.font.Font(self.font, int(24 * self.app.scale))
        fps_text = font.render(f"FPS: {self.current_fps}", True, self.font_color)
        fps_text_rect = fps_text.get_rect()
        fps_text_rect.midtop = (self.app.width//2, 10)
        self.app.screen.blit(fps_text, fps_text_rect)

        t2 = time.time()
        # print(t2-t1)

        if self.place_mode:
            direction_x = (math.cos(self.player.angle) * self.place_block_radius // 96) * 96
            direction_y = (math.sin(self.player.angle) * self.place_block_radius // 96) * 96

            # Calculate the position of the tile 2 blocks away in the direction the player is facing
            # closest_tile_x = round((self.player.relative_position[
            #                             0] + self.app.width // 2 + direction_x * self.tile_size) / self.tile_size) * self.tile_size
            # closest_tile_y = round((self.player.relative_position[
            #                             1] + self.app.height // 2 + direction_y * self.tile_size) / self.tile_size) * self.tile_size

            closest_tile_x = ((self.player.x + 100 + direction_x) // 96) * 96
            closest_tile_y = ((self.player.y + 100 + direction_y) // 96) * 96

            pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(closest_tile_x, closest_tile_y, 96, 96))


    def generate_rain(self):
        if self.is_raining:
            for _ in range(3):
                x = random.randint(-self.app.width // 10, self.app.width)
                y = 0
                vx = 1
                vy = random.uniform(2, 5)
                speed = 2
                lifespan = 250
                size = random.randint(5, 7)
                red, green, blue, alpha = 25, 25, 250, 255
                shape = 'water_drop'
                damage = 0
                self.environmentparticlesystem.add_particle(x, y, vx, vy, speed, lifespan, size, red, green, blue,
                                                            alpha, shape, damage, face_direction=True)

    def events(self):
        keys = pygame.key.get_pressed()

        collidesWithAnything = False
        player_x = self.player.x
        player_y = self.player.y

        for obj in self.objects:
            if obj.collision is True:
                obj_x = obj.x
                obj_y = obj.y
                if obj_x <= player_x + self.player.w <= obj_x + obj.w and ((player_y >= obj_y and player_y <= obj_y + obj.h) or (player_y + self.player.h >= obj_y and player_y + self.player.h <= obj_y + obj.h)): # Left
                    collidesWithAnything = True
                    self.player.canMoveRight = False
                    #print(self.player.gameObjectPos[0], self.player.gameObjectPos[1], obj.x, obj.y)
                elif obj_x <= player_x <= obj_x + obj.w and ((player_y >= obj_y and player_y <= obj_y + obj.h) or (player_y + self.player.h >= obj_y and player_y + self.player.h <= obj_y + obj.h)): # Right
                    collidesWithAnything = True
                    self.player.canMoveLeft = False
                if ((obj_x <= player_x <= obj_x + obj.w) or (obj_x <= player_x + self.player.w <= obj_x + obj.w)) and player_y >= obj_y and player_y <= obj_y + obj.h:  # Up
                    collidesWithAnything = True
                    self.player.canMoveUp = False
                elif ((obj_x <= player_x <= obj_x + obj.w) or (obj_x <= player_x + self.player.w <= obj_x + obj.w)) and player_y + self.player.h >= obj_y and player_y + self.player.h <= obj_y + obj.h:  # Down
                    collidesWithAnything = True
                    self.player.canMoveDown = False


        if collidesWithAnything is False:
            self.player.canMoveRight = True
            self.player.canMoveLeft = True
            self.player.canMoveUp = True
            self.player.canMoveDown = True

        if keys[pygame.K_w] and self.player.canMoveUp:
            self.dy = -self.speed
        elif keys[pygame.K_s] and self.player.canMoveDown:
            self.dy = self.speed
        else:
            self.dy = 0

        if keys[pygame.K_a] and self.player.canMoveLeft:
            self.dx = -self.speed
        elif keys[pygame.K_d] and self.player.canMoveRight:
            self.dx = self.speed
        else:
            self.dx = 0
        # print('aa',2*self.dx)
        current_time = time.time()
        if current_time - self.last_hunger_update >= 10:
            if self.player.hunger > 70:
                self.player.delta_health = -(1 / (self.player.hunger)*100)
            elif self.player.hunger < 70:
                self.player.delta_health = (1 / (self.player.hunger) * 100)
                self.player.image = images.damagedplayer
            if self.player.thirst > 70:
                self.player.delta_health += -(1 / (self.player.thirst) * 100)
            elif self.player.thirst < 70:
                self.player.delta_health += (1 / (self.player.thirst) * 100)
                self.player.image = images.damagedplayer
            if self.player.hunger < 0:
                self.player.hunger = 0
            if self.player.thirst < 0:
                self.player.thirst = 0
            self.player.hunger -= self.player.delta_hunger
            self.player.thirst -= self.player.delta_thirst
            self.player.health -= self.player.delta_health
            self.last_hunger_update = current_time
        self.move_x+=2*self.dx
        self.move_x=self.move_x%self.tile_size
        self.move_y += 2*self.dy
        self.move_y = self.move_y % self.tile_size
        # print(self.move_x,self.move_y)
        if keys[pygame.K_e]:
            if self.e==False:
                self.e = True
                try:
                    self.collect()
                except:
                    self.start_building()


        else:
            if self.e:
                self.end_building()
                self.e=False
        # print(self.e)
        if self.e:
            self.build()

        # Update player position based on current dx and dy
        self.player.relative_position[0] += self.dx
        self.player.relative_position[1] += self.dy
        # print(self.player.relative_position)

        self.player.gameObjectPos[0] += self.dx
        self.player.gameObjectPos[1] += self.dy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
            self.player.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.hotbar.select_slot(0)
                elif event.key == pygame.K_2:
                    self.hotbar.select_slot(1)
                elif event.key == pygame.K_3:
                    self.hotbar.select_slot(2)
                elif event.key == pygame.K_4:
                    self.hotbar.select_slot(3)
                elif event.key == pygame.K_5:
                    self.hotbar.select_slot(4)

                elif event.key == pygame.K_e:
                    if self.selected_chest is not None:
                        if self.chest_ui is not None:
                            self.chest_ui = None
                        else:
                                if self.selected_chest.opened == True:
                                    pass
                                else:
                                    self.selected_chest.opened = True
                                    self.resource_manager.resources[0][1] -= 50
                                    break
                                self.chest_ui = hotbar.Hotbar(self, self.selected_chest.x - 100,
                                                              self.selected_chest.y - 100, 5)
                                for i in range(len(self.selected_chest.Items)):
                                    self.chest_ui.add_item(self.selected_chest.Items[i], i)
                                self.helpText = ""
                elif event.key == pygame.K_q:
                    self.place_mode = not self.place_mode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.place_mode:
                if self.resource_manager.resources[1][1] >= 10:
                    direction_x = (math.cos(self.player.angle) * self.place_block_radius // 96) * 96
                    direction_y = (math.sin(self.player.angle) * self.place_block_radius // 96) * 96

                    closest_tile_x = ((self.player.x + 100 + direction_x) // 96) * 96
                    closest_tile_y = ((self.player.y + 100 + direction_y) // 96) * 96

                    # self.add_tile(closest_tile_x, closest_tile_y, 'your_block_image_here', force=True)
                    self.objects.append(GameObject.Block(self, closest_tile_x, closest_tile_y, 96, 96, images.wood_planks, True))

                    self.resource_manager.resources[1][1] -= 10
                    print(closest_tile_x, closest_tile_y)

                    # Deduct 10 wood from the player's resources
                    # self.resource_manager.resources['wood'] -= 10
            if self.weapon_selection_ui:
                selected_weapon = self.weapon_selection_ui.handle_event(event)
                if selected_weapon:
                    selected_weapon.total_ammo += self.weapon_selection_ui.return_ammothing_ammo()
                    self.weapon_selection_ui = None
