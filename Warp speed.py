import pygame
from pygame.locals import *
import random

from Particle import particle
from Rastro import Rastro

Center = 0; Stoped = 1
My_direction = Stoped

def Change_position(lista, tam, My_direction):
    check_par = 1
    for i in range(len(lista) - 1):
        #if the particle out of screen, so i'll put it in other position 
        if(lista[i].pos_x < 1 or lista[i].pos_x > 499 or lista[i].pos_y < 0 or lista[i].pos_y > 499):
            if(My_direction == Center):
                if(check_par%2 == 0):
                    lista[i].pos_x = random.randint(125,375)
                    lista[i].pos_y = random.randint(125,375)
                    lista[i].speed_log = 1.01 
                    continue
                lista[i].pos_x = random.randint(1,499)
                lista[i].pos_y = random.randint(1,499)
                lista[i].speed_log = 1.01
        check_par+=1

#just generating an array of particle
def Generate_particle(how_mparticle):
    lista = []
    for i in range(how_mparticle):
        lista.append(particle(random.randint(1,499),random.randint(1,499)))
    return lista

def create_surface_color_percent(tam_x, tam_y, i=7):
    object_surface = pygame.Surface((tam_x,tam_y))
    #just creating a system selector color
    if(i%6 == 0):
        object_surface.fill((0,0,255))
        return object_surface
    elif(i%2 == 0):
        object_surface.fill((250,128,114))
        return object_surface
    else:
        object_surface.fill((240,255,240))
        return object_surface


def move_particle(lista, qtd_particle,My_direction):
    if(My_direction == Center):
        for i in range(qtd_particle):
            #i was been thinking about this too much time, the logic is product the vector of the center
            #to the particle with a scalar
            lista[i].pos_x = 250*(1-lista[i].speed_log) + lista[i].speed_log*lista[i].pos_x
            lista[i].pos_y = 250*(1-lista[i].speed_log) + lista[i].speed_log*lista[i].pos_y
            lista[i].speed_log += 0.005
#main function
def Main():
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    screen.fill((0,0,0))
    pygame.display.set_caption("Light speed") 

    quantity_particle = 100;lista_global = Generate_particle(quantity_particle)
    check_one_time = True;time_mls = pygame.time.Clock();key_pressed = []
    control_color = 1; tam_stars = 4; tam_rastro = 4
    background = Generate_particle(50)
    while True:
        #this variable control the time of the loop, like 30 miliseconds for each loop i did
        time_mls.tick(120)
        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break
        #plot particles
        screen.fill((0,0,0))
        for i in range(quantity_particle):
            #check if particle is almost out of screen, if it then i'll plot a second particle behind the other one
            if(lista_global[i].pos_x < 100 or lista_global[i].pos_x > 400 or lista_global[i].pos_y < 100 or lista_global[i].pos_y > 400):
                obj_r = Rastro((250*(1-1/1.01) + lista_global[i].pos_x/1.01),(250*(1-1/1.01) + lista_global[i].pos_y/1.01))
                screen.blit(create_surface_color_percent(tam_rastro,tam_rastro,control_color),(obj_r.posr_x,obj_r.posr_y))
            #plot particle
            screen.blit(create_surface_color_percent(tam_stars,tam_stars,control_color),(lista_global[i].pos_x,lista_global[i].pos_y))
            control_color+=1
        for k in range(50):
            screen.blit(create_surface_color_percent(2,2),(background[k].pos_x,background[k].pos_y))
        #implementation of camera movimentation
        if(key_pressed[pygame.K_w]):
            My_direction = Center
        else:
            My_direction = Stoped
        #creating a new position for particle if the camera move
        if(not My_direction == Stoped):
            move_particle(lista_global, quantity_particle,My_direction)
        #implementation to take a particle to the center of camera just if this particle get rid of camera
        Change_position(lista_global, quantity_particle,My_direction)
        pygame.display.update()
        control_color = 1

if __name__ == "__main__":
    Main()