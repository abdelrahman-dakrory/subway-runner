import pygame
import random
import sys
import math

pygame.init()

# ---- Sound ----
sound_enabled = False
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    sound_enabled = True
except:
    pass

# ---- Screen ----
WIDTH, HEIGHT = 1080, 2300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Runner")

# ---- Colors ----
WHITE          = (255, 255, 255)
BLACK          = (0,   0,   0)
RED            = (220, 50,  50)
SKIN_COL       = (255, 200, 150)
GREY           = (120, 120, 120)
DARK_GREY      = (40,  40,  40)
YELLOW         = (255, 220, 50)
ORANGE         = (255, 140, 0)
GREEN          = (50,  200, 80)
PURPLE         = (160, 60,  200)
NEON_CYAN      = (0,   240, 255)
ROAD_COLOR     = (60,  60,  65)
STRIPE_COLOR   = (200, 200, 50)
GOLD           = (255, 200, 0)
HEART_RED      = (255, 50,  80)
SHIELD_COLOR   = (100, 200, 255)
SLOW_COLOR     = (180, 100, 255)
RED_COIN_COLOR = (255, 60,  60)
RED_SHIELD_COL = (255, 90,  90)

# ======================== SKINS (25 total) ========================
# type: "human" | "moto" | "car"
PLAYER_SKINS = [
    # Human – Brown Hair
    {"name":"Classic", "price":0,   "type":"human","hair":(35,22,10),   "body":(30,60,140),  "pants":(15,15,15),   "shoes":(45,45,45)},
    {"name":"Red",     "price":50,  "type":"human","hair":(35,22,10),   "body":(165,30,30),  "pants":(85,0,0),     "shoes":(55,0,0)},
    {"name":"Green",   "price":100, "type":"human","hair":(35,22,10),   "body":(20,135,55),  "pants":(0,75,22),    "shoes":(0,52,12)},
    {"name":"Purple",  "price":150, "type":"human","hair":(35,22,10),   "body":(125,40,175), "pants":(72,0,115),   "shoes":(52,0,82)},
    {"name":"Gold",    "price":300, "type":"human","hair":(35,22,10),   "body":(185,145,0),  "pants":(115,82,0),   "shoes":(82,52,0)},
    # Human – Blonde Hair
    {"name":"Blonde",  "price":150, "type":"human","hair":(225,185,45), "body":(205,205,225),"pants":(82,82,125),  "shoes":(62,62,92)},
    {"name":"Surfer",  "price":175, "type":"human","hair":(225,185,45), "body":(0,155,185),  "pants":(0,82,135),   "shoes":(0,62,105)},
    {"name":"Sandy",   "price":200, "type":"human","hair":(225,185,45), "body":(215,145,62), "pants":(145,82,22),  "shoes":(105,58,12)},
    {"name":"Lemon",   "price":225, "type":"human","hair":(225,185,45), "body":(210,210,0),  "pants":(140,140,0),  "shoes":(100,100,0)},
    {"name":"Cotton",  "price":250, "type":"human","hair":(225,185,45), "body":(255,175,195),"pants":(200,100,130),"shoes":(160,70,100)},
    # Human – Special
    {"name":"Ninja",   "price":200, "type":"human","hair":(12,12,12),   "body":(22,22,22),   "pants":(12,12,12),   "shoes":(32,32,32)},
    {"name":"Ocean",   "price":225, "type":"human","hair":(0,105,165),  "body":(0,165,205),  "pants":(0,82,145),   "shoes":(255,255,255)},
    {"name":"Fire",    "price":250, "type":"human","hair":(205,82,0),   "body":(225,82,0),   "pants":(165,32,0),   "shoes":(125,22,0)},
    {"name":"Snow",    "price":275, "type":"human","hair":(242,242,255),"body":(222,238,255),"pants":(162,182,222),"shoes":(202,222,255)},
    {"name":"Shadow",  "price":400, "type":"human","hair":(8,8,8),      "body":(32,32,38),   "pants":(18,18,22),   "shoes":(22,22,28)},
    # Motorcycle (top-down)
    {"name":"Moto Red",    "price":350,"type":"moto","body":(200,30,30),  "accent":(255,90,90),  "helmet":(140,0,0)},
    {"name":"Moto Blue",   "price":350,"type":"moto","body":(20,60,200),  "accent":(80,140,255), "helmet":(0,30,140)},
    {"name":"Moto Green",  "price":400,"type":"moto","body":(20,150,50),  "accent":(80,230,110), "helmet":(0,100,20)},
    {"name":"Moto Orange", "price":400,"type":"moto","body":(220,110,0),  "accent":(255,175,40), "helmet":(160,70,0)},
    {"name":"Moto Purple", "price":450,"type":"moto","body":(120,20,180), "accent":(190,90,255), "helmet":(80,0,130)},
    # Car (top-down)
    {"name":"Car Red",    "price":500,"type":"car","body":(200,30,30),   "glass":(160,210,240),"detail":(130,0,0)},
    {"name":"Car Blue",   "price":500,"type":"car","body":(20,60,200),   "glass":(160,210,240),"detail":(0,30,140)},
    {"name":"Car Yellow", "price":550,"type":"car","body":(220,200,0),   "glass":(160,210,240),"detail":(150,135,0)},
    {"name":"Car White",  "price":550,"type":"car","body":(230,230,235), "glass":(160,210,240),"detail":(170,170,175)},
    {"name":"Car Black",  "price":600,"type":"car","body":(25,25,30),    "glass":(100,150,180),"detail":(15,15,20)},
]

current_skin    = 0
owned_skins     = {0}
CARD_H          = 240
CARD_GAP        = 18
SHOP_TOP        = 230
shop_scroll_y   = 0.0
shop_scroll_vel = 0.0
shop_max_scroll = max(0, SHOP_TOP + len(PLAYER_SKINS)*(CARD_H+CARD_GAP) + 160 - HEIGHT)

# ======================== SOUNDS ========================
def make_sound(freq, dur, vol=0.3, wave="sine"):
    if not sound_enabled: return None
    try:
        sr = 44100; n = int(sr*dur/1000); buf = bytearray(n)
        for i in range(n):
            t = i/sr
            v = math.sin(2*math.pi*freq*t) if wave=="sine" else (1.0 if math.sin(2*math.pi*freq*t)>0 else -1.0)
            fade = min(1.0,(n-i)/(sr*0.05))
            buf[i] = int(127+127*v*vol*fade)
        return pygame.sndarray.make_sound(__import__('array').array('b',buf))
    except: return None

snd_coin    = make_sound(880,80,0.25,"sine")
snd_hit     = make_sound(120,300,0.4,"square")
snd_powerup = make_sound(660,150,0.3,"sine")
snd_levelup = make_sound(440,200,0.3,"sine")

def play_sound(s):
    try:
        if s and sound_enabled: s.play()
    except: pass

# ======================== ROAD ========================
road_x = 80; road_w = WIDTH-160; N_LANES = 3
lane_centers = [int(road_x+road_w*(1/6)), int(road_x+road_w*(3/6)), int(road_x+road_w*(5/6))]

# ======================== PLAYER ========================
player_w, player_h = 100, 200
player_y = HEIGHT - player_h - 100
current_lane = 1; target_lane = 1
player_x_current = float(lane_centers[1]-player_w//2)
SLIDE_SPEED = 28
run_frame = 0; run_timer = 0; RUN_SPEED = 4

# ======================== OBSTACLES ========================
obs_speed = 18.0; spawn_delay = 1800
last_spawn_time = pygame.time.get_ticks()
obstacles = []
last_spawned_lane = -1; consecutive_count = 0
MAX_OBS_ON_SCREEN = 5; MIN_OBS_DISTANCE = 350
OBS_TYPES = [
    {"color":RED,    "shape":"rect",    "w":130,"h":240},
    {"color":ORANGE, "shape":"barrier", "w":160,"h":120},
    {"color":PURPLE, "shape":"truck",   "w":150,"h":320},
    {"color":GREEN,  "shape":"cone",    "w":100,"h":160},
]
moving_obs = None; MOVING_OBS_FREQ = 8000
last_moving_time = pygame.time.get_ticks()

# ======================== COINS ========================
coins = []; COIN_R = 28
last_coin_time = pygame.time.get_ticks(); COIN_DELAY = 1200
coin_total = 0; coin_anim = []
red_coin_count = 0; RED_COIN_NEEDED = 5
last_red_coin_time = pygame.time.get_ticks(); RED_COIN_DELAY = 4000

# ======================== LIVES ========================
MAX_LIVES = 3; lives = MAX_LIVES; invincible_until = 0

# ======================== POWER-UPS ========================
powerups = []; POWERUP_R = 36
last_pu_time = pygame.time.get_ticks(); PU_DELAY = 7000
SHIELD_DURATION     = 15000
RED_SHIELD_DURATION = 30000
SLOW_DURATION       = 1500
INVINCIBLE_AFTER_HIT= 1500
active_shield_until     = 0
active_slow_until       = 0
active_red_shield_until = 0

# ======================== LEVELS ========================
level = 1; level_flash = 0
LEVEL_ROAD_COLORS = [(60,60,65),(40,60,40),(50,40,70),(70,40,40),(30,50,70)]
def get_road_color():
    return LEVEL_ROAD_COLORS[min(level-1,len(LEVEL_ROAD_COLORS)-1)]

# ======================== BACKGROUND ========================
stripe_y_offset = 0.0; STRIPE_H = 140; STRIPE_GAP = 80
stars       = [(random.randint(0,WIDTH), random.randint(0,HEIGHT)) for _ in range(80)]
star_speeds = [random.uniform(1,4)   for _ in range(80)]
star_bright = [random.randint(150,255) for _ in range(80)]  # fixed, no random per frame
edge_flash  = 0

# ======================== FONTS ========================
font_score    = pygame.font.SysFont("Arial",64,bold=True)
font_gameover = pygame.font.SysFont("Arial",160,bold=True)
font_sub      = pygame.font.SysFont("Arial",70,bold=True)
font_label    = pygame.font.SysFont("Arial",48,bold=True)
font_big      = pygame.font.SysFont("Arial",100,bold=True)
font_small    = pygame.font.SysFont("Arial",38,bold=True)
font_ver      = pygame.font.SysFont("Arial",36,bold=True)

clock = pygame.time.Clock()

# ======================== PRE-ALLOCATE SURFACES ========================
# لا بنعمل Surface جديدة جوه اللوب خالص
draw_surface = pygame.Surface((WIDTH, HEIGHT))
ef_surf      = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
go_overlay   = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
go_card_surf = pygame.Surface((900, 770),      pygame.SRCALPHA)

# ======================== PRE-CACHE STATIC TEXT ========================
_skin_name_surfs  = [font_label.render(s["name"], True, WHITE) for s in PLAYER_SKINS]
_skin_price_surfs = [font_label.render(f"$ {s['price']}", True, GOLD) for s in PLAYER_SKINS]
_shop_inuse_surf  = font_small.render("In Use", True, GREEN)
_shop_equip_surf  = font_small.render("Equip",  True, BLACK)
_shop_buy_y_surf  = font_small.render("Buy",    True, BLACK)
_shop_buy_n_surf  = font_small.render("Buy",    True, GREY)
_shop_title_surf  = font_sub.render("S H O P", True, GOLD)
_shop_back_surf   = font_sub.render("Back",    True, WHITE)
_shop_scroll_surf = font_small.render("v  Scroll Down", True, GREY)
_anim_gold_surf   = font_label.render("+1 $", True, GOLD)
_anim_red_surf    = font_label.render("+Heart", True, HEART_RED)
# pre-cache level text (levels 1–30)
_level_surfs = {i: font_big.render(f"LEVEL {i}!", True, YELLOW) for i in range(1,31)}

# ======================== GAME STATE ========================
score = 0; high_score = 0
touch_start_x = None; touch_start_y = None; last_touch_y = None
game_state = "menu"; game_over_alpha = 0
btn_rect_ref = None; back_to_menu_ref = None
menu_btn_ref = None; shop_btn_ref = None
shop_btns = []; shop_back_btn = None


# ======================== HELPER FUNCTIONS ========================
def reset_game():
    global obstacles,coins,powerups,moving_obs,score,obs_speed,spawn_delay
    global last_spawn_time,current_lane,target_lane,player_x_current
    global game_over_alpha,lives,invincible_until
    global active_shield_until,active_slow_until,active_red_shield_until
    global level,level_flash,coin_anim,edge_flash
    global last_coin_time,last_pu_time,last_moving_time
    global last_spawned_lane,consecutive_count,red_coin_count,last_red_coin_time

    obstacles.clear(); coins.clear(); powerups.clear(); coin_anim.clear()
    moving_obs=None; score=0; obs_speed=18.0; spawn_delay=1800
    now=pygame.time.get_ticks()
    last_spawn_time=last_coin_time=last_pu_time=last_moving_time=last_red_coin_time=now
    current_lane=1; target_lane=1
    player_x_current=float(lane_centers[1]-player_w//2)
    game_over_alpha=0; lives=MAX_LIVES; invincible_until=0
    active_shield_until=0; active_slow_until=0; active_red_shield_until=0
    level=1; level_flash=0; edge_flash=0
    last_spawned_lane=-1; consecutive_count=0; red_coin_count=0

def spawn_coin():
    l=random.randint(0,N_LANES-1)
    coins.append({"x":lane_centers[l],"y":-COIN_R*2,"anim":0,"kind":"gold"})

def spawn_red_coin():
    l=random.randint(0,N_LANES-1)
    coins.append({"x":lane_centers[l],"y":-COIN_R*2,"anim":0,"kind":"red"})

def spawn_powerup():
    l=random.randint(0,N_LANES-1)
    powerups.append({"x":lane_centers[l],"y":-POWERUP_R*2,"kind":random.choice(["shield","slow"])})

def pick_spawn_lane():
    global last_spawned_lane,consecutive_count
    if last_spawned_lane==-1:               lane=random.randint(0,N_LANES-1)
    elif consecutive_count>=2:              lane=random.choice([l for l in range(N_LANES) if l!=last_spawned_lane])
    elif random.random()<0.6:               lane=random.choice([l for l in range(N_LANES) if l!=last_spawned_lane])
    else:                                   lane=last_spawned_lane
    consecutive_count = consecutive_count+1 if lane==last_spawned_lane else 1
    last_spawned_lane=lane; return lane

def can_spawn_obstacle():
    if len(obstacles)>=MAX_OBS_ON_SCREEN: return False
    for o in obstacles:
        if o["rect"].y<MIN_OBS_DISTANCE: return False
    return True


# ======================== ICON HELPERS ========================
def draw_shield_icon(surface,x,y,r,color):
    pts=[(x,y-r),(x+r,y-r//2),(x+r,y+r//3),(x,y+r),(x-r,y+r//3),(x-r,y-r//2)]
    pygame.draw.polygon(surface,color,pts)
    pygame.draw.polygon(surface,WHITE,pts,3)
    pygame.draw.lines(surface,WHITE,False,[(x-r//3,y),(x,y+r//3),(x+r//3,y-r//5)],3)

def draw_turtle_icon(surface,x,y,r):
    pygame.draw.ellipse(surface,(0,160,70),pygame.Rect(x-r,y-r//2,r*2,int(r*1.3)))
    pygame.draw.ellipse(surface,(0,120,50),pygame.Rect(x-r+4,y-r//2+4,r*2-8,int(r*1.3)-8),2)
    pygame.draw.circle(surface,(0,145,60),(x,y-r//2-r//3),r//3)
    pygame.draw.circle(surface,BLACK,(x-4,y-r//2-r//3),3)
    pygame.draw.circle(surface,BLACK,(x+4,y-r//2-r//3),3)
    for dx,dy in [(-r+4,r//3),(r-4,r//3),(-r//2,r//2+4),(r//2,r//2+4)]:
        pygame.draw.circle(surface,(0,135,55),(x+dx,y+dy),r//4)

def draw_heart_icon(surface,x,y,r,color):
    pygame.draw.circle(surface,color,(x-r//2,y-r//4),r//2)
    pygame.draw.circle(surface,color,(x+r//2,y-r//4),r//2)
    pygame.draw.polygon(surface,color,[(x-r,y-r//4),(x,y+r//2+4),(x+r,y-r//4)])

def draw_shield_halo(surface,cx,cy,shielded,red_shielded):
    t=pygame.time.get_ticks()/1000.0
    if red_shielded:
        p=abs(math.sin(t*3.5))
        rc=(min(255,int(200+55*p)),min(255,int(40+30*p)),min(255,int(40+30*p)))
        pygame.draw.circle(surface,rc,(cx,cy),96,7)
    elif shielded:
        p=abs(math.sin(t*3.0))
        sc=(min(255,int(SHIELD_COLOR[0]*p+50)),
            min(255,int(SHIELD_COLOR[1]*p+50)),
            min(255,int(SHIELD_COLOR[2]*p+50)))
        pygame.draw.circle(surface,sc,(cx,cy),90,5)


# ======================== DRAW HUMAN ========================
def draw_human(surface,x,y,frame,skin,shielded,red_shielded):
    cx=x+player_w//2
    ls=math.sin(frame*0.35)*28
    pygame.draw.ellipse(surface,(8,8,8),pygame.Rect(x+8,y+player_h-12,player_w-8,18))
    draw_shield_halo(surface,cx,y+player_h//2,shielded,red_shielded)
    hy=y+18
    pygame.draw.ellipse(surface,SKIN_COL,pygame.Rect(cx-27,hy,54,44))
    pygame.draw.ellipse(surface,skin["hair"],pygame.Rect(cx-27,hy,54,22))
    pygame.draw.circle(surface,BLACK,(cx-10,hy+28),5)
    pygame.draw.circle(surface,BLACK,(cx+10,hy+28),5)
    pygame.draw.circle(surface,WHITE,(cx-8,hy+26),2)
    pygame.draw.circle(surface,WHITE,(cx+12,hy+26),2)
    sy=y+60
    pygame.draw.ellipse(surface,skin["body"],pygame.Rect(cx-48,sy,96,28))
    pygame.draw.rect(surface,skin["body"],pygame.Rect(cx-33,sy+12,66,72),border_radius=12)
    dk=tuple(max(0,c-40) for c in skin["body"])
    pygame.draw.line(surface,dk,(cx,sy+12),(cx,sy+84),3)
    lax=cx-46+int(-ls*0.45)
    pygame.draw.line(surface,skin["body"],(cx-33,sy+18),(lax,sy+56),18)
    pygame.draw.circle(surface,SKIN_COL,(lax,sy+56),12)
    rax=cx+46+int(ls*0.45)
    pygame.draw.line(surface,skin["body"],(cx+33,sy+18),(rax,sy+56),18)
    pygame.draw.circle(surface,SKIN_COL,(rax,sy+56),12)
    py2=sy+80
    pygame.draw.rect(surface,skin["pants"],pygame.Rect(cx-30,py2,60,44),border_radius=8)
    llx=cx-17+int(ls); lly=y+player_h-18
    rlx=cx+17-int(ls); rly=y+player_h-18+int(abs(math.sin(frame*0.35))*8)
    pygame.draw.line(surface,skin["pants"],(cx-17,py2+38),(llx,lly),20)
    pygame.draw.ellipse(surface,skin["shoes"],pygame.Rect(llx-20,lly-10,40,20))
    pygame.draw.line(surface,skin["pants"],(cx+17,py2+38),(rlx,rly),20)
    pygame.draw.ellipse(surface,skin["shoes"],pygame.Rect(rlx-20,rly-10,40,20))


# ======================== DRAW MOTORCYCLE ========================
def draw_moto(surface,x,y,frame,skin,shielded,red_shielded):
    cx=x+player_w//2; bc=skin["body"]; ac=skin["accent"]; hc=skin["helmet"]
    sw=int(math.sin(frame*0.35)*4)
    pygame.draw.ellipse(surface,(8,8,8),pygame.Rect(cx-22,y+player_h-10,44,16))
    draw_shield_halo(surface,cx,y+player_h//2,shielded,red_shielded)
    # Rear wheel
    pygame.draw.ellipse(surface,(15,15,15),pygame.Rect(cx-16+sw,y+player_h-52,32,46))
    pygame.draw.ellipse(surface,(60,60,60),pygame.Rect(cx-10+sw,y+player_h-46,20,34))
    # Chassis
    pygame.draw.ellipse(surface,bc,pygame.Rect(cx-20,y+24,40,player_h-74))
    pygame.draw.ellipse(surface,ac,pygame.Rect(cx-9,y+34,18,player_h-96))
    # Fuel tank
    pygame.draw.ellipse(surface,ac,pygame.Rect(cx-16,y+player_h//2-18,32,26))
    # Front wheel
    pygame.draw.ellipse(surface,(15,15,15),pygame.Rect(cx-14-sw,y+8,28,40))
    pygame.draw.ellipse(surface,(60,60,60),pygame.Rect(cx-9-sw,y+13,18,30))
    # Handlebars
    pygame.draw.line(surface,(110,110,110),(cx-26+sw,y+38),(cx+26+sw,y+38),6)
    pygame.draw.circle(surface,(85,85,85),(cx-26+sw,y+38),5)
    pygame.draw.circle(surface,(85,85,85),(cx+26+sw,y+38),5)
    # Helmet
    pygame.draw.circle(surface,hc,(cx+sw,y+player_h//2-12),20)
    pygame.draw.ellipse(surface,(180,215,255),pygame.Rect(cx-11+sw,y+player_h//2-24,22,11))
    # Rider torso
    light=tuple(min(255,c+30) for c in hc)
    pygame.draw.ellipse(surface,light,pygame.Rect(cx-12+sw,y+player_h//2+6,24,18))
    # Exhaust
    pygame.draw.rect(surface,(165,165,165),pygame.Rect(cx+18,y+player_h-56,7,26),border_radius=3)


# ======================== DRAW CAR ========================
def draw_car_skin(surface,x,y,frame,skin,shielded,red_shielded):
    cx=x+player_w//2; bc=skin["body"]; gl=skin["glass"]; dt=skin["detail"]
    pygame.draw.ellipse(surface,(8,8,8),pygame.Rect(cx-42,y+player_h-10,84,18))
    draw_shield_halo(surface,cx,y+player_h//2,shielded,red_shielded)
    pygame.draw.rect(surface,bc,pygame.Rect(cx-40,y+8,80,player_h-16),border_radius=18)
    pygame.draw.rect(surface,dt,pygame.Rect(cx-28,y+52,56,player_h-104),border_radius=12)
    pygame.draw.rect(surface,gl,pygame.Rect(cx-26,y+14,52,36),border_radius=8)
    pygame.draw.rect(surface,gl,pygame.Rect(cx-22,y+player_h-55,44,30),border_radius=8)
    pygame.draw.rect(surface,gl,pygame.Rect(cx-41,y+65,14,42),border_radius=5)
    pygame.draw.rect(surface,gl,pygame.Rect(cx+27,y+65,14,42),border_radius=5)
    pygame.draw.rect(surface,dt,pygame.Rect(cx-50,y+22,10,12),border_radius=3)
    pygame.draw.rect(surface,dt,pygame.Rect(cx+40,y+22,10,12),border_radius=3)
    wh=(18,18,18); ri=(115,115,115)
    for wx,wy in [(cx-51,y+16),(cx+39,y+16),(cx-51,y+player_h-48),(cx+39,y+player_h-48)]:
        pygame.draw.rect(surface,wh,pygame.Rect(wx,wy,12,26),border_radius=4)
        pygame.draw.rect(surface,ri,pygame.Rect(wx+2,wy+4,8,18),border_radius=3)
    pygame.draw.rect(surface,YELLOW,      pygame.Rect(cx-36,y+10,16,8),border_radius=3)
    pygame.draw.rect(surface,YELLOW,      pygame.Rect(cx+20,y+10,16,8),border_radius=3)
    pygame.draw.rect(surface,(230,20,20), pygame.Rect(cx-36,y+player_h-22,16,8),border_radius=3)
    pygame.draw.rect(surface,(230,20,20), pygame.Rect(cx+20,y+player_h-22,16,8),border_radius=3)


# ======================== PLAYER DISPATCHER ========================
def draw_player(surface,x,y,frame,shielded=False,red_shielded=False):
    sk=PLAYER_SKINS[current_skin]; t=sk.get("type","human")
    if   t=="moto": draw_moto(surface,x,y,frame,sk,shielded,red_shielded)
    elif t=="car":  draw_car_skin(surface,x,y,frame,sk,shielded,red_shielded)
    else:           draw_human(surface,x,y,frame,sk,shielded,red_shielded)


# ======================== SKIN PREVIEWS ========================
def draw_human_preview(surface,skin,cx,ty):
    pygame.draw.ellipse(surface,SKIN_COL,    pygame.Rect(cx-18,ty+4,36,30))
    pygame.draw.ellipse(surface,skin["hair"],pygame.Rect(cx-18,ty+4,36,15))
    pygame.draw.ellipse(surface,skin["body"],pygame.Rect(cx-28,ty+32,56,18))
    pygame.draw.rect(surface,  skin["body"], pygame.Rect(cx-20,ty+44,40,42),border_radius=6)
    pygame.draw.rect(surface,  skin["pants"],pygame.Rect(cx-18,ty+84,36,28),border_radius=5)
    pygame.draw.ellipse(surface,skin["shoes"],pygame.Rect(cx-24,ty+108,22,12))
    pygame.draw.ellipse(surface,skin["shoes"],pygame.Rect(cx+2, ty+108,22,12))

def draw_moto_preview(surface,skin,cx,ty):
    bc=skin["body"]; ac=skin["accent"]; hc=skin["helmet"]; ph=122
    pygame.draw.ellipse(surface,(15,15,15),pygame.Rect(cx-10,ty+ph-32,20,28))
    pygame.draw.ellipse(surface,(60,60,60),pygame.Rect(cx-6, ty+ph-26,12,20))
    pygame.draw.ellipse(surface,bc,pygame.Rect(cx-12,ty+14,24,ph-46))
    pygame.draw.ellipse(surface,ac,pygame.Rect(cx-6, ty+22,12,ph-64))
    pygame.draw.ellipse(surface,ac,pygame.Rect(cx-10,ty+ph//2-10,20,16))
    pygame.draw.ellipse(surface,(15,15,15),pygame.Rect(cx-9,ty+4,18,24))
    pygame.draw.ellipse(surface,(60,60,60),pygame.Rect(cx-5,ty+7,10,18))
    pygame.draw.circle(surface,hc,(cx,ty+ph//2-6),13)
    pygame.draw.ellipse(surface,(180,215,255),pygame.Rect(cx-8,ty+ph//2-16,16,8))
    pygame.draw.line(surface,(110,110,110),(cx-16,ty+24),(cx+16,ty+24),4)

def draw_car_preview(surface,skin,cx,ty):
    bc=skin["body"]; gl=skin["glass"]; dt=skin["detail"]; ph=122; pw=48
    pygame.draw.rect(surface,bc,pygame.Rect(cx-pw//2,ty+4,pw,ph),border_radius=10)
    pygame.draw.rect(surface,dt,pygame.Rect(cx-16,ty+28,32,ph-55),border_radius=7)
    pygame.draw.rect(surface,gl,pygame.Rect(cx-14,ty+8, 28,20),border_radius=5)
    pygame.draw.rect(surface,gl,pygame.Rect(cx-11,ty+ph-30,22,16),border_radius=5)
    for wx,wy in [(cx-pw//2-5,ty+10),(cx+pw//2-5,ty+10),
                  (cx-pw//2-5,ty+ph-26),(cx+pw//2-5,ty+ph-26)]:
        pygame.draw.rect(surface,(18,18,18),pygame.Rect(wx,wy,10,16),border_radius=3)
    pygame.draw.rect(surface,YELLOW,     pygame.Rect(cx-20,ty+6,10,5),border_radius=2)
    pygame.draw.rect(surface,YELLOW,     pygame.Rect(cx+10,ty+6,10,5),border_radius=2)
    pygame.draw.rect(surface,(220,30,30),pygame.Rect(cx-20,ty+ph-14,10,5),border_radius=2)
    pygame.draw.rect(surface,(220,30,30),pygame.Rect(cx+10,ty+ph-14,10,5),border_radius=2)

def draw_skin_preview(surface,skin,cx,ty):
    t=skin.get("type","human")
    if   t=="moto": draw_moto_preview(surface,skin,cx,ty)
    elif t=="car":  draw_car_preview(surface,skin,cx,ty)
    else:           draw_human_preview(surface,skin,cx,ty)


# ======================== DRAW OBSTACLE ========================
def draw_obstacle(surface,obs):
    r=obs["rect"]; ot=obs["type"]; color=ot["color"]; shape=ot["shape"]; cx=r.centerx
    if shape=="rect":
        pygame.draw.rect(surface,color,r,border_radius=18)
        wc=(180,220,255)
        pygame.draw.rect(surface,wc,pygame.Rect(r.x+15,r.y+20,r.w-30,55),border_radius=10)
        pygame.draw.rect(surface,wc,pygame.Rect(r.x+15,r.y+90,r.w-30,45),border_radius=8)
        for wx in [r.x+12,r.x+r.w-28]:
            pygame.draw.circle(surface,BLACK,(wx+8,r.bottom-20),22)
            pygame.draw.circle(surface,GREY,(wx+8,r.bottom-20),14)
    elif shape=="barrier":
        pygame.draw.rect(surface,color,r,border_radius=10)
        for i in range(0,r.w,35):
            pygame.draw.line(surface,WHITE,(r.x+i,r.y),(min(r.x+i+25,r.right),r.bottom),6)
        pygame.draw.rect(surface,WHITE,r,4,border_radius=10)
    elif shape=="truck":
        pygame.draw.rect(surface,color,r,border_radius=12)
        cab=pygame.Rect(r.x+10,r.y,r.w-20,100)
        pygame.draw.rect(surface,(color[0]//2,color[1]//2,color[2]//2),cab,border_radius=14)
        pygame.draw.rect(surface,(180,220,255),pygame.Rect(r.x+20,r.y+10,r.w-40,50),border_radius=8)
        for wx in [r.x+8,r.x+r.w-36]:
            pygame.draw.circle(surface,BLACK,(wx+14,r.bottom-25),26)
            pygame.draw.circle(surface,GREY,(wx+14,r.bottom-25),16)
    elif shape=="cone":
        pts=[(cx,r.y),(r.x,r.bottom),(r.right,r.bottom)]
        pygame.draw.polygon(surface,color,pts)
        pygame.draw.line(surface,WHITE,(cx,r.y+20),(cx-18,r.bottom-20),5)
        pygame.draw.line(surface,WHITE,(cx,r.y+20),(cx+18,r.bottom-20),5)
        pygame.draw.rect(surface,WHITE,pygame.Rect(r.x,r.bottom-18,r.w,18),border_radius=4)


# ======================== DRAW COIN ========================
def draw_coin(surface,coin):
    x,y=coin["x"],coin["y"]; a=coin["anim"]; kind=coin.get("kind","gold")
    ar=int(math.sin(a*0.2)*4)
    if kind=="gold":
        r=COIN_R+ar
        pygame.draw.circle(surface,GOLD,(x,y),r)
        pygame.draw.circle(surface,YELLOW,(x,y),r-7)
        pygame.draw.circle(surface,GOLD,(x,y),r-7,3)
        ct=font_label.render("$",True,DARK_GREY); surface.blit(ct,ct.get_rect(center=(x,y)))
    elif kind=="red":
        r=COIN_R+ar
        pygame.draw.circle(surface,RED_COIN_COLOR,(x,y),r)
        pygame.draw.circle(surface,(255,130,130),(x,y),r-6)
        draw_heart_icon(surface,x,y-2,r-10,HEART_RED)


# ======================== DRAW POWERUP ========================
def draw_powerup(surface,pu):
    x,y=pu["x"],pu["y"]; kind=pu["kind"]
    if kind=="shield":
        pygame.draw.circle(surface,(20,50,110),(x,y),POWERUP_R)
        pygame.draw.circle(surface,SHIELD_COLOR,(x,y),POWERUP_R,4)
        draw_shield_icon(surface,x,y,POWERUP_R-7,SHIELD_COLOR)
    elif kind=="slow":
        pygame.draw.circle(surface,(50,15,70),(x,y),POWERUP_R)
        pygame.draw.circle(surface,SLOW_COLOR,(x,y),POWERUP_R,4)
        draw_turtle_icon(surface,x,y,POWERUP_R-7)


# ======================== DRAW MENU ========================
def draw_menu(surface):
    surface.fill((15,15,30))
    for i,(sx,sy) in enumerate(stars):
        b=star_bright[i]
        pygame.draw.circle(surface,(b,b,b),(sx,sy),2)
    pygame.draw.rect(surface,ROAD_COLOR,(road_x,0,road_w,HEIGHT))
    for li in (1,2):
        lx=int(road_x+road_w*li/3)
        pygame.draw.line(surface,STRIPE_COLOR,(lx,0),(lx,HEIGHT),4)

    t1=font_gameover.render("SUBWAY",True,NEON_CYAN)
    t2=font_gameover.render("RUNNER",True,YELLOW)
    surface.blit(t1,t1.get_rect(center=(WIDTH//2,HEIGHT//2-350)))
    surface.blit(t2,t2.get_rect(center=(WIDTH//2,HEIGHT//2-180)))
    draw_player(surface,WIDTH//2-player_w//2,HEIGHT//2-40,30)

    pb=pygame.Rect(WIDTH//2-250,HEIGHT//2+270,500,110)
    pygame.draw.rect(surface,GREEN,pb,border_radius=24)
    pt=font_sub.render("PLAY",True,BLACK); surface.blit(pt,pt.get_rect(center=pb.center))

    sb=pygame.Rect(WIDTH//2-250,HEIGHT//2+410,500,110)
    pygame.draw.rect(surface,GOLD,sb,border_radius=24)
    st=font_sub.render("SHOP",True,BLACK); surface.blit(st,st.get_rect(center=sb.center))

    if high_score>0:
        hs=font_label.render(f"Best: {high_score}",True,YELLOW)
        surface.blit(hs,hs.get_rect(center=(WIDTH//2,HEIGHT//2+560)))
    ct=font_label.render(f"$ {coin_total}",True,GOLD)
    surface.blit(ct,ct.get_rect(center=(WIDTH//2,HEIGHT//2+625)))

    # ---- نص الإصدار والاسم (خلفية بيضاء + كتابة سوداء) ----
    # لتغيير الإصدار: عدّل ver_str
    ver_str  = "run 4.0.2 V2"
    # لتغيير الاسم: عدّل auth_str
    auth_str = "BY: Abdelrahman Dakrory"
    pygame.draw.rect(surface,(220,220,220),pygame.Rect(0,HEIGHT-115,WIDTH,115))
    vt=font_ver.render(ver_str, True,BLACK); surface.blit(vt, vt.get_rect(center=(WIDTH//2,HEIGHT-84)))
    at=font_ver.render(auth_str,True,BLACK); surface.blit(at, at.get_rect(center=(WIDTH//2,HEIGHT-44)))

    return pb,sb


# ======================== DRAW SHOP ========================
def draw_shop(surface,scroll_y):
    surface.fill((10,10,25))
    surface.blit(_shop_title_surf,_shop_title_surf.get_rect(center=(WIDTH//2,100)))
    ct=font_label.render(f"$ {coin_total}",True,GOLD)
    surface.blit(ct,ct.get_rect(center=(WIDTH//2,175)))
    pygame.draw.line(surface,GREY,(80,210),(WIDTH-80,210),2)

    btn_rects=[]; off=SHOP_TOP-int(scroll_y)

    for i,skin in enumerate(PLAYER_SKINS):
        cy=off+i*(CARD_H+CARD_GAP)
        if cy+CARD_H<215 or cy>HEIGHT: btn_rects.append(None); continue

        card=pygame.Rect(WIDTH//2-430,cy,860,CARD_H)
        if i==current_skin:
            pygame.draw.rect(surface,(18,60,18),card,border_radius=20)
            pygame.draw.rect(surface,GREEN,card,4,border_radius=20)
        elif i in owned_skins:
            pygame.draw.rect(surface,(15,18,50),card,border_radius=20)
            pygame.draw.rect(surface,NEON_CYAN,card,4,border_radius=20)
        else:
            pygame.draw.rect(surface,(18,18,38),card,border_radius=20)
            pygame.draw.rect(surface,GREY,card,3,border_radius=20)

        draw_skin_preview(surface,skin,card.x+85,cy+55)
        surface.blit(_skin_name_surfs[i],(card.x+155,cy+25))

        if i==current_skin:
            surface.blit(_shop_inuse_surf,(card.x+155,cy+90))
            btn_rects.append(None)
        elif i in owned_skins:
            eb=pygame.Rect(card.x+155,cy+155,200,58)
            pygame.draw.rect(surface,NEON_CYAN,eb,border_radius=14)
            surface.blit(_shop_equip_surf,_shop_equip_surf.get_rect(center=eb.center))
            btn_rects.append(("select",i,eb))
        else:
            surface.blit(_skin_price_surfs[i],(card.x+155,cy+90))
            can=coin_total>=skin["price"]
            bb=pygame.Rect(card.x+155,cy+155,200,58)
            pygame.draw.rect(surface,GREEN if can else DARK_GREY,bb,border_radius=14)
            surface.blit(_shop_buy_y_surf if can else _shop_buy_n_surf,
                         (_shop_buy_y_surf if can else _shop_buy_n_surf).get_rect(center=bb.center))
            btn_rects.append(("buy",i,bb) if can else None)

    bk=pygame.Rect(WIDTH//2-200,HEIGHT-125,400,100)
    pygame.draw.rect(surface,(160,30,30),bk,border_radius=20)
    surface.blit(_shop_back_surf,_shop_back_surf.get_rect(center=bk.center))

    if scroll_y<shop_max_scroll-5:
        surface.blit(_shop_scroll_surf,_shop_scroll_surf.get_rect(center=(WIDTH//2,HEIGHT-148)))

    return btn_rects,bk


# ======================== DRAW GAME OVER ========================
def draw_game_over(surface,sc,hs,alpha):
    go_overlay.fill((0,0,0,min(alpha,180)))
    surface.blit(go_overlay,(0,0))
    if alpha<80: return None,None

    cw,ch=900,770; cx2=(WIDTH-cw)//2; cy2=(HEIGHT-ch)//2-80
    go_card_surf.fill((20,20,40,220))
    pygame.draw.rect(go_card_surf,RED,pygame.Rect(0,0,cw,ch),5,border_radius=30)
    surface.blit(go_card_surf,(cx2,cy2))

    go=font_gameover.render("GAME OVER",True,RED); surface.blit(go,go.get_rect(center=(WIDTH//2,cy2+120)))

    for txt,col,yy in [(f"Score: {sc}",WHITE,cy2+285),(f"Best:  {hs}",YELLOW,cy2+368),(f"Coins: {coin_total}",GOLD,cy2+451)]:
        s=font_sub.render(txt,True,col); surface.blit(s,s.get_rect(center=(WIDTH//2,yy)))

    pb=pygame.Rect(WIDTH//2-240,cy2+540,480,100)
    pygame.draw.rect(surface,GREEN,pb,border_radius=22)
    pt=font_sub.render("Play Again",True,BLACK); surface.blit(pt,pt.get_rect(center=pb.center))

    bk=pygame.Rect(WIDTH//2-240,cy2+658,480,82)
    pygame.draw.rect(surface,(90,90,90),bk,border_radius=18)
    bt=font_small.render("Main Menu",True,WHITE); surface.blit(bt,bt.get_rect(center=bk.center))

    return pb,bk


# ======================== MAIN LOOP ========================
while True:
    dt           = clock.tick(120)
    current_time = pygame.time.get_ticks()

    # ---- Events ----
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit(); sys.exit()

        elif event.type==pygame.MOUSEBUTTONDOWN:
            touch_start_x=event.pos[0]; touch_start_y=event.pos[1]; last_touch_y=event.pos[1]

            if game_state=="menu":
                if menu_btn_ref and menu_btn_ref.collidepoint(event.pos):
                    reset_game(); game_state="playing"
                elif shop_btn_ref and shop_btn_ref.collidepoint(event.pos):
                    shop_scroll_y=0.0; shop_scroll_vel=0.0; game_state="shop"

            elif game_state=="gameover":
                if btn_rect_ref and btn_rect_ref.collidepoint(event.pos):
                    reset_game(); game_state="playing"
                elif back_to_menu_ref and back_to_menu_ref.collidepoint(event.pos):
                    game_state="menu"

            elif game_state=="shop":
                if shop_back_btn and shop_back_btn.collidepoint(event.pos):
                    game_state="menu"

        elif event.type==pygame.MOUSEMOTION:
            # ---- الـ scroll السلس عبر MOUSEMOTION ----
            if game_state=="shop" and touch_start_x is not None and last_touch_y is not None:
                dy=last_touch_y-event.pos[1]
                shop_scroll_y=max(0.0,min(shop_scroll_y+dy,float(shop_max_scroll)))
                shop_scroll_vel=float(dy)*0.9
                last_touch_y=event.pos[1]

        elif event.type==pygame.MOUSEBUTTONUP:
            if touch_start_x is not None:
                dx=event.pos[0]-touch_start_x; dy=event.pos[1]-touch_start_y

                if game_state=="playing":
                    if abs(dx)>abs(dy) and abs(dx)>80:
                        if dx<0 and target_lane>0:             target_lane-=1
                        elif dx>0 and target_lane<N_LANES-1:   target_lane+=1

                elif game_state=="shop":
                    if abs(dy)<25 and abs(dx)<25:
                        for item in shop_btns:
                            if item is None: continue
                            action,idx,btn_r=item
                            if btn_r.collidepoint(event.pos):
                                if action=="buy":
                                    coin_total-=PLAYER_SKINS[idx]["price"]
                                    owned_skins.add(idx); current_skin=idx
                                elif action=="select":
                                    current_skin=idx
                                break
            touch_start_x=None; touch_start_y=None; last_touch_y=None

    # ---- Shop momentum ----
    if game_state=="shop":
        shop_scroll_vel*=0.88
        shop_scroll_y=max(0.0,min(shop_scroll_y+shop_scroll_vel,float(shop_max_scroll)))
        if abs(shop_scroll_vel)<0.3: shop_scroll_vel=0.0

    # ---- Menu ----
    if game_state=="menu":
        menu_btn_ref,shop_btn_ref=draw_menu(draw_surface)
        screen.blit(draw_surface,(0,0)); pygame.display.update(); continue

    # ---- Shop ----
    if game_state=="shop":
        shop_btns,shop_back_btn=draw_shop(draw_surface,shop_scroll_y)
        screen.blit(draw_surface,(0,0)); pygame.display.update(); continue

    # ======================== GAME LOGIC ========================
    if game_state=="playing":
        has_shield     = current_time<active_shield_until
        has_red_shield = current_time<active_red_shield_until
        has_slow       = current_time<active_slow_until
        is_invincible  = current_time<invincible_until

        real_speed=obs_speed*(0.4 if has_slow else 1.0)

        stripe_y_offset=(stripe_y_offset+real_speed*0.6)%(STRIPE_H+STRIPE_GAP)
        for i in range(len(stars)):
            sx,sy=stars[i]; sy+=star_speeds[i]
            if sy>HEIGHT: sy=0; sx=random.randint(0,WIDTH)
            stars[i]=(sx,sy)

        tx=float(lane_centers[target_lane]-player_w//2)
        if player_x_current<tx: player_x_current=min(player_x_current+SLIDE_SPEED,tx)
        elif player_x_current>tx: player_x_current=max(player_x_current-SLIDE_SPEED,tx)

        run_timer+=1
        if run_timer>=RUN_SPEED: run_frame+=1; run_timer=0

        if current_time-last_spawn_time>spawn_delay:
            if can_spawn_obstacle():
                lc=pick_spawn_lane(); ot=random.choice(OBS_TYPES); lx=lane_centers[lc]
                obstacles.append({"rect":pygame.Rect(lx-ot["w"]//2,-ot["h"],ot["w"],ot["h"]),"type":ot})
            last_spawn_time=current_time
            if spawn_delay>350:   spawn_delay=max(350,spawn_delay-3)
            if obs_speed<40:      obs_speed+=0.04

        for obs in obstacles: obs["rect"].y+=int(real_speed)
        obstacles=[o for o in obstacles if o["rect"].y<HEIGHT+200]

        if current_time-last_moving_time>MOVING_OBS_FREQ:
            side=random.choice([0,2])
            moving_obs={"rect":pygame.Rect(lane_centers[side]-65,HEIGHT//3,130,200),
                        "type":OBS_TYPES[0],"dir":1 if side==0 else -1}
            last_moving_time=current_time
        if moving_obs:
            moving_obs["rect"].x+=moving_obs["dir"]*12
            cx2=moving_obs["rect"].centerx
            if cx2>lane_centers[2]+80 or cx2<lane_centers[0]-80: moving_obs["dir"]*=-1
            if moving_obs["rect"].y>HEIGHT+100: moving_obs=None

        if current_time-last_coin_time>COIN_DELAY:     spawn_coin();     last_coin_time=current_time
        if current_time-last_red_coin_time>RED_COIN_DELAY: spawn_red_coin(); last_red_coin_time=current_time

        for c in coins: c["y"]+=int(real_speed); c["anim"]+=1
        coins=[c for c in coins if c["y"]<HEIGHT+50]

        if current_time-last_pu_time>PU_DELAY: spawn_powerup(); last_pu_time=current_time
        for pu in powerups: pu["y"]+=int(real_speed)
        powerups=[pu for pu in powerups if pu["y"]<HEIGHT+50]

        px=int(player_x_current)
        prect  =pygame.Rect(px+15,player_y+20,player_w-30,player_h-20)
        pcenter=(px+player_w//2,player_y+player_h//2)

        for c in coins[:]:
            if math.hypot(pcenter[0]-c["x"],pcenter[1]-c["y"])<COIN_R+40:
                coins.remove(c); play_sound(snd_coin)
                if c["kind"]=="gold":
                    coin_total+=1; score+=50
                    coin_anim.append([c["x"],c["y"],255,0,"gold"])
                elif c["kind"]=="red":
                    red_coin_count+=1
                    coin_anim.append([c["x"],c["y"],255,0,"red"])
                    if red_coin_count>=RED_COIN_NEEDED:
                        red_coin_count=0
                        if lives<MAX_LIVES: lives+=1
                        else: active_red_shield_until=current_time+RED_SHIELD_DURATION
                        play_sound(snd_powerup)

        for pu in powerups[:]:
            if math.hypot(pcenter[0]-pu["x"],pcenter[1]-pu["y"])<POWERUP_R+40:
                powerups.remove(pu); play_sound(snd_powerup)
                if pu["kind"]=="shield": active_shield_until=current_time+SHIELD_DURATION
                else:                    active_slow_until  =current_time+SLOW_DURATION

        # ✅ FIX SHIELD: أعد الحساب بعد الجمع عشان القيم تكون محدثة
        has_shield     = current_time<active_shield_until
        has_red_shield = current_time<active_red_shield_until
        is_invincible  = current_time<invincible_until

        # ✅ FIX SHIELD: لو عندك درع = مفيش ضرر خالص (مش بيتكسر الدرع بالاصطدام)
        if not has_shield and not has_red_shield and not is_invincible:
            all_obs=obstacles+([moving_obs] if moving_obs else [])
            for obs in all_obs:
                if prect.colliderect(obs["rect"].inflate(-20,-20)):
                    lives-=1; invincible_until=current_time+INVINCIBLE_AFTER_HIT
                    edge_flash=20; play_sound(snd_hit)
                    if lives<=0:
                        game_state="gameover"; high_score=max(high_score,score)
                    break

        new_level=score//2000+1
        if new_level>level:
            level=new_level; level_flash=240; play_sound(snd_levelup)

        if level_flash>0: level_flash-=1
        if edge_flash>0:  edge_flash-=1
        score+=1

    # ======================== DRAWING ========================
    draw_surface.fill((15,15,30))

    for i,(sx,sy) in enumerate(stars):
        b=star_bright[i]
        pygame.draw.circle(draw_surface,(b,b,b),(sx,sy),2)

    pygame.draw.rect(draw_surface,get_road_color(),(road_x,0,road_w,HEIGHT))
    for li in (1,2):
        lx=int(road_x+road_w*li/3)
        y2=int(stripe_y_offset)-(STRIPE_H+STRIPE_GAP)
        while y2<HEIGHT:
            pygame.draw.rect(draw_surface,STRIPE_COLOR,pygame.Rect(lx-5,y2,10,STRIPE_H))
            y2+=STRIPE_H+STRIPE_GAP
    pygame.draw.rect(draw_surface,WHITE,(road_x-8,0,8,HEIGHT))
    pygame.draw.rect(draw_surface,WHITE,(road_x+road_w,0,8,HEIGHT))

    if game_state in ("playing","gameover"):
        has_shield     = current_time<active_shield_until
        has_red_shield = current_time<active_red_shield_until
        has_slow       = current_time<active_slow_until
        is_invincible  = current_time<invincible_until

        for obs in obstacles: draw_obstacle(draw_surface,obs)
        if moving_obs: draw_obstacle(draw_surface,moving_obs)
        for c in coins: draw_coin(draw_surface,c)
        for pu in powerups: draw_powerup(draw_surface,pu)

        # أنيميشن جمع العملات (بدون new Surface - نستخدم copy من pre-cached)
        for ca in coin_anim[:]:
            base = _anim_red_surf if (len(ca)>=5 and ca[4]=="red") else _anim_gold_surf
            txt  = base.copy()
            txt.set_alpha(ca[2])
            draw_surface.blit(txt,(ca[0]-30,ca[1]-ca[3]))
            ca[2]-=7; ca[3]+=2
            if ca[2]<=0: coin_anim.remove(ca)

        show_player=not(is_invincible and (current_time//80)%2==0)
        if show_player:
            draw_player(draw_surface,int(player_x_current),player_y,run_frame,
                        shielded=has_shield,red_shielded=has_red_shield)

        # ---- HUD ----
        sb=pygame.Rect(20,20,310,80)
        pygame.draw.rect(draw_surface,BLACK,sb,border_radius=16)
        pygame.draw.rect(draw_surface,NEON_CYAN,sb,3,border_radius=16)
        draw_surface.blit(font_score.render(f"Score: {score}",True,WHITE),(35,30))

        hs=font_label.render(f"Best: {high_score}",True,YELLOW)
        draw_surface.blit(hs,hs.get_rect(topright=(WIDTH-20,30)))

        for i in range(MAX_LIVES):
            hc2=HEART_RED if i<lives else DARK_GREY
            hx=30+i*80; hy=120
            pygame.draw.circle(draw_surface,hc2,(hx+12,hy+10),18)
            pygame.draw.circle(draw_surface,hc2,(hx+36,hy+10),18)
            pygame.draw.polygon(draw_surface,hc2,[(hx,hy+16),(hx+24,hy+50),(hx+48,hy+16)])

        rl=font_small.render("Red:",True,RED_COIN_COLOR)
        draw_surface.blit(rl,(28,192))
        for i in range(RED_COIN_NEEDED):
            rc2=HEART_RED if i<red_coin_count else DARK_GREY
            rx=128+i*46; ry=200
            pygame.draw.circle(draw_surface,rc2,(rx+8,ry+6),7)
            pygame.draw.circle(draw_surface,rc2,(rx+22,ry+6),7)
            pygame.draw.polygon(draw_surface,rc2,[(rx+2,ry+10),(rx+15,ry+24),(rx+28,ry+10)])

        lv=font_label.render(f"Lv.{level}",True,NEON_CYAN)
        draw_surface.blit(lv,(WIDTH//2-lv.get_width()//2,25))
        co=font_label.render(f"$ {coin_total}",True,GOLD)
        draw_surface.blit(co,(WIDTH//2-co.get_width()//2,90))

        if has_shield:
            rem=max(0,(active_shield_until-current_time)/SHIELD_DURATION)
            pygame.draw.rect(draw_surface,DARK_GREY,   (WIDTH-330,90,300,22),border_radius=8)
            pygame.draw.rect(draw_surface,SHIELD_COLOR,(WIDTH-330,90,int(300*rem),22),border_radius=8)
            draw_surface.blit(font_small.render("SHIELD",True,SHIELD_COLOR),(WIDTH-330,60))
        if has_red_shield:
            rem=max(0,(active_red_shield_until-current_time)/RED_SHIELD_DURATION)
            pygame.draw.rect(draw_surface,DARK_GREY,     (WIDTH-330,90,300,22),border_radius=8)
            pygame.draw.rect(draw_surface,RED_SHIELD_COL,(WIDTH-330,90,int(300*rem),22),border_radius=8)
            draw_surface.blit(font_small.render("RED SHIELD",True,RED_SHIELD_COL),(WIDTH-330,60))
        if has_slow:
            rem=max(0,(active_slow_until-current_time)/SLOW_DURATION)
            pygame.draw.rect(draw_surface,DARK_GREY, (WIDTH-330,150,300,22),border_radius=8)
            pygame.draw.rect(draw_surface,SLOW_COLOR,(WIDTH-330,150,int(300*rem),22),border_radius=8)
            draw_surface.blit(font_small.render("SLOW",True,SLOW_COLOR),(WIDTH-330,120))

        if level_flash>0:
            lf=_level_surfs.get(level)
            if lf:
                lfc=lf.copy(); lfc.set_alpha(min(255,level_flash*3))
                draw_surface.blit(lfc,lfc.get_rect(center=(WIDTH//2,HEIGHT//2-200)))

        if edge_flash>0:
            ef_surf.fill((0,0,0,0))
            a=min(180,edge_flash*9)
            pygame.draw.rect(ef_surf,(220,0,0,a),(0,       0,      30,     HEIGHT))
            pygame.draw.rect(ef_surf,(220,0,0,a),(WIDTH-30,0,      30,     HEIGHT))
            pygame.draw.rect(ef_surf,(220,0,0,a),(0,       0,      WIDTH,  30))
            pygame.draw.rect(ef_surf,(220,0,0,a),(0,       HEIGHT-30,WIDTH,30))
            draw_surface.blit(ef_surf,(0,0))

    if game_state=="gameover":
        game_over_alpha=min(game_over_alpha+40,255)
        btn_rect_ref,back_to_menu_ref=draw_game_over(draw_surface,score,high_score,game_over_alpha)

    screen.blit(draw_surface,(0,0))
    pygame.display.update()
