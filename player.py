import settings
import inits
import pygame
import math
import time



class PlayerInfo():

    def __init__(self, player, obtained_potion_IDs):
        self.gameOver = False
        self.id = player.id
        self.name = player.name
        self.x = player.x
        self.y = player.y
        self.vel_x = player.vel_x
        self.vel_y = player.vel_y
        self.score = player.score
        self.health = player.health
        self.icon_num = player.icon_num
        self.orientation = player.orientation
        self.hitDisp = player.hitDisp
        self.hitType = player.hitType
        self.hitRotAngle = player.hitRotAngle
        self.hit_img_center = player.hit_img_center
        self.hit_img_orientation = player.hit_img_orientation
        self.hitList = player.hitList
        #self.lastHitTime = player.lastHitTime
        #self.hitDispTime = player.hitDispTime
        self.moveTime = player.moveTime
        self.obtained_potion_IDs = obtained_potion_IDs


class Player():

    def __init__(self, id, name, posInfo, player_icon_img, orientation, icon_num, hitInfo, score, health, mpw, mkw, pd, kd):

        # player id, score & health
        self.id = id
        self.name = name
        self.icon_num = icon_num
        self.score = score
        self.health = health

        # player location & movement features: acceleration, current speed (hor/ver), max speed, last-move-time
        self.x = posInfo[0]
        self.y = posInfo[1]
        self.vel_x = posInfo[2]
        self.vel_y = posInfo[3]
        self.max_vel = 2.25
        self.acceleration = 0.25
        self.moveTime = 0

        # hit variables:
        # hit-img-rotation (degrees), hit-disp-time, last-hit-time
        # current-hit-type, current-hit-bool,  current-hit-disp-bool
        # punch-wait-time, punch-damage
        # kick-wait-time, kick-damage
        self.lastHitTime = -10
        self.hitDisp = hitInfo[0]
        self.hit_img_orientation= hitInfo[1]
        self.hit_img_center = hitInfo[2]
        self.hitList = hitInfo[3]
        self.hitRotAngle = hitInfo[4]
        self.hitType = hitInfo[5]
        self.punchDamage = pd
        self.minPunchWait = mpw
        self.kickDamage = kd
        self.minKickWait = mkw
        self.KO = False
        self.hit_img_topleft=(0, 0)

        # player-icon-features
        self.img = player_icon_img
        self.orientation = orientation

    def copy(self, player):
        self.id = player.id
        self.name = player.name
        self.x = player.x
        self.y = player.y
        self.score = player.score
        self.health = player.health
        self.icon_num = player.icon_num
        self.orientation = player.orientation
        self.hitDisp = player.hitDisp
        self.hitType = player.hitType
        self.hitRotAngle = player.hitRotAngle
        self.hit_img_center = player.hit_img_center
        self.hit_img_orientation = player.hit_img_orientation
        self.hitList = player.hitList
        #self.lastHitTime = player.lastHitTime
        #self.hitDispTime = player.hitDispTime
        self.moveTime = player.moveTime

    def getPlayerRect(self):
        return self.img.get_rect(topleft=(self.x,self.y))
    def getDamage(self,hitType):
        if hitType == "PUNCH":
            hitDamage = self.punchDamage
        elif hitType == "KICK":
            hitDamage = self.kickDamage
        return hitDamage
    def setHitDamage(self,hitType,pts):
        if hitType == "PUNCH":
            self.punchDamage = pts
        elif hitType == "KICK":
            self.kickDamage = pts

    def updateHitList(self, other_id, pts):
        self.hitList.append((other_id, pts))
    def resetHitList(self):
        self.hitList = []
    def getHitList(self):
        return self.hitList
    def move(self, move_time_wait, win_dim, player_icon_width, zero_divide_threshold):
        win_width = win_dim[0]
        win_heigth = win_dim[1]
        frame_width = win_dim[2]

        direction = "unalter"
        keys = pygame.key.get_pressed()
        check_move_time=time.perf_counter()
        diff_move_time=check_move_time-self.moveTime

        # update moving direction and last-move-time if
        # any key is pressed & a duration of "move_time_wait" is passed
        if keys[pygame.K_RIGHT] and diff_move_time > move_time_wait:
            direction = "right"
            self.moveTime=check_move_time
        if keys[pygame.K_LEFT] and diff_move_time > move_time_wait:
            direction = "left"
            self.moveTime=check_move_time
        if keys[pygame.K_UP] and diff_move_time > move_time_wait:
            direction = "up"
            self.moveTime = check_move_time
        if keys[pygame.K_DOWN] and diff_move_time > move_time_wait:
            direction = "down"
            self.moveTime = check_move_time
        if keys[pygame.K_SPACE] and diff_move_time > move_time_wait:
            direction = "stop"
            self.moveTime = check_move_time

        # update player speed based on direction & acceleration
        if direction == "unalter":
            self.vel_x = self.vel_x
            self.vel_y = self.vel_y
        elif direction == "up":
            if self.vel_y - self.acceleration < -self.max_vel:
                self.vel_y = -self.max_vel
            else:
                self.vel_y -= self.acceleration
        elif direction == "down":
            if self.vel_y + self.acceleration > self.max_vel:
                self.vel_y = self.max_vel
            else:
                self.vel_y += self.acceleration
        elif direction == "left":
            if self.vel_x - self.acceleration < -self.max_vel:
                self.vel_x = -self.max_vel
            else:
                self.vel_x -= self.acceleration
        elif direction == "right":
            if self.vel_x + self.acceleration > self.max_vel:
                self.vel_x = self.max_vel
            else:
                self.vel_x += self.acceleration
        elif direction == "stop":
            self.vel_x = 0
            self.vel_y = 0

        # update player orientation
        if self.vel_x > 0 and abs(self.vel_x) > zero_divide_threshold:
            self.orientation = "right"
            self.hit_img_orientation = "right"
        elif self.vel_x < 0 and abs(self.vel_x) > zero_divide_threshold:
            self.orientation = "left"
            self.hit_img_orientation = "left"


        # update player location based on speed & window/frame/icon dimensions
        if self.y + self.vel_y < frame_width:
            self.y = frame_width
        elif self.y + self.vel_y > win_heigth-player_icon_width:
            self.y = win_heigth-player_icon_width
        else:
            self.y = self.y + self.vel_y


        if self.x + self.vel_x > win_width-player_icon_width:
            self.x = win_width-player_icon_width
        if self.x + self.vel_x < 0:
            self.x = 0
        else:
            self.x = self.x + self.vel_x


    def hit(self,hitType, pygame_mixer, hit_try_music, punch_img, kick_img, punch_icon_width, kick_icon_width, player_icon_width, zero_divide_threshold):

            # decide whether to finish an ongoing hit display
            dispHit_time=time.perf_counter()
            if self.hitDisp and dispHit_time-self.lastHitTime > settings.HIT_ICON_DURATION:
                self.hitDisp = False
                hitType = "NONE"
            if self.KO and dispHit_time-self.lastHitTime > 2*settings.HIT_ICON_DURATION:
                self.KO = False

            # get the wait-time for a given hit-type
            hit_rect = []
            if hitType == "PUNCH":
                wait_time = self.minPunchWait
            elif hitType == "KICK":
                wait_time = self.minKickWait
            elif hitType == "NONE":
                wait_time = 100

            # get current hit-time
            hit_time = time.perf_counter()

            hitHappened = "NO"
            # update hit-info
            if hit_time-self.lastHitTime > wait_time and hitType != "NONE":
                # play hit-try-sound
                inits.game_sound_mixer.Channel(2).play(inits.game_sound_mixer.Sound(settings.hit_try_music))

                self.lastHitTime = time.perf_counter()
                self.hitDisp = True
                self.hitType = hitType
                hitHappened = "YES"


                if self.vel_x > 0:
                    self.hit_img_orientation = "right"
                    if hitType == "PUNCH":
                        self.hitImg = punch_img
                    elif hitType == "KICK":
                        self.hitImg = kick_img

                else:
                    self.hit_img_orientation = "left"
                    if hitType == "PUNCH":
                        self.hitImg = pygame.transform.flip(punch_img, True, False)
                    elif hitType == "KICK":
                        self.hitImg = pygame.transform.flip(kick_img, True, False)

                if abs(self.vel_x) > zero_divide_threshold:
                    self.hitRotAngle = -math.degrees(math.atan(self.vel_y / self.vel_x))
                else:
                    if abs(self.vel_y) > zero_divide_threshold:
                        if self.vel_y > 0:
                            self.hitRotAngle = 90
                        else:
                            self.hitRotAngle = -90
                    else:
                        self.hitRotAngle = 0

                if hitType == "PUNCH":
                    hit_width = punch_icon_width
                elif hitType == "KICK":
                    hit_width = kick_icon_width

                change_xy = findXYstep(self.vel_x, self.vel_y, zero_divide_threshold, player_icon_width / 2 + hit_width / 2)
                self.hit_img_center = (self.x + player_icon_width / 2 + change_xy[0], self.y + player_icon_width / 2 + change_xy[1])
                rotated_image = pygame.transform.rotate(self.hitImg, self.hitRotAngle)
                hit_rect = rotated_image.get_rect(center=self.hit_img_center)


            hit_info=[]
            hit_info.append(hitHappened)
            hit_info.append(hit_rect)
            return hit_info

    def drawPlayer(self, win, player_icon_width):
        if self.orientation == "right":
            win.blit(pygame.transform.flip(self.img, True, False), (self.x, self.y))
        else:
            win.blit(self.img, (self.x, self.y))
        fonts = pygame.font.SysFont(settings.DISP_FONT, settings.FONT_SIZE[10])
        name_label = fonts.render(self.name, 1, settings.PLAYER_NAME_COLOR)
        win.blit(name_label, (self.x + player_icon_width / 2 - 7 * math.ceil(len(self.name) / 2), self.y + player_icon_width))

    def drawHit(self, win, punch_img, kick_img, player_icon_width, punch_icon_width, kick_icon_width, zero_divide_threshold):

        if self.hitDisp:

            if self.hit_img_orientation == "right":
                if self.hitType == "PUNCH":
                    self.hitImg = punch_img
                elif self.hitType == "KICK":
                    self.hitImg = kick_img
            else:
                if self.hitType == "PUNCH":
                    self.hitImg = pygame.transform.flip(punch_img, True, False)
                elif self.hitType == "KICK":
                    self.hitImg = pygame.transform.flip(kick_img, True, False)

            if self.hitType == "PUNCH":
                hit_width = punch_icon_width
            elif self.hitType == "KICK":
                hit_width = kick_icon_width

            change_xy=findXYstep(self.vel_x,self.vel_y,zero_divide_threshold,player_icon_width/2+hit_width/2)
            self.hit_img_center=(self.x+player_icon_width/2+change_xy[0],self.y+player_icon_width/2+change_xy[1])
            rotated_image = pygame.transform.rotate(self.hitImg, self.hitRotAngle)
            new_rect = rotated_image.get_rect(center=self.hit_img_center)
            self.hit_img_topleft=new_rect.topleft
            win.blit(rotated_image, self.hit_img_topleft)
        if self.KO:
            win.blit(inits.ko_img, self.hit_img_topleft)


    def drawPointer(self,win, player_icon_width, pointer_features, zero_divide_threshold):


        start_x = self.x + player_icon_width/2
        start_y = self.y + player_icon_width/2
        start_pt=(start_x, start_y)

        xy_change = findXYstep(self.vel_x,self.vel_y,zero_divide_threshold,pointer_features[2])
        x_change = xy_change[0]
        y_change = xy_change[1]
        end_x =  start_x + x_change
        end_y = start_y + y_change
        end_pt=(end_x, end_y)
        draw_dashed_line(win, pointer_features[0], start_pt, end_pt, pointer_features[1], 8)

def findXYstep(dX, dY, zero_divide_threshold, line_length):
    # find change in X and Y coordinates based on a vector in the same direction as v=[dx  dy] & of length line_length
    if abs(dX) > zero_divide_threshold and abs(dY) > zero_divide_threshold:
        x_change = line_length * math.sin(math.atan(abs(dX) / abs(dY)))
        y_change = line_length * math.cos(math.atan(abs(dX) / abs(dY)))
        if dX < -zero_divide_threshold:
            x_change = -x_change
        if dY < -zero_divide_threshold:
            y_change = -y_change
    elif abs(dX) > zero_divide_threshold and abs(dY) < zero_divide_threshold:
        x_change = line_length
        y_change = 0
        if dX < -zero_divide_threshold:
            x_change = -x_change
    elif abs(dY) > zero_divide_threshold and abs(dX) < zero_divide_threshold:
        y_change = line_length
        x_change = 0
        if dY < -zero_divide_threshold:
            y_change = -y_change
    elif abs(dY) < zero_divide_threshold and abs(dX) < zero_divide_threshold:
        x_change = -line_length
        y_change = 0

    xy_change=[]
    xy_change.append(x_change)
    xy_change.append(y_change)
    return xy_change

def draw_dashed_line(surf, color, start_pos, end_pos, width, dash_length):
    origin=[start_pos[0], start_pos[1]]
    target=[end_pos[0],end_pos[1]]
    displacement=[(target[0] - origin[0]),(target[1] - origin[1])]
    length = (math.sqrt(displacement[0] ** 2 + displacement[1] ** 2))
    changeXY=[displacement[0] / length,displacement[1] / length]

    num_dashes = math.ceil(length / dash_length)
    start_p=[0,1]
    end_p=[0,1]
    for ll in range(0, num_dashes):
        start_p[0] = origin[0] + (changeXY[0] *ll* dash_length)
        start_p[1] = origin[1] + (changeXY[1] * ll * dash_length)
        end_p[0] = start_p[0]+ changeXY[0] * dash_length/2
        end_p[1] = start_p[1]+ changeXY[1] * dash_length/2
        pygame.draw.line(surf, color, (start_p[0],start_p[1]), (end_p[0],end_p[1]), width)


