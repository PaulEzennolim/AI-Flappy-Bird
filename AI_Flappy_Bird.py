# Import all the necessary modules
import pygame
import neat
import os
import random # random is for randomly placing the height of the tubes

# Setting dimensions of the screen
WIN_WIDTH = 500
WIN_HEIGHT = 800

"""
# Loading bird images as a list. bird1, bird2 and bird3 are loaded in sequence to create the animation effect (check
imgs folder).
"""
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs", "bird1.png"))),  
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs", "bird2.png"))),  
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs", "bird3.png")))   
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs", "pipe.png")))  
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs", "base.png")))  
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs", "bg.png")))  

# Bird class will represent the bird objects moving
class Bird: 
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 # MAX_ROTATION is how much the bird is going to tilt
    ROT_VEL = 20 # ROT_VEL is how much the bird is going to rotate on each frame every time that we move the bird
    """
    ANIMATION_TIME is how long we are going to show each bird animation. By changing this to be larger or smaller,
    we can change how fast or how slow the bird is going to be flapping its wings in the frame.
    """
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x # Represents the starting position of the bird
        self.y = y # Represents the starting position of the bird
        """
        self.tilt is how much the image is tilted. This starts of as 0 because the bird is going to be looking flat.
        """
        self.tilt = 0 
        self.tick_count = 0 
        self.velocity = 0 
        self.height = self.y 
        """
        self.img_count is to know which image is currently showing for the bird.
        """
        self.img_count = 0 
        """
        self.img is referencing BIRD_IMGS and BIRD_IMGS[0] is bird1.png.
        """
        self.img = self.IMGS[0]

    # jump is called when the bird has to flap up/jump up
    def jump(self):
        """
        self.velocity is negative because in pygame, the coordinate (0,0) is the top left of the screen. Which means 
        to go upwards a negative velocity is needed and to go downwards a positive velocity is needed. 
        """
        self.velocity = -10.5 
        self.tick_count = 0  # self.tick_count keeps track of when the bird last jumped
        self.height = self.y  # self.height keeps track of where the bird jumped from

    # move is called every single frame to move the bird
    def move(self): 
        """
        self.tick_count += 1 means a tick happened/ a frame went by and keeps track of how many times the bird has 
        moved since the last jump.
        """
        self.tick_count += 1

        """
        d (displacement) is how many pixels the bird is moving up or down this frame. This will be what the bird ends
        up actually moving when we change the y position of the bird.
        In this equation, self.tick_count represents how many seconds the bird has been moving for. Every time the 
        bird changes direction or we apply a velocity to the bird, the bird either moves up or it stops moving up, 
        this self.tick_count is going to keep increasing. Based on what that self.tick_count is the bird is either 
        moving up, where the bird has reached the top of its jump, and now its moving down.
        As soon as the bird jumps, self.tick_count is reset to 0, the height of our bird is set to self.y
        (self.height = self.y) and the velocity of the bird is set to -10.5 (self.velocity = -10.5). When 
        self.tick_count = 1, d = -10.5*1 + 1.5*1**2 = -9. On this current frame the bird is moving 9 pixels upwards 
        and in the next frame it'll be moving less pixels upwards, 7 then 5 then 3 and so on, until d = 0. Then the
        bird goes down and is moving positive again. That results in an arc for the bird as it does its jump.
        """
        d = self.velocity * self.tick_count + 1.5 * self.tick_count**2 

        if d >= 16: # Makes sure that the birds velocity is not moving too far up or too far down (termianl velocity)
            d = 16 # If the bird is moving down more than 16, simply move down 16
         
        if d < 0:
            d -= 2 # This if statement is saying if the bird is moving upwards, let the bird move up a little bit more
        
        self.y = self.y + d # Change the bird's y position based on the displacement

        # Adjusting the bird's tilt based on its vertical movement
        """
        In this case the bird will be tilted upwards. We are checking if d < 0, which means the bird is moving upwards 
        or self.y < self.height + 50, which means every time the bird jumps, the bird keeps tracks from where it jumped
        from. Depending on where the bird jumped from, it checks if its position is currently above from where it jumped
        from. If it is, that means that the bird is still moving upwards. Even if the bird is on a downwards curve, the
        bird will still make it look like its upwards a little bit. Once the bird gets a little bit below the position 
        it jumped from, then the bird will begin to tilt downwards.
        """
        if d < 0 or self.y < self.height + 50:

            if self.tilt < self.MAX_ROTATION:
                """
                Rather than moving the bird up slowly because the MAX_ROTATION is only 25, the birds rotation is 
                immediately set to be 25 degrees.
                """
                self.tilt = self.MAX_ROTATION
        else: # If the bird is not moving upwards and we dont want to tilt it upwards, then tilt it downwards
            """
            This if statement allows for the bird to rotate completely 90 degrees. As the bird starts falling downwards 
            faster, it looks as if it is nose diving into the ground. That is why MAX_ROTATION has not been used,
            because when the bird is going up we dont want the bird to tilt completely up, only slightly. When the 
            bird is going down, the bird should tilt all the way down to 90 degrees.
            """
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL # How much the bird is going to get rotated downwards

    def draw(self, win): # win represents the window that the bird is being drawn onto
        """
        self.img_count keeps track of how many ticks we have shown a current image for. Ticks refers to how many times 
        has the main game loop run and how many times have we already shown one image.
        """
        self.img_count += 1

        """
        Checking what image should be shown based on the current img_count. If the img_count < 5 (ANIMATION_TIME), the
        first flappy bird image is displayed. If we get to point where the ANIMATION_COUNT is larger than 5, the next 
        elif statement is checked. If the img_count < 10 (ANIMATION_TIME * 2), the second flappy bird image is 
        displayed. If the img_count < 15 (ANIMATION_TIME), the last flappy bird image is displayed. Then the second 
        image is shown again, then the first image is shown again and reset the img_count. This creates the flaaping 
        animation. If we reset img_count after the last image (IMGS[2]), the bird would flapp up and then it would 
        instantly go back to its starting position, looking like it skipped a frame.
        """
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        # When the bird is tilted almost 90 degrees going downwards, the birds wings should not flap 
        if self.tilt <= -80:
            self.img = self.IMGS[1] # The image where the wings are leveled will be displayed instead
            """
            When the bird jumps back up, the bird won't skip a frame. The bird will start at what it should be to show 
            this image, which is an ANIMATION_TIME of 10.
            """
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt) # Rotates the image around the top left corner
        # Rotates the image around the centre
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    # get_mask is used when there are collisions in the game
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
class Pipe:
    GAP = 200 # GAP represents how much space is between the pipes
    """
    VEL represents how fast the pipes are going to be moving. In flappy bird, the bird doesn't move, but all the objects
    on the sceen move. The pipes should be moving backwrds or towards the bird, to make it look like it's moving.
    """
    VEL = 5

    """
    x is used and not y or not both of them, because the height of theses tubes and where they show up on the screen is
    completely random everytime.
    """
    def __init__(self, x):
        self.x = x
        self.height =  0

        """
        self.top, self.bottom, self.PIPE_TOP, self.PIPE_BOTTOM are variables created to keep track of where the top and
        bottom of the pipe is going to be drawn. self.PIPE_TOP = pygame.transfrom.flip(PIPE_IMG, False, True) and 
        self.PIPE_BOTTOM = PIPE_IMG gets the image for the top pipe and the bottom pipe.The pipe starts facing 
        vertically (check imgs folder), but a pipe that faces upside down is also needed. So we flip the pipe image and 
        store that image inside the class.
        """
        self.top = 0
        self.bottom = 0 
        self.PIPE_TOP = pygame.transfrom.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False # self.passed stands for if the bird is already passed by this pipe
        self.set_height()

    """
    The method set_height() is going to define where the top and bottom of the pipe is and how tall the pipe is 
    (How tall is the top one vs the bottom one and wheres that gap) and that is going to be randomly defined.
    """    
    def set_height(self):
        """
        random.randrange() gets a random number for where the top of the pipe should be.
        """   
        self.height = random.randrange(50, 450)
        """
        To figure out where the top of the pipe should be, we need to figure out the top left position of the image for 
        our pipe. Depending on where you want the top pipe to be located, to figure out where the pipe should be
        drawn on the screen, we need to figure the height of that image and substract. So the pipe will most likely be 
        drawn at a negative location, but since it is so long, the pipe will go down the screen and where we want the 
        bottom of the top pipe to be will be in the correct position.
        """   
        self.top = self.height - self.PiPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    """
    To move the pipe, the x position needs to be changed based on the velocity that the pipe should move each frame.
    """   
    def move(self):
        self.x -= self.VEL # Every time move is called, the pipe will be moved to the left based on the velocity

    # draw method is going to draw our pipe. A pipe is considered both top and bottom, this method will draw both
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    """
    A mask is an array/list of where all of the pixles are inside of a box. If we have two boxes and there are two cicles 
    within each box, a mask tells us where these circles are. So we can see if these two boxes collide by checking if 
    any of the pixels inside these boxes are touching. Because these pixles have transparent backgrounds, a mask is 
    able to see if the pixle is transparent or if its not. Then it creates a 2D list and it's going to have as many 
    rows as there are pixles going down and as many columns as there is pixes going across. Imagine that is 10 by 10, 
    so there'd be 10 rows and 10 columns.We'll have one list for each image, a mask will compare these two lists 
    together and will see if there is any pixle in each list that collide with each other or sit in the same area. That
    way we can dtermine whether there is pixel perfect collision.
    """ 
    def collide(self, bird):
        bird_mask = bird.get_mask()
        # Creates a mask for the top pipe and the bottom pipe
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        """
        offset is how far away these masks are from each other, so the function we are passing this to knows how to 
        check these pixles up against each other.
        """
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        """
        b_point and t_point tells us the point of collision/overlap using the bottom_offset (how far away the bird is from the 
        bottom pipe) and the top_offset (how far away the bird is from the bottom pipe). If there is no collision, the 
        functions return none.
        """
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        # If there is no collision, both t_point and b_point will be none
        if t_point or b_point: # If t_point and b_point are not none
            return True # There is a collision
        return False

class Base:
    VEL = 5 # VEL must be the same as the pipe, otherwise there is an inconsistent speed on screen
    WIDTH = BASE_IMG.get_width() # gets how wide one of these base images are
    IMG = BASE_IMG

    def __init__(self, y): # The x is going to be moving to the left, so no need to define it
        self.y = y 
        self.x1 = 0 # One base at x position 0
        self.x2 = self.WIDTH # One base directly behind the base at x position 0
    
    def move(self):
        # Move both bases with the same velocity
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        """
        These if statement checks if one of those bases is ever of the screen completely, if it is the base is cycled 
        to the back (behind the base that is currently on screen).
        """
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    # draws the base
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

# drw_window draws the window for the game
def draw_window(win, bird):
    # win.blit draws whatever is in the paranthesis on the window
    win.blit(BG_IMG, (0,0)) # (0,0) is the topleft positon of the image where its being drawn
    """
    When doing bird.draw(win), the draw method is called and it'll handle all the animations, tilting and draw the bird.
    """
    bird.draw(win)
    pygame.display.update()# updates the displays

# main runs the loop of the game
def main():
    bird = Bird(200, 200) # Starting position of the bird
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # Creates a pygame window
    """
    clock will set the tick rate/frame rate (how fast the while loop is running) to be at a consistent rate. 
    """
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30) # We are going to do at most 30 ticks every second
        """
        for event in pygame.event.get() keeps track of whenever something happens, eg the user clicking the mouse, the 
        for loop will run
        """
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False

        # bird.move() # bird.move is called every frame. Everytime the while loop ticks, the bird is going to move   
        draw_window(win, bird)
    
    pygame.quit()
    quit()

main()
