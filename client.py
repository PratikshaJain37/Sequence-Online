import pygame
from network import Network
from classes import Button
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")



def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            '''
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))
            '''
            if game.p1Went:
                text1 = font.render(move1, 1, (0,0,0))
                game.btns.remove
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went:
                text2 = font.render(move2, 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in game.playerButtons(p):
            btn.draw(win)

    pygame.display.update()


#btns = [Button("H-1-0", 50, 500, (0,0,0)), Button("S-2-0", 250, 500, (255,0,0)), Button("H-3-0", 450, 500, (0,255,0))]
#btns = [Button("Rock", 50, 500, (0,0,0)), Button("Paper", 250, 500, (255,0,0)), Button("Scissors", 450, 500, (0,255,0))]





def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP()) 
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get") 
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
            
            # gui
            font = pygame.font.SysFont("comicsans", 90)
            '''
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
            '''
            if game.winner() == 1:
                text = font.render("You Won!", 1, (255,0,0))
                # reset buttons to original
                game.resetWent()
                game.setButtons()

            else:
                text = font.render("Try again...", 1, (255,0,0))
                #game.resetWent()
                game.p1Went = False
                game.p2Went = False       



            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for btn in game.playerButtons(player):
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                run = False

    main()

while True:
    menu_screen()