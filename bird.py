import pygame  
import neat  
import random  
import os  
import time  
pygame.init()  
WINDOW_WIDTH = 800  
WINDOW_HEIGHT = 600  
BIRD_SIZE = 30  
PIPE_WIDTH = 70  
PIPE_GAP = 160  
GRAVITY = 0.7  
JUMP_SPEED = -8 
GEN = 0  
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
GREEN = (0, 255, 0)  
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  
pygame.display.set_caption("Flappy Bird")  

class Bird:  
    def __init__(self, x, y):  
        self.x = x  
        self.y = y  
        self.velocity = 0  
        self.tick_count = 0  
        self.height = y  
        self.alive = True  
        self.distance = 0
        
    def jump(self):  
        self.velocity = JUMP_SPEED  
        self.tick_count = 0  
        
    def update(self):  
        if self.alive:  
            self.tick_count += 1  
            self.velocity += GRAVITY  
            self.y += self.velocity  
            self.distance += 1
            
    def draw(self):  
        if self.alive:  
            pygame.draw.circle(screen, WHITE, (self.x, int(self.y)), BIRD_SIZE // 2)  

class Pipe:  
    def __init__(self):  
        self.x = WINDOW_WIDTH  
        self.gap_y = random.randint(150, 450)  
        self.scored = False 
        
    def update(self):  
        self.x -= 5  
        
    def draw(self):  
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.gap_y - PIPE_GAP//2))  
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_y + PIPE_GAP//2,   
                                       PIPE_WIDTH, WINDOW_HEIGHT))  
    
    def collide(self, bird):  
        if (bird.x + BIRD_SIZE//2 > self.x and bird.x - BIRD_SIZE//2 < self.x + PIPE_WIDTH):  
            if (bird.y - BIRD_SIZE//2 < self.gap_y - PIPE_GAP//2 or   
                bird.y + BIRD_SIZE//2 > self.gap_y + PIPE_GAP//2):  
                return True  
        return False  

def eval_genomes(genomes, config):
    max_distance = 20000 
    global GEN  
    GEN += 1  
    
    nets = []  
    birds = []  
    ge = []  
    
    for genome_id, genome in genomes:  
        genome.fitness = 0  
        net = neat.nn.FeedForwardNetwork.create(genome, config)  
        nets.append(net)  
        birds.append(Bird(200, WINDOW_HEIGHT//2))  
        ge.append(genome) 
    if not birds:  
        return   
    pipes = [] 
    pipes.append(Pipe())
    score = 0  
    clock = pygame.time.Clock()  
    running = True  
    
    while running and len(birds) > 0:  
        clock.tick(60000)  
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  
                pygame.quit()  
                quit()  
                
        pipe_ind = 0  
        if len(birds) > 0:  
            if len(pipes) > 1 and birds[0].x > pipes[0].x + PIPE_WIDTH:  
                pipe_ind = 1  
                
        for x, bird in enumerate(birds):  
            ge[x].fitness += 0.1 
            bird.update()  
            
            output = nets[x].activate((  
                bird.y,  
                bird.velocity, 
                abs(bird.y - pipes[pipe_ind].gap_y),  
                pipes[pipe_ind].gap_y - PIPE_GAP//2,  
                pipes[pipe_ind].gap_y + PIPE_GAP//2, 
                abs(bird.x - pipes[pipe_ind].x)  
            ))  
            
            if output[0] > 0.5:  
                bird.jump()  
        if len(birds) == 0:  
            break 
        for pipe in pipes:  
            if pipe.x + PIPE_WIDTH < birds[0].x and not pipe.scored:  
                score += 10.0  
                pipe.scored = True  
        pipe_center = pipes[pipe_ind].gap_y  
        distance_to_center = abs(bird.y - pipe_center)  
        ge[x].fitness += (1.0 / (distance_to_center + 1)) * 0.1  
        for pipe in pipes[:]: 
            pipe.update()  
            
            for x, bird in enumerate(birds):  
                if pipe.collide(bird):  
                    ge[x].fitness -= 5  
                    birds[x].alive = False  
            
            if pipe.x + PIPE_WIDTH < 0:  
                pipes.remove(pipe)  
                    
        if len(pipes) < 2 and (len(pipes) == 0 or pipes[-1].x < WINDOW_WIDTH - 300):
            pipes.append(Pipe())  
            
        for x in range(len(birds)-1, -1, -1):  
            if not birds[x].alive or birds[x].y > WINDOW_HEIGHT or birds[x].y < 0:  
                birds.pop(x)  
                nets.pop(x)  
                ge.pop(x)  
            
        screen.fill(BLACK)  
        for bird in birds:  
            bird.draw()  
        for pipe in pipes:  
            pipe.draw()  
            
        font = pygame.font.Font(None, 36)  
        score_text = font.render(f'Score: {score}', True, WHITE)  
        gen_text = font.render(f'Generation: {GEN}', True, WHITE)  
        alive_text = font.render(f'Alive: {len(birds)}', True, WHITE)  
        screen.blit(score_text, (10, 10))  
        screen.blit(gen_text, (10, 50))  
        screen.blit(alive_text, (10, 90))  
        
        pygame.display.flip()  
        if len(birds) > 0 and birds[0].distance > max_distance: 
            break  

# def run(config_path):  
#     config = neat.config.Config(  
#         neat.DefaultGenome,  
#         neat.DefaultReproduction,  
#         neat.DefaultSpeciesSet,  
#         neat.DefaultStagnation,  
#         config_path  
#     )  
    
#     pop = neat.Population(config)  
#     pop.add_reporter(neat.StdOutReporter(True))  
#     stats = neat.StatisticsReporter()  
#     pop.add_reporter(stats)  
    
#     checkpointer = neat.Checkpointer(5, filename_prefix='neat-checkpoint-')  
#     pop.add_reporter(checkpointer)  
    
#     winner = pop.run(eval_genomes, 100)
def run(config_path):  
    config = neat.config.Config(  
        neat.DefaultGenome,  
        neat.DefaultReproduction,  
        neat.DefaultSpeciesSet,  
        neat.DefaultStagnation,  
        config_path  
    )  
    
    pop = neat.Population(config)  
    pop.add_reporter(neat.StdOutReporter(True))  
    stats = neat.StatisticsReporter()  
    pop.add_reporter(stats)  
    
    checkpointer = neat.Checkpointer(5, filename_prefix='neat-checkpoint-')  
    pop.add_reporter(checkpointer)  
    
    winner = pop.run(eval_genomes, 100)

if __name__ == "__main__":  
    local_dir = os.path.dirname(__file__)  
    config_path = os.path.join(local_dir, "config-feedforward.txt")  
    run(config_path)