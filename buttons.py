import pygame
import settings

class ShopButton:
    def __init__(self, x, y, width, heigth, text, cost, type):
        self.w = width
        self.h = heigth
        self.clicked = False
        self.text = text
        self.x = x
        self.y = y
        self.cost = cost
        self.type = type
        self.font = settings.FONT_SIZE[9]
        self.alpha = settings.ALPHA_VAL[4]
        self.answer = False
        self.question = "Are you sure? (Y/N or Enter/Esc)"

    def mouseHoover(self, mx, my):
        touched = False
        if mx >= self.x + 2 and mx <= self.x + self.w - 2 and my >= self.y + 2 and my <= self.y + self.h - 2:
            touched = True
        return touched

    def mouseAction(self, mx, my):
        if mx >= self.x + 2 and mx <= self.x + self.w - 2 and my >= self.y + 2 and my <= self.y + self.h - 2:
            self.alpha = settings.ALPHA_VAL[6]
            self.clicked = True

    def drawButton(self, win):
        border_color = settings.RECT_BORDER_COLOR
        fill_color = settings.SHOP_COLOR[1]
        text_color = settings.SHOP_COLOR[2]
        cost_color = settings.SHOP_COLOR[3]

        fonts = pygame.font.SysFont(settings.DISP_FONT, self.font)
        info_text = fonts.render(self.text, 1, text_color)
        info_text.set_alpha(self.alpha)
        cost_text = fonts.render("Cost: "+str(int(self.cost))+" Coins", 1, cost_color)
        cost_text.set_alpha(self.alpha)

        shop_rect = pygame.Surface((self.w, self.h))
        shop_rect.set_alpha(self.alpha)
        shop_rect.fill(fill_color)
        pygame.draw.rect(shop_rect, border_color, shop_rect.get_rect(), 2)
        win.blit(shop_rect, (self.x, self.y))
        win.blit(info_text, (self.x+5, self.y+5))
        win.blit(cost_text, (self.x + 5, self.y + settings.RECT_DIM[5]-20))

    def drawClickedButton(self, win):

        fonts = pygame.font.SysFont(settings.DISP_FONT, self.font)
        quest_rect_color = settings.SHOP_COLOR[4]
        quest_text_color = settings.SHOP_COLOR[5]
        quest_text = fonts.render(self.question, 1, quest_text_color)
        quest_text.set_alpha(self.alpha)
        quest_rect = pygame.Surface((2 * self.w, self.h/4))
        quest_rect.fill(quest_rect_color)
        win.blit(quest_rect, (self.x, self.y + 20))
        win.blit(quest_text, (self.x + 5, self.y + 25))



class SoundButton:
    def __init__(self, x1,y1, button_width):
        self.bg_sound = True
        self.kick_sound = True
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1+button_width
        self.y2 = y1
        self.w = button_width

    def mouseAction(self, mx, my):
        if mx >= self.x1 + 2 and mx <= self.x1 + self.w - 2 and my >= self.y1 + 2 and my <= self.y1 + self.w - 2:
            self.bg_sound = not self.bg_sound

        if mx >= self.x2  + 2 and mx <= self.x2 + self.w - 2 and my >= self.y2 + 2 and my <= self.y2 + self.w - 2:
            self.kick_sound = not self.kick_sound

    def drawSoundButton(self,win, bg_volume_on_img, bg_volume_off_img, hit_volume_on_img, hit_volume_off_img):
        if self.bg_sound == True:
            win.blit(bg_volume_on_img,(self.x1,self.y1))
        elif self.bg_sound == False:
            win.blit(bg_volume_off_img, (self.x1, self.y1))

        if self.kick_sound == True:
            win.blit(hit_volume_on_img,(self.x2,self.y2))
        elif self.kick_sound == False:
            win.blit(hit_volume_off_img, (self.x2, self.y2))

class NameButton:

    def __init__(self, width, heigth, name):
        self.w = width
        self.h = heigth
        self.clicked = False
        self.name = name
        self.font1 = settings.FONT_SIZE[2]
        self.font2 = settings.FONT_SIZE[3]


    def drawNameButton(self, win, x, y):
        rect_color = settings.NAME_BUT_COLOR[0]
        field_color = settings.NAME_BUT_COLOR[1]
        title_color =  settings.NAME_BUT_COLOR[2]
        input_color =  settings.NAME_BUT_COLOR[3]
        pygame.draw.rect(win, rect_color, (x, y, self.w, self.h))
        pygame.draw.rect(win, field_color, (x+9, y+30, self.w-30, self.h-40))
        fonts1 = pygame.font.SysFont(settings.DISP_FONT, self.font1)
        fonts2 = pygame.font.SysFont(settings.DISP_FONT, self.font2)
        display_text = fonts1.render(str("Enter User Name:"), 1, title_color)
        display_name = fonts2.render(self.name, 1, input_color)
        win.blit(display_text, (x + 10, y + 4))
        win.blit(display_name, (x + 10, y + 35))

class DockButton:
    def __init__(self, x, y, width, heigth, text):
        self.x = x
        self.y = y
        self.w = width
        self.h = heigth
        self.clicked = False
        self.text = text

    def mouseAction(self, mx, my):
        if mx >= self.x + 2 and mx <= self.x + self.w - 2 and my >= self.y + 2 and my <= self.y + self.h - 2:
            self.clicked = True

    def drawCloseButton(self, win):
        color = settings.DOCK_BUT_COLOR[0]
        pygame.draw.rect(win, color, (self.x, self.y, self.w, self.h))
        fonts = pygame.font.SysFont(settings.DISP_FONT, settings.FONT_SIZE[1])
        display_text = fonts.render(self.text, 1, settings.DOCK_BUT_COLOR[1])
        win.blit(display_text, (self.x + 8, self.y + 4))

class HitLoadButton():

    def __init__(self, punchWait, kickWait, health):
        self.punchWait = punchWait
        self.kickWait = kickWait
        self.health = health
        self.health_rem = health
        self.lastHitTime = -10
        self.punchLoad = 1
        self.kickLoad = 1
        self.clicked = True

    def updateHitLoad(self, current_time):
        self.punchLoad = min(1, (current_time - self.lastHitTime) / self.punchWait)
        self.kickLoad = min(1, (current_time - self.lastHitTime) / self.kickWait)

    def drawHitLoad(self, win, x, y):

        rect_size = (settings.RECT_DIM[2], settings.RECT_DIM[3])
        border_color = settings.RECT_BORDER_COLOR
        rect_color = settings.HIT_RECT_COLOR
        load_color = settings.HIT_FILL_COLOR
        font = pygame.font.SysFont(settings.DISP_FONT, settings.FONT_SIZE[6])
        health_text = font.render("HEALTH", 1, settings.HIT_TEXT_COLOR)
        health_text.set_alpha(settings.ALPHA_VAL[3])
        punch_text = font.render("PUNCH", 1, settings.HIT_TEXT_COLOR)
        punch_text.set_alpha(settings.ALPHA_VAL[3])
        kick_text = font.render("KICK", 1, settings.HIT_TEXT_COLOR)
        kick_text.set_alpha(settings.ALPHA_VAL[3])

        health_rect = pygame.Surface(rect_size)
        health_rect.set_alpha(settings.ALPHA_VAL[2])
        health_rect.fill(rect_color)
        pygame.draw.rect(health_rect, border_color, health_rect.get_rect(), 2)
        win.blit(health_rect, (x, y - rect_size[1] - 3))
        ratio = self.health_rem/self.health
        health_size = (rect_size[0]*ratio, rect_size[1])
        health_load_rect = pygame.Surface(health_size)
        health_load_rect.set_alpha(settings.ALPHA_VAL[2])
        if ratio <= 1 and ratio > 0.75:
            color = settings.HEALTH_FILL_COLOR[0]
        elif ratio <= 0.75 and ratio > 0.5:
            color = settings.HEALTH_FILL_COLOR[1]
        elif ratio <= 0.5 and ratio > 0.25:
            color = settings.HEALTH_FILL_COLOR[2]
        elif ratio <= 0.25:
            color = settings.HEALTH_FILL_COLOR[3]
        health_load_rect.fill(color)
        win.blit(health_load_rect, (x, y- rect_size[1] - 3))
        win.blit(health_text, (x + 2, y - rect_size[1] - 1))

        hit_rect1 = pygame.Surface(rect_size)
        hit_rect1.set_alpha(settings.ALPHA_VAL[2])
        hit_rect1.fill(rect_color)
        pygame.draw.rect(hit_rect1, border_color, hit_rect1.get_rect(), 2)
        win.blit(hit_rect1, (x, y))
        if self.punchLoad != 1:
            punch_size = (int(rect_size[0] * (1 - self.punchLoad)), rect_size[1])
            punch_load_rect = pygame.Surface(punch_size)
            punch_load_rect.set_alpha(30)
            punch_load_rect.fill(load_color)
            win.blit(punch_load_rect,(x, y))
        win.blit(punch_text, (x + 2, y + 2))


        hit_rect2 = pygame.Surface(rect_size)
        hit_rect2.set_alpha(settings.ALPHA_VAL[2])
        hit_rect2.fill(rect_color)
        pygame.draw.rect(hit_rect2, border_color, hit_rect2.get_rect(), 2)
        win.blit(hit_rect2, (x, y + rect_size[1] + 3))
        if self.kickLoad != 1:
            kick_size = (int(rect_size[0] * (1 - self.kickLoad)), rect_size[1])
            punch_load_rect = pygame.Surface(kick_size)
            punch_load_rect.set_alpha(settings.ALPHA_VAL[2])
            punch_load_rect.fill(load_color)
            win.blit(punch_load_rect, (x, y + rect_size[1] + 3))
        win.blit(kick_text, (x + 2, y + rect_size[1] + 5))



