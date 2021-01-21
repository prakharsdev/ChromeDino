import pygame
from pygame.locals import *

import random

random.seed(34535) 
#random.seed(34533)

def initialize_game():
    #modules initialized
    x = pygame.init()

    #screen height and width
    screen = pygame.display.set_mode((950, 573))
    #screen title
    pygame.display.set_caption("Chrome Dino")
    message = pygame.font.Font('freesansbold.ttf', 30)

    white = (255,255,255)
    orange = (255, 100, 100)

    #images
    cactus = pygame.image.load("cactusSmallMany0000.png")
    cactus = pygame.transform.scale(cactus, (200, 110))
    cactus1 = pygame.image.load("cactusBig0000.png")
    cactus1 = pygame.transform.scale(cactus1, (100, 120))
    cactus2 = pygame.image.load("cactusSmall0000.png")
    cactus2 = pygame.transform.scale(cactus2, (100, 120))
    dino = pygame.image.load("dinorun0000.png")
    dino1 = pygame.image.load("dinorun0001.png")


    walk = [dino,dino, dino1, dino1, dino,dino]
    walk1 = [dino,dino, dino1, dino1, dino,dino]
    walk2 = [dino,dino, dino1, dino1, dino,dino]
    background = pygame.image.load("background.png")

    return screen

num_of_gen = 10

def k_point_crossover(k,parent1,parent2):
    """
        This function has the implementation for k point crossover 
    """
    
    child1={}
    child2={}

    """randomly select k crossing points"""
    key_points=sorted(random.sample(list(range(0,len(parent1))), k))

    key_index=0
    for p1_var,p2_var in zip(parent1,parent2):
        if not p1_var=="fitness" and not p2_var=="fitness":
            """when the crossing point is 1 then below logic is applied"""
            if k==1 and list(parent1).index(p1_var)>key_points[0]:
                child1[p1_var]=parent2[p2_var]
                child2[p2_var]=parent1[p1_var]
            elif k==1 and list(parent1).index(p1_var)<=key_points[0]:
                child1[p1_var]=parent1[p1_var]
                child2[p2_var]=parent2[p2_var]
                """when the crossing points k are more than 1 then below logic is applied"""
            elif k>1:
                start=key_points[key_index]
                if key_points[key_index+1]>=len(parent1)-2:
                    end=None
                else:
                    end=key_points[key_index+1]
                current=list(parent1.keys()).index(p1_var)
                if end==None and current>start:
                    child1[p1_var]=parent2[p2_var]
                    child2[p2_var]=parent1[p1_var]
                elif end==None and current<=start:
                    child1[p1_var]=parent1[p1_var]
                    child2[p2_var]=parent2[p2_var]
                elif current<=start:
                    child1[p1_var]=parent1[p1_var]
                    child2[p2_var]=parent2[p2_var]
                elif current>start and current<=end:
                    child1[p1_var]=parent2[p2_var]
                    child2[p2_var]=parent1[p1_var]
                elif current>end and current<=len(parent1)-2:
                    if start+2<len(key_points):
                        key_index += 2
                    child1[p1_var]=parent1[p1_var]
                    child2[p2_var]=parent2[p2_var]

    return child1, child2

def gameloop(parents):

    #modules initialized
    x = pygame.init()

    #screen height and width
    screen = pygame.display.set_mode((950, 573))
    #screen title
    pygame.display.set_caption("Chrome Dino")
    message = pygame.font.Font('freesansbold.ttf', 30)

    white = (255,255,255)
    orange = (255, 100, 100)

    #images
    cactus = pygame.image.load("cactusSmallMany0000.png")
    cactus = pygame.transform.scale(cactus, (200, 110))
    cactus1 = pygame.image.load("cactusBig0000.png")
    cactus1 = pygame.transform.scale(cactus1, (100, 120))
    cactus2 = pygame.image.load("cactusSmall0000.png")
    cactus2 = pygame.transform.scale(cactus2, (100, 120))
    dino = pygame.image.load("dinorun0000.png")
    dino1 = pygame.image.load("dinorun0001.png")

    walk = [dino,dino, dino1, dino1, dino,dino]
    background = pygame.image.load("background.png")

    cactusx = 100
    cactusy = 430
    
    # initialize chromosome index
    ch_i = 0

    backx={}
    backy={}
    drawx={}
    drawy={}
    backvelocity={}
    game={}
    gameover={}
    gravity={}
    score={}
    jump={}
    walkpoint={}

    for ii in range(10):
        backx[ii]=0
        backy[ii]=0
        drawx[ii]=310
        drawy[ii]=440
        game[ii]=False
        gameover[ii]=False
        gravity[ii]=10
        score[ii]=0
        jump[ii]=False
        walkpoint[ii]=0

    gen_gameover=False

    max_play = 0

    # run till the game is not over
    while gen_gameover==False:
        
        max_play += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        jump_nums = [0,2,4,6,8]

        for par_ind in range(10):
            #print("par---->",par)
            # only jump if it is in this number
            if ch_i<6:
                this_par = list(parents[par_ind])
                par_dict = parents[par_ind]
                #print("this parent is--->",parents[par_ind])
                ind_val = this_par[ch_i]
                ch_val = par_dict[ind_val]
                #print("ind_val--->",ind_val)
                #print("ch_val---->",ch_val)
                if ch_i in this_par:
                    if ch_val in jump_nums:
                        jump[par_ind] = False

                        #Change the speed then alter the value of below backvelocity
                        backvelocity[par_ind] = ch_val
                        game[par_ind] = True
                    else:
                        if drawy[par_ind] == 440:
                            jump[par_ind] = True
                            #Change the speed then alter the value of below backvelocity
                            backvelocity[par_ind] = ch_val
                            game[par_ind] = True
                else:
                    jump[par_ind] = True
                    #Change the speed then alter the value of below backvelocity
                    backvelocity[par_ind] = ch_val
                    game[par_ind] = True

            if backx[par_ind] == -600:
                backx[par_ind] = 0
            if cactusx < -1600:
                cactusx = 550
            if 441 > drawy[par_ind] > 50:
                if jump[par_ind] == True:
                    drawy[par_ind] -= 10
            else:
                jump[par_ind] = False
            #print(drawy)
            if drawy[par_ind] < 440:
                if jump[par_ind] == False:
                    drawy[par_ind] +=gravity[par_ind]

            #collision
            if cactusx < drawx[par_ind] + 100 < cactusx +200 and cactusy < drawy[par_ind] + 100 < cactusy + 100 :
                backvelocity[par_ind] = 0
                walkpoint[par_ind] = 0
                game[par_ind] = False
                gameover[par_ind] = True

            if cactusx +800 < drawx[par_ind] + 100 < cactusx +1000 and cactusy < drawy[par_ind] + 100 < cactusy + 100 :
                backvelocity[par_ind] = 0
                walkpoint[par_ind] = 0
                game[par_ind] = False
                gameover[par_ind] = True

            if cactusx + 1600< drawx[par_ind] + 100 < cactusx +1800 and cactusy < drawy[par_ind] + 100 < cactusy + 100 :
                backvelocity[par_ind] = 0
                walkpoint[par_ind] = 0
                game[par_ind] = False
                gameover[par_ind] = True


            if game[par_ind] == True:
                score[par_ind] += 1
            screen.fill(white)
            text = message.render("Score: "+ str(score), True, orange)
            
            backx[par_ind] -= backvelocity[par_ind]
            cactusx -= backvelocity[par_ind]

            
            screen.blit(background, [backx[par_ind],backy[par_ind]])
            screen.blit(background, [backx[par_ind] + 780,backy[par_ind]])
            screen.blit(text, [700, 100])
            
            """
            if gameover[par_ind] == True:
                msg = "GAME OVER for "+ str(par_ind)
                text1 = message.render(msg, True, (255,255,0))
                screen.blit(text1, [400, 190])
            """

        # number of generations
        
        for gen_ind in range(10):
            dy = drawy[gen_ind]
            dx = drawx[gen_ind]
            if gameover[gen_ind] == False:
                wp = walkpoint[gen_ind]
                kx = random.randint(20,50)
                ky = random.randint(10,20)
                screen.blit(walk[wp], [dx+kx, dy-ky])


        go_check_flag=0
        for go_ind in range(10):
            if gameover[go_ind]==True:
                go_check_flag += 1
        
        #print("number died:",go_check_flag)
        
        if go_check_flag == 10:
            gen_gameover=True

        for wp_ind in range(10):
            if game[wp_ind] == True:
                #print("Game--->", game)
                walkpoint[wp_ind] +=1
                #print("Walkpoint--->", walkpoint)
                if walkpoint[wp_ind] > 5:
                    walkpoint[wp_ind] = 0
            screen.blit(cactus, [cactusx,cactusy])
            screen.blit(cactus1, [cactusx + 800,cactusy - 8])
            screen.blit(cactus2, [cactusx + 1600,cactusy - 10])
            pygame.display.update()

        ch_i += 1

        if max_play==80:
            break

    return score

# initialize the initial population (20 number)
population_size=10
def ini_pop():
    #ref_dict = {1:2, 4:6, 2:9, 7:1, 3:5, 8:3, 9:7, 5:8, 6:2, 14:3, 20:3, 45:1, 9:3}

    # source knowledge/info for chromosomes and their values, just to keep the scope in control
    # each key is a chromosome name and value is it's value
    ref_dict = {1:2, 2:6, 3:9, 4:1, 5:5, 6:3, 7:7, 8:8, 9:2, 10:3, 11:3, 12:1, 13:3, 14:5, 15:8, 16:3, 17:1,18:5,19:7,20:9,21:11,22:13,23:13,24:3,25:1}

    parents = []

    # size of chromozome
    chrom_size = 6
    # generating 10 parents
    for par_in in range(0,population_size):
        parent = {}
        # each parent has 6 chromosomes
        for z in range(chrom_size):
            rand_key = random.choice(list(ref_dict.values()))
            while rand_key in parent:
                rand_key = random.choice(list(ref_dict.values()))
            
            if len(parent)<=chrom_size-1:
                parent[rand_key]=ref_dict[rand_key]
        parents.append(parent)
    print("\n\n\n")
    print("initial population is (generation 0) ",parents)
    return parents, chrom_size

# mutation brings a big variance in the gene
# in this approach we first copy the parents to the children and then 
# modify the values of 2 chromosomes randomly for both children
def mutation(chrom_size,parent1,parent2):
    val_ind1=random.randint(0,parent1_chrom-1)
    val_ind2=random.randint(0,parent1_chrom-1)

    child1=parent1.copy()
    child2=parent2.copy()

    if len(child1) == chrom_size and len(child2)==chrom_size:
        child1[val_ind1]=random.randint(0,20)
        child1[val_ind2]=random.randint(0,20)

        child2[val_ind1]=random.randint(0,20)
        child2[val_ind2]=random.randint(0,20)

    return child1,child2


"""
    start of the program
"""

# step -1 initialize the pop only in the beginning
parents,chrom_size = ini_pop()

# set initial value for keep track of the number of generations
gen_val=0

# ... loop for the number of generations
while gen_val < num_of_gen:
    # runs till the max number of generations are reached
    
    numpar = len(parents)

    print("number of parents in this generation ",gen_val, " : ",numpar)

    # step - 2 invoke the game loop so that all the parents from the current generation can play, score
    score = gameloop(parents)
    
    print("GAME OVER for ",gen_val)
    print("score of generation for ",gen_val," is (key is the parent name and value is it's score): ",score)

    new_pop=[]
    pop_index = len(new_pop)
    while pop_index < population_size:
        ind1 = random.randint(0,numpar-1)
        parent1 = parents[ind1]
        ind2 = random.randint(0,numpar-1)
        parent2 = parents[ind2]
        
        # Step -3 reproduction (either k-point crossover or mutation)
        # reproduce using k-point crossover
        # either 1-point cross is chosen or 2-point crossover is chosen
        # choosing a higher number of k can cause higher degree of mutation, which is no easy to keep a track of

        k = random.choice([1,2])
        child1, child2 = k_point_crossover(k,parent1,parent2)
        
        # get the number of chromosomes in the children and parents
        child1_chrom=len(child1)
        child2_chrom=len(child2)
        parent1_chrom=len(parent1)
        parent2_chrom=len(parent2)

        # apply mutation when crossover resulted in reduction or increament of chromosomes
        if parent1_chrom != chrom_size or parent2_chrom != chrom_size:
            child1,child2 = mutation(chrom_size,parent1,parent2)
        elif child1_chrom!=parent1_chrom or child2_chrom!=parent2_chrom:
            child1,child2 = mutation(chrom_size,parent1,parent2)
        else:
            new_pop.append(child1)
            new_pop.append(child2)

        pop_index = len(new_pop)

    parents.clear()
    
    # Step -4 children from previous generation become the parent of next generation
    parents = new_pop.copy()
    new_pop.clear()

    # it is a list of dictionaries
    # each dictionary represent a parent in a sequencial order
    # inside each dictionary key represents a chromosome and value represents the value of a chromosome
    print("children produced are (list of chromosomes): ",parents)
    print(">>>these produced children will be the parents for next generation")
    
    print("\n")
    if gen_val<9:
        print("--------------------generation:",int(gen_val+1), " initialized-------------------")
        #picktopparents() # based on the score pick top five parents | these top 5 will live 

    gen_val += 1

