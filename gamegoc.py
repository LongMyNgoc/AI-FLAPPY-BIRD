import pygame  
import random  

pygame.init()  


WINDOW_WIDTH = 800  
WINDOW_HEIGHT = 600  
BIRD_SIZE = 30  
PIPE_WIDTH = 70  
PIPE_GAP = 200  
GRAVITY = 0.5  
JUMP_SPEED = -10  


WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
GREEN = (0, 255, 0)  


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  
pygame.display.set_caption("Flappy Bird")  
clock = pygame.time.Clock()  

class Bird:  
    def __init__(self):  
        self.x = 200  
        self.y = WINDOW_HEIGHT // 2  
        self.velocity = 0  
    
    def jump(self):  
        self.velocity = JUMP_SPEED  
    
    def update(self):  
        self.velocity += GRAVITY  
        self.y += self.velocity  
        
    def draw(self):  
        pygame.draw.circle(screen, WHITE, (self.x, int(self.y)), BIRD_SIZE // 2)  

class Pipe:  
    def __init__(self):  
        self.x = WINDOW_WIDTH  
        self.gap_y = random.randint(200, 400)  
        
    def update(self):  
        self.x -= 3  
        
    def draw(self):  
        # Draw top pipe  
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.gap_y - PIPE_GAP//2))  
        # Draw bottom pipe  
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_y + PIPE_GAP//2,   
                                       PIPE_WIDTH, WINDOW_HEIGHT))  

def main():  
    bird = Bird()  
    pipes = [Pipe()]  
    score = 0  
    running = True  
    
    while running:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_SPACE:  
                    bird.jump()  
        

        bird.update()  
        

        for pipe in pipes:  
            pipe.update()  
        

        if pipes[-1].x < WINDOW_WIDTH - 300:  
            pipes.append(Pipe())  
            

        if pipes[0].x < -PIPE_WIDTH:  
            pipes.pop(0)  
            score += 1  
            

        for pipe in pipes:  
            if (bird.x + BIRD_SIZE//2 > pipe.x and   
                bird.x - BIRD_SIZE//2 < pipe.x + PIPE_WIDTH):  
                if (bird.y - BIRD_SIZE//2 < pipe.gap_y - PIPE_GAP//2 or   
                    bird.y + BIRD_SIZE//2 > pipe.gap_y + PIPE_GAP//2):  
                    running = False  
        
 
        if bird.y > WINDOW_HEIGHT or bird.y < 0:  
            running = False  
            

        screen.fill(BLACK)  
        bird.draw()  
        for pipe in pipes:  
            pipe.draw()  
            font = pygame.font.Font(None, 36)  
        score_text = font.render(f'Score: {score}', True, WHITE)  
        screen.blit(score_text, (10, 10))  
        
        pygame.display.flip()  
        clock.tick(60)  

    pygame.quit()  

if __name__ == "__main__":  
    main()