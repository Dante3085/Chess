
from Board import Board
import sys, pygame

board = Board()

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

while 1:
    # check pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitEvent = pygame.event.Event(pygame.QUIT, {})
                pygame.event.post(quitEvent)
            
            elif event.key == pygame.K_RETURN:
                print(board)

    board.update(screen)
    board.render(screen)
    
    # update display surface to screen
    pygame.display.flip()  