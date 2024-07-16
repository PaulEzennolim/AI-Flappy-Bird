"""
The classic game of flappy bird. Made with python and pygame. Features pixel perfect collision using masks.
"""

# Import all the necessary modules
import pygame
import random # random is for randomly placing the height of the tubes
import os
import time
import neat
import pickle
pygame.font.init()  # init font

# Setting dimensions of the screen
WIN_WIDTH = 600
WIN_HEIGHT = 800

FLOOR = 730
STAT_FONT = pygame.font.SysFont("bold", 50)
END_FONT = pygame.font.SysFont("bold", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

"""
Load bird images as a list. bird1, bird2, and bird3 are loaded in sequence to create an animation effect 
(check imgs folder).
"""
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs","bird" + str(x) + ".png"))) 
               for x in range(1,4)]

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs", "pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "imgs","bg.png")).convert_alpha(), (600, 900))
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "imgs","base.png")).convert_alpha())

gen = 0

# Bird class representing the flappy bird
class Bird:
    MAX_ROTATION = 25  # Maximum tilt angle for the bird in degrees
    IMGS = bird_images
    ROT_VEL = 20 # Rotation velocity for the bird in degrees per frame
    ANIMATION_TIME = 5 # Duration to display each bird animation frame, affecting wing flap speed

    def __init__(self, x, y):
        self.x = x # Bird's starting x position
        self.y = y # Bird's starting y position
        self.tilt = 0  # Initial tilt angle of the bird image, starting flat (0 degrees)
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0 # Counter to track the current bird image for animation
        self.img = self.IMGS[0] # Initial image of the bird, referencing the first image in BIRD_IMGS (bird1.png)

    # Make the bird jump
    def jump(self):
        """
        Initial velocity of the bird, negative to move upwards in pygame coordinates where (0,0) is the top left of 
        the screen.
        """
        self.vel = -10.5
        self.tick_count = 0 # Keeps track of the time since the bird last jumped
        self.height = self.y # Keeps track of the vertical position from which the bird last jumped

    # Make the bird move
    def move(self):
        self.tick_count += 1
        """
        displacement calculates how many pixels the bird moves up or down in each frame. The self.tick_count keeps 
        track of the number of frames since the bird last jumped. When the bird changes direction or its velocity, 
        self.tick_count increases accordingly. Initially, when the bird jumps, self.tick_count is reset to 0, and 
        self.height is set to self.y (self.height = self.y), while the bird's velocity is set to -10.5 
        (self.velocity = -10.5). For instance, when self.tick_count = 1, displacement is calculated as 
        -10.5 * 1 + 0.5 * 3 * 1 ** 2 = -9. This means the bird moves 9 pixels upwards in this frame. In subsequent 
        frames, the bird continues to move upwards less and less until displacement becomes 0. Then, the bird 
        starts descending, moving positively again, resulting in an arc-like trajectory for its jump.
        """
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement

        """
        Ensures the bird's velocity does not exceed a terminal velocity in either upward or downward motion
        """
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            """
            Adjusts the displacement when the bird is moving upwards, allowing it to ascend slightly more
            """
            displacement -= 2

        self.y = self.y + displacement # Update the bird's vertical position based on the calculated displacement

        """
        # Adjusting the bird's tilt based on its vertical movement. If displacement is negative (indicating the bird is 
        moving upwards) or if the bird's current y-position is above its jump height plus 50 pixels, tilt the bird 
        upwards to simulate a flapping motion. Once the bird starts descending beyond its jump height, tilt it downwards.
        """
        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                """
                Rather than gradually tilting the bird upwards due to the limited MAX_ROTATION of 25 degrees, the tilt 
                angle is immediately set to 25 degrees.
                """
                self.tilt = self.MAX_ROTATION
        else: # If the bird is not moving upwards or we don't want it to tilt upwards, then tilt it downwards
            """
            If the bird is falling downward (displacement > 0), tilt it downwards up to 90 degrees. We do not limit 
            the tilt to MAX_ROTATION because we want the bird to tilt more significantly when diving down, giving the 
            appearance of a nose dive.
            """
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL # Decreases the bird's tilt angle to make it rotate downwards

    # Draw the bird onto the specified window (win)
    def draw(self, win):
        self.img_count += 1 # Tracks how many times the current bird image has been displayed in the game loop ticks

        """
        Determines which bird image to display based on img_count for animation. The animation cycles through three 
        images (flapping wings) based on ANIMATION_TIME. When img_count reaches ANIMATION_TIME * 4 + 1, it resets to 
        create smooth animation loops.
        """
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # When the bird tilts almost 90 degrees downwards, it stops flapping its wings to simulate a nose dive
        if self.tilt <= -80:
            self.img = self.IMGS[1] # Display the image where the wings are level
            self.img_count = self.ANIMATION_TIME*2 # Reset img_count to continue the flapping animation smoothly

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt) # Title the bird

    # get_mask generates a collision mask for the current bird image to handle collisions in the game
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

#Represents a pipe object
class Pipe():
    GAP = 200 # GAP represents the vertical space between the upper and lower pipes
    """
    VEL represents the velocity at which the pipes move towards the bird, creating the illusion of the bird flying 
    forward in Flappy Bird.
    """
    VEL = 5

    """
    The x parameter is used because the vertical positioning (height) of the pipes on the screen is randomly generated 
    each time.
    """
    def __init__(self, x):
        self.x = x
        self.height = 0
        """
        Variables to track the top and bottom positions of the pipe for drawing. PIPE_TOP and PIPE_BOTTOM store the 
        images for the top-facing and bottom-facing pipes respectively. PIPE_TOP is flipped vertically from the 
        original pipe image (check imgs folder) to create the bottom-facing pipe image.
        """
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img
        self.passed = False # Flag to indicate if the bird has already passed this pipe
        self.set_height()
    
    """
    Sets the height of the pipe and calculates positions for top and bottom pipes. The top pipe's height and position 
    are randomly determined, creating a gap of GAP pixels between it and the bottom pipe.
    """  
    def set_height(self):
        self.height = random.randrange(50, 450) # Determine a random height for the top of the pipe within a range
        """
        Calculate positions for the top and bottom of the pipe based on its height and gap.
        """   
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    """
    Update the horizontal position of the pipe based on its velocity.
    """
    def move(self):
        self.x -= self.VEL # Move the pipe to the left based on its velocity

    # Draw both the top and bottom pipes at their current positions
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    """
    A mask represents an array of pixels inside a defined boundary. In the context of collision detection, it helps 
    determine if two objects collide by checking the overlap of non-transparent pixels in their respective masks. Each 
    image in the game has its own mask, which consists of rows and columns corresponding to the pixel layout of the 
    image. By comparing these masks, the game can accurately detect pixel-perfect collisions between objects.
    """
    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        # Creates masks for the top and bottom pipes for collision detection
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        # Calculates offsets to determine pixel-perfect collision position between bird and pipes
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        # Determines collision points using offsets (bottom_offset and top_offset). Returns None if no collision occurs
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        """
        Checks for collision based on overlap points between bird and pipes. Returns True if collision detected, 
        False otherwise.
        """
        if b_point or t_point:
            return True # Collision detected

        return False # No collision detected

# Represents the moving floor of the game
class Base:
    """
    VEL represents the speed at which the pipes and other moving elements on the screen move horizontally. It should be 
    synchronized with the speed of the pipes to maintain consistent movement across the screen.
    """
    VEL = 5
    WIDTH = base_img.get_width() # WIDTH represents the width of a base image used in the game
    IMG = base_img

    """
    Initializes a base object with a given y-coordinate.

    Parameters:
    y (int): The y-coordinate representing the vertical position of the base on the screen.

    Note:
    Since the base moves horizontally to the left, the x-coordinate is managed dynamically
    and does not need to be explicitly defined in the constructor.
    """
    def __init__(self, y):
        self.y = y
        self.x1 = 0 # x-coordinate of the first base image, positioned at the start of the screen
        self.x2 = self.WIDTH # x-coordinate of the second base image, positioned directly behind the first base

    # Move floor so it looks like its scrolling
    def move(self):
        # Move both base images horizontally with the same velocity (VEL)
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Check if either base image has moved completely off-screen, then cycle it to the back
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH # Move self.x1 to the position just behind self.x2

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH # Move self.x2 to the position just behind self.x1

    # Draw the floor, this is two images that move together
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotates an image and blits it onto a surface at a specified angle around its center.
    Args:
    - surf: The surface (window) onto which the rotated image will be drawn.
    - image: The image surface that you want to rotate and draw.
    - topleft: Tuple (x, y) specifying the top-left corner coordinates where the rotated image will be positioned.
    - angle: The angle in degrees by which you want to rotate the image.
    """
    # Rotate the original image by the specified angle
    rotated_image = pygame.transform.rotate(image, angle)
    # Align the center of the rotated image with the original image's center
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
     # Blit (draw) the rotated image onto the surface ('surf') at the calculated position
    surf.blit(rotated_image, new_rect.topleft)

# Draws the window for the main game loop
def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    # Ensure generation number starts from 1 for display purposes
    if gen == 0:
        gen = 1

    # Draw the background image on the game window
    win.blit(bg_img, (0,0))

    # Draw all pipes on the game window
    for pipe in pipes:
        pipe.draw(win)

    # Draw the base (ground) on the game window
    base.draw(win)

    # Draw each bird on the game window
    for bird in birds:
        # Optionally draw lines from birds to pipes (for debugging or visualizing)
        if DRAW_LINES:
            try:
                 # Draw a line from bird center to top pipe center
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), 
                            (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                # Draw a line from bird center to bottom pipe center
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), 
                            (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # Draw each bird's image on the game window
        bird.draw(win)

    # Render and display the current score on the game window
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # Render and display the current generation number on the game window
    gen_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(gen_label, (10, 10))

    # Render and display the number of alive birds on the game window
    alive_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(alive_label, (10, 50))

    # Update the display to show all changes made to the game window
    pygame.display.update()

"""
Runs the simulation of the current population of birds and sets their fitness based on the distance they reach in the 
game.
"""
def eval_genomes(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1
    """
    List to keep track of the neural network controlling each bird in the population.Each element corresponds to the 
    neural network associated with a bird's behavior and position on the screen.
    """
    nets = []
    birds = []
    """
    List to keep track of genomes associated with each bird in the population. Each element corresponds to the genome 
    of a specific bird, allowing users to modify bird fitness based on its performance, such as distance traveled or 
    collisions with pipes. The three lists (nets, ge, and birds) are synchronized such that each position in these 
    lists corresponds to the same bird:
    - Position 0 in `ge` corresponds to the genome of bird 0.
    - Position 0 in `nets` corresponds to the neural network controlling bird 0.
    - Position 0 in `birds` corresponds to the bird object representing bird 0.
    This organization allows for coordinated management of bird genomes, neural networks, and bird objects.
    """
    ge = []
    
    """
    This for loop iterates over genomes and sets up a neural network and a bird object for each genome.
    """
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        """
        Creates a feedforward neural network (net) using the provided genome and configuration.
        """
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        """
        Appends the given genome object to the ge list. This operation ensures that the genome, representing genetic 
        information for a bird controlled by a neural network created in NEAT, is stored alongside its corresponding 
        neural network and other relevant data. This allows for detailed tracking of each bird's genetic makeup and 
        fitness evaluation throughout the evolutionary process.
        """
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0
    clock = pygame.time.Clock() # Creates a pygame Clock object to control the frame rate of the game loop
    run = True

    while run and len(birds) > 0:
        clock.tick(30) # Limits the maximum frame rate to 30 frames per second (fps).

        # Process events from the Pygame event queue to handle user inputs such as mouse clicks or window closure
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        """
        Determine which pipe the bird should consider for its neural network input based on its position relative to 
        the pipes.
        """
        pipe_ind = 0 # Initialize pipe index to 0 for the input to the neural network
        if len(birds) > 0:
            # Update the pipe index that the bird should consider for its neural network input.
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  
                pipe_ind = 1

        """
        This loop iterates through each bird in the `birds` list, passing specific inputs to its associated neural 
        network, receiving an output value, and triggering a jump if the output value is greater than 0.5.
        """
        for x, bird in enumerate(birds):
            """
            Adjusting the fitness of the bird: incrementing the bird's fitness score slightly for its survival up to 
            this point. This encourages the bird to continue progressing forward. The fitness is incremented by 0.1 to 
            reward the bird for each frame it remains active. This increment rate is designed to provide incentive for 
            the bird to maintain its position without flying excessively high or low, given that this loop runs 30 
            times per second (`clock.tick(30)`).
            """
            ge[x].fitness += 0.1
            bird.move()
            """
            Activating the neural network with specific inputs:
            - `bird.y`: Current y-coordinate of the bird.
            - `abs(bird.y - pipes[pipe_ind].height)`: Vertical distance between the bird and the top of the selected 
            pipe.
            - `abs(bird.y - pipes[pipe_ind].bottom)`: Vertical distance between the bird and the bottom of the selected 
            pipe.
            """
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), 
                                                       abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()

        base.move()
        """
        Check the x position of each pipe. If a pipe moves off-screen (i.e., its x position is less than 0), mark it 
        for removal from the list.
        """
        rem = []
        add_pipe = False

        for pipe in pipes: # Move each pipe horizontally across the screen by a fixed velocity
            pipe.move()

            for bird in birds: # Check collision of each bird with each pipe in the game
                if pipe.collide(bird, win):
                    """
                    Every time a bird hits a pipe, its fitness score will decrease by 1. This ensures there is no bias 
                    towards birds that cover more distance but frequently collide with pipes. By deducting fitness on 
                    collision, a bird that avoids hitting pipes will have a higher fitness score compared to a bird 
                    that collides with pipes. This encourages birds to navigate between the pipes effectively.
                    """
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird)) # Remove the neural network associated with the bird 
                    ge.pop(birds.index(bird)) # Remove the genome associated with the bird
                    birds.pop(birds.index(bird)) # Remove the bird object from the list

            """
            This if statement checks if the bird has passed the pipe. If the bird's x-coordinate is greater than the
            pipe's x-coordinate (indicating that the bird has flown past the pipe), and if the pipe hasn't been 
            marked as passed yet (`pipe.passed` is False), then the pipe is marked as passed (`pipe.passed = True`). 
            This triggers the addition of a new pipe to the game.
            """
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            """
            This if statement checks if the bird has passed the pipe. As soon as the bird passes a pipe, a new pipe
            is generated.
            """
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1 # Increment the score by 1 each time a bird successfully passes a pipe 

            for genome in ge: # Increase the fitness of each genome by 5 if a bird passes through a pipe
                genome.fitness += 5
            """
            Add a new Pipe object to the pipes list, spawning it at the specified x position (WIN_WIDTH).
            """
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem: # Remove pipes from the pipes list that have gone off the screen, based on the rem list
            pipes.remove(r)

        """
        Iterate through each bird in the birds list to check if it has hit the ground. If a bird's y-coordinate plus 
        its image height minus 10 is greater than or equal to FLOOR (730) or if its y-coordinate is less than -50, 
        remove that bird from the list.
        """
        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)

# Runs the NEAT algorithm to train a neural network to play flappy bird
def run(config_file):
    # Load configuration settings from the provided config file path
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config) # Initialize a NEAT population using the loaded configuration settings
    """
    Add reporters to the NEAT population to provide detailed statistics about each generation in the console.
    """
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    """
    The bird's fitness is determined by how far it moves in the game. The main function acts as the fitness function for 
    the NEAT algorithm. It will be called 50 times, passing all genomes and the config file each time.
    """
    winner = p.run(eval_genomes, 50) # 50 specifies the number of generations to run

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__) # Get the directory containing the script
    config_path = os.path.join(local_dir, 'Config_Feedforward.txt') # Construct the absolute path to the config file
    run(config_path)
