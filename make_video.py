#!/usr/bin/env python3
"""Zero-cost explainer video for one FrontierRadar research item.
Usage: python3 make_video.py data/2026-10-29.json <item-id> [--voice en-US-AriaNeural]
Script: videos/<id>.script.json = {"hook":..., "sections":[[label,text],...]} (else auto-built from item fields).
Captions show the text as written; TTS gets PRON phonetic replacements.
Tools (all free): edge-tts -> Piper (local) -> espeak-ng, cairosvg, Pillow, ffmpeg (loudnorm -16 LUFS).
Layout respects Instagram Reels/Shorts safe zones (top 220px, bottom 380px, right 140px kept clear)."""
import json,sys,os,re,subprocess,asyncio,tempfile
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import cairosvg
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from art2 import stage_name
W,H,FPS=1080,1920,30
ROOT=os.path.dirname(os.path.abspath(__file__))
F="/usr/share/fonts/truetype/dejavu/DejaVuSans"
GREEN,RED,BG,TX,MUT=(46,204,113),(255,92,92),(8,14,24),(235,242,250),(160,175,195)
SEC_COL={"Hook":(176,124,255),"What it is":(77,163,255),"What it does":GREEN,"Before":RED,"After":GREEN,"Why it matters":(245,197,66),"Next":GREEN}
STAGES={1:"Paper",2:"Prototype",3:"Factories & orders",4:"Revenue"}
PRON={"PsiQuantum":"Sigh-Quantum","HBM4":"H B M 4","DuoPD":"Duo P D","GPU":"G P U","FPGAs":"F P G As","FPGA":"F P G A",
 "Agilex":"Adjilex","Altera":"Al-tera","Ceva":"Seeva","NeuPro":"New Pro","SK hynix":"S K Hi-nix","Q2 2027":"the second quarter of 2027",
 "dB":"decibels","1.6 nanometres":"one point six nanometres","research.celesys.ai":"research dot celesys dot A I","celesys":"cel-ee-sis"}
X0,XW=60,880  # text column inside safe zone
def spoken(t):
    for k in sorted(PRON,key=len,reverse=True): t=re.sub(r'(?<![\w-])'+re.escape(k)+r'(?![\w])',PRON[k],t)
    return t
def auto_script(it):
    s1=lambda t:re.split(r'(?<=[.!?])\s+',t.strip())[0]
    clean=lambda t:re.sub(r'\s*\([^)]*\)','',t)
    win=[clean(w) for w in it.get("win",[])[:2]]
    bear=clean(it["bear"][0][0]) if it.get("bear") else ""
    plan=it.get("plan","Watch")
    return {"hook":s1(it.get("eli10","")) if it.get("eli10") else it["title"],"sections":[
      ["What it is",clean(it["title"])+"."],
      ["What it does",s1(it["found"])+" Think of it like this: "+it["analogy"]],
      ["Before",s1(it.get("brief",""))],
      ["After","Who could benefit: "+" and ".join(win)+"."],
      ["Why it matters",f"We rate it Stage {it['stage']}, {stage_name(it.get('topic','Chips'),it['stage'])}, readiness {it['ready']} out of 100. The catch: {bear.rstrip('.')}. Our judgment: {plan.lower()}. Not financial advice."]]}
def sentences(t):
    out=[]
    for x in re.split(r'(?<=[.!?])\s+',t.strip()):
        if out and (len(x)<28 or x.startswith("Not financial")): out[-1]+=" "+x
        elif x: out.append(x)
    return out
USED=[];PIPER=os.path.expanduser("~/piper/en_US-lessac-medium.onnx")
def tts(text,out,voice):
    try:
        import edge_tts
        asyncio.run(edge_tts.Communicate(text,voice,rate="+4%").save(out));USED.append("edge-tts "+voice);return
    except Exception: pass
    w=out+".wav"
    try:
        subprocess.run([sys.executable,"-m","piper","-m",PIPER,"-f",w,"--length-scale","0.93","--sentence-silence","0.1"],input=text.encode(),check=True,capture_output=True);USED.append("Piper en_US-lessac-medium (local)")
    except Exception:
        subprocess.run(["espeak-ng","-w",w,text],check=True);USED.append("espeak-ng")
    subprocess.run(["ffmpeg","-y","-v","error","-i",w,"-af","silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse",out],check=True)
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
def wrap(d,text,font,maxw):
    out=[];line=""
    for w in text.split():
        t=(line+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: line=t
        else: out.append(line);line=w
    out.append(line);return out
fb=lambda n:ImageFont.truetype(F+"-Bold.ttf",n);fr=lambda n:ImageFont.truetype(F+".ttf",n)
def slide(art,sec,text,idx,total,it,path):
    g=Image.new("RGB",(W,H),BG);gd=ImageDraw.Draw(g)
    gd.ellipse((-300,200,700,1100),fill=(10,60,40));gd.ellipse((500,1100,1500,2100),fill=(60,15,25))
    im=g.filter(ImageFilter.GaussianBlur(160));d=ImageDraw.Draw(im)
    d.text((X0,230),"FRONTIER",font=fb(50),fill=TX);d.text((X0+d.textlength("FRONTIER",font=fb(50)),230),"RADAR",font=fb(50),fill=GREEN)
    st=f"Stage {it['stage']} · {stage_name(it.get('topic','Chips'),it['stage'])}   Readiness {it['ready']}/100";d.text((X0,296),st,font=fb(28),fill=MUT)
    r=it['ready'];rc=GREEN if r>=60 else (245,197,66) if r>=35 else RED
    d.rounded_rectangle((X0,340,X0+XW,350),5,fill=(40,52,70));d.rounded_rectangle((X0,340,X0+int(XW*r/100),350),5,fill=rc)
    if art:
        a=art.copy();a.thumbnail((XW,440));im.paste(a,(X0+(XW-a.width)//2,380))
    y=860;col=SEC_COL.get(sec,GREEN);lab=sec.upper()
    d.rounded_rectangle((X0,y,X0+d.textlength(lab,font=fb(38))+50,y+66),33,fill=col);d.text((X0+25,y+11),lab,font=fb(38),fill=BG)
    for sz in (66,58,50,44):
        f=fb(sz);lines=wrap(d,text,f,XW)
        if len(lines)*(sz+16)<=1500-(y+100): break
    ty=y+100
    for l in lines: d.text((X0,ty),l,font=f,fill=TX);ty+=f.size+16
    d.rounded_rectangle((X0,1515,X0+XW,1527),6,fill=(40,52,70));d.rounded_rectangle((X0,1515,X0+int(XW*idx/total),1527),6,fill=GREEN)
    d.text((X0,1542),"research.celesys.ai  ·  Not financial advice",font=fr(28),fill=MUT)
    im.save(path)
def main():
    day,iid=sys.argv[1],sys.argv[2]
    voice=sys.argv[sys.argv.index("--voice")+1] if "--voice" in sys.argv else "en-US-AriaNeural"
    D=json.load(open(day));it=next(x for x in D["research"] if x["id"]==iid)
    if len(sys.argv)>3 and sys.argv[3]=="--auto" and os.path.exists(os.path.join(ROOT,"videos",iid+".script.json")): pass
    sp=os.path.join(ROOT,"videos",iid+".script.json");sc=json.load(open(sp)) if os.path.exists(sp) else auto_script(it)
    if isinstance(sc,list): sc={"hook":"","sections":sc}
    secs=([["Hook",sc["hook"]]] if sc.get("hook") else [])+sc["sections"]+[["Next","Full scores and sources at research.celesys.ai."]]
    tmp=tempfile.mkdtemp();art=None;svg=os.path.join(ROOT,"assets",iid+".svg")
    if os.path.exists(svg): from art2 import topic_art;cairosvg.svg2png(bytestring=topic_art(it,title=False).encode(),write_to=f"{tmp}/art.png",output_width=1760);art=Image.open(f"{tmp}/art.png").convert("RGB")
    chunks=[(s,t) for s,txt in secs for t in sentences(txt)]
    gap=lambda i,ch:(0.45 if i+1<len(ch) and ch[i+1][0]!=ch[i][0] else 0.2)
    aud=[]
    for i,(s,t) in enumerate(chunks):
        a=f"{tmp}/a{i}.mp3";tts(spoken(t),a,voice);aud.append(a)
    total=lambda ch,au:sum(dur(x) for x in au)+sum(gap(i,ch) for i in range(len(ch)))
    LIM=59.0
    # 1) drop extra sentences from long sections (keep first sentence of each section), 2) mild speed-up up to 1.12x
    while total(chunks,aud)>LIM*1.12:
        cand=[i for i in range(1,len(chunks)) if chunks[i][0]==chunks[i-1][0] and chunks[i][0] not in ("Why it matters","What it does")]
        cand=cand or [i for i in range(1,len(chunks)) if chunks[i][0]==chunks[i-1][0]]
        if not cand: break
        k=max(cand,key=lambda i:dur(aud[i]));chunks.pop(k);aud.pop(k)
    f=total(chunks,aud)/LIM
    if f>1:
        f=min(f,1.12)
        for i,a in enumerate(aud):
            b2=a.replace(".mp3","f.mp3");subprocess.run(["ffmpeg","-y","-v","error","-i",a,"-filter:a",f"atempo={f:.3f}",b2],check=True);aud[i]=b2
    secs=[];[secs.append([s,t]) if not secs or secs[-1][0]!=s else secs[-1].__setitem__(1,secs[-1][1]+" "+t) for s,t in chunks]
    clips=[]
    for i,(s,t) in enumerate(chunks):
        a=aud[i];dd=dur(a)+gap(i,chunks)
        p=f"{tmp}/s{i}.png";slide(art,s,t,i+1,len(chunks),it,p);v=f"{tmp}/c{i}.mov";n=int(dd*FPS)+1
        subprocess.run(["ffmpeg","-y","-v","error","-loop","1","-i",p,"-i",a,"-filter_complex",
          f"[0]scale=1134:2016,zoompan=z='min(1+0.0004*on,1.05)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={W}x{H}:fps={FPS},format=yuv420p[v];[1]apad[a]",
          "-map","[v]","-map","[a]","-t",f"{dd:.2f}","-c:v","libx264","-preset","medium","-crf","30","-c:a","pcm_s16le","-ar","44100","-ac","1",v],check=True)
        clips.append(v)
    open(f"{tmp}/l.txt","w").write("".join(f"file '{c}'\n" for c in clips))
    out=os.path.join(ROOT,"videos",iid+".mp4")
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c:v","copy","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-c:a","aac","-b:a","96k","-ar","44100","-movflags","+faststart",out],check=True)
    notes=f"FrontierRadar explainer: {it['title']}\nIssue: {D['date']} | Stage {it['stage']} · {stage_name(it.get('topic','Chips'),it['stage'])} | Readiness {it['ready']}/100 | Voice: {', '.join(sorted(set(USED)))}\n\n"+"\n\n".join(f"{s.upper()}\n{t}" for s,t in secs)
    notes+="\n\nSOURCES\n"+"; ".join(l[0] for l in it.get("links",[]))+". Judgment calls are labelled. Not financial advice.\n"
    open(os.path.join(ROOT,"videos",iid+".txt"),"w").write(notes)
    print(iid,round(dur(out),1),"s",os.path.getsize(out)//1024,"KB")
main()
