from pygame import *
'''Необходимые классы'''


#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):  #Класс Sprite из модуля sprite
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height): #Заимствуем свойства и методы из суперкласса
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (wight, height))  #создать прямоугольник в который вписан спрайт, вместе 55,55 - параметры
        #transform - подгоняем под нужный размер
        self.speed = player_speed  #скорость движения спрайта
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()  #вписать картинку в прямоугольник с областью, ..
        self.rect.x = player_x  #Положение спрайта на сцене
        self.rect.y = player_y
#метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  # Отобразить спрайт в точке с заданными координатами

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite): 
    def update_r(self): # - метод перемещения игрока, если только методы __init__ не надо
        keys = key.get_pressed() #Возвращает структуру с текущим состоянием клавиш (True — опущена, False — поднята).
        if keys[K_UP] and self.rect.y > 5: #если клавиша нажата и координата у не у потолка
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80: #если клавиша нажата и координата у не у пола
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


#игровая сцена:
back = (200, 255, 255) #цвет фона (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height)) #создать окно размерами ширина длина
window.fill(back)


#флаги, отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60


#создания мяча и ракетки   
racket1 = Player('platform.png', 30, 200, 4, 50, 150) 
racket2 = Player('platform.png', 520, 200, 4, 50, 150)
ball = GameSprite('ball.png', 200, 200, 4, 50, 50)

#шрифты и надписи
font.init()
font = font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))


speed_x = 3
speed_y = 3


while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        #мяч касается платформы
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
        
        #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1


        #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True


        #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True
        # отрисовываем
        racket1.reset()  
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
