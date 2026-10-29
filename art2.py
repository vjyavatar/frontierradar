"""Topic-specific, per-item SVG illustrations (FrontierRadar v10). Pure Python, no deps."""
import random,math,re,html
PALS={"Chips":["#2ecc71","#4da3ff","#0a1f1a"],"Medical/Biotech":["#ff6b8b","#ffd166","#2a0d16"],"Neuro/BCI":["#c77dff","#4cc9f0","#1a0d2a"],
"Superintelligence/AI":["#00e5ff","#7c4dff","#071a2a"],"Quantum":["#b07cff","#00f5d4","#120a2a"],"Materials/Energy":["#ffb703","#fb5607","#2a1a05"],
"DNA data storage":["#06d6a0","#118ab2","#04201c"],"Space/Rockets":["#ff8c42","#a0c4ff","#0a0f24"]}
LADDERS={"Chips":["Paper","Prototype","Factories & orders","Revenue"],
"Medical/Biotech":["Preclinical","Early trial (Ph 1/2)","Late trial (Ph 3)","Approved"],
"Neuro/BCI":["Lab study","Pilot / feasibility","Pivotal trial","Approved device"],
"Superintelligence/AI":["Research","Preview","Shipping","Widely adopted"],
"Quantum":["Lab physics","Hardware demo","Cloud access / customers","Commercial advantage"],
"Materials/Energy":["Lab cell","Pilot cell","Pilot line","Mass production"],
"DNA data storage":["Lab proof","Prototype system","Pilot archives","Commercial service"],
"Space/Rockets":["Design","Testing","Flight","Operations"]}
def stage_name(topic,n): return LADDERS.get(topic,LADDERS["Chips"])[n-1]
def key_number(t):
    m=re.findall(r'\d[\d.,]*\s?(?:×|%|ms|nm|qubits|hours|patients|PB|mW|mAh)|\d[\d.,]*×',t)
    return m[0].strip() if m else ""
def _bg(o,r,w,h,a,b,c):
    o.append(f'<defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
      f'<radialGradient id="bg" cx="{r.uniform(.15,.85):.2f}" cy="{r.uniform(.1,.6):.2f}" r="1"><stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="#05080e"/></radialGradient>'
      f'<filter id="f"><feGaussianBlur stdDeviation="3"/></filter></defs><rect width="{w}" height="{h}" fill="url(#bg)"/>')
    for _ in range(30): o.append(f'<circle cx="{r.random()*w:.0f}" cy="{r.random()*h:.0f}" r="{r.random()*1.3:.1f}" fill="#cfd8e6" opacity=".35"/>')
def chip_extra(o,r,cx,cy,s,a,b,area,w,h):
    A=area.lower()
    if "photon" in A or "optic" in A or "light" in A:
        for i in range(8):
            y=cy-s+i*s/3.5;o.append(f'<path d="M0 {y+r.uniform(-50,50):.0f} C {cx*.5:.0f} {y:.0f}, {cx*.8:.0f} {cy:.0f}, {cx-s:.0f} {cy-s*.7+i*s*.2:.0f}" stroke="url(#g)" stroke-width="2" fill="none" opacity=".8"/>')
        for i in range(5):o.append(f'<path d="M{cx+s:.0f} {cy-s*.6+i*s*.3:.0f} L{w} {cy-s*1.4+i*s*.7:.0f}" stroke="{b}" stroke-width="2.5" opacity=".7"/>')
    elif "memory" in A or "analog" in A:
        for i in range(r.randint(3,6)):o.append(f'<rect x="{cx+s*1.4:.0f}" y="{cy+s*.8-i*s*.35:.0f}" width="{s*1.2:.0f}" height="{s*.28:.0f}" rx="4" fill="{[a,b][i%2]}" opacity=".75"/>')
        o.append(f'<path d="M{cx+s:.0f} {cy:.0f} H{cx+s*1.4:.0f}" stroke="#fff" stroke-width="3"/>')
    elif "neuro" in A or "spik" in A:
        y0=h*.85;o.append('<polyline points="'+" ".join(f"{i*12},{y0-(r.random()>.85)*40:.0f}" for i in range(w//12+1))+f'" stroke="{b}" fill="none" stroke-width="2"/>')
        for i in range(10):o.append(f'<circle cx="{r.uniform(20,w-20):.0f}" cy="{r.uniform(20,h*.7):.0f}" r="{r.uniform(3,7):.0f}" fill="{a}" filter="url(#f)"/>')
    elif "transistor" in A or "material" in A or "2d" in A:
        for i in range(9):
            for j in range(5):o.append(f'<circle cx="{40+i*28+(j%2)*14}" cy="{60+j*28}" r="6" fill="{[a,b][(i+j)%2]}" opacity=".55"/>')
    else:
        for i in range(r.randint(2,4)):o.append(f'<rect x="{cx-s*1.3+i*12:.0f}" y="{cy+s*1.3-i*14:.0f}" width="{s*2.6:.0f}" height="10" rx="3" fill="{[a,b][i%2]}" opacity=".6"/>')
def m_chip(o,r,cx,cy,s,a,b):
    o.append(f'<rect x="{cx-s}" y="{cy-s}" width="{2*s}" height="{2*s}" rx="{s/5:.0f}" fill="#0c1422" stroke="url(#g)" stroke-width="3"/>')
    n=r.randint(5,8)
    for i in range(n):
        p=-s+(i+.5)*2*s/n;o.append(f'<path d="M{cx+p:.0f} {cy-s}v-14M{cx+p:.0f} {cy+s}v14M{cx-s} {cy+p:.0f}h-14M{cx+s} {cy+p:.0f}h14" stroke="{a}" stroke-width="3" opacity=".7"/>')
    k=r.randint(2,5)
    for i in range(k):
        for j in range(k):o.append(f'<rect x="{cx-s+12+i*(2*s-24)/k:.0f}" y="{cy-s+12+j*(2*s-24)/k:.0f}" width="{(2*s-24)/k-5:.0f}" height="{(2*s-24)/k-5:.0f}" rx="3" fill="{a if r.random()>.5 else b}" opacity="{r.uniform(.25,.9):.2f}"/>')
def m_dna(o,r,cx,cy,s,a,b):
    L=s*3.2;turns=r.uniform(1.5,3);ang=r.uniform(-.5,.5)
    o.append(f'<g transform="rotate({math.degrees(ang):.0f} {cx} {cy})">')
    for k in range(60):
        t=k/59;x=cx-L/2+t*L;ph=t*turns*2*math.pi
        y1=cy+math.sin(ph)*s*.6;y2=cy-math.sin(ph)*s*.6
        if k%3==0:o.append(f'<line x1="{x:.0f}" y1="{y1:.0f}" x2="{x:.0f}" y2="{y2:.0f}" stroke="{[a,b,"#ffd166","#ef476f"][k//3%4]}" stroke-width="3" opacity=".75"/>')
        o.append(f'<circle cx="{x:.0f}" cy="{y1:.0f}" r="4" fill="{a}"/><circle cx="{x:.0f}" cy="{y2:.0f}" r="4" fill="{b}"/>')
    o.append('</g>')
    for i in range(r.randint(4,9)):o.append(f'<text x="{r.uniform(20,600):.0f}" y="{r.uniform(30,200):.0f}" font-family="DejaVu Sans Mono" font-size="14" fill="{a}" opacity=".35">{"".join(r.choice("01") for _ in range(8))}</text>')
def m_qubit(o,r,cx,cy,s,a,b):
    n=r.randint(3,7)
    for i in range(n):
        x=cx+(i-(n-1)/2)*s*.8;y=cy+r.uniform(-s*.4,s*.4)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s*.32:.0f}" fill="none" stroke="url(#g)" stroke-width="2"/><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s*.32:.0f}" ry="{s*.1:.0f}" fill="none" stroke="{b}" opacity=".6"/>')
        th=r.uniform(0,2*math.pi);o.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.cos(th)*s*.3:.0f}" y2="{y+math.sin(th)*s*.3:.0f}" stroke="#fff" stroke-width="3"/><circle cx="{x+math.cos(th)*s*.3:.0f}" cy="{y+math.sin(th)*s*.3:.0f}" r="5" fill="{a}" filter="url(#f)"/>')
        if i:o.append(f'<path d="M{x-s*.8+s*.32:.0f} {cy} q {s*.08:.0f} -20 {s*.16:.0f} 0" stroke="{a}" fill="none" stroke-dasharray="4 4"/>')
def m_cell(o,r,cx,cy,s,a,b):
    for i in range(r.randint(5,9)):
        x=cx+r.uniform(-s*1.8,s*1.8);y=cy+r.uniform(-s*.7,s*.7);rr=r.uniform(s*.25,s*.55)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{rr*r.uniform(.7,1):.0f}" fill="{a}" opacity=".18" stroke="{a}" stroke-width="2"/><circle cx="{x+r.uniform(-5,5):.0f}" cy="{y:.0f}" r="{rr*.3:.0f}" fill="{b}" opacity=".8"/>')
    o.append(f'<path d="M{cx-s*2} {cy+s*.9} h{s*.8} l15 -40 l20 70 l15 -30 h{s*2.5}" stroke="{b}" stroke-width="3" fill="none" filter="url(#f)"/><path d="M{cx-s*2} {cy+s*.9} h{s*.8} l15 -40 l20 70 l15 -30 h{s*2.5}" stroke="#fff" stroke-width="1.2" fill="none"/>')
def m_brain(o,r,cx,cy,s,a,b):
    o.append(f'<path d="M{cx-s} {cy} C{cx-s} {cy-s},{cx-s*.2} {cy-s*1.1},{cx} {cy-s*.8} C{cx+s*.3} {cy-s*1.1},{cx+s*1.1} {cy-s*.9},{cx+s} {cy} C{cx+s*1.1} {cy+s*.7},{cx+s*.2} {cy+s*.9},{cx} {cy+s*.6} C{cx-s*.4} {cy+s*.9},{cx-s*1.1} {cy+s*.6},{cx-s} {cy}Z" fill="{a}" fill-opacity=".12" stroke="url(#g)" stroke-width="3"/>')
    for i in range(r.randint(4,7)):
        x=cx+r.uniform(-s*.8,s*.8);y=cy+r.uniform(-s*.6,s*.5);o.append(f'<path d="M{x:.0f} {y:.0f} q {r.uniform(-30,30):.0f} {r.uniform(-30,30):.0f} {r.uniform(-50,50):.0f} {r.uniform(-20,20):.0f}" stroke="{a}" fill="none" stroke-width="2" opacity=".6"/>')
    for i in range(r.randint(6,12)):
        x=cx+r.uniform(-s*.8,s*.8);y=cy+r.uniform(-s*.6,s*.5);o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{b}" filter="url(#f)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="2" fill="#fff"/>')
    y0=cy+s*1.05;o.append('<polyline points="'+" ".join(f"{cx-s*2+i*8:.0f},{y0+r.uniform(-12,12):.0f}" for i in range(int(s*4/8)))+f'" stroke="{b}" fill="none" stroke-width="2" opacity=".8"/>')
def m_net(o,r,cx,cy,s,a,b):
    L=[r.randint(3,5),r.randint(4,7),r.randint(4,7),r.randint(2,4)];P=[]
    for li,n in enumerate(L):
        x=cx-s*1.6+li*s*3.2/(len(L)-1);P.append([(x,cy+(j-(n-1)/2)*s*1.5/max(n-1,1)) for j in range(n)])
    for l1,l2 in zip(P,P[1:]):
        for p in l1:
            for q in l2:
                if r.random()>.3:o.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="url(#g)" stroke-width="1.2" opacity="{r.uniform(.2,.8):.2f}"/>')
    for l in P:
        for x,y in l:o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="#0c1422" stroke="{a}" stroke-width="2.5"/><circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="{b if r.random()>.5 else a}"/>')
def m_energy(o,r,cx,cy,s,a,b):
    if r.random()>.5:
        for i in range(r.randint(2,4)):
            x=cx-s*1.5+i*s*1.05;h=s*1.6;lvl=r.uniform(.3,1)
            o.append(f'<rect x="{x:.0f}" y="{cy-h/2:.0f}" width="{s*.7:.0f}" height="{h:.0f}" rx="10" fill="#0c1422" stroke="url(#g)" stroke-width="3"/><rect x="{x+s*.25:.0f}" y="{cy-h/2-10:.0f}" width="{s*.2:.0f}" height="10" fill="{a}"/><rect x="{x+6:.0f}" y="{cy+h/2-6-(h-12)*lvl:.0f}" width="{s*.7-12:.0f}" height="{(h-12)*lvl:.0f}" rx="6" fill="{a if lvl>.5 else b}" opacity=".8"/>')
    else:
        for i in range(4):
            for j in range(3):o.append(f'<polygon points="{cx-s*1.6+i*s*.8:.0f},{cy-s*.2+j*s*.45:.0f} {cx-s*1.0+i*s*.8:.0f},{cy-s*.2+j*s*.45:.0f} {cx-s*1.2+i*s*.8:.0f},{cy+s*.2+j*s*.45:.0f} {cx-s*1.8+i*s*.8:.0f},{cy+s*.2+j*s*.45:.0f}" fill="{b}" opacity="{r.uniform(.3,.8):.2f}" stroke="{a}"/>')
        o.append(f'<circle cx="{cx+s*1.4:.0f}" cy="{cy-s*.8:.0f}" r="{s*.35:.0f}" fill="{a}" filter="url(#f)"/>')
    o.append(f'<path d="M{cx+s*.1:.0f} {cy-s*1.1:.0f} l-30 55 h28 l-18 50 l50 -70 h-28 l18 -35z" fill="#fff" opacity=".9"/>')
def m_rocket(o,r,cx,cy,s,a,b):
    ang=r.uniform(-35,35);x=cx+r.uniform(-s,s)
    o.append(f'<path d="M{cx-s*2:.0f} {cy+s*1.2:.0f} Q {cx:.0f} {cy-s*1.6:.0f} {cx+s*2.2:.0f} {cy+s*1.1:.0f}" stroke="{b}" stroke-dasharray="6 8" fill="none" opacity=".5"/>')
    o.append(f'<circle cx="{cx+r.choice([-1,1])*s*1.7:.0f}" cy="{cy+s*1.4:.0f}" r="{s*.9:.0f}" fill="{b}" opacity=".2"/>')
    o.append(f'<g transform="rotate({ang:.0f} {x:.0f} {cy:.0f})"><path d="M{x:.0f} {cy-s:.0f} c 22 25 26 60 22 {s*1.4:.0f} h-44 c-4 -{s*1.4-60:.0f} 0 -{s*1.4-25:.0f} 22 -{s*1.4:.0f}z" fill="#e8eef7"/><circle cx="{x:.0f}" cy="{cy-s*.35:.0f}" r="9" fill="{b}"/><path d="M{x-22:.0f} {cy+s*.25:.0f} l-18 30 h18zM{x+22:.0f} {cy+s*.25:.0f} l18 30 h-18z" fill="{a}"/><path d="M{x-14:.0f} {cy+s*.45:.0f} q 14 {s*.9:.0f} 28 0z" fill="{a}" filter="url(#f)"/><path d="M{x-7:.0f} {cy+s*.45:.0f} q 7 {s*.5:.0f} 14 0z" fill="#fff"/></g>')
MOT={"Chips":m_chip,"Medical/Biotech":m_cell,"Neuro/BCI":m_brain,"Superintelligence/AI":m_net,"Quantum":m_qubit,"Materials/Energy":m_energy,"DNA data storage":m_dna,"Space/Rockets":m_rocket}
ICON={"Chips":"CHIPS","Medical/Biotech":"BIOTECH","Neuro/BCI":"NEURO / BCI","Superintelligence/AI":"FRONTIER AI","Quantum":"QUANTUM","Materials/Energy":"ENERGY","DNA data storage":"DNA STORAGE","Space/Rockets":"SPACE"}
def topic_art(it,w=640,h=300,title=True):
    t=it.get("topic","Chips");a,b,c=PALS.get(t,PALS["Chips"]);r=random.Random(it["id"])
    if r.random()>.5:a,b=b,a
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'];_bg(o,r,w,h,a,b,c)
    s=min(w,h)*r.uniform(.2,.27);cx=w*r.choice([.36,.5,.64]);cy=h*.45
    if t=="Chips":
        a,b=r.choice([("#2ecc71","#4da3ff"),("#4da3ff","#f5c542"),("#b07cff","#2ecc71"),("#f5c542","#ff5c5c"),("#00e5ff","#b07cff")]);s*=r.uniform(.7,1);cx=w*r.choice([.3,.5,.7])
        chip_extra(o,r,cx,cy,s,a,b,it.get("area",""),w,h)
    if t=="Quantum": s*=1.5
    MOT.get(t,m_chip)(o,r,cx,cy,s,a,b)
    o.append(f'<rect x="14" y="14" rx="11" width="{len(ICON.get(t,t))*9+26}" height="24" fill="{a}"/><text x="27" y="31" font-family="DejaVu Sans" font-weight="bold" font-size="13" fill="#05080e">{ICON.get(t,t)}</text>')
    k=key_number(it.get("title",""))
    if k: o.append(f'<rect x="{w-len(k)*15-34}" y="12" rx="14" width="{len(k)*15+20}" height="38" fill="#05080ecc" stroke="{b}" stroke-width="2"/><text x="{w-24}" y="39" text-anchor="end" font-family="DejaVu Sans" font-weight="bold" font-size="22" fill="{b}">{html.escape(k)}</text>')
    if title:
        tt=it.get("title","");tt=tt if len(tt)<=68 else tt[:66].rsplit(" ",1)[0]+"…"
        o.append(f'<rect x="0" y="{h-40}" width="{w}" height="40" fill="#05080ecc"/><text x="16" y="{h-15}" font-family="DejaVu Sans" font-size="15" fill="#e8eef7">{html.escape(tt)}</text>')
    o.append('</svg>');return "".join(o)
