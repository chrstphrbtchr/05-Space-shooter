import sys, logging, os, random, math, open_color, arcade, time

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
MOVE_SPEED = 5
SCREEN_TITLE = "I, Foreign Eye"


j = 2000
NUM_ENEMIES = 4
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 73
PLAYER_HP = 10
KILL_SCORE = 981

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class BadBullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/badbullet.png", 1.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.hurts = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y -= self.dy

# OK!


def gameover():
    arcade.draw_text(str("G A M E \n OVER!!!"), 50, SCREEN_HEIGHT - 40, open_color.lime_3, 36) ####################################
    


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets\ship01_fly\sprite_ship09.png", 0.7)
        self.hp = PLAYER_HP
        (self.center_x, self.center_y) = STARTING_LOCATION
        


class Enemy(arcade.Sprite):
    def __init__(self, position):
        super().__init__()
        self.frequency = 1
        self.timer = time.time()
        eyes = ["0","1","2","3","4","5","6","7"]
        self.eyeRange = len(eyes)-1
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
        for e in eyes:
            texture = arcade.load_texture("assets\L2 Eye Animation\L2E{}.png".format(e))
            self.textures.append(texture)
        whichTexture = random.randint(0,self.eyeRange)
        self.set_texture(whichTexture)

    def update(self):
        now = time.time()
        if (now - self.timer) >= self.frequency:
            self.timer = time.time()
            whichTexture = random.randint(0,self.eyeRange)
            self.set_texture(whichTexture)



        


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.blue_4)
        self.background = None
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.badbullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.deadbullet_list = []

    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 160 * (i+1)
            y = 520
            enemy = Enemy((x,y))
            
           
            self.enemy_list.append(enemy)
        self.player_list.append(self.player)

        self.background = arcade.load_texture("assets/bckgrnd.png")
    

    def update(self, delta_time):
        self.bullet_list.update()
        self.badbullet_list.update()
        self.player.update()
        self.player_list.update()
        self.enemy_list.update()
        
    
        
        
        for e in self.enemy_list:

            damage = arcade.check_for_collision_with_list(e,self.bullet_list)
            # for every bullet that hits, decrease the hp and then see if it dies
            for z in damage:
                e.hp = e.hp - z.damage
                z.kill()        # Removes z (the bullet?) - add img for explosion in next project.
                                # .kill() removes sprites.
            # increase the score
            
            # e.kill() will remove the enemy sprite from the game
                if e.hp <= 0:
                    self.score = self.score + KILL_SCORE
                    e.kill()
                    self.enemy_list.update() 
                    self.deadbullet_list.append(BadBullet) 
                    self.deadbullet_list.append(e)
                else:
                    self.score = self.score + HIT_SCORE
            # the pass statement is a placeholder. Remove line 81 when you add your code

            
            for f in range(NUM_ENEMIES):
                if random.randint(1,j) <= 5:
                    print("Fire")
                    x = 160 * (f+1)
                    y = 500
                    badbullet = BadBullet((x,y), (0,10), BULLET_DAMAGE)
                    self.badbullet_list.append(badbullet)
                    if e.hp <=0:
                        f = -1

            for p in self.player_list:
                hurts = arcade.check_for_collision_with_list(p,self.badbullet_list)
                for h in hurts:
                    p.hp = p.hp - h.hurts
                    h.kill()
                    p.kill()
                    if p.hp <= 0:
                        #self.player = arcade.SpriteList
                        p.kill()
                        self.player_list.update()
                        

                
                

            


        #################################################################


    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH //2, SCREEN_HEIGHT //2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        #self.player.draw()
        self.bullet_list.draw()
        self.badbullet_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        

    

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            print("Left")
            self.player.change_x = -MOVE_SPEED
        elif key == arcade.key.RIGHT:
            print("Right")
            self.player.change_x = MOVE_SPEED
        elif key == arcade.key.UP:
            print("Up")
            self.player.change_y = MOVE_SPEED
        elif key == arcade.key.DOWN:
            print("Down")
            self.player.change_y = -MOVE_SPEED
        elif key == arcade.key.SPACE:
            print("Fire")
            x = self.player.center_x
            y = self.player.center_y + 88
            bullet = Bullet((x,y), (0,10), BULLET_DAMAGE)
            self.bullet_list.append(bullet)


    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0




def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()