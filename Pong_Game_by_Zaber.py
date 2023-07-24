import pygame, random
pygame.init()

_game_window = pygame.display.set_mode([800, 700])
pygame.display.set_caption("Pong")

class Player:
    def __init__(self) -> None:
        self.x_pos = 0
        self.y_pos = 0
        self.width = 12
        self.height = 150
        self.motion = 7
        self.score = 0
        self.autoplay = False
        
    def draw_player(self):
        self.frame = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        pygame.draw.rect(_game_window, _white, self.frame)
        
    def auto_play(self, ball_centery, _horizontal_bar):
        if self.autoplay:
            self.motion = 5
            if self.frame.centery < ball_centery and p_A.y_pos + p_A.height + p_A.motion < _game_window.get_height():
                self.y_pos += self.motion
            if self.frame.centery > ball_centery and p_A.y_pos - p_A.motion > _horizontal_bar.y + _horizontal_bar.height:
                self.y_pos -= self.motion
        
class Ball:
    def __init__(self) -> None:
        self.x_pos = 0
        self.y_pos = 0
        self.size = 15
        self.x_velocity = 5
        self.y_velocity = 5
    
    def draw_ball(self):
        self.frame = pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)
        pygame.draw.rect(_game_window, _white, self.frame, border_radius = self.size)
        
    def reset(self):
        self.x_pos = _game_window.get_width() / 2 - self.size
        self.y_pos = _game_window.get_height() / 2 - self.size
        self.x_velocity *= random.choice((1, -1))
        self.y_velocity *= random.choice((1, -1))

#Globals
_white = (255, 255, 255)
_black = (0, 0, 0)
_grey = (175, 175, 175)

_clock = pygame.time.Clock()
_fps = 60
_font = pygame.font.SysFont(None, 40)

p_A = Player()
p_B = Player()
ball = Ball()

def gameloop():
    _end_game = False
    
    #Left side Player
    p_A.x_pos = 50
    p_A.y_pos = 100
    
    #Right side Player
    p_B.x_pos = 738
    p_B.y_pos = 100
    
    ball.reset()
    
    _collide_A = _collide_B = False
        
    while not _end_game:
        _game_window.fill(_black)
        
        p_A.draw_player()
        p_B.draw_player()
        ball.draw_ball()
        
        _horizontal_bar = pygame.Rect(0, 70, 800, 7)
        pygame.draw.rect(_game_window, _grey, _horizontal_bar)
        pygame.draw.rect(_game_window, _grey, [_game_window.get_width() / 2 - 3.5, _horizontal_bar.y, 7, _game_window.get_height() - _horizontal_bar.y])
        
        _player_A_score = _font.render("TEAM-A : " + str(p_A.score), 1, _white)
        _game_window.blit(_player_A_score, [(_game_window.get_width() / 4) - (_player_A_score.get_width() / 2), 40])
        
        _player_B_score = _font.render("TEAM-B : " + str(p_B.score), 1, _white)
        _game_window.blit(_player_B_score, [(_game_window.get_width() - (_game_window.get_width() / 4)) - (_player_B_score.get_width() / 2), 40])
        
        pygame.display.update()
        _clock.tick(_fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _end_game = True
                                    
        _keys_pressed = pygame.key.get_pressed()
        #Player A movements
        if p_A.autoplay:
            p_A.auto_play(ball.frame.centery, _horizontal_bar)
        else:
            if _keys_pressed[pygame.K_w] and p_A.y_pos - p_A.motion > _horizontal_bar.y + _horizontal_bar.height:
                p_A.y_pos -= p_A.motion
            if _keys_pressed[pygame.K_s] and p_A.y_pos + p_A.height + p_A.motion < _game_window.get_height():
                p_A.y_pos += p_A.motion
    
        #Player B movements
        if _keys_pressed[pygame.K_UP] and p_B.y_pos - p_B.motion > _horizontal_bar.y + _horizontal_bar.height:
            p_B.y_pos -= p_B.motion
        if _keys_pressed[pygame.K_DOWN] and p_B.y_pos + p_B.height + p_B.motion < _game_window.get_height():
            p_B.y_pos += p_B.motion
        
        ball.x_pos += ball.x_velocity
        ball.y_pos += ball.y_velocity
        
        if (ball.y_pos + ball.size) + ball.y_velocity >= _game_window.get_height() or ball.y_pos + ball.y_velocity <= _horizontal_bar.y + _horizontal_bar.height: #bottom collision
            ball.y_velocity *= -1
            
            if ball.y_velocity > 0:
                ball.y_velocity = random.choice((7, 5))
            if ball.y_velocity < 0:
                ball.y_velocity = random.choice((-7, -5))
        
        
        if ball.frame.colliderect(p_A.frame) and not _collide_A:
            ball.x_velocity *= -1
            _collide_A = True
            
            if ball.frame.centery >= p_A.frame.top and ball.frame.centery <= p_A.frame.top + (p_A.frame.height / 3) or ball.frame.centery <= p_A.frame.bottom and ball.frame.centery >= p_A.frame.bottom - (p_A.frame.height / 3):
                if ball.x_velocity > 0:
                    ball.x_velocity = random.choice((7, 5))
                if ball.x_velocity < 0:
                    ball.x_velocity = random.choice((-7, -5))
            if ball.frame.centery > p_A.frame.top + (p_A.frame.height / 3) and ball.frame.centery < p_A.frame.bottom - (p_A.frame.height / 3):
                if ball.y_velocity > 0:
                    ball.y_velocity = random.choice((7, 5))
                if ball.y_velocity < 0:
                    ball.y_velocity = random.choice((-7, -5))
                
        if ball.frame.colliderect(p_B.frame) and not _collide_B:
            ball.x_velocity *= -1
            _collide_B = True
            
            if ball.frame.centery >= p_B.frame.top and ball.frame.centery <= p_B.frame.top + (p_B.frame.height / 3) or ball.frame.centery <= p_B.frame.bottom and ball.frame.centery >= p_B.frame.bottom - (p_B.frame.height / 3):
                if ball.x_velocity > 0:
                    ball.x_velocity = random.choice((7, 5))
                if ball.x_velocity < 0:
                    ball.x_velocity = random.choice((-7, -5))
            if ball.frame.centery > p_B.frame.top + (p_B.frame.height / 3) and ball.frame.centery < p_B.frame.bottom - (p_B.frame.height / 3):
                if ball.y_velocity > 0:
                    ball.y_velocity = random.choice((7, 5))
                if ball.y_velocity < 0:
                    ball.y_velocity = random.choice((-7, -5))
        
            
        if _collide_A and ball.x_pos > _game_window.get_width() / 2:
            _collide_A = False
        if _collide_B and ball.x_pos < _game_window.get_width() / 2:
            _collide_B = False
            
        if ball.x_pos < 0:
            ball.reset()
            p_B.score += 1
        if ball.x_pos > _game_window.get_width():
            ball.reset()
            p_A.score += 1
    #End Of While
    return
#End Of gameloop

def main_menu():
    _end_loop = False
    _font1 = pygame.font.SysFont(None, 30)
    _font2 = pygame.font.SysFont("Arial Rounded MT", 40)
    _font3 = pygame.font.SysFont("Bauhaus 93", 200)
    
    _options_dict = {1 : pygame.Rect((_game_window.get_width() / 2) - 100, 460, 200, 30), 
                     2 : pygame.Rect((_game_window.get_width() / 2) - 100, 490, 200, 30)}
    i = 1
    
    while not _end_loop:
        
        _game_window.fill(_black)
        
        _wlc_font = _font2.render("HEY! Welcome to", 1, _white)
        _game_window.blit(_wlc_font, [(_game_window.get_width() / 2) - (_wlc_font.get_width() / 2), 150])
        
        _pong_font = _font3.render("PONG", 1, _white)
        _game_window.blit(_pong_font, [(_game_window.get_width() / 2) - (_pong_font.get_width() / 2), 150])
        
        _dev_name = _font2.render("by Zaber", 1, _white)
        _game_window.blit(_dev_name, [(_game_window.get_width() / 2) - (_dev_name.get_width() / 2), 350])
        
        pygame.draw.rect(_game_window, _grey, _options_dict[i])
        
        if i == 1:
            _opt_1 = _font1.render("SINGLE PLAYER", 1, _black)
            _game_window.blit(_opt_1, [(_options_dict[1].centerx - _opt_1.get_width() / 2), _options_dict[1].centery - _opt_1.get_height() / 2])
        else:
            _opt_1 = _font1.render("SINGLE PLAYER", 1, _white)
            _game_window.blit(_opt_1, [(_options_dict[1].centerx - _opt_1.get_width() / 2), _options_dict[1].centery - _opt_1.get_height() / 2])
        
        if i == 2:
            _opt_2 = _font1.render("TWO PLAYERS", 1, _black)
            _game_window.blit(_opt_2, [(_options_dict[2].centerx - _opt_2.get_width() / 2), _options_dict[2].centery - _opt_2.get_height() / 2])
        else:
            _opt_2 = _font1.render("TWO PLAYERS", 1, _white)
            _game_window.blit(_opt_2, [(_options_dict[2].centerx - _opt_2.get_width() / 2), _options_dict[2].centery - _opt_2.get_height() / 2])
        
        pygame.display.update()
        _clock.tick(_fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _end_loop = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if i > 1:
                        i -= 1
                if event.key == pygame.K_DOWN:
                    if i == 1:
                        i += 1
                        
                if event.key == pygame.K_RETURN:
                    if i == 1:
                        p_A.autoplay = True
                    
                    gameloop()
                    _end_loop = True
                    break
    #End Of While           
    pygame.quit()
    return

#Game starts here
main_menu()
