import pygame
import os
import random
import math
import sys
import neat
import pickle
pygame.init()

# Global Constants
SCREEN_HEIGHT = 573
SCREEN_WIDTH = 1000
PLAYGROUND_WIDTH = 780
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino Runner')

# Load images for the game to display on the screen
# Dino states
RUNNING = [pygame.image.load(os.path.join("images", "DinoRun1.png")),
           pygame.image.load(os.path.join("images", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("images", "DinoJump.png"))

# Obstacles 
SMALL_CACTUS = [pygame.image.load(os.path.join("images", "SmallCactus1.png")),
                pygame.image.load(os.path.join("images", "SmallCactus2.png")),
                pygame.image.load(os.path.join("images", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("images", "LargeCactus1.png")),
                pygame.image.load(os.path.join("images", "LargeCactus2.png")),
                pygame.image.load(os.path.join("images", "LargeCactus3.png"))]


# Background
BG = pygame.image.load(os.path.join("images", "Sky.png"))
TRACK = pygame.image.load(os.path.join("images", "Grass.png"))


FONT = pygame.font.Font('freesansbold.ttf', 18)

gen = 0

class Dinosaur:
    X_POS = 80
    Y_POS = 440
    JUMP_VELOCITY = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VELOCITY
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.step_index = 0


    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1


    def jump(self):
        self.image = JUMPING
        if self.dino_jump: # check for the jumping state
            self.rect.y -= self.jump_vel * 4 # dino moves up in the screen
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VELOCITY: # as soon as dino reaches the ground
            self.dino_jump = False # no longer in jumping state
            self.dino_run = True
            self.jump_vel = self.JUMP_VELOCITY


    def update(self):
        """
        Updates Dino state every loop iteration
        """
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        # animate Dino
        if self.step_index >= 10:
            self.step_index = 0


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type 
        self.rect = self.image[self.type].get_rect()
        self.rect.x = PLAYGROUND_WIDTH # every time when the obstacle is created, it's just off the edge of the right-hand side of the screen

    def update(self):
        self.rect.x -= game_speed # move the obstacle across the screen towards Dino
        if self.rect.x < -self.rect.width:
            obstacles.pop() # remove the obstacle once it's off the sceen on the left-hand side

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2) # 0 - one cactus, 1 - two cactus, 2 - three cactus
        super().__init__(image, self.type)
        self.rect.y = 465


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2) # 0 - one cactus, 1 - two cactus, 2 - three cactus
        super().__init__(image, self.type)
        self.rect.y = 440        



def kill_dino(index):
    """Kill a bad Dino"""
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return math.sqrt(dx**2+dy**2)


def eval_genomes(genomes, config):
    # global speed keeps track of how fast eveything is moving on the screen
    # x_pos_bg background x-coordinate
    # y_pos_bg background y-coordinate
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaurs, ge, nets, gen
    clock = pygame.time.Clock()
    points = 0 # game score
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = SCREEN_HEIGHT - TRACK.get_height()

    dinosaurs = []
    obstacles = []
    ge = []
    nets = []

    gen += 1 # generation count

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0


    def display_score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = FONT.render(f"Score: {points}", True, (0, 0, 0))
        SCREEN.blit(text, (800, 50))

        text = FONT.render(f"Speed: {game_speed}", True, (0, 0, 0))
        SCREEN.blit(text, (800, 100))


    def display_generations():
        global gen
        text = FONT.render(f"Generations: {gen}", True, (0, 0, 0))
        SCREEN.blit(text, (800, 150))

    
    def display_alive_dinos():
        global dinosaurs
        text = FONT.render(f"Alive dinos: {len(dinosaurs)}", True, (0, 0, 0))
        SCREEN.blit(text, (800, 200))


    def background():
        global x_pos_bg, y_pos_bg
        image_width = TRACK.get_width()
        SCREEN.blit(TRACK, (x_pos_bg, y_pos_bg))
        SCREEN.blit(TRACK, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed


    run = True
    while run and len(dinosaurs) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
                run = False
        
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(BG, (0,0))
        background()
        SCREEN.fill((255, 255, 255), (PLAYGROUND_WIDTH, 0, SCREEN_WIDTH, SCREEN.get_height()))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)

        

        # put obstacles on the sceen
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))


        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                # Here we dicrease the level of fitness of a Dino running into an obstacle
                if dinosaur.rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1
                    kill_dino(i) # remove dino from a Jurassic world


        for i, dinosaur in enumerate(dinosaurs):
            #obstacle = obstacles[0]
            output = nets[i].activate((dinosaur.rect.y,
                                        distance((dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop)))

            # if the output of neural net is greater than 0.5 and
            # Dino is not currently jumping
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:
                # initiate a jump
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        
        SCREEN.fill((255, 255, 255), (PLAYGROUND_WIDTH, 0, SCREEN_WIDTH, SCREEN.get_height()))
        display_score()
        display_generations()
        display_alive_dinos()

        clock.tick(30)
        pygame.display.update()

        # break if the score gets large enough, i.e. dino is pretty good at the game
        if points > 2000:
            pickle.dump(nets[0],open("best_dino.pickle", "wb"))
            break



# Setup the NEAT
def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config) # create the initial population

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(5))
    
    winner = pop.run(eval_genomes, 50) # run for up to 50 generations

    
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    """
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)
    """

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

        
