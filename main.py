# ═══════════════════════════════════════
#   SUBWAY RUNNER - KIVY  v3.0
#   Fixes: orientation, shop, menu text,
#          35 skins (+ 10 rolling balls)
# ═══════════════════════════════════════
import random, math, json, os, time, wave, struct
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import (Color, Ellipse, Rectangle, Line,
                            RoundedRectangle, Triangle,
                            PushMatrix, PopMatrix, Scale, Translate, Rotate)
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

W = Window.width
H = Window.height

# ── Colors ─────────────────────────────
def C(r,g,b): return (r/255, g/255, b/255, 1)
BG    = C(15,15,30);   ROAD  = C(60,60,65)
CYAN  = C(0,240,255);  GOLD  = C(255,200,0)
GREEN = C(50,200,80);  RED   = C(220,50,50)
GREY  = C(120,120,120);DGREY = C(40,40,40)
HRED  = C(255,50,80);  SHLD  = C(100,200,255)
SLOW  = C(180,100,255);RSHLD = C(255,90,90)
WHITE = C(255,255,255);STRP  = C(200,200,50)
YEL   = C(255,220,50); RCOIN = C(255,60,60)

# ── Road / Lane ───────────────────────
RX = int(W * 0.074)
RW = int(W * 0.852)
LANES = [RX+RW//6, RX+RW//2, RX+5*RW//6]
PW = int(W * 0.093)
PH = int(H * 0.087)
PY = int(H * 0.044)

ROAD_COLORS = [(60,60,65),(40,60,40),(50,40,70),(70,40,40),(30,50,70)]

# ── Obstacle types ────────────────────
OD = [
    {"c":(220,50,50),  "sh":"rect",   "w":int(W*.12), "h":int(H*.104)},
    {"c":(255,140,0),  "sh":"barrier","w":int(W*.148),"h":int(H*.052)},
    {"c":(160,60,200), "sh":"truck",  "w":int(W*.139),"h":int(H*.139)},
    {"c":(50,200,80),  "sh":"cone",   "w":int(W*.093),"h":int(H*.070)},
]

# ── Skins  (35 total: 15 human + 5 moto + 5 car + 10 ball) ──────────
SK = [
    # ── Human – Brown Hair ────────────────────────────────────────────
    {"n":"Classic","p":0,  "t":"h","hr":(35,22,10),   "b":(30,60,140),  "pt":(15,15,15),   "s":(45,45,45)},
    {"n":"Red",    "p":50, "t":"h","hr":(35,22,10),   "b":(165,30,30),  "pt":(85,0,0),     "s":(55,0,0)},
    {"n":"Green",  "p":100,"t":"h","hr":(35,22,10),   "b":(20,135,55),  "pt":(0,75,22),    "s":(0,52,12)},
    {"n":"Purple", "p":150,"t":"h","hr":(35,22,10),   "b":(125,40,175), "pt":(72,0,115),   "s":(52,0,82)},
    {"n":"Gold",   "p":300,"t":"h","hr":(35,22,10),   "b":(185,145,0),  "pt":(115,82,0),   "s":(82,52,0)},
    # ── Human – Blonde Hair ───────────────────────────────────────────
    {"n":"Blonde", "p":150,"t":"h","hr":(225,185,45), "b":(205,205,225),"pt":(82,82,125),  "s":(62,62,92)},
    {"n":"Surfer", "p":175,"t":"h","hr":(225,185,45), "b":(0,155,185),  "pt":(0,82,135),   "s":(0,62,105)},
    {"n":"Sandy",  "p":200,"t":"h","hr":(225,185,45), "b":(215,145,62), "pt":(145,82,22),  "s":(105,58,12)},
    {"n":"Lemon",  "p":225,"t":"h","hr":(225,185,45), "b":(210,210,0),  "pt":(140,140,0),  "s":(100,100,0)},
    {"n":"Cotton", "p":250,"t":"h","hr":(225,185,45), "b":(255,175,195),"pt":(200,100,130),"s":(160,70,100)},
    # ── Human – Special ───────────────────────────────────────────────
    {"n":"Ninja",  "p":200,"t":"h","hr":(12,12,12),   "b":(22,22,22),   "pt":(12,12,12),   "s":(32,32,32)},
    {"n":"Ocean",  "p":225,"t":"h","hr":(0,105,165),  "b":(0,165,205),  "pt":(0,82,145),   "s":(255,255,255)},
    {"n":"Fire",   "p":250,"t":"h","hr":(205,82,0),   "b":(225,82,0),   "pt":(165,32,0),   "s":(125,22,0)},
    {"n":"Snow",   "p":275,"t":"h","hr":(242,242,255), "b":(222,238,255),"pt":(162,182,222),"s":(202,222,255)},
    {"n":"Shadow", "p":400,"t":"h","hr":(8,8,8),      "b":(32,32,38),   "pt":(18,18,22),   "s":(22,22,28)},
    # ── Motorcycle ────────────────────────────────────────────────────
    {"n":"Moto R", "p":350,"t":"m","b":(200,30,30),   "a":(255,90,90),  "m":(140,0,0)},
    {"n":"Moto B", "p":350,"t":"m","b":(20,60,200),   "a":(80,140,255), "m":(0,30,140)},
    {"n":"Moto G", "p":400,"t":"m","b":(20,150,50),   "a":(80,230,110), "m":(0,100,20)},
    {"n":"Moto O", "p":400,"t":"m","b":(220,110,0),   "a":(255,175,40), "m":(160,70,0)},
    {"n":"Moto P", "p":450,"t":"m","b":(120,20,180),  "a":(190,90,255), "m":(80,0,130)},
    # ── Car ───────────────────────────────────────────────────────────
    {"n":"Car R",  "p":500,"t":"c","b":(200,30,30),   "g":(160,210,240),"d":(130,0,0)},
    {"n":"Car B",  "p":500,"t":"c","b":(20,60,200),   "g":(160,210,240),"d":(0,30,140)},
    {"n":"Car Y",  "p":550,"t":"c","b":(220,200,0),   "g":(160,210,240),"d":(150,135,0)},
    {"n":"Car W",  "p":550,"t":"c","b":(230,230,235), "g":(160,210,240),"d":(170,170,175)},
    {"n":"Car K",  "p":600,"t":"c","b":(25,25,30),    "g":(100,150,180),"d":(15,15,20)},
    # ── Ball (rolling) ────────────────────────────────────────────────
    {"n":"Soccer", "p":200,"t":"b","b":(240,240,240), "c1":(15,15,15),  "st":"soccer"},
    {"n":"Basket", "p":225,"t":"b","b":(210,95,20),   "c1":(20,20,20),  "st":"basketball"},
    {"n":"Tennis", "p":250,"t":"b","b":(185,215,30),  "c1":(255,255,255),"st":"tennis"},
    {"n":"Earth",  "p":275,"t":"b","b":(30,100,210),  "c1":(30,175,55), "st":"earth"},
    {"n":"Fire B", "p":325,"t":"b","b":(225,45,0),    "c1":(255,210,0), "st":"fireball"},
    {"n":"Ice",    "p":325,"t":"b","b":(195,230,255), "c1":(120,190,255),"st":"ice"},
    {"n":"Neon",   "p":375,"t":"b","b":(255,20,200),  "c1":(255,180,240),"st":"neon"},
    {"n":"Galaxy", "p":375,"t":"b","b":(8,4,28),      "c1":(195,145,255),"st":"galaxy"},
    {"n":"8-Ball", "p":425,"t":"b","b":(10,10,10),    "c1":(255,255,255),"st":"pool8"},
    {"n":"Rainbow","p":475,"t":"b","b":(220,0,0),     "c1":(220,220,0), "st":"rainbow"},
]

# ── Save / Load ───────────────────────
SF = "sr_save.json"
SOUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sr_sfx")

def _clamp16(v):
    return max(-32767, min(32767, int(v)))

def _write_tone(path, seq, volume=.42, sample_rate=22050):
    frames=[]
    for freq,dur,wave_type in seq:
        count=max(1,int(sample_rate*dur))
        for i in range(count):
            t=i/sample_rate
            if wave_type=="square":
                base=1.0 if math.sin(2*math.pi*freq*t)>=0 else -1.0
            elif wave_type=="noise":
                base=random.uniform(-1,1)*(1-(i/max(1,count-1)))
            else:
                base=math.sin(2*math.pi*freq*t)
            attack=max(1,int(count*.08))
            release=max(1,int(count*.18))
            env=min(1.0, i/attack, (count-i)/release)
            frames.append(_clamp16(base*32767*volume*env))
    with wave.open(path,'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(struct.pack('<h',f) for f in frames))

def ensure_sfx():
    os.makedirs(SOUND_DIR, exist_ok=True)
    specs={
        "button":   [(740,.05,"square")],
        "pause":    [(520,.06,"square"),(390,.07,"square")],
        "coin":     [(1100,.05,"sine"),(1450,.06,"sine")],
        "red_coin": [(720,.05,"square"),(980,.05,"square"),(1280,.06,"square")],
        "powerup":  [(540,.05,"sine"),(760,.05,"sine"),(980,.08,"sine")],
        "hit":      [(160,.10,"square"),(95,.12,"noise")],
        "gameover": [(420,.08,"square"),(260,.11,"square"),(160,.16,"sine")],
    }
    out={}
    for name,seq in specs.items():
        p=os.path.join(SOUND_DIR,f"{name}.wav")
        if not os.path.exists(p):
            _write_tone(p,seq)
        out[name]=p
    return out

def save(ct, hs, ski, ow, vol=None, muted=None):
    try:
        prev_vol=1.0
        prev_muted=False
        if os.path.exists(SF):
            try:
                prev=json.loads(open(SF).read())
                prev_vol=float(prev.get("v",1.0))
                prev_muted=bool(prev.get("m",False))
            except:
                pass
        if vol is None: vol=prev_vol
        if muted is None: muted=prev_muted
        with open(SF,"w") as f:
            json.dump({"c":ct,"h":hs,"s":ski,"o":list(ow),"v":vol,"m":muted},f)
    except: pass

def load():
    try:
        if os.path.exists(SF):
            d = json.loads(open(SF).read())
            return (
                d.get("c",0),
                d.get("h",0),
                d.get("s",0),
                set(d.get("o",[0])),
                float(d.get("v",1.0)),
                bool(d.get("m",False)),
            )
    except: pass
    return 0,0,0,{0},1.0,False


# ═══════════════════════════════════════
#   DRAW MIXIN
#   Shared by GameCanvas + MenuPlayerWidget
# ═══════════════════════════════════════
class DrawMixin:
    """All primitive drawing helpers and skin renderers."""

    def _ms(self): return int(time.time()*1000)
    def _rc2(self,raw,a=1): return (raw[0]/255,raw[1]/255,raw[2]/255,a)
    def _el(self,x,y,w,h,col,a=1): Color(*col[:3],a); Ellipse(pos=(x,y),size=(w,h))
    def _rr(self,x,y,w,h,col,a=1,r=0):
        Color(*col[:3],a)
        if r>0: RoundedRectangle(pos=(x,y),size=(w,h),radius=[r])
        else:   Rectangle(pos=(x,y),size=(w,h))
    def _cr(self,cx,cy,r,col,a=1): Color(*col[:3],a); Ellipse(pos=(cx-r,cy-r),size=(2*r,2*r))
    def _ln(self,x1,y1,x2,y2,col,lw=2,a=1): Color(*col[:3],a); Line(points=[x1,y1,x2,y2],width=lw)
    def _tr(self,pts,col,a=1):
        Color(*col[:3],a)
        Triangle(points=[pts[0][0],pts[0][1],pts[1][0],pts[1][1],pts[2][0],pts[2][1]])

    # ── Human ─────────────────────────
    def _dh(self,x,y,fr,sk,hs,hrs):
        cx=x+PW//2; ls=math.sin(fr*.35)*PW*.28
        bc=self._rc2(sk["b"]); hc=self._rc2(sk["hr"])
        pc=self._rc2(sk["pt"]); sc=self._rc2(sk["s"])
        self._el(x+8,y-12,PW-8,38,(.03,.03,.03),.06)
        t=self._ms()/1000
        if hrs:
            p=abs(math.sin(t*3.5))
            Color(min(1,(200+55*p)/255),min(1,(40+30*p)/255),min(1,(40+30*p)/255),1)
            Line(circle=(cx,y+PH//2,int(PW*.96)),width=7)
        elif hs:
            p=abs(math.sin(t*3))
            Color(min(1,(100*p+50)/255),min(1,(200*p+50)/255),1,1)
            Line(circle=(cx,y+PH//2,int(PW*.9)),width=5)
        hy=y+int(PH*.09)
        self._el(cx-int(PW*.27),hy,int(PW*.54),int(PH*.19),(1,.784,.588))
        self._el(cx-int(PW*.27),hy,int(PW*.54),int(PH*.095),hc)
        self._cr(cx-int(PW*.1),hy+int(PH*.12),int(PW*.05),(0,0,0))
        self._cr(cx+int(PW*.1),hy+int(PH*.12),int(PW*.05),(0,0,0))
        sy2=y+int(PH*.26)
        self._el(cx-int(PW*.48),sy2,int(PW*.96),int(PH*.12),bc)
        self._rr(cx-int(PW*.33),sy2+int(PH*.05),int(PW*.66),int(PH*.31),bc,r=12)
        lax=int(cx-PW*.46+(-ls*.45))
        self._ln(cx-int(PW*.33),sy2+int(PH*.08),lax,sy2+int(PH*.17),bc,lw=int(PW*.18))
        self._cr(lax,sy2+int(PH*.17),int(PW*.12),(1,.784,.588))
        rax=int(cx+PW*.46+(ls*.45))
        self._ln(cx+int(PW*.33),sy2+int(PH*.08),rax,sy2+int(PH*.17),bc,lw=int(PW*.18))
        self._cr(rax,sy2+int(PH*.17),int(PW*.12),(1,.784,.588))
        py2=sy2+int(PH*.35)
        self._rr(cx-int(PW*.3),py2,int(PW*.6),int(PH*.19),pc,r=8)
        ls2=int(ls)
        llx=cx-int(PW*.17)+ls2; lly=y+PH-int(PH*.08)
        rlx=cx+int(PW*.17)-ls2; rly=y+PH-int(PH*.08)+int(abs(math.sin(fr*.35))*PH*.035)
        self._ln(cx-int(PW*.17),py2+int(PH*.17),llx,lly,pc,lw=int(PW*.2))
        self._el(llx-int(PW*.2),lly-int(PH*.04),int(PW*.4),int(PH*.087),sc)
        self._ln(cx+int(PW*.17),py2+int(PH*.17),rlx,rly,pc,lw=int(PW*.2))
        self._el(rlx-int(PW*.2),rly-int(PH*.04),int(PW*.4),int(PH*.087),sc)

    # ── Motorcycle ────────────────────
    def _dm(self,x,y,fr,sk,hs,hrs):
        cx=x+PW//2; sw=int(math.sin(fr*.35)*4)
        bc=self._rc2(sk["b"]); ac=self._rc2(sk["a"]); mc=self._rc2(sk["m"])
        self._el(cx-22,y-0,44,200,(.03,.03,.03),.06)
        t=self._ms()/1000
        if hrs:
            p=abs(math.sin(t*3.5))
            Color(min(1,(200+55*p)/255),min(1,(40+30*p)/255),min(1,(40+30*p)/255),1)
            Line(circle=(cx,y+PH//2,int(PW*.96)),width=7)
        elif hs:
            p=abs(math.sin(t*3))
            Color(min(1,(100*p+50)/255),min(1,(200*p+50)/255),1,1)
            Line(circle=(cx,y+PH//2,int(PW*.9)),width=5)
        self._el(cx-16+sw,y+PH-52,32,46,(.06,.06,.06))
        self._el(cx-10+sw,y+PH-46,20,34,(.24,.24,.24))
        self._el(cx-20,y+24,40,PH-74,bc)
        self._el(cx-9,y+34,18,PH-96,ac)
        self._el(cx-16,y+PH//2-18,32,26,ac)
        self._el(cx-14-sw,y+8,28,40,(.06,.06,.06))
        self._el(cx-9-sw,y+13,18,30,(.24,.24,.24))
        Color(.43,.43,.43,1); Line(points=[cx-26+sw,y+38,cx+26+sw,y+38],width=6)
        self._cr(cx+sw,y+PH//2-12,20,mc)

    # ── Car ───────────────────────────
    def _dc(self,x,y,fr,sk,hs,hrs):
        cx=x+PW//2
        bc=self._rc2(sk["b"]); gc=self._rc2(sk["g"]); dc=self._rc2(sk["d"])
        self._el(cx-42,y-10,84,18,(.03,.03,.03),.06)
        t=self._ms()/1000
        if hrs:
            p=abs(math.sin(t*3.5))
            Color(min(1,(200+55*p)/255),min(1,(40+30*p)/255),min(1,(40+30*p)/255),1)
            Line(circle=(cx,y+PH//2,int(PW*.96)),width=7)
        elif hs:
            p=abs(math.sin(t*3))
            Color(min(1,(100*p+50)/255),min(1,(200*p+50)/255),1,1)
            Line(circle=(cx,y+PH//2,int(PW*.9)),width=5)
        self._rr(cx-40,y+8,80,PH-16,bc,r=18)
        self._rr(cx-28,y+52,56,PH-104,dc,r=12)
        self._rr(cx-26,y+14,52,36,gc,r=8)
        self._rr(cx-22,y+PH-55,44,30,gc,r=8)
        self._rr(cx-41,y+65,14,42,gc,r=5)
        self._rr(cx+27,y+65,14,42,gc,r=5)
        for wx,wy in[(cx-51,y+16),(cx+39,y+16),(cx-51,y+PH-48),(cx+39,y+PH-48)]:
            self._rr(wx,wy,12,26,(.07,.07,.07),r=4)
        self._rr(cx-36,y+10,16,8,(.1,.86,.2),r=3)
        self._rr(cx+20,y+10,16,8,(.1,.86,.2),r=3)
        self._rr(cx-36,y+PH-22,16,8,(.9,.08,.08),r=3)
        self._rr(cx+20,y+PH-22,16,8,(.9,.08,.08),r=3)

    # ── Ball (rolling animation) ───────
    def _db(self,x,y,fr,sk,hs,hrs):
        cx=x+PW//2; cy=y+PH//2
        r=min(PW,PH)//2-2
        bc=self._rc2(sk["b"]); c1=self._rc2(sk["c1"])
        st=sk.get("st","soccer")
        t=self._ms()/1000
        ang=getattr(self,'ball_angle',0)  # rolling angle driven by speed

        # Shield halo
        if hrs:
            p=abs(math.sin(t*3.5))
            Color(min(1,(200+55*p)/255),min(1,(40+30*p)/255),min(1,(40+30*p)/255),1)
            Line(circle=(cx,cy,int(PW*.96)),width=7)
        elif hs:
            p=abs(math.sin(t*3))
            Color(min(1,(100*p+50)/255),min(1,(200*p+50)/255),1,1)
            Line(circle=(cx,cy,int(PW*.9)),width=5)

        # Shadow
        Color(.03,.03,.03,.55); Ellipse(pos=(cx-r,cy+r+0),size=(r*2,12))
        # Base ball
        self._cr(cx,cy,r,bc)

        # ── Soccer ────────────────────
        if st=="soccer":
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang,axis=(0,0,1)); Translate(-cx,-cy,0)
            for a2 in [0,72,144,216,288]:
                rad=math.radians(a2)
                px2=cx+int(r*.55*math.cos(rad)); py2=cy+int(r*.55*math.sin(rad))
                self._cr(px2,py2,int(r*.28),(.08,.08,.08))
            self._cr(cx,cy,int(r*.28),(.08,.08,.08))
            PopMatrix()

        # ── Basketball ────────────────
        elif st=="basketball":
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang,axis=(0,0,1)); Translate(-cx,-cy,0)
            Color(*c1[:3],1)
            Line(circle=(cx,cy,int(r*.58)),width=2)
            Line(points=[cx-r,cy,cx+r,cy],width=2)
            Line(points=[cx,cy-r,cx,cy+r],width=1)
            PopMatrix()

        # ── Tennis ────────────────────
        elif st=="tennis":
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang,axis=(0,0,1)); Translate(-cx,-cy,0)
            Color(1,1,1,.9)
            Line(points=[cx-r+6,cy-r//4,cx+r-6,cy+r//4],width=3)
            Line(points=[cx-r+6,cy+r//4,cx+r-6,cy-r//4],width=3)
            PopMatrix()

        # ── Earth ─────────────────────
        elif st=="earth":
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang,axis=(0,0,1)); Translate(-cx,-cy,0)
            Color(.12,.70,.24,1)
            Ellipse(pos=(cx-r//3,cy),size=(r//2,r//2))
            Ellipse(pos=(cx+r//6,cy-r//3),size=(r//2,r//3))
            Ellipse(pos=(cx-r//2,cy-r//5),size=(r//3,r//3))
            PopMatrix()

        # ── Fire Ball ─────────────────
        elif st=="fireball":
            pulse=abs(math.sin(t*5))*.2
            rp=r+int(r*pulse)
            Color(*bc[:3],.35); Ellipse(pos=(cx-rp,cy-rp),size=(rp*2,rp*2))
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang*2,axis=(0,0,1)); Translate(-cx,-cy,0)
            self._cr(cx,cy,r//2,c1)
            self._cr(cx,cy,r//5,(1,1,.8))
            PopMatrix()

        # ── Ice ───────────────────────
        elif st=="ice":
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang,axis=(0,0,1)); Translate(-cx,-cy,0)
            Color(*c1[:3],.8)
            for a2 in range(0,360,60):
                rad=math.radians(a2)
                ex=cx+int(r*.7*math.cos(rad)); ey=cy+int(r*.7*math.sin(rad))
                Line(points=[cx,cy,ex,ey],width=2)
                self._cr(ex,ey,int(r*.1),c1)
            PopMatrix()
            self._cr(cx-r//3,cy+r//3,r//5,(1,1,1),.75)

        # ── Neon ──────────────────────
        elif st=="neon":
            glow=abs(math.sin(t*3))*.45+.25
            Color(*bc[:3],glow*.4); Ellipse(pos=(cx-r-10,cy-r-10),size=((r+10)*2,(r+10)*2))
            Color(*bc[:3],glow*.65); Ellipse(pos=(cx-r-4,cy-r-4),size=((r+4)*2,(r+4)*2))
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang*1.5,axis=(0,0,1)); Translate(-cx,-cy,0)
            self._cr(cx,cy,r-5,c1)
            PopMatrix()

        # ── Galaxy ────────────────────
        elif st=="galaxy":
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang*.35,axis=(0,0,1)); Translate(-cx,-cy,0)
            random.seed(42)
            for _ in range(18):
                sx=cx+random.randint(-r+5,r-5); sy2=cy+random.randint(-r+5,r-5)
                if math.hypot(sx-cx,sy2-cy)<r-3:
                    self._cr(sx,sy2,random.randint(1,3),c1)
            random.seed()
            PopMatrix()
            self._cr(cx,cy,r//4,(80/255,50/255,120/255),.85)

        # ── 8-Ball ────────────────────
        elif st=="pool8":
            self._cr(cx,cy,int(r*.6),(1,1,1))
            # Circle marker stays centred (no rotation — realistic 8-ball look)
            self._cr(cx,cy,int(r*.22),(.04,.04,.04))
            Color(1,1,1,1)
            Ellipse(pos=(cx-int(r*.1),cy-int(r*.1)),size=(int(r*.2),int(r*.2)))

        # ── Rainbow ───────────────────
        elif st=="rainbow":
            PushMatrix()
            Translate(cx,cy,0); Rotate(angle=ang*.25,axis=(0,0,1)); Translate(-cx,-cy,0)
            cols=[(220,0,0),(220,100,0),(220,220,0),(0,160,0),(0,80,220),(120,0,220),(200,0,180)]
            for idx,col in enumerate(reversed(cols)):
                self._cr(cx,cy,r-idx*int(r*.12),self._rc2(col))
            PopMatrix()

        # Highlight (not rotated — stays top-left of ball)
        self._cr(cx-r//3,cy+r//3,r//5,(1,1,1),.3)

    # ── Player dispatcher ─────────────
    def _dp(self,x,y,fr,hs,hrs):
        sk=SK[self.ski]; t=sk["t"]
        if   t=="m": self._dm(x,y,fr,sk,hs,hrs)
        elif t=="c": self._dc(x,y,fr,sk,hs,hrs)
        elif t=="b": self._db(x,y,fr,sk,hs,hrs)
        else:        self._dh(x,y,fr,sk,hs,hrs)

    # ── Obstacle ──────────────────────
    def _do(self,o):
        ox=o["x"]; oy=o["y"]; ow=o["w"]; oh=o["h"]
        cl=self._rc2(o["t"]["c"]); sh=o["t"]["sh"]; cx=ox+ow//2
        if sh=="rect":
            self._rr(ox,oy,ow,oh,cl,r=18)
            self._rr(ox+15,oy+20,ow-30,55,(.706,.863,1),r=10)
            self._rr(ox+15,oy+90,ow-30,45,(.706,.863,1),r=8)
            for wx in[ox+12,ox+ow-28]:
                self._cr(wx+8,oy+oh-20,22,(0,0,0)); self._cr(wx+8,oy+oh-20,14,(.47,.47,.47))
        elif sh=="barrier":
            self._rr(ox,oy,ow,oh,cl,r=10)
            for i in range(0,ow,35):
                x1=ox+i; x2=min(x1+25,ox+ow)
                self._ln(x1,oy,x2,oy+oh,(1,1,1),lw=6)
            Color(*cl); Line(rectangle=(ox,oy,ow,oh),width=4)
        elif sh=="truck":
            self._rr(ox,oy,ow,oh,cl,r=12)
            dc2=(o["t"]["c"][0]//2/255,o["t"]["c"][1]//2/255,o["t"]["c"][2]//2/255,1)
            self._rr(ox+10,oy,ow-20,100,dc2,r=14)
            self._rr(ox+20,oy+10,ow-40,50,(.706,.863,1),r=8)
            for wx in[ox+8,ox+ow-36]:
                self._cr(wx+14,oy+oh-25,26,(0,0,0)); self._cr(wx+14,oy+oh-25,16,(.47,.47,.47))
        elif sh=="cone":
            self._tr([(cx,oy+oh),(ox,oy),(ox+ow,oy)],cl)
            self._ln(cx,oy+oh-20,cx-18,oy+20,(1,1,1),lw=5)
            self._ln(cx,oy+oh-20,cx+18,oy+20,(1,1,1),lw=5)
            self._rr(ox,oy,ow,18,(1,1,1),r=4)

    # ── Coin ──────────────────────────
    def _dco(self,c):
        x=c["x"]; y=c["y"]; ar=int(math.sin(c["a"]*.2)*4)
        if c["k"]=="g":
            r=self.CR+ar
            self._cr(x,y,r,(1,.784,0)); self._cr(x,y,r-7,(1,.863,.2))
            Color(1,.784,0,1); Line(circle=(x,y,r-7),width=3)
        else:
            r=self.CR+ar
            self._cr(x,y,r,(1,.235,.235)); self._cr(x,y,r-6,(1,.51,.51))
            hr=r-10
            # FIX: flip heart so it points downward correctly (Kivy y-up)
            PushMatrix()
            Translate(x,y,0); Scale(1,-1,1); Translate(-x,-y,0)
            self._cr(x-hr//2,y-hr//4,hr//2,(1,.196,.314))
            self._cr(x+hr//2,y-hr//4,hr//2,(1,.196,.314))
            self._tr([(x-hr,y-hr//4),(x,y+hr//2+4),(x+hr,y-hr//4)],(1,.196,.314))
            PopMatrix()

    # ── Powerup ───────────────────────
    def _dpu(self,p):
        PR=getattr(self,'PR',int(W*.033))
        x=p["x"]; y=p["y"]; r=PR
        if p["k"]=="s":
            self._cr(x,y,r,(.08,.2,.43))
            Color(*SHLD); Line(circle=(x,y,r),width=4)
            pts=[(x,y+r),(x+r,y+r//2),(x+r,y-r//3),(x,y-r),(x-r,y-r//3),(x-r,y+r//2)]
            Color(*SHLD)
            for i in range(len(pts)):
                p1=pts[i]; p2=pts[(i+1)%len(pts)]
                Triangle(points=[x,y,p1[0],p1[1],p2[0],p2[1]])
        else:
            self._cr(x,y,r,(.2,.06,.27))
            Color(*SLOW); Line(circle=(x,y,r),width=4)
            self._el(x-r+7,y-r//2,(r-7)*2,int((r-7)*1.3),(.0,.627,.275))
            self._cr(x,y-r//2-r//3,r//3,(.0,.569,.235))


# ═══════════════════════════════════════
#   GAME CANVAS WIDGET
# ═══════════════════════════════════════
class GameCanvas(DrawMixin, Widget):
    def __init__(self,app_ref,**kw):
        super().__init__(**kw)
        self.app=app_ref
        self.size=(W,H); self.pos=(0,0)
        ct,hs,ski,ow,_,_=load()
        self.ct=ct; self.hs=hs; self.ski=ski; self.ow=ow
        self._reset(); self._job=None

    def _reset(self):
        self.sc=0; self.lv=3; self.lvl=1
        self.ospd=H*.0078; self.sdel=1800
        self.obs=[]; self.coins=[]; self.pups=[]; self.canim=[]
        self.mob=None; self.rf=0; self.rt=0
        self.cl=1; self.tl=1
        self.px=float(LANES[1]-PW//2)
        self.lfl=0; self.efl=0; self.rc=0
        self.run_coins=0
        self.paused=False
        self.sty=0.0
        self.ball_angle=0.0          # rolling angle for ball skins
        self.iu=self.su=self.slu=self.rsu=0
        n=self._ms()
        self.ts=self.tc=self.tr=self.tp=self.tm=n
        self.ll=-1; self.lco=0
        self.stars=[(random.randint(0,W),random.randint(0,H)) for _ in range(60)]
        self.star_s=[random.uniform(.5,2) for _ in range(60)]
        self.star_b=[random.uniform(.5,1) for _ in range(60)]
        self.touch_x=self.touch_y=None
        self.CR=int(W*.026); self.PR=int(W*.033)

    def start(self):
        self._reset()
        if self._job: self._job.cancel()
        self._job=Clock.schedule_interval(self._upd,1/60)

    def stop(self):
        if self._job: self._job.cancel(); self._job=None

    def pause(self):
        if self.paused: return
        self.paused=True
        if self._job: self._job.cancel(); self._job=None

    def resume(self):
        if not self.paused: return
        self.paused=False
        if not self._job:
            self._job=Clock.schedule_interval(self._upd,1/60)

    # ── Touch ──────────────────────────
    def on_touch_down(self,t):
        if self.paused: return True
        self.touch_x=t.x; self.touch_y=t.y; return True

    def on_touch_up(self,t):
        if self.paused or self.touch_x is None: return True
        dx=t.x-self.touch_x; dy=t.y-self.touch_y
        if abs(dx)>abs(dy) and abs(dx)>W*.05:
            if dx<0 and self.tl>0:   self.tl-=1
            elif dx>0 and self.tl<2: self.tl+=1
        self.touch_x=self.touch_y=None; return True

    # ── Lane logic ─────────────────────
    def _pick_lane(self):
        if self.ll==-1: l=random.randint(0,2)
        elif self.lco>=2: l=random.choice([x for x in range(3) if x!=self.ll])
        elif random.random()<.6: l=random.choice([x for x in range(3) if x!=self.ll])
        else: l=self.ll
        self.lco=self.lco+1 if l==self.ll else 1
        self.ll=l; return l

    def _can_spawn(self):
        if len(self.obs)>=5: return False
        for o in self.obs:
            if o["y"]>H-H*.15: return False
        return True

    # ═══════════════════════════════════
    #   UPDATE  (game logic — unchanged)
    # ═══════════════════════════════════
    def _upd(self,dt):
        if self.paused: return
        n=self._ms()
        hs=n<self.su; hrs=n<self.rsu; hsl=n<self.slu; inv=n<self.iu
        spd=self.ospd*(.4 if hsl else 1)

        # Stars move downward
        for i in range(len(self.stars)):
            sx,sy=self.stars[i]; sy-=self.star_s[i]
            if sy<0: sy=H; sx=random.randint(0,W)
            self.stars[i]=(sx,sy)

        # FIX: sty decreases → stripes scroll top→bottom (correct direction)
        self.sty=(self.sty-spd*.6)%220

        # Ball rolling angle increases with speed
        self.ball_angle=(self.ball_angle+spd*3.0)%360

        # Move player toward target lane
        tx=float(LANES[self.tl]-PW//2); sl=W*.026
        if   self.px<tx: self.px=min(self.px+sl,tx)
        elif self.px>tx: self.px=max(self.px-sl,tx)

        # Animation frame
        self.rt+=1
        if self.rt>=4: self.rf+=1; self.rt=0

        # Spawn obstacles
        if n-self.ts>self.sdel:
            if self._can_spawn():
                lc=self._pick_lane(); ot=random.choice(OD)
                lx=LANES[lc]
                self.obs.append({"x":lx-ot["w"]//2,"y":H+ot["h"],"w":ot["w"],"h":ot["h"],"t":ot})
            self.ts=n
            if self.sdel>350: self.sdel=max(350,self.sdel-3)
            if self.ospd<H*.017: self.ospd+=H*.000017

        for o in self.obs: o["y"]-=spd
        self.obs=[o for o in self.obs if o["y"]>-o["h"]]

        # Moving obstacle
        if n-self.tm>8000:
            sd=random.choice([0,2])
            self.mob={"x":LANES[sd]-int(W*.06),"y":H*.67,
                      "w":int(W*.12),"h":int(H*.087),
                      "t":OD[0],"d":1 if sd==0 else -1}
            self.tm=n
        if self.mob:
            self.mob["x"]+=self.mob["d"]*int(W*.011)
            cx2=self.mob["x"]+self.mob["w"]//2
            if cx2>LANES[2]+int(W*.074) or cx2<LANES[0]-int(W*.074):
                self.mob["d"]*=-1
            self.mob["y"]-=spd
            if self.mob["y"]<-self.mob["h"]: self.mob=None

        # Coins
        if n-self.tc>1200:
            l=random.randint(0,2)
            self.coins.append({"x":LANES[l],"y":H+self.CR*2,"a":0,"k":"g"})
            self.tc=n
        if n-self.tr>4000:
            l=random.randint(0,2)
            self.coins.append({"x":LANES[l],"y":H+self.CR*2,"a":0,"k":"r"})
            self.tr=n
        for c in self.coins: c["y"]-=spd; c["a"]+=1
        self.coins=[c for c in self.coins if c["y"]>-self.CR*2]

        # Powerups
        if n-self.tp>7000:
            l=random.randint(0,2)
            self.pups.append({"x":LANES[l],"y":H+self.PR*2,"k":random.choice(["s","sl"])})
            self.tp=n
        for p in self.pups: p["y"]-=spd
        self.pups=[p for p in self.pups if p["y"]>-self.PR*2]

        # Collect
        pxi=int(self.px); pcx=pxi+PW//2; pcy=PY+PH//2
        for c in self.coins[:]:
            if math.hypot(pcx-c["x"],pcy-c["y"])<self.CR+W*.037:
                self.coins.remove(c)
                if c["k"]=="g":
                    self.ct+=1; self.sc+=50; self.run_coins+=1
                    if hasattr(self,'app') and self.app: self.app.play_sfx('coin')
                    self.canim.append({"x":c["x"],"y":c["y"],"al":255,"vy":0,"k":"g"})
                else:
                    self.rc+=1
                    if hasattr(self,'app') and self.app: self.app.play_sfx('red_coin')
                    self.canim.append({"x":c["x"],"y":c["y"],"al":255,"vy":0,"k":"r"})
                    if self.rc>=5:
                        self.rc=0
                        if self.lv<3: self.lv+=1
                        else: self.rsu=n+30000

        for p in self.pups[:]:
            if math.hypot(pcx-p["x"],pcy-p["y"])<self.PR+W*.037:
                self.pups.remove(p)
                if hasattr(self,'app') and self.app: self.app.play_sfx('powerup')
                if p["k"]=="s": self.su=n+15000
                else:           self.slu=n+1500

        # Recalc shields after collection
        hs=n<self.su; hrs=n<self.rsu; inv=n<self.iu

        # Collision
        if not hs and not hrs and not inv:
            all_o=self.obs+([self.mob] if self.mob else [])
            for o in all_o:
                inf=int(W*.019)
                if (pxi<o["x"]+o["w"]-inf and pxi+PW>o["x"]+inf and
                    PY <o["y"]+o["h"]-inf and PY+PH >o["y"]+inf):
                    self.lv-=1; self.iu=n+3000; self.efl=20
                    if hasattr(self,'app') and self.app: self.app.play_sfx('hit')
                    if self.lv<=0:
                        self.hs=max(self.hs,self.sc)
                        save(self.ct,self.hs,self.ski,self.ow)
                        if hasattr(self,'app') and self.app: self.app.play_sfx('gameover')
                        self.stop()
                        Clock.schedule_once(lambda dt:self.app.show_gameover(
                            self.sc,self.hs,self.ct,self.ski,self.ow),0)
                    break

        # Level
        nl=self.sc//2000+1
        if nl>self.lvl: self.lvl=nl; self.lfl=180
        if self.lfl>0: self.lfl-=1
        if self.efl>0: self.efl-=1
        self.sc+=1

        for ca in self.canim[:]:
            ca["vy"]+=.3; ca["y"]+=ca["vy"]*.2; ca["al"]-=6
            if ca["al"]<=0: self.canim.remove(ca)

        self._draw(n)

    # ═══════════════════════════════════
    #   DRAW
    # ═══════════════════════════════════
    def _draw(self,n):
        hs=n<self.su; hrs=n<self.rsu; hsl=n<self.slu; inv=n<self.iu
        self.canvas.clear()
        with self.canvas:
            # Background
            Color(*BG); Rectangle(pos=(0,0),size=(W,H))
            # Stars
            for i,(sx,sy) in enumerate(self.stars):
                b=self.star_b[i]; Color(b,b,b,1); Ellipse(pos=(sx-2,sy-2),size=(4,4))
            # Road
            rc=ROAD_COLORS[min(self.lvl-1,4)]
            Color(rc[0]/255,rc[1]/255,rc[2]/255,1); Rectangle(pos=(RX,0),size=(RW,H))
            # FIX: sty decreases each frame → stripes scroll downward ✓
            Color(*STRP)
            for li in(1,2):
                lx=int(RX+RW*li/3)
                y2=int(self.sty)
                while y2<H: Rectangle(pos=(lx-5,y2),size=(10,140)); y2+=220
                y2=int(self.sty)-220
                while y2>-140: Rectangle(pos=(lx-5,y2),size=(10,140)); y2-=220
            # Borders
            Color(*WHITE)
            Rectangle(pos=(RX-8,0),size=(8,H)); Rectangle(pos=(RX+RW,0),size=(8,H))
            # Game objects (obstacles orientation correct — no flip needed)
            for o in self.obs: self._do(o)
            if self.mob: self._do(self.mob)
            for c in self.coins: self._dco(c)
            for p in self.pups:  self._dpu(p)

            # FIX: Player — flip vertically (Kivy y=0 at bottom → sprites inverted)
            show=not(inv and (n//80)%2==0)
            if show:
                pcx=int(self.px)+PW//2; pcy=PY+PH//2
                PushMatrix()
                Translate(pcx,pcy,0); Scale(1,-1,1); Translate(-pcx,-pcy,0)
                self._dp(int(self.px),PY,self.rf,hs,hrs)
                PopMatrix()

            # Score box
            Color(0,0,0,1)
            RoundedRectangle(pos=(20,H-int(H*.043)),size=(int(W*.287),int(H*.035)),radius=[16])
            Color(*CYAN)
            Line(rounded_rectangle=(20,H-int(H*.043),int(W*.287),int(H*.035),16),width=3)

            # FIX: Lives hearts — flipped so they point downward (correct ♥ shape)
            for i in range(3):
                hc=HRED if i<self.lv else DGREY
                hx=30+i*int(W*.074); hy=H-int(H*.082)
                PushMatrix()
                Translate(hx+24,hy+25,0); Scale(1,-1,1); Translate(-(hx+24),-(hy+25),0)
                self._cr(hx+12,hy+10,18,hc)
                self._cr(hx+36,hy+10,18,hc)
                self._tr([(hx,hy+16),(hx+24,hy+50),(hx+48,hy+16)],hc)
                PopMatrix()

            # FIX: Red coin counter hearts — same flip
            for i in range(5):
                rc2=HRED if i<self.rc else DGREY
                rx=int(W*.15)+i*int(W*.043); ry=H-int(H*.104)
                PushMatrix()
                Translate(rx+15,ry+14,0); Scale(1,-1,1); Translate(-(rx+15),-(ry+14),0)
                self._cr(rx+8,ry+6,7,rc2)
                self._cr(rx+22,ry+6,7,rc2)
                self._tr([(rx+2,ry+10),(rx+15,ry+24),(rx+28,ry+10)],rc2)
                PopMatrix()

            # Shield bars
            bw=int(W*.278); bx=W-int(W*.306)
            if hs:
                rem=max(0,(self.su-n)/15000)
                self._rr(bx,H-int(H*.079),bw,22,DGREY,r=8)
                self._rr(bx,H-int(H*.079),int(bw*rem),22,SHLD,r=8)
            if hrs:
                rem=max(0,(self.rsu-n)/30000)
                self._rr(bx,H-int(H*.049),bw,22,DGREY,r=8)
                self._rr(bx,H-int(H*.049),int(bw*rem),22,RSHLD,r=8)
            if hsl:
                rem=max(0,(self.slu-n)/1500)
                self._rr(bx,H-int(H*.095),bw,22,DGREY,r=8)
                self._rr(bx,H-int(H*.095),int(bw*rem),22,SLOW,r=8)
            # Edge flash on hit
            if self.efl>0:
                a=min(.7,self.efl*.035); Color(.86,0,0,a)
                Rectangle(pos=(0,0),size=(30,H)); Rectangle(pos=(W-30,0),size=(30,H))
                Rectangle(pos=(0,0),size=(W,30)); Rectangle(pos=(0,H-30),size=(W,30))

        if hasattr(self,'app') and self.app:
            self.app.update_hud(self.sc,self.hs,self.ct,self.lvl,
                                hs,hrs,hsl,self.lfl,self.rc,self.canim)


# ═══════════════════════════════════════
#   HELPERS
# ═══════════════════════════════════════
def mk_btn(text,color,on_press,size_hint=(1,None),height=None,font_size=None):
    if height is None: height=int(H*.048)
    if font_size is None: font_size=int(H*.025)
    btn=Button(text=text,font_size=font_size,size_hint=size_hint,height=height,
               background_normal='',background_color=color,
               color=(0,0,0,1) if color[1]>.5 else (1,1,1,1),bold=True)
    btn.bind(on_press=on_press); return btn

def mk_lbl(text,font_size,color=(1,1,1,1),bold=True,halign='center'):
    return Label(text=text,font_size=font_size,color=color,bold=bold,halign=halign,
                 size_hint=(1,None),height=int(font_size*1.6))

def mk_lbl_outline(text,font_size,fg=(1,1,1,1)):
    """White text with thick black outline — high contrast on any background."""
    return Label(text=text,font_size=font_size,color=fg,
                 outline_color=(0,0,0,1),outline_width=3,
                 bold=True,halign='center',
                 size_hint=(1,None),height=int(font_size*1.6))


class SoundToggleButton(Button):
    def __init__(self, app_ref, **kw):
        super().__init__(**kw)
        self.app=app_ref
        self.text=""
        self.background_normal=''
        self.background_down=''
        self.background_color=(0,0,0,0)
        self.border=(0,0,0,0)
        self.bind(pos=self._redraw,size=self._redraw)
        self.bind(on_press=self._on_press)
        Clock.schedule_once(lambda dt:self._redraw(),0)

    def _on_press(self,*_):
        self.app.toggle_mute()
        self._redraw()

    def _redraw(self,*_):
        self.canvas.before.clear()
        self.canvas.after.clear()
        x,y=self.pos; w,h=self.size
        r=max(12,int(min(w,h)*.28))
        with self.canvas.before:
            Color(0,0,0,.55)
            RoundedRectangle(pos=(x,y),size=(w,h),radius=[r])
        with self.canvas.after:
            Color(1,1,1,1)
            bx=x+w*.2; by=y+h*.36; bw=w*.16; bh=h*.28
            Rectangle(pos=(bx,by),size=(bw,bh))
            Triangle(points=[bx+bw, y+h*.28, bx+bw, y+h*.72, x+w*.54, y+h*.5])
            if getattr(self.app,'sound_muted',False):
                Line(points=[x+w*.63,y+h*.33,x+w*.84,y+h*.67],width=2.8)
                Line(points=[x+w*.84,y+h*.33,x+w*.63,y+h*.67],width=2.8)
            else:
                Line(circle=(x+w*.63,y+h*.5,w*.09,-35,35),width=2.2)
                Line(circle=(x+w*.68,y+h*.5,w*.15,-35,35),width=2.2)


# ═══════════════════════════════════════
#   MENU PLAYER PREVIEW  (animated)
# ═══════════════════════════════════════
class MenuPlayerWidget(DrawMixin, Widget):
    """Draws the selected skin with running/rolling animation for the menu."""
    def __init__(self,ski,**kw):
        super().__init__(**kw)
        self.ski=ski; self.rf=0; self.rt=0
        self.su=self.rsu=0
        self.ball_angle=0.0
        self.PR=int(W*.033); self.CR=int(W*.026)
        self._job=None

    def start(self):
        if self._job: self._job.cancel()
        self._job=Clock.schedule_interval(self._tick,1/30)

    def stop(self):
        if self._job: self._job.cancel(); self._job=None

    def _tick(self,dt):
        self.rt+=1
        if self.rt>=4: self.rf+=1; self.rt=0
        self.ball_angle=(self.ball_angle+4.5)%360   # constant roll in menu
        px=int(self.center_x-PW//2)
        py=int(self.center_y-PH//2)
        pcx=px+PW//2; pcy=py+PH//2
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            Translate(pcx,pcy,0); Scale(1,-1,1); Translate(-pcx,-pcy,0)
            self._dp(px,py,self.rf,False,False)
            PopMatrix()


# ═══════════════════════════════════════
#   MENU SCREEN
# ═══════════════════════════════════════
class MenuScreen(Screen):
    def __init__(self,app_ref,**kw):
        super().__init__(**kw)
        self.app=app_ref
        self._pw=None
        self._build()

    def _build(self):
        if self._pw: self._pw.stop(); self._pw=None
        self.clear_widgets()
        layout=FloatLayout(size=(W,H))

        with layout.canvas.before:
            # Background + road (static in menu)
            Color(*BG); Rectangle(pos=(0,0),size=(W,H))
            Color(*ROAD); Rectangle(pos=(RX,0),size=(RW,H))
            Color(*STRP)
            for li in(1,2):
                lx=int(RX+RW*li/3)
                for y2 in range(0,int(H),220):
                    Rectangle(pos=(lx-5,y2),size=(10,140))
            Color(*WHITE)
            Rectangle(pos=(RX-8,0),size=(8,H))
            Rectangle(pos=(RX+RW,0),size=(8,H))
            # FIX: dark strip at bottom — replaces the old ugly white rectangle
            Color(0,0,0,.72)
            Rectangle(pos=(0,0),size=(W,int(H*.07)))

        # Title
        t1=mk_lbl("SUBWAY",int(H*.07),color=(*CYAN[:3],1)); t1.pos=(0,H*.82); layout.add_widget(t1)
        t2=mk_lbl("RUNNER",int(H*.07),color=(*YEL[:3],1));  t2.pos=(0,H*.74); layout.add_widget(t2)

        btn_w=int(W*.14); btn_h=int(H*.055)
        self.sound_btn=SoundToggleButton(
            self.app,
            size_hint=(None,None),
            size=(btn_w,btn_h),
            pos=(int(W*.03), H-btn_h-int(H*.02))
        )
        layout.add_widget(self.sound_btn)

        # Animated player preview
        ct,hs,ski,_,_,_=load()
        self._pw=MenuPlayerWidget(ski,size=(W,int(PH*1.8)),pos=(0,int(H*.06)))
        layout.add_widget(self._pw)
        self._pw.start()

        # Coins + Best  — positioned BELOW the player
        cl=mk_lbl(f"$ {ct}",int(H*.028),color=(*GOLD[:3],1)); cl.pos=(0,H*.38); layout.add_widget(cl)
        hl=mk_lbl(f"Best: {hs}",int(H*.024),color=(*YEL[:3],1)); hl.pos=(0,H*.34); layout.add_widget(hl)

        # PLAY button (position unchanged)
        pb=mk_btn("PLAY",(*GREEN[:3],1),lambda x:self.app.start_game(),
                  size_hint=(.6,None),height=int(H*.065),font_size=int(H*.032))
        pb.pos=(W*.2,H*.27); layout.add_widget(pb)

        # SHOP button (position unchanged)
        sb=mk_btn("SHOP",(*GOLD[:3],1),lambda x:self.app.go_shop(),
                  size_hint=(.6,None),height=int(H*.065),font_size=int(H*.032))
        sb.pos=(W*.2,H*.19); layout.add_widget(sb)

        # FIX: Version/Author — white text with black outline, no white rectangle
        vl=mk_lbl_outline("V2_4.0.3",int(H*.018)); vl.pos=(0,int(H*.037)); layout.add_widget(vl)
        al=mk_lbl_outline("BY: Abdelrahman Dakrory  (⁠^_^)",int(H*.018)); al.pos=(0,int(H*.010)); layout.add_widget(al)

        self.add_widget(layout)

    def on_pre_enter(self): self._build()

    def refresh_sound_button(self):
        if getattr(self,'sound_btn',None):
            self.sound_btn._redraw()

    def on_leave(self):
        if self._pw: self._pw.stop()


# ═══════════════════════════════════════
#   GAME SCREEN
# ═══════════════════════════════════════
class GameScreen(Screen):
    def __init__(self,app_ref,**kw):
        super().__init__(**kw)
        self.app=app_ref; self.gc=None
        self.layout=FloatLayout(size=(W,H))
        self.add_widget(self.layout)

        fs=int(H*.022)
        self.lbl_score=Label(font_size=fs,bold=True,color=(1,1,1,1),
                             pos=(125,H-int(H*.047)),size_hint=(None,None))
        self.lbl_best=Label(font_size=int(H*.018),bold=True,color=(*YEL[:3],1),
                            pos=(W-int(W*.25),H-int(H*.038)),size_hint=(None,None))
        self.lbl_lv=Label(font_size=int(H*.02),bold=True,color=(*CYAN[:3],1),
                          pos=(W//2-50,H-int(H*.038)),size_hint=(None,None))
        self.lbl_coins=Label(font_size=int(H*.018),bold=True,color=(*GOLD[:3],1),
                             pos=(W//2-50,H-int(H*.065)),size_hint=(None,None))
        self.lbl_shield=Label(font_size=int(H*.016),bold=True,color=(*SHLD[:3],1),
                              pos=(W-int(W*.31),H-int(H*.08)),size_hint=(None,None))
        self.lbl_lvflash=Label(font_size=int(H*.045),bold=True,color=(*YEL[:3],1),
                               pos=(W//2-100,H//2-50),size_hint=(None,None))
        self.lbl_red=Label(font_size=int(H*.016),bold=True,color=(*RCOIN[:3],1),
                           pos=(33,H-int(H*.104)-30),size_hint=(None,None))
        for lb in[self.lbl_score,self.lbl_best,self.lbl_lv,self.lbl_coins,
                  self.lbl_shield,self.lbl_lvflash,self.lbl_red]:
            self.layout.add_widget(lb)
        self.btn_pause=Button(text="II",font_size=int(H*.022),bold=True,
                              background_normal='',background_color=(.32,.32,.32,.92),
                              color=(1,1,1,1),size_hint=(None,None),
                              size=(int(W*.1),int(H*.038)),
                              pos=(W-int(W*.15),H-int(H*.15)))
        self.btn_pause.bind(on_press=self.pause_game)
        self.layout.add_widget(self.btn_pause)
        self.pause_overlay=None
        self.anim_lbls=[]

    def start(self,ski,ow,ct,hs):
        if self.pause_overlay and self.pause_overlay.parent:
            self.layout.remove_widget(self.pause_overlay)
        self.pause_overlay=None
        self.btn_pause.disabled=False
        self.btn_pause.opacity=1
        if self.gc:
            self.gc.stop(); self.layout.remove_widget(self.gc)
        self.gc=GameCanvas(self.app)
        self.gc.ski=ski; self.gc.ow=ow; self.gc.ct=ct; self.gc.hs=hs
        self.layout.add_widget(self.gc,index=len(self.layout.children))
        self.gc.start()

    def pause_game(self,*_):
        if not self.gc or self.gc.paused: return
        self.gc.pause()
        self.app.play_sfx('pause')
        self.btn_pause.disabled=True
        self.btn_pause.opacity=0
        if self.pause_overlay and self.pause_overlay.parent:
            self.layout.remove_widget(self.pause_overlay)
        self.pause_overlay=self._build_pause_overlay()
        self.layout.add_widget(self.pause_overlay)

    def resume_game(self,*_):
        if self.pause_overlay and self.pause_overlay.parent:
            self.layout.remove_widget(self.pause_overlay)
        self.pause_overlay=None
        self.btn_pause.disabled=False
        self.btn_pause.opacity=1
        if self.gc: self.gc.resume()
        self.app.play_sfx('button')

    def _build_pause_overlay(self):
        overlay=FloatLayout(size=(W,H))
        with overlay.canvas.before:
            Color(0,0,0,.7); Rectangle(pos=(0,0),size=(W,H))
            cw=int(W*.83); ch=int(H*.38); cx=(W-cw)//2; cy=(H-ch)//2
            Color(.08,.08,.16,.9); RoundedRectangle(pos=(cx,cy),size=(cw,ch),radius=[30])
            Color(*RED); Line(rounded_rectangle=(cx,cy,cw,ch,30),width=5)
        cw=int(W*.83); ch=int(H*.38); cx=(W-cw)//2; cy=(H-ch)//2
        title=mk_lbl("PAUSED",int(H*.055),color=(*RED[:3],1))
        title.pos=(0,cy+ch-int(H*.075)); overlay.add_widget(title)
        for i,(txt,col) in enumerate([
            (f"Coins Collected: {self.gc.run_coins}",(*GOLD[:3],1)),
            (f"Score: {self.gc.sc}",(1,1,1,1)),
        ]):
            lbl=mk_lbl(txt,int(H*.03),color=col)
            lbl.pos=(0,cy+ch-int(H*.14)-i*int(H*.042))
            overlay.add_widget(lbl)
        cont=mk_btn("Continue",(*GREEN[:3],1),self.resume_game,
                    size_hint=(.6,None),height=int(H*.055),font_size=int(H*.028))
        cont.pos=(W*.2,cy+int(H*.085)); overlay.add_widget(cont)
        menu=mk_btn("Main Menu",(.35,.35,.35,1),self.go_menu_from_pause,
                    size_hint=(.6,None),height=int(H*.044),font_size=int(H*.022))
        menu.pos=(W*.2,cy-int(H*-.02)); overlay.add_widget(menu)
        return overlay

    def go_menu_from_pause(self,*_):
        if self.gc:
            self.app.ct=self.gc.ct
            self.app.ski=self.gc.ski
            self.app.ow=self.gc.ow
            save(self.app.ct,self.app.hs,self.app.ski,self.app.ow)
        self.app.play_sfx('button')
        self.app.go_menu()

    def update_hud(self,sc,hs,ct,lvl,has_s,has_rs,has_sl,lfl,rc,canim):
        self.lbl_score.text=f"Score: {sc}"
        self.lbl_best.text=f"Best: {hs}"
        self.lbl_lv.text=f"Lv.{lvl}"
        self.lbl_coins.text=f"$ {ct}"
        self.lbl_red.text=f"Red: {rc}/5"
        if has_rs:   self.lbl_shield.text="RED SHIELD"
        elif has_s:  self.lbl_shield.text="SHIELD"
        elif has_sl: self.lbl_shield.text="SLOW"
        else:        self.lbl_shield.text=""
        if lfl>0:
            a=min(1.0,lfl/60)
            self.lbl_lvflash.text=f"LEVEL {lvl}!"; self.lbl_lvflash.color=(*YEL[:3],a)
        else:
            self.lbl_lvflash.text=""

    def on_leave(self):
        if self.pause_overlay and self.pause_overlay.parent:
            self.layout.remove_widget(self.pause_overlay)
        self.pause_overlay=None
        self.btn_pause.disabled=False
        self.btn_pause.opacity=1
        if self.gc: self.gc.stop()


# ═══════════════════════════════════════
#   GAME OVER SCREEN
# ═══════════════════════════════════════
class GameOverScreen(Screen):
    def __init__(self,app_ref,**kw):
        super().__init__(**kw)
        self.app=app_ref
        self.sc=0; self.hs=0; self.ct=0; self.ski=0; self.ow={0}

    def setup(self,sc,hs,ct,ski,ow):
        self.sc=sc; self.hs=hs; self.ct=ct; self.ski=ski; self.ow=ow
        self.clear_widgets()
        layout=FloatLayout(size=(W,H))
        with layout.canvas.before:
            Color(0,0,0,.7); Rectangle(pos=(0,0),size=(W,H))
            cw=int(W*.83); ch=int(H*.38); cx=(W-cw)//2; cy=(H-ch)//2
            Color(.08,.08,.16,.9); RoundedRectangle(pos=(cx,cy),size=(cw,ch),radius=[30])
            Color(*RED); Line(rounded_rectangle=(cx,cy,cw,ch,30),width=5)
        cw=int(W*.83); ch=int(H*.38); cx=(W-cw)//2; cy=(H-ch)//2
        go_lbl=mk_lbl("GAME OVER",int(H*.055),color=(*RED[:3],1))
        go_lbl.pos=(0,cy+ch-int(H*.075)); layout.add_widget(go_lbl)
        for i,(txt,col) in enumerate([
            (f"Score: {sc}",(1,1,1,1)),
            (f"Best:  {hs}",(*YEL[:3],1)),
            (f"Coins: {ct}",(*GOLD[:3],1)),
        ]):
            lbl=mk_lbl(txt,int(H*.03),color=col)
            lbl.pos=(0,cy+ch-int(H*.14)-i*int(H*.042))
            layout.add_widget(lbl)
        pa=mk_btn("Play Again",(*GREEN[:3],1),
                  lambda x:self.app.start_game(self.ski,self.ow,self.ct,self.hs),
                  size_hint=(.6,None),height=int(H*.055),font_size=int(H*.028))
        pa.pos=(W*.2,cy+int(H*.085)); layout.add_widget(pa)
        mm=mk_btn("Main Menu",(.35,.35,.35,1),
                  lambda x:self.app.go_menu(),
                  size_hint=(.6,None),height=int(H*.044),font_size=int(H*.022))
        mm.pos=(W*.2,cy-int(H*-.02)); layout.add_widget(mm)
        self.add_widget(layout)


# ═══════════════════════════════════════
#   SHOP SCREEN
# ═══════════════════════════════════════
_TYPE_LABEL = {"h":"Human","m":"Moto","c":"Car","b":"Ball"}

class ShopScreen(Screen):
    def __init__(self,app_ref,**kw):
        super().__init__(**kw)
        self.app=app_ref

    def build(self,ct,hs,ski,ow):
        self.ct=ct; self.hs=hs; self.ski=ski; self.ow=ow
        self.clear_widgets()
        root=FloatLayout(size=(W,H))
        with root.canvas.before:
            Color(.04,.04,.1,1); Rectangle(pos=(0,0),size=(W,H))

        hdr=mk_lbl("S H O P",int(H*.032),color=(*GOLD[:3],1))
        hdr.pos=(0,H-int(H*.065)); root.add_widget(hdr)
        coins_lbl=mk_lbl(f"$ {ct}",int(H*.024),color=(*GOLD[:3],1))
        coins_lbl.pos=(0,H-int(H*.095)); root.add_widget(coins_lbl)
        with root.canvas.after:
            Color(*GREY); Line(points=[80,H-int(H*.1),W-80,H-int(H*.1)],width=2)

        # FIX: scroll_y=1 → starts at top (first skins visible immediately)
        sv=ScrollView(size=(W,H-int(H*.115)-int(H*.065)),
                      pos=(0,int(H*.065)),
                      do_scroll_x=False,do_scroll_y=True)
        box=GridLayout(cols=1,spacing=10,padding=[10,420,10,10],
size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        for i,sk in enumerate(SK):
            box.add_widget(self._mk_card(i,sk,ct,ski,ow))
        sv.add_widget(box)
        sv.scroll_y=1.2 # FIX: show first skins, not last
        root.add_widget(sv)

        back=mk_btn("Back",(.63,.12,.12,1),lambda x:self.app.go_menu(),
                    size_hint=(.5,None),height=int(H*.055),font_size=int(H*.028))
        back.pos=(W*.25,5); root.add_widget(back)
        self.add_widget(root)

    def _mk_card(self,i,sk,ct,ski,ow):
        is_cur=(i==ski); is_owned=(i in ow); can_buy=(ct>=sk["p"]) and not is_owned
        if is_cur:     bg=(.07,.24,.07,1); bd=(*GREEN[:3],1)
        elif is_owned: bg=(.06,.07,.2, 1); bd=(*CYAN[:3],1)
        else:          bg=(.07,.07,.15,1); bd=(*GREY[:3],1)

        card_h=int(H*.115)
        # FIX: RelativeLayout → child positions relative to card (scroll-safe)
        card=RelativeLayout(size_hint=(1,None),height=card_h)

        pr=int(card_h*.36); px2=int(card_h*.06); py2=card_h//2-pr
        prev_col=sk.get("b",(128,128,128))

        with card.canvas.before:
            Color(*bg)
            RoundedRectangle(pos=(5,2),size=(W-30,card_h-4),radius=[60])
            Color(*bd)
            Line(rounded_rectangle=(5,2,W-30,card_h-4,60),width=3)
            # Skin colour swatch
            Color(prev_col[0]/255,prev_col[1]/255,prev_col[2]/255,1)
            Ellipse(pos=(px2,py2),size=(pr*2,pr*2))
            Color(1,1,1,.22)
            Ellipse(pos=(px2+pr//2,py2+pr),size=(pr//2,pr//2))

        lx=int(W*.22)

        # Type badge
        card.add_widget(Label(
            text=_TYPE_LABEL.get(sk["t"],""),
            font_size=int(H*.020),color=(*bd[:3],.9),bold=True,halign='left',
            pos=(lx,card_h-int(H*.032)),size_hint=(None,None),size=(int(W*.2),int(H*.022))
        ))
        # Name
        card.add_widget(Label(
            text=sk["n"],font_size=int(H*.022),bold=True,
            color=(1,1,1,1),halign='left',
            pos=(lx,card_h//2+8),size_hint=(None,None),size=(int(W*.4),40)
        ))

        if is_cur:
            card.add_widget(Label(
                text="Used",font_size=int(H*.018),color=(*GREEN[:3],1),halign='left',
                pos=(lx,card_h//3-22),size_hint=(None,None),size=(int(W*.3),30)
            ))
        elif is_owned:
            eq=Button(text="Equip",font_size=int(H*.018),bold=True,
                      background_normal='',background_color=(*CYAN[:3],1),
                      color=(0,0,0,1),pos=(lx,8),
                      size_hint=(None,None),size=(int(W*.2),int(H*.04)))
            eq.bind(on_press=lambda x,idx=i:self.app.equip_skin(idx))
            card.add_widget(eq)
        else:
            card.add_widget(Label(
                text=f"$ {sk['p']}",font_size=int(H*.02),color=(*GOLD[:3],1),halign='left',
                pos=(lx,card_h//2.5-22),size_hint=(None,None),size=(int(W*.25),30)
            ))
            buy=Button(text="Buy",font_size=int(H*.018),bold=True,
                       background_normal='',
                       background_color=(*GREEN[:3],1) if can_buy else (*DGREY[:3],1),
                       color=(0,0,0,1) if can_buy else (.5,.5,.5,1),
                       pos=(lx+int(W*.21),8),
                       size_hint=(None,None),size=(int(W*.18),int(H*.04)))
            if can_buy:
                buy.bind(on_press=lambda x,idx=i:self.app.buy_skin(idx))
            card.add_widget(buy)
        return card

    def on_pre_enter(self):
        ct,hs,ski,ow,_,_=load()
        self.build(ct,hs,ski,ow)


# ═══════════════════════════════════════
#   MAIN APP
# ═══════════════════════════════════════
class SubwayRunnerApp(App):
    def build(self):
        Window.clearcolor=(0,0,0,1)
        self.ct,self.hs,self.ski,self.ow,self.master_volume,self.sound_muted=load()
        self.master_volume=max(0.0,min(1.5,self.master_volume))
        self.base_sfx_volumes={
            "button":.55,
            "pause":.55,
            "coin":.55,
            "red_coin":.15,
            "powerup":.55,
            "hit":.55,
            "gameover":.5,
        }
        self.sfx={}
        for name,path in ensure_sfx().items():
            self.sfx[name]=SoundLoader.load(path)
        self._apply_sound_settings()
        self.sm=ScreenManager(transition=NoTransition())

        self.menu_scr=MenuScreen(self,name='menu')
        self.game_scr=GameScreen(self,name='game')
        self.go_scr  =GameOverScreen(self,name='gameover')
        self.shop_scr=ShopScreen(self,name='shop')

        self.sm.add_widget(self.menu_scr)
        self.sm.add_widget(self.game_scr)
        self.sm.add_widget(self.go_scr)
        self.sm.add_widget(self.shop_scr)

        self.sm.current='menu'
        return self.sm

    def _apply_sound_settings(self):
        mult=0.0 if self.sound_muted else self.master_volume
        for name,snd in getattr(self,'sfx',{}).items():
            if snd:
                snd.volume=max(0.0,min(1.0,self.base_sfx_volumes.get(name,.75)*mult))

    def set_master_volume(self,value):
        self.master_volume=max(0.0,min(1.5,float(value)))
        self.sound_muted=(self.master_volume<=0)
        self._apply_sound_settings()
        save(self.ct,self.hs,self.ski,self.ow,self.master_volume,self.sound_muted)
        if hasattr(self,'menu_scr') and self.menu_scr:
            self.menu_scr.refresh_sound_button()

    def change_volume(self,delta):
        self.set_master_volume(self.master_volume+delta)

    def toggle_mute(self):
        self.sound_muted=not self.sound_muted
        self._apply_sound_settings()
        save(self.ct,self.hs,self.ski,self.ow,self.master_volume,self.sound_muted)
        if hasattr(self,'menu_scr') and self.menu_scr:
            self.menu_scr.refresh_sound_button()
        if not self.sound_muted:
            self.play_sfx('button')

    def play_sfx(self,name):
        snd=getattr(self,'sfx',{}).get(name)
        if not snd: return
        try:
            snd.stop()
            snd.play()
        except:
            pass

    def start_game(self,ski=None,ow=None,ct=None,hs=None):
        self.play_sfx('button')
        if ski is None: ski=self.ski
        if ow  is None: ow=self.ow
        if ct  is None: ct=self.ct
        if hs  is None: hs=self.hs
        self.ski=ski; self.ow=ow; self.ct=ct; self.hs=hs
        self.game_scr.start(ski,ow,ct,hs)
        self.sm.current='game'

    def show_gameover(self,sc,hs,ct,ski,ow):
        self.ct=ct; self.hs=hs; self.ski=ski; self.ow=ow
        self.go_scr.setup(sc,hs,ct,ski,ow)
        self.sm.current='gameover'

    def go_menu(self):
        if self.sm.current=='game' and self.game_scr.gc:
            gc=self.game_scr.gc
            self.ct=gc.ct
            self.ski=gc.ski
            self.ow=gc.ow
            save(self.ct,self.hs,self.ski,self.ow)
            gc.stop()
        self.sm.current='menu'

    def go_shop(self): self.sm.current='shop'

    def equip_skin(self,idx):
        self.ski=idx
        save(self.ct,self.hs,self.ski,self.ow)
        self.shop_scr.build(self.ct,self.hs,self.ski,self.ow)

    def buy_skin(self,idx):
        price=SK[idx]["p"]
        if self.ct>=price:
            self.ct-=price
            self.ow.add(idx)
            self.ski=idx
            save(self.ct,self.hs,self.ski,self.ow)
            self.shop_scr.build(self.ct,self.hs,self.ski,self.ow)

    def update_hud(self,sc,hs,ct,lvl,has_s,has_rs,has_sl,lfl,rc,canim):
        self.ct=ct; self.hs=hs
        if self.sm.current=='game':
            self.game_scr.update_hud(sc,hs,ct,lvl,has_s,has_rs,has_sl,lfl,rc,canim)


if __name__=='__main__':
    SubwayRunnerApp().run()
