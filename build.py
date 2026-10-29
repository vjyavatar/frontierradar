"""FrontierRadar daily builder: data/*.json -> dated pages + report.html (latest) + index archive."""
import json,glob,html,os
E=lambda s:html.escape(str(s))
BASE="https://vjyavatar.github.io/frontierradar/"
CSS=""":root{--bg:#070b12;--card:#101826;--bd:#1f2b3d;--tx:#e8eef5;--tx2:#a9b6c6;--tx3:#71839a;--acc:#4da3ff;--g:#2ecc71;--r:#ff5c5c;--y:#f5c542;--p:#b07cff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--acc)}#prog{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--g),var(--acc));width:0;z-index:20}
header.nav{position:sticky;top:0;z-index:10;display:flex;justify-content:space-between;align-items:center;padding:10px 20px;background:rgba(7,11,18,.9);backdrop-filter:blur(8px);border-bottom:1px solid var(--bd)}
.brand{font-weight:800;font-size:19px;text-decoration:none;color:var(--tx)}.brand span{color:var(--g)}.nav a.l{margin-left:14px;text-decoration:none;font-size:14px}
.hero{padding:56px 20px 36px;background:radial-gradient(1000px 400px at 20% 0,#123a2a55,transparent),radial-gradient(800px 400px at 90% 10%,#1b3a6b66,transparent);border-bottom:1px solid var(--bd)}
.hero h1{font-size:44px;line-height:1.15;margin:.2em 0;max-width:900px}.hero .hook{font-size:20px;color:var(--tx2);max-width:820px}
.pill{display:inline-block;font-size:12px;padding:3px 10px;border:1px solid var(--bd);border-radius:99px;margin:0 6px 6px 0;color:var(--tx2)}
.layout{max-width:1240px;min-width:0;margin:0 auto;padding:20px;display:grid;grid-template-columns:220px 1fr;gap:28px}
.toc{position:sticky;top:70px;align-self:start;font-size:14px}.toc a{display:block;padding:5px 10px;color:var(--tx2);text-decoration:none;border-left:2px solid var(--bd)}.toc a.on{color:var(--tx);border-color:var(--g)}
main{min-width:0}h2{font-size:28px;overflow-wrap:anywhere;margin:1.8em 0 .5em;scroll-margin-top:70px}.lead{color:var(--tx2);margin-top:0}
.card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:18px}.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.tl b{display:block;font-size:17px}.tl .e{font-size:26px}.pos{border-top:3px solid var(--g)}.neg{border-top:3px solid var(--r)}.mix{border-top:3px solid var(--y)}
.kpi .v{font-size:30px;font-weight:800}.kpi .d.pos,.tg{color:var(--g)}.kpi .d{border:0;font-size:13px}.kpi .d.neg{color:var(--r)}
.an{font-size:14px;color:#bfe9cf;background:#0d1f16;border-radius:8px;padding:6px 10px;margin-top:8px}
.dyk{background:linear-gradient(135deg,#1b1233,#101826);border:1px solid #3a2a66;border-radius:16px;padding:16px 18px;margin:18px 0}.dyk b{color:var(--p)}
svg{width:100%;height:auto}.cap{font-size:13px;color:var(--tx3)}sup a{text-decoration:none;font-size:11px}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:9px;border-bottom:1px solid var(--bd);text-align:left}th{color:var(--tx2)}.tw{overflow-x:auto}
.tabs button{background:var(--card);color:var(--tx2);border:1px solid var(--bd);border-radius:99px;padding:7px 14px;margin:0 6px 8px 0;cursor:pointer}.tabs button.on{background:var(--acc);color:#001;border-color:var(--acc)}
.c-High{color:var(--g);font-weight:700}.c-Medium{color:var(--y);font-weight:700}.c-Speculative{color:#ff9b5c;font-weight:700}.c-Watch{color:var(--tx3);font-weight:700}
.time{border-left:2px solid var(--bd);margin-left:8px}.time div{position:relative;padding:4px 0 14px 20px}.time div:before{content:"";position:absolute;left:-7px;top:9px;width:12px;height:12px;border-radius:50%;background:var(--acc)}
.cta{background:linear-gradient(135deg,#0f3d2a,#10263f);border-radius:18px;padding:26px;text-align:center}.cta input{padding:12px;border-radius:10px;border:1px solid var(--bd);background:#0a111b;color:var(--tx);width:min(320px,90%)}
.btn{display:inline-block;background:var(--g);color:#012;border:0;border-radius:10px;padding:11px 18px;font-weight:700;text-decoration:none;cursor:pointer;margin:4px}
.share a{display:inline-block;margin:4px;padding:8px 12px;border:1px solid var(--bd);border-radius:10px;text-decoration:none;font-size:14px}
.warn{border-left:4px solid var(--y);background:#1d1a0d;padding:12px 16px;border-radius:10px;font-size:14px}
.mn{display:flex;gap:4px;overflow-x:auto}.mn a.m{padding:7px 12px;border-radius:99px;text-decoration:none;color:var(--tx2);font-size:14px;white-space:nowrap}.mn a.m.on{background:var(--acc);color:#001;font-weight:700}
.st{display:inline-block;font-size:12px;font-weight:700;padding:3px 9px;border-radius:99px;color:#012}.s1{background:#b07cff}.s2{background:#4da3ff}.s3{background:#f5c542}.s4{background:#2ecc71}
details{background:#0b121d;border:1px solid var(--bd);border-radius:10px;padding:8px 12px;margin-top:8px}summary{cursor:pointer;color:var(--acc);font-weight:600}.ri h3{margin:.3em 0}.meta{font-size:13px;color:var(--tx3)}.kv{font-size:14px;margin:6px 0}.kv b{color:var(--tx2)}
footer{border-top:1px solid var(--bd);padding:24px;color:var(--tx3);font-size:13px;text-align:center}
@media(max-width:860px){main{min-width:0}#opp thead{display:none}#opp tr{display:block;border-bottom:2px solid var(--bd);padding:8px 0}#opp td{display:block;border:0;padding:3px 6px}#opp td:nth-child(2){font-size:17px}#opp td:nth-child(3):before{content:"Region: ";color:var(--tx3);font-size:12px}#opp td:nth-child(4):before{content:"Ticker: ";color:var(--tx3);font-size:12px}#opp td:nth-child(5):before{content:"Catalyst: ";color:var(--tx3);font-size:12px}#opp td:nth-child(6):before{content:"Timeline: ";color:var(--tx3);font-size:12px}#opp td:nth-child(7):before{content:"Risk: ";color:var(--tx3);font-size:12px}#opp td:nth-child(8):before{content:"Conviction: ";color:var(--tx3);font-size:12px}#opp td:nth-child(9):before{content:"Research: ";color:var(--tx3);font-size:12px}.pipe{display:none}.brand{display:none}.brand{font-size:16px}.mn a.m{padding:6px 8px;font-size:12px}header.nav{gap:8px;padding:8px 10px}.layout{grid-template-columns:1fr}.toc{display:none}.hero h1{font-size:30px}.nav a.l{display:none}}"""
JS="""addEventListener('scroll',()=>{const h=document.documentElement;document.getElementById('prog').style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';let c;document.querySelectorAll('section[id]').forEach(s=>{if(s.getBoundingClientRect().top<120)c=s.id});document.querySelectorAll('.toc a').forEach(a=>a.classList.toggle('on',a.hash=='#'+c))});
function flt(b,k,v){document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');document.querySelectorAll('#opp tbody tr').forEach(r=>r.style.display=(v=='All'||r.dataset[k]==v)?'':'none')}"""
def head(title,desc,url):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | FrontierRadar</title><meta name="description" content="{E(desc)}"><meta name="robots" content="index,follow">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)} | FrontierRadar"><meta property="og:description" content="{E(desc)}"><link rel="canonical" href="{url}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="FrontierRadar"><meta property="og:image" content="{BASE}og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)} | FrontierRadar"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BASE}og-image.png">
<link rel="icon" href="data:,"><link rel="alternate" type="application/rss+xml" href="{BASE}feed.xml"><style>{CSS}{CSS3}</style></head><body><div id="prog"></div>"""
def nav(p="",on=""):
    it=[("research.html","🔬 Research"),("results.html","📊 Results"),("opportunities.html","🎯 Opportunities")]
    return f'<header class="nav"><a class="brand" href="{p}index.html">Frontier<span>Radar</span></a><nav class="mn">'+"".join(f'<a class="m{" on" if h==on else ""}" href="{h}">{t}</a>' for h,t in it)+'</nav></header>'
def src(n): return f'<sup><a href="#s{n}">[{n}]</a></sup>' if n else ''
def hbar(rows,unit="",colors=None,w=640):
    mx=max(r[1] for r in rows);bh=34;h=len(rows)*bh+10;o=[f'<svg viewBox="0 0 {w} {h}" role="img">']
    for i,r in enumerate(rows):
        y=i*bh+6;L=(w-300)*r[1]/mx;c=(colors[i] if colors else "#2ecc71")
        o.append(f'<text x="0" y="{y+18}" fill="#a9b6c6" font-size="13">{E(r[0])}</text><rect x="210" y="{y+4}" width="{L:.0f}" height="20" rx="5" fill="{c}"/><text x="{216+L:.0f}" y="{y+19}" fill="#e8eef5" font-size="13" font-weight="700">{unit}{r[1]:g}</text>')
    return "".join(o)+"</svg>"
def pair(rows,w=640):
    mx=max(max(r[1],r[2]) for r in rows);bh=52;h=len(rows)*bh+24;o=[f'<svg viewBox="0 0 {w} {h}"><text x="210" y="12" fill="#71839a" font-size="11">■ year ago</text><text x="300" y="12" fill="#2ecc71" font-size="11">■ latest</text>']
    for i,r in enumerate(rows):
        y=i*bh+22;a=(w-300)*r[1]/mx;b=(w-300)*r[2]/mx;g=(r[2]/r[1]-1)*100
        o.append(f'<text x="0" y="{y+22}" fill="#a9b6c6" font-size="13">{E(r[0])}</text><rect x="210" y="{y}" width="{a:.0f}" height="16" rx="4" fill="#3a4a60"/><text x="{214+a:.0f}" y="{y+13}" fill="#a9b6c6" font-size="11">${r[1]:g}B</text><rect x="210" y="{y+20}" width="{b:.0f}" height="16" rx="4" fill="#2ecc71"/><text x="{214+b:.0f}" y="{y+33}" fill="#e8eef5" font-size="12" font-weight="700">${r[2]:g}B (+{g:.0f}%)</text>')
    return "".join(o)+"</svg>"
def flow():
    st=[("Design","USA","#4da3ff"),("Tools","NL/Japan/USA","#b07cff"),("Make","Taiwan","#2ecc71"),("Memory","Korea","#2ecc71"),("Package","Taiwan/India","#f5c542"),("Data center","Cloud giants","#4da3ff")]
    o=['<svg viewBox="0 0 760 120">']
    for i,(a,b,c) in enumerate(st):
        x=i*126+4;o.append(f'<rect x="{x}" y="20" width="110" height="70" rx="12" fill="#101826" stroke="{c}" stroke-width="2"/><text x="{x+55}" y="50" fill="#e8eef5" font-size="14" font-weight="700" text-anchor="middle">{a}</text><text x="{x+55}" y="70" fill="#a9b6c6" font-size="11" text-anchor="middle">{b}</text>')
        if i<5:o.append(f'<path d="M{x+112} 55 l12 0 m-5 -5 l5 5 l-5 5" stroke="#71839a" fill="none" stroke-width="2"/>')
    return "".join(o)+'<text x="380" y="112" fill="#f5c542" font-size="12" text-anchor="middle">Yellow = current bottleneck (advanced packaging)</text></svg>'
def gauge(rows):
    o=[]
    for n,v in rows:
        c="#2ecc71" if v>=70 else "#f5c542" if v>=40 else "#ff5c5c"
        o.append(f'<div style="margin:8px 0"><div style="display:flex;justify-content:space-between;font-size:14px"><span>{E(n)}</span><b style="color:{c}">{v}/100</b></div><div style="background:#1f2b3d;border-radius:99px;height:10px"><div style="width:{v}%;background:{c};height:10px;border-radius:99px"></div></div></div>')
    return "".join(o)
STAGES=[(1,"Paper","Scientists prove an idea in a lab. Like a recipe in a cookbook.","#b07cff"),(2,"Prototype","A working sample chip exists. Like the first cake baked at home.","#4da3ff"),(3,"Factories & orders","Machines are bought, customers place orders. Like a bakery opening.","#f5c542"),(4,"Revenue","It shows up in company earnings. Like the bakery's profit report.","#2ecc71")]
def stb(n): return f'<span class="st s{n}">Stage {n} · {STAGES[n-1][1]}</span>'
def pipeline():
    o=['<svg viewBox="0 0 800 170" role="img" aria-label="Paper to profit pipeline">']
    for i,(n,t,x,c) in enumerate(STAGES):
        X=i*200+6;o.append(f'<rect x="{X}" y="10" width="180" height="90" rx="14" fill="#101826" stroke="{c}" stroke-width="3"/><text x="{X+90}" y="42" text-anchor="middle" fill="{c}" font-size="15" font-weight="800">STAGE {n}</text><text x="{X+90}" y="66" text-anchor="middle" fill="#e8eef5" font-size="16" font-weight="700">{t}</text><text x="{X+90}" y="88" text-anchor="middle" fill="#a9b6c6" font-size="11">{["~5-10 yrs early","~3-6 yrs early","~1-3 yrs early","priced in"][i]}</text>')
        if i<3:o.append(f'<path d="M{X+184} 55 h12 m-6 -6 l6 6 l-6 6" stroke="#71839a" stroke-width="2" fill="none"/>')
    o.append('<defs><linearGradient id="gr"><stop offset="0" stop-color="#2ecc71"/><stop offset="1" stop-color="#ff5c5c"/></linearGradient></defs><rect x="6" y="122" width="780" height="10" rx="5" fill="url(#gr)"/><text x="6" y="154" fill="#2ecc71" font-size="13" font-weight="700">Biggest upside · we track here</text><text x="786" y="154" fill="#ff5c5c" font-size="13" font-weight="700" text-anchor="end">Least surprise · everyone sees it</text></svg>')
    return "".join(o)
def scatter(R):
    W,H=780,360;o=[f'<svg viewBox="0 0 {W} {H}" role="img"><rect x="50" y="10" width="{W-70}" height="{H-60}" fill="#0b121d" rx="10"/>']
    for v in (0,25,50,75,100):
        y=10+(H-60)*(1-v/100);o.append(f'<line x1="50" x2="{W-20}" y1="{y}" y2="{y}" stroke="#1f2b3d"/><text x="44" y="{y+4}" fill="#71839a" font-size="11" text-anchor="end">{v}</text>')
    for yr in range(0,11,2):
        x=50+(W-70)*yr/10;o.append(f'<text x="{x}" y="{H-32}" fill="#71839a" font-size="11" text-anchor="middle">{yr}y</text>')
    o.append(f'<text x="{W/2}" y="{H-10}" fill="#a9b6c6" font-size="12" text-anchor="middle">Years to market (our estimate) →</text><text x="14" y="{H/2}" fill="#a9b6c6" font-size="12" transform="rotate(-90 14 {H/2})" text-anchor="middle">Readiness 0-100</text>')
    for i,r in enumerate(R):
        a=r["years"].replace("+","-10").split("-");yr=(float(a[0])+float(a[1]))/2 if len(a)>1 else float(a[0])
        x=50+(W-70)*min(yr,10)/10;y=10+(H-60)*(1-r["ready"]/100);c=STAGES[r["stage"]-1][3]
        o.append(f'<a href="#{r["id"]}"><circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{c}" opacity=".9"/><text x="{x:.0f}" y="{y+4:.0f}" fill="#012" font-size="10" font-weight="800" text-anchor="middle">{i+1}</text></a>')
    return "".join(o)+"</svg>"
def shell(d,url,p,on,title,hero,body,toc):
    b=[head(title,d["desc"],url),nav(p,on)]
    b.append(f'<div class="hero"><div style="max-width:1200px;margin:0 auto">{"".join(f"<span class=pill>{E(t)}</span>" for t in d["tags"])}<span class="pill">📅 {d["date"]}</span>{hero}</div></div>')
    b.append('<div class="layout"><aside class="toc">'+"".join(f'<a href="#{i}">{t}</a>' for i,t in toc)+'</aside><main>'+body)
    sh=url;tx=html.escape(title)
    b.append(f'<section id="subscribe" style="margin-top:32px"><div class="cta"><h2 style="margin-top:0">📬 Get tomorrow\'s breakthroughs first</h2><p>New papers and patents, decoded in plain English, every morning.</p><form onsubmit="alert(\'Thanks! Sign-up opens soon.\');return false"><input type="email" required placeholder="you@email.com"> <button class="btn">Subscribe free</button></form><div class="share" style="margin-top:14px">Share: <a href="https://twitter.com/intent/tweet?text={tx}&url={sh}">X</a><a href="https://www.linkedin.com/sharing/share-offsite/?url={sh}">LinkedIn</a><a href="https://wa.me/?text={tx}%20{sh}">WhatsApp</a><a href="https://t.me/share/url?url={sh}&text={tx}">Telegram</a><a href="https://www.reddit.com/submit?url={sh}&title={tx}">Reddit</a></div></div></section>')
    b.append(f'</main></div><footer>Not investment advice. Readiness, years-to-market, patent-risk notes and conviction are FrontierRadar editorial judgment, not legal or financial advice. © 2026 FrontierRadar. · <a href="{p}index.html#archive">Archive</a> · <a href="{p}feed.xml">RSS</a></footer><script>{JS}{JS3}</script><button class="switch" id="kidb" onclick="kid()">🧒 Explain like I\'m 10</button><div class="badge" id="badge" style="display:{"block" if on=="research.html" else "none"}"></div></body></html>')
    return "".join(b)
def research(d,url,p):
    R=d["research"];b=[]
    b.append(botd_html(d,p))
    b.append(f'<section id="pipe"><h2>🧪 Paper to Profit: the 4 stages</h2><p class="lead">Every chip breakthrough walks this path. Stock prices usually move at stage 4. We spot ideas at stages 1-2, years earlier.</p><div class="card pipe">{pipeline()}</div><div class="grid" style="margin-top:12px">'+"".join(f'<div class="card" style="border-top:3px solid {c}"><b>{stb(n)}</b><p>{E(x)}</p><span class="meta">{sum(1 for r in R if r["stage"]==n)} items this issue</span></div>' for n,t,x,c in STAGES)+'</div></section>')
    b.append(f'<section id="map"><h2>🗺 Readiness map</h2><p class="lead">Top-left = closest to making money. Bottom-right = long shots with big upside. Tap a dot. (Our judgment.)</p><div class="card">{scatter(R)}<div class="cap">'+" · ".join(f'<a href="#{r["id"]}">{i+1}. {E(r["area"])}</a>' for i,r in enumerate(R))+'</div></div></section>')
    b.append('<section id="items"><h2>📄 This issue\'s papers & patents</h2><div class="tabs">'+'<button class="on" onclick="fr(this,0)">All</button>'+"".join(f'<button onclick="fr(this,{n})">Stage {n}</button>' for n in (1,2,3))+'</div>')
    for i,r in enumerate(R):
        c="#2ecc71" if r["ready"]>=60 else "#f5c542" if r["ready"]>=30 else "#ff5c5c"
        b.append(f'<article class="card ri" id="{r["id"]}" data-s="{r["stage"]}" style="margin:14px 0;scroll-margin-top:70px">{stb(r["stage"])} <span class="pill">{E(r["area"])}</span><h3>{i+1}. {E(r["title"])}</h3><div class="meta">🏛 {E(r["who"])} · 📅 {E(r["date"])}</div>'
          f'<img class="art" src="{p}assets/{r["id"]}.svg" alt="Concept illustration: {E(r["area"])}" loading="lazy" width="640" height="300"><button class="fol" data-id="{r["id"]}" onclick="fol(this,\'{r["id"]}\')">☆ Follow this tech</button>'
          f'<p class="adult"><b>What they found:</b> {E(r["found"])}</p><p class="eli">🧒 <b>Like I\'m 10:</b> {E(r.get("eli10",""))}</p><div class="an">🧩 Think of it like: {E(r["analogy"])}</div>'
          f'<div class="grid" style="margin-top:10px"><div><div class="kv"><b>Readiness</b> <span style="color:{c};font-weight:800">{r["ready"]}/100</span></div><div style="background:#1f2b3d;border-radius:99px;height:8px"><div style="width:{r["ready"]}%;background:{c};height:8px;border-radius:99px"></div></div><div class="kv"><b>Years to market:</b> {E(r["years"])}</div><div class="meta">Our judgment</div></div>'
          f'<div>{hype_meter(r.get("hype",0),r["ready"])}</div><div><div class="kv"><b>⚖️ Patent / IP risk</b></div>{prem("<div class=meta>"+E(r["ip"])+"</div>","Patent risk note")}</div>'
          f'<div><div class="kv"><b>🏆 Who could win</b></div>{"".join(f"<span class=pill>{E(w)}</span>" for w in r["win"])}</div></div>'
          f'<p class="kv"><b>👀 What to watch next:</b> {E(r["watch"])}</p>'
          f'<div class="tmach card" style="padding:10px;margin:8px 0"><b>⏰ Time Machine</b> <span class="meta">drag: 1 → 3 → 5 years (our scenario, not a forecast)</span><input type="range" min="0" max="2" value="0" aria-label="Time Machine: years ahead" data-t=\'{E(json.dumps(r.get("tm",["","",""])))}\' oninput="tm(this,\'{r["id"]}\')"><div class="out" id="tm-{r["id"]}">In 1 year: {E(r.get("tm",[""])[0])}</div></div>'
          f'<details><summary>📋 Executive briefing <span class="pill">teaser free</span></summary><p>{E(r["brief"].split(". ")[0])}.</p>{prem("<p>"+E(r["brief"])+"</p>","Full executive briefing")}</details><details><summary>🎬 30-second video script <span class="pill">Premium</span></summary>{prem("<p>"+E(r["video"])+"</p>","Video script with citations")}</details>'
          f'<p class="meta">🔗 Sources: '+" · ".join(f'<a href="{u}" rel="noopener" target="_blank">{E(t)}</a>' for t,u in r["links"])+'</p></article>')
    b.append('</section><div class="dyk"><b>💡 Did you know?</b> Patents are often filed months before the paper appears. When a company files a patent and a paper on the same idea (like IBM here), it usually means they plan to sell it.</div>')
    b.append(poll(d)+countdowns(d)+pricing())
    b.append('<script>function fr(b,n){document.querySelectorAll("#items .tabs button").forEach(x=>x.classList.remove("on"));b.classList.add("on");document.querySelectorAll(".ri").forEach(a=>a.style.display=(!n||a.dataset.s==n)?"":"none")}</script>')
    hero=f'<span class="pill">🔬 Research radar</span><h1>{E(d["title"])}</h1><p class="hook">{E(d["hook"])}</p><a class="btn" href="#items">Read the breakthroughs ↓</a><a class="btn" style="background:transparent;color:var(--tx);border:1px solid var(--bd)" href="opportunities.html">See linked opportunities</a>'
    return shell(d,url,p,"research.html",d["title"],hero,"".join(b),[("pipe","Paper → Profit"),("map","Readiness map"),("items","Papers & patents"),("poll","Quick poll"),("dates","Countdowns"),("premium","Plans"),("subscribe","Subscribe")])
def results(d,url,p):
    X=d["results"];b=[f'<div class="warn" style="margin-top:20px">📊 <b>Stage 4: proof the bets are paying off.</b> These are company results: by the time you read them, the market already knows. Use them to confirm that the research trends on our Research page are turning into real money.</div>']
    b.append('<section id="numbers"><h2>Key numbers</h2><div class="grid">'+"".join(f'<div class="card kpi {c}"><div class="v">{E(v)}</div>{E(l)}{src(s)}<div class="d {c}">{E(dl)}</div></div>' for v,l,dl,c,s in X["kpis"])+'</div></section>')
    r=X["revenue"];b.append(f'<section id="money"><h2>💸 Follow the money</h2><div class="card"><b>{E(r["title"])}</b>{pair(r["rows"])}<div class="cap">AMD year-ago figure derived from reported 107% growth. {" ".join(src(x[3]) for x in r["rows"])}</div></div>')
    c=X["capex"];m=X["margins"];b.append(f'<div class="grid" style="margin-top:14px"><div class="card"><b>{E(c["title"])}</b>{hbar(c["rows"],"$",w=560)}<div class="cap">Midpoints of guidance {src(6)}{src(2)}</div></div><div class="card"><b>{E(m["title"])}</b>{hbar(m["rows"],"",w=560)}<div class="cap">{src(4)}{src(1)}{src(2)}</div></div></div>')
    t=X["tam"];b.append(f'<div class="card" style="margin-top:14px"><b>{E(t["title"])}</b>{hbar(t["rows"],"$",["#4da3ff"]*4)}<div class="cap">{E(t["note"])} {" ".join(src(x[2]) for x in t["rows"])}</div></div></section>')
    v=X["valuation"];b.append(f'<section id="value"><h2>💵 Valuations</h2><div class="card tw"><table><tr><th>Company</th><th>Ticker</th><th>Market cap</th><th>Forward P/E</th></tr>'+"".join(f'<tr><td>{E(a)}</td><td>{E(b_)}</td><td>{E(c_)}</td><td>{E(dd)}</td></tr>' for a,b_,c_,dd,s in v["rows"])+f'</table><div class="cap">{E(v["title"])} {src(9)}</div></div></section>')
    b.append('<section id="dates"><h2>📅 Key dates</h2><div class="card time">'+"".join(f'<div><b>{E(a)}</b> {E(x)}{src(s)}</div>' for a,x,s in X["dates"])+'</div></section>')
    b.append('<section id="sources"><h2>📚 Sources</h2><ol class="cap">'+"".join(f'<li id="s{n}"><a href="{u if u.startswith("http") else p+u}">{E(t)}</a></li>' for n,t,u in d["sources"])+'</ol></section>')
    hero='<span class="pill">📊 Stage 4</span><h1>Company results: is the money showing up?</h1><p class="hook">Big tech plans ~$720B+ of data-centre spending in 2026. Here\'s who is cashing in.</p>'
    return shell(d,url,p,"results.html","AI-chip company results: proof the bets are paying off",hero,"".join(b),[("numbers","Key numbers"),("money","Follow the money"),("value","Valuations"),("dates","Key dates"),("sources","Sources")])
def opps(d,url,p):
    O=d["opportunities"];R={r["id"]:(i+1,r["title"]) for i,r in enumerate(d["research"])}
    regs=sorted({o["region"] for o in O})
    f=lambda k,vals,lab:'<div class="tabs" data-k="'+k+'"><span class="meta">'+lab+': </span><button class="on" onclick="fo(this)">All</button>'+"".join(f'<button onclick="fo(this)">{v}</button>' for v in vals)+'</div>'
    b=['<section id="table"><h2>🎯 Opportunities, earliest first</h2><p class="lead">Every row links back to the research that could drive it. Earlier stage = more upside, more risk.</p>',f("s",["1","2","3","4"],"Stage"),f("r",regs,"Region"),f("c",["High","Medium","Speculative","Watch"],"Conviction"),
       '<div class="card tw"><table id="opp"><thead><tr><th>Stage</th><th>Company</th><th>Region</th><th>Ticker</th><th>Catalyst</th><th>Timeline</th><th>Risk</th><th>Conviction</th><th>Driven by research</th></tr></thead><tbody>']
    for o in O:
        b.append(f'<tr data-s="{o["stage"]}" data-r="{E(o["region"])}" data-c="{o["conv"]}"><td>{stb(o["stage"])}</td><td><b>{E(o["name"])}</b></td><td>{E(o["region"])}</td><td>{E(o["ticker"])}</td><td>{E(o["catalyst"])}</td><td>{E(o["timeline"])}</td><td style="color:#ff9b9b">{E(o["risk"])}</td><td class="c-{o["conv"]}">{o["conv"]}</td><td>'+"<br>".join(f'<a href="research.html#{l}">#{R[l][0]} {E(R[l][1][:38])}…</a>' for l in o["links"])+'</td></tr>')
    b.append('</tbody></table></div><p class="warn">⚠️ <b>Not financial advice.</b> Conviction reflects our editorial view of how strong the research-to-revenue story is, not a buy or sell recommendation. Prices and facts change; do your own research and consult a registered investment adviser.</p></section>')
    b.append('<script>const F={};function fo(b){const t=b.parentNode;t.querySelectorAll("button").forEach(x=>x.classList.remove("on"));b.classList.add("on");F[t.dataset.k]=b.textContent;document.querySelectorAll("#opp tbody tr").forEach(r=>{r.style.display=Object.entries(F).every(([k,v])=>v=="All"||r.dataset[k]==v)?"":"none"})}</script>')
    hero='<span class="pill">🎯 Early-stage first</span><h1>Opportunities ahead, traced to the lab</h1><p class="hook">Most investors find out at stage 4. Here are companies tied to stage 1-3 breakthroughs, so you can watch them early.</p>'
    return shell(d,url,p,"opportunities.html","AI-chip opportunities traced to research",hero,"".join(b),[("table","Opportunities"),("subscribe","Subscribe")])
def main():
    issues=sorted(ALL,key=lambda d:d["date"],reverse=True)
    for d in issues:
        os.makedirs(d["slug"],exist_ok=True)
        for fn,g in (("research.html",research),("results.html",results),("opportunities.html",opps)):
            open(f'{d["slug"]}/{fn}',"w").write(g(d,f'{BASE}{d["slug"]}/{fn}',"../"))
        open(f'{d["slug"]}/index.html',"w").write('<meta http-equiv="refresh" content="0;url=research.html">')
    L=issues[0];make_assets(L)
    for fn,g in (("research.html",research),("results.html",results),("opportunities.html",opps)):open(fn,"w").write(g(L,BASE+fn,""))
    open("report.html","w").write(research(L,BASE+"report.html",""))
    cards="".join(f'<a class="card" style="text-decoration:none;color:inherit" href="{d["slug"]}/research.html"><span class="pill">{d["topic"]}</span><span class="pill">{d["date"]}</span><h3>{E(d["title"])}</h3><p class="cap">{len(d["research"])} papers & patents · {len(d["opportunities"])} opportunities</p></a>' for d in issues)
    top="".join(f'<a class="card ri" style="text-decoration:none;color:inherit" href="research.html#{r["id"]}">{stb(r["stage"])}<h3>{E(r["title"])}</h3><span class="meta">{E(r["who"])}</span></a>' for r in sorted(L["research"],key=lambda r:r["stage"])[:6])
    ix=head("Spot deep-tech breakthroughs before the market does","FrontierRadar tracks new research papers and patents in AI chips and deep tech, explains them in plain English, and scores how close they are to making money. Not investment advice.",BASE)+nav()
    ix+=f'<div class="hero"><div style="max-width:1200px;margin:0 auto"><span class="pill">New issue: {L["date"]}</span><h1>See tomorrow\'s chip winners<br><span style="color:var(--g)">while they\'re still lab papers.</span></h1><p class="hook">{E(L["hook"])}</p><a class="btn" href="research.html">Open the Research radar →</a><a class="btn" style="background:transparent;color:var(--tx);border:1px solid var(--bd)" href="opportunities.html">Opportunities</a><img src="assets/hero.svg" alt="Concept art: light flowing into a chip" style="width:100%;border-radius:18px;margin-top:22px;max-height:360px;object-fit:cover"></div></div>'
    ix+=f'<main style="max-width:1100px;margin:0 auto;padding:20px">{botd_html(L)}<h2>🧪 Paper to Profit</h2><div class="card pipe">{pipeline()}</div><p class="meta">Stage 1 Paper → 2 Prototype → 3 Factories & orders → 4 Revenue. The earlier we spot it, the bigger the head start.</p><h2>🔬 Earliest breakthroughs this issue</h2><div class="grid">{top}</div><h2 id="archive">🗂 Archive</h2><div class="grid">{cards}<a class="card" style="text-decoration:none;color:inherit" href="breakthroughs.html"><span class="pill">AI Chips</span><span class="pill">2026-10-28</span><h3>5 AI-chip breakthroughs (first issue)</h3></a></div>{countdowns(L)}{pricing()}<section id="subscribe"><div class="cta" style="margin-top:28px"><h2 style="margin-top:0">📬 Get every issue free</h2><form onsubmit="alert(\'Sign-up opens soon.\');return false"><input type="email" required placeholder="you@email.com"> <button class="btn">Subscribe</button></form></div></section></main><footer>Not investment advice. © 2026 FrontierRadar.</footer><script>{JS}{JS3}</script></body></html>'
    open("index.html","w").write(ix)
    rss="".join(f'<item><title>{E(d["title"])}</title><link>{BASE}{d["slug"]}/research.html</link><description>{E(d["hook"])}</description><pubDate>{d["date"]}</pubDate></item>' for d in issues)
    open("feed.xml","w").write(f'<?xml version="1.0"?><rss version="2.0"><channel><title>FrontierRadar</title><link>{BASE}</link><description>Deep tech research radar</description>{rss}</channel></rss>')
    urls=[BASE]+[BASE+x for x in ("research.html","results.html","opportunities.html","report.html","breakthroughs.html")]+[f'{BASE}{d["slug"]}/{x}' for d in issues for x in ("research.html","results.html","opportunities.html")]
    open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc></url>" for u in urls)+"</urlset>")

# ---------- v3: art + engagement ----------
import random,math
KIND={"Optical compute":"light","Photonic interconnect":"light","Photonic neuromorphic":"neuro","In-memory / analog compute":"grid","In-memory compute":"grid","New transistors":"stack","Chiplets / packaging":"stack","Packaging materials":"glass","Neuromorphic":"neuro","Neuromorphic / 2D materials":"neuro"}
PAL=[("#2ecc71","#4da3ff"),("#b07cff","#4da3ff"),("#4da3ff","#2ecc71"),("#f5c542","#b07cff")]
def art(seed,kind,w=640,h=300):
    rnd=random.Random(seed);a,b=PAL[rnd.randrange(4)];o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient><radialGradient id="bg" cx=".3" cy=".2" r="1"><stop offset="0" stop-color="#14233a"/><stop offset="1" stop-color="#070b12"/></radialGradient><filter id="f"><feGaussianBlur stdDeviation="3"/></filter></defs><rect width="{w}" height="{h}" fill="url(#bg)"/>']
    for i in range(40):o.append(f'<circle cx="{rnd.random()*w:.0f}" cy="{rnd.random()*h:.0f}" r="{rnd.random()*1.4:.1f}" fill="#9fb4d0" opacity=".5"/>')
    cx,cy=w/2,h/2
    # central chip
    o.append(f'<rect x="{cx-70}" y="{cy-70}" width="140" height="140" rx="14" fill="#0c1422" stroke="url(#g)" stroke-width="3"/>')
    for i in range(7):
        p=cx-60+i*20;o.append(f'<path d="M{p} {cy-70}v-14M{p} {cy+70}v14M{cx-70} {p-cx+cy}h-14M{cx+70} {p-cx+cy}h14" stroke="{a}" stroke-width="3" opacity=".7"/>')
    if kind=="light":
        for i in range(9):
            y=30+i*30;o.append(f'<path d="M0 {y} C {w*.3} {y+rnd.randint(-40,40)}, {w*.4} {cy}, {cx-70} {cy-50+i*12}" stroke="url(#g)" stroke-width="2" fill="none" opacity=".8" filter="url(#f)"/><path d="M0 {y} C {w*.3} {y+rnd.randint(-40,40)}, {w*.4} {cy}, {cx-70} {cy-50+i*12}" stroke="#e8fff4" stroke-width=".8" fill="none" opacity=".7"/>')
        for i in range(5):o.append(f'<path d="M{cx+70} {cy-40+i*20} L{w} {cy-90+i*45}" stroke="{b}" stroke-width="2" opacity=".7"/>')
    elif kind=="grid":
        for i in range(5):
            for j in range(5):o.append(f'<rect x="{cx-55+i*22}" y="{cy-55+j*22}" width="16" height="16" rx="3" fill="{a if rnd.random()>.5 else b}" opacity="{rnd.uniform(.3,1):.2f}"/>')
        for i in range(12):o.append(f'<circle cx="{rnd.choice([rnd.uniform(20,170),rnd.uniform(470,620)]):.0f}" cy="{rnd.uniform(30,270):.0f}" r="{rnd.uniform(6,16):.0f}" fill="none" stroke="url(#g)" stroke-width="2" opacity=".6"/>')
    elif kind=="stack":
        for i in range(6):
            y=cy+40-i*22;o.append(f'<path d="M{cx-170} {y} l60 -30 h220 l-60 30 z" fill="{[a,b][i%2]}" opacity="{.25+i*.1:.2f}" stroke="#e8eef5" stroke-opacity=".3"/>')
        for i in range(10):x=cx-120+i*26;o.append(f'<circle cx="{x}" cy="{cy+60}" r="4" fill="#f5c542"/>')
    elif kind=="glass":
        o.append(f'<path d="M60 {cy+60} L{cx} {cy+120} L{w-60} {cy+60} L{cx} {cy} Z" fill="#7fe3ff" opacity=".15" stroke="#7fe3ff" stroke-opacity=".7"/>')
        for i in range(14):x=rnd.uniform(120,520);o.append(f'<line x1="{x}" y1="{cy+40}" x2="{x}" y2="{cy+90}" stroke="#7fe3ff" opacity=".6"/>')
    else:
        pts=[(rnd.uniform(30,w-30),rnd.uniform(25,h-25)) for _ in range(22)]
        for i,(x,y) in enumerate(pts):
            for x2,y2 in pts[i+1:i+3]:o.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="url(#g)" opacity=".45"/>')
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(3,7):.0f}" fill="{a}" filter="url(#f)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="2" fill="#fff"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="url(#g)" opacity=".85" filter="url(#f)"/><circle cx="{cx}" cy="{cy}" r="10" fill="#fff" opacity=".9"/></svg>')
    return "".join(o)
def make_assets(L):
    for r in L["research"]:open(f'assets/{r["id"]}.svg',"w").write(art(r["id"],KIND.get(r["area"],"neuro")))
    open("assets/hero.svg","w").write(art("hero-frontier","light",1200,420))
CSS3=""".art{width:100%;border-radius:12px;display:block;margin:6px 0 10px;aspect-ratio:640/300;object-fit:cover}
.botd{display:grid;grid-template-columns:1.1fr 1fr;gap:18px;align-items:center;background:linear-gradient(135deg,#0f3d2a,#1b1233);border:1px solid #2ecc7155;border-radius:18px;padding:18px;margin:20px 0}.botd .tag{color:var(--g);font-weight:800;letter-spacing:.08em;font-size:12px}
.hype{display:flex;gap:6px;align-items:center;font-size:12px;margin:6px 0}.hype .bar{flex:1;height:10px;border-radius:99px;background:linear-gradient(90deg,#2ecc71,#f5c542,#ff5c5c);position:relative}.hype .pin{position:absolute;top:-4px;width:4px;height:18px;background:#fff;border-radius:2px}
.tmach input{width:100%;accent-color:var(--g)}.tmach .out{background:#0b121d;border-radius:8px;padding:8px 10px;font-size:14px;min-height:42px}
.fol{background:transparent;border:1px solid var(--bd);color:var(--tx);border-radius:99px;padding:6px 12px;cursor:pointer;font-size:13px}.fol.on{background:var(--y);color:#111;border-color:var(--y)}
.eli{display:none;background:#1d1a0d;border-left:4px solid var(--y);padding:8px 12px;border-radius:8px}body.kid .eli{display:block}body.kid .adult{display:none}
.switch{position:fixed;right:14px;bottom:14px;z-index:30;background:var(--card);border:1px solid var(--bd);border-radius:99px;padding:8px 14px;font-size:13px;box-shadow:0 6px 24px #0008;cursor:pointer}
.badge{position:fixed;left:14px;bottom:14px;z-index:30;background:var(--card);border:1px solid var(--g);border-radius:99px;padding:8px 14px;font-size:13px}
.prem{position:relative}.prem .lock{filter:blur(5px);user-select:none;pointer-events:none}.prem .cta2{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:6px;text-align:center}
.cd{font-variant-numeric:tabular-nums;font-weight:800;color:var(--g)}.price{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}.price .card ul{padding-left:18px;font-size:14px}.price .hot{border:2px solid var(--g)}
.poll button{display:block;width:100%;text-align:left;margin:6px 0;background:#0b121d;color:var(--tx);border:1px solid var(--bd);border-radius:10px;padding:10px;cursor:pointer;position:relative;overflow:hidden}.poll button i{position:absolute;left:0;top:0;bottom:0;background:#2ecc7133}.poll button span{position:relative}
@media(max-width:860px){.botd{grid-template-columns:1fr}.badge{font-size:11px;padding:6px 10px}.switch{font-size:11px;padding:6px 10px}}"""
JS3="""const LS=(k,v)=>v===undefined?JSON.parse(localStorage.getItem(k)||'null'):localStorage.setItem(k,JSON.stringify(v));
function kid(){document.body.classList.toggle('kid');LS('kid',document.body.classList.contains('kid'));(document.getElementById('kidb')||{}).textContent=document.body.classList.contains('kid')?'🧒 Explain like I\\'m 10: ON':'🧒 Explain like I\\'m 10'}
function tm(el,id){const t=JSON.parse(el.dataset.t);document.getElementById('tm-'+id).textContent=['In 1 year: ','In 3 years: ','In 5 years: '][el.value]+t[el.value]}
function fol(b,id){let w=LS('watch')||[];w=w.includes(id)?w.filter(x=>x!=id):[...w,id];LS('watch',w);paint()}
function paint(){const w=LS('watch')||[];document.querySelectorAll('.fol').forEach(b=>{const on=w.includes(b.dataset.id);b.classList.toggle('on',on);b.textContent=on?'★ Following':'☆ Follow this tech'});const r=LS('read')||[];const n=document.querySelectorAll('.ri[data-s]').length;const bd=document.getElementById('badge');if(bd&&n){const k=r.filter(x=>document.getElementById(x)).length;bd.textContent=(k>=n?'🏆 ':'📖 ')+'Read '+k+' of '+n+' · 🔥 '+(LS('streak')||{n:1}).n+'-day streak · ★ '+w.length}}
function streak(){const t=new Date().toDateString(),s=LS('streak')||{d:'',n:0};if(s.d!==t){const y=new Date(Date.now()-864e5).toDateString();s.n=s.d===y?s.n+1:1;s.d=t;LS('streak',s)}}
function vote(b,id,q){if(LS('vote'+q))return;LS('vote'+q,id);showPoll(q)}
function showPoll(q){const v=LS('vote'+q);document.querySelectorAll('.poll button').forEach(b=>{if(!v)return;const m=b.dataset.id==v;b.querySelector('i').style.width=m?'100%':'0';b.querySelector('span').textContent=(m?'✅ ':'')+b.dataset.t});const p=document.getElementById('pollmsg');if(p&&v)p.textContent='Thanks! Your pick is saved on this device. We\\'ll show how it played out in future issues.'}
function cds(){document.querySelectorAll('.cd').forEach(e=>{const d=Math.ceil((new Date(e.dataset.d)-new Date())/864e5);e.textContent=d>0?d+' days':'today/past'})}
addEventListener('DOMContentLoaded',()=>{streak();if(LS('kid'))kid();const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){const r=LS('read')||[];if(!r.includes(e.target.id)){r.push(e.target.id);LS('read',r);paint()}}}),{threshold:.6});document.querySelectorAll('.ri[data-s]').forEach(x=>io.observe(x));paint();cds();showPoll('q1')});"""
PREM="#premium"
def prem(html_,label):
    return f'<div class="prem"><div class="lock">{html_}</div><div class="cta2"><b>🔒 {label}</b><span class="meta">Included in Pro & Institutional</span><a class="btn" href="{PREM}">Unlock Premium</a></div></div>'
def hype_meter(h,ready):
    gap=h-ready;msg="Reality is catching up" if gap<=10 else "Some hype; watch for proof" if gap<=35 else "Mostly hype so far"
    col="#2ecc71" if gap<=10 else "#f5c542" if gap<=35 else "#ff5c5c"
    return f'<div class="kv"><b>🎢 Hype vs Reality</b></div><div class="hype"><span>Hype {h}</span><div class="bar"><div class="pin" style="left:{h}%"></div></div></div><div class="hype"><span>Reality {ready}</span><div class="bar" style="background:#1f2b3d"><div style="width:{ready}%;height:10px;border-radius:99px;background:#2ecc71"></div></div></div><div class="meta" style="color:{col}">{msg} (our judgment)</div>'
def botd_html(d,p=""):
    b=d.get("botd");
    if not b:return ""
    r=next(x for x in d["research"] if x["id"]==b["id"])
    return f'<div class="botd"><div><div class="tag">⭐ BREAKTHROUGH OF THE DAY · {d["date"]}</div><h2 style="margin:.3em 0">{E(r["title"])}</h2>{stb(r["stage"])}<p>{E(b["why"])}</p><a class="btn" href="{p}research.html#{r["id"]}">Read the 60-second version →</a></div><img class="art" style="margin:0" src="{p}assets/{r["id"]}.svg" alt="Concept illustration: {E(r["area"])}" loading="lazy" width="640" height="300"></div>'
def pricing():
    return '''<section id="premium"><h2>💎 Plans</h2><p class="lead">Read the radar for free. Teams that act on it early get the full briefings.</p><div class="price">
<div class="card"><h3>Free</h3><p class="metric">₹0 / $0</p><ul><li>Daily research radar</li><li>Stage, readiness, hype meter</li><li>Plain-English explainers</li></ul><a class="btn" href="#subscribe">Start free</a></div>
<div class="card hot"><h3>Pro</h3><p class="metric">From $150/mo</p><ul><li>Full executive briefings</li><li>Patent / IP risk notes</li><li>30-sec video scripts with citations</li><li>Watchlist alerts</li></ul><a class="btn" href="#subscribe">Join Pro waitlist</a></div>
<div class="card"><h3>Institutional</h3><p class="metric">Up to $500/mo</p><ul><li>Everything in Pro</li><li>360° technical teardowns & decks</li><li>Custom topics (quantum, bio, materials)</li><li>Team seats</li></ul><a class="btn" href="#subscribe">Talk to us</a></div></div><p class="meta">Placeholder plans. Payment and sign-up links coming soon.</p></section>'''
def poll(d):
    R={r["id"]:r for r in d["research"]}
    return '<section id="poll"><h2>🗳 Quick poll: which breakthrough makes money first?</h2><div class="card poll">'+"".join(f'<button data-id="{i}" data-t="{E(R[i]["title"])}" onclick="vote(this,\'{i}\',\'q1\')"><i></i><span>{E(R[i]["title"])}</span></button>' for i in d.get("poll",[]))+'<p class="meta" id="pollmsg">Tap one. Saved only on your device.</p></div></section>'
def countdowns(d):
    return '<section id="dates"><h2>⏳ Countdown to key dates</h2><div class="grid">'+"".join(f'<div class="card"><b>{E(t[1])}</b><div class="cd" data-d="{t[0].split(" ")[0]}"></div><span class="meta">{E(t[0])}'+(f' · <a href="{t[2]}" target="_blank" rel="noopener">source</a>' if len(t)>2 else '')+'</span></div>' for t in d.get("dates",[]))+'</div></section>'


# ---------- v4: daily / date-wise layer ----------
import re,datetime as _dt
_ORIG={"research":research,"results":results,"opps":opps,"shell":shell,"main":main}
ALL=[]  # issues oldest->newest, set in main4
def _oid(o): return re.sub(r'[^a-z0-9]+','-',o["name"].lower()).strip('-')
def annotate(issues):
    """Per-item first_seen / last_updated / history, plus diffs vs previous issue. Only real data from data/*.json."""
    hist={};ohist={};kp={}
    for i,d in enumerate(issues):
        prev=issues[i-1] if i else None
        d["_prev"]=prev["date"] if prev else None
        pr={r["id"]:r for r in prev["research"]} if prev else {}
        po={_oid(o):o for o in prev["opportunities"]} if prev else {}
        for r in d["research"]:
            h=hist.setdefault(r["id"],[]);old=pr.get(r["id"])
            changed=old is None or any(old.get(k)!=r.get(k) for k in ("stage","ready","found","watch","years"))
            h.append({"date":d["date"],"stage":r["stage"],"ready":r["ready"]})
            r["first_seen"]=h[0]["date"];r["history"]=list(h)
            r["last_updated"]=d["date"] if changed else (old or {}).get("last_updated",d["date"])
            r["_dr"]=None if old is None else r["ready"]-old["ready"]
            r["_ds"]=None if old is None else r["stage"]-old["stage"]
        for o in d["opportunities"]:
            k=_oid(o);o["id"]=k;h=ohist.setdefault(k,[]);old=po.get(k)
            h.append({"date":d["date"],"stage":o["stage"],"conv":o["conv"]})
            o["first_seen"]=h[0]["date"];o["history"]=list(h)
            o["last_updated"]=d["date"] if (old is None or old.get("stage")!=o["stage"] or old.get("catalyst")!=o["catalyst"] or old.get("conv")!=o["conv"]) else old.get("last_updated",d["date"])
            o["_ds"]=None if old is None else o["stage"]-old["stage"]
        pk={k[1]:k for k in (prev["results"]["kpis"] if prev else [])}
        d["_kpd"]={k[1]:(None if k[1] not in pk else (pk[k[1]][0]==k[0], pk[k[1]][0])) for k in d["results"]["kpis"]}
        d["_vhist"]={}
        for j in issues[:i+1]:
            for row in j["results"]["valuation"]["rows"]:d["_vhist"].setdefault(row[0],[]).append((j["date"],row[2],row[3]))
        d["_removed"]=[r["title"] for r in (prev["research"] if prev else []) if r["id"] not in {x["id"] for x in d["research"]}]
    return issues
FIRST='<div class="warn fi">🌱 <b>First issue — history starts today.</b> Change arrows, “moved up” alerts and day-over-day markers appear automatically once the next daily issue is published.</div>'
def datebar(d,fn,p):
    ds=[x["date"] for x in ALL];i=ds.index(d["date"]);slug={x["date"]:x["slug"] for x in ALL}
    lk=lambda dt:f'{p}{slug[dt]}/{fn}'
    pv=f'<a class="dbn" href="{lk(ds[i-1])}" aria-label="Previous issue">◀ {ds[i-1]}</a>' if i>0 else '<span class="dbn off" aria-disabled="true">◀ older</span>'
    nx=f'<a class="dbn" href="{lk(ds[i+1])}" aria-label="Next issue">{ds[i+1]} ▶</a>' if i<len(ds)-1 else '<span class="dbn off" aria-disabled="true">newer ▶</span>'
    opt="".join(f'<option value="{lk(x)}"{" selected" if x==d["date"] else ""}>{x}{" (latest)" if x==ds[-1] else ""}</option>' for x in reversed(ds))
    return (f'<div class="datebar" role="navigation" aria-label="Issue date">{pv}<label>📅 Issue <select aria-label="Choose issue date" onchange="location.href=this.value">{opt}</select></label>'
            f'<input type="date" aria-label="Jump to date" min="{ds[0]}" max="{ds[-1]}" value="{d["date"]}" onchange="jd(this.value)">{nx}<a class="dbn" href="{p}archive.html">🗓 Archive</a></div>'
            f'<div class="card wn" id="wn" data-issue="{d["date"]}" aria-live="polite"></div>'
            '<script>const ISS='+json.dumps({x:lk(x) for x in ds})+';function jd(v){const k=Object.keys(ISS).filter(x=>x<=v).pop()||Object.keys(ISS)[0];location.href=ISS[k]}</script>')
def shell(d,url,p,on,title,hero,body,toc):
    h=re.sub(r'<svg (?![^>]*role)','<svg role="img" aria-label="Chart: values shown in the labels" ',_ORIG["shell"](d,url,p,on,title,hero,body,toc))
    return h.replace('<div class="layout">',datebar(d,on,p)+'<div class="layout">',1).replace('</body>',f'<script>{JS4}</script></body>',1)
def _arrow(v,unit=""):
    if v is None: return '<span class="dd nw0" title="Not in previous issue">🆕 new</span>'
    if v>0: return f'<span class="dd up" title="vs previous issue">▲ +{v}{unit}</span>'
    if v<0: return f'<span class="dd dn" title="vs previous issue">▼ {v}{unit}</span>'
    return '<span class="dd eq" title="vs previous issue">= no change</span>'
def research(d,url,p):
    h=_ORIG["research"](d,url,p)
    for r in d["research"]:
        new=r["first_seen"]==d["date"]
        badge=(('<span class="pill newt">🆕 New today</span>' if new else f'<span class="pill">Tracked since {r["first_seen"]}</span>')+
               f' <span class="meta">Readiness vs prev: {_arrow(r["_dr"]) if d["_prev"] else "history starts today"}{(" · Stage <span class=\"dd up\">▲ S"+str(r["stage"]-r["_ds"])+"→S"+str(r["stage"])+"</span>") if (r["_ds"] or 0)>0 else ""} · Updated {r["last_updated"]}</span>'+
               ('<div class="meta">History: '+" → ".join(f'{x["date"][5:]} S{x["stage"]}/{x["ready"]}' for x in r["history"])+'</div>' if len(r["history"])>1 else ''))
        h=re.sub(rf'(<article class="card ri" id="{r["id"]}" data-s="\d")([^>]*>)',lambda m:f'{m.group(1)} data-f="{r["first_seen"]}" data-u="{r["last_updated"]}" data-a="{E(r["area"])}"{m.group(2)}<div class="dline">{badge}</div>',h,count=1)
    areas=sorted({r["area"] for r in d["research"]})
    ds=sorted({x["date"] for x in ALL if x["date"]<=d["date"]})
    feed="".join(f'<li><b>{x["date"]}</b> — {sum(1 for r in x["research"] if r["first_seen"]==x["date"])} new, {sum(1 for r in x["research"] if r["last_updated"]==x["date"] and r["first_seen"]!=x["date"])} updated'+(f', moved up: {", ".join(E(r["area"]) for r in x["research"] if (r["_ds"] or 0)>0)}' if any((r["_ds"] or 0)>0 for r in x["research"]) else '')+f' · <a href="{p}{x["slug"]}/research.html">open</a></li>' for x in reversed([x for x in ALL if x["date"]<=d["date"]]))
    flt=(f'<div class="card fbar"><b>🔎 Filter</b> <label>From <input type="date" id="f1" value="{ds[0]}" onchange="rf()"></label> <label>To <input type="date" id="f2" value="{d["date"]}" onchange="rf()"></label> '
         '<label>Topic <select id="ft" onchange="rf()"><option value="">All topics</option>'+"".join(f'<option>{E(a)}</option>' for a in areas)+'</select></label> '
         '<label><input type="checkbox" id="fn" onchange="rf()"> New today only</label> <span class="meta" id="fc"></span></div>')
    tl=f'<section id="timeline"><h2>🗞 Daily timeline</h2>{"" if d["_prev"] else FIRST}<ol class="tl">{feed}</ol></section>'
    h=h.replace('<section id="items">',tl+'<section id="items">',1).replace('<div class="tabs">'+'<button class="on" onclick="fr(this,0)">',flt+'<div class="tabs">'+'<button class="on" onclick="fr(this,0)">',1)
    h=h.replace('<script>function fr(b,n){','<script>let FS=0;function rf(){const a=f1.value,b=f2.value,t=ft.value,n=fn.checked;let c=0;document.querySelectorAll(".ri[data-f]").forEach(x=>{const ok=(!FS||x.dataset.s==FS)&&(!t||x.dataset.a==t)&&(!a||x.dataset.u>=a)&&(!b||x.dataset.f<=b)&&(!n||x.querySelector(".newt"));x.style.display=ok?"":"none";c+=ok});fc.textContent=c+" shown"}function fr(b,n){FS=n;document.querySelectorAll("#items .tabs button").forEach(x=>x.classList.remove("on"));b.classList.add("on");rf();return;',1)
    h=h.replace('("items","Papers & patents")','("timeline","Daily timeline"),("items","Papers & patents")')
    h=h.replace('<a href="#items">Papers &amp; patents</a>','<a href="#timeline">Daily timeline</a><a href="#items">Papers &amp; patents</a>').replace('<a href="#items">Papers & patents</a>','<a href="#timeline">Daily timeline</a><a href="#items">Papers & patents</a>',1)
    return h
def _cal(evs,start,months=4):
    """evs: {iso:[label]} -> month grids"""
    out=[];y,m=start.year,start.month
    for _ in range(months):
        f=_dt.date(y,m,1);nd=(_dt.date(y+(m==12),m%12+1,1)-f).days
        cells=['<span></span>']*f.weekday()
        for dd in range(1,nd+1):
            k=f"{y}-{m:02d}-{dd:02d}";e=evs.get(k)
            cells.append(f'<span class="cd1{" ev" if e else ""}" title="{E("; ".join(e)) if e else k}">{dd}</span>')
        out.append(f'<div class="mcal"><b>{f.strftime("%b %Y")}</b><div class="mg">'+"".join(f'<i>{w}</i>' for w in "MTWTFSS")+"".join(cells)+'</div></div>')
        y,m=(y+1,1) if m==12 else (y,m+1)
    return '<div class="cals">'+"".join(out)+'</div>'
def results(d,url,p):
    h=_ORIG["results"](d,url,p)
    for v,l,dl,c,s in d["results"]["kpis"]:
        k=d["_kpd"].get(l);mk=('<span class="dd eq">= same as prev issue</span>' if k[0] else f'<span class="dd up">changed (was {E(k[1])})</span>') if k else ('' if not d["_prev"] else '<span class="dd nw0">🆕 new metric</span>')
        h=h.replace(f'<div class="v">{E(v)}</div>{E(l)}{src(s)}',f'<div class="v">{E(v)}</div>{E(l)}{src(s)}<div>{mk}</div>',1)
    if not d["_prev"]:h=h.replace('<section id="numbers"><h2>Key numbers</h2>','<section id="numbers"><h2>Key numbers</h2><p class="meta">🌱 First issue: day-over-day change markers start with the next issue.</p>',1)
    X=d["results"];evs={}
    for t in X["dates"]:
        if re.match(r'\d{4}-\d\d-\d\d$',t[0]):evs.setdefault(t[0],[]).append(t[1])
    for t in d.get("dates",[]):evs.setdefault(t[0],[]).append(t[1])
    est="".join(f'<li>{E(a)} — {E(x)}{src(s)}</li>' for a,x,s in X["dates"] if not re.match(r'\d{4}-\d\d-\d\d$',a))
    cal=f'<section id="cal"><h2>🗓 Earnings & events calendar</h2><p class="lead">Highlighted days have a confirmed date (hover/tap for detail). Estimated dates are listed below and are <b>not</b> confirmed by the companies.</p><div class="card">{_cal(evs,_dt.date.fromisoformat(d["date"]))}<ul class="cap">{est}</ul></div></section>'
    hist="".join(f'<tr><td>{E(c)}</td><td>'+(" → ".join(f'{dt}: {E(mc)} · P/E {E(pe)}' for dt,mc,pe in rows))+'</td></tr>' for c,rows in d["_vhist"].items())
    hs=f'<section id="hist"><h2>📈 Results history per company</h2>{"" if d["_prev"] else FIRST}<div class="card tw"><table><tr><th>Company</th><th>Market cap & forward P/E by issue</th></tr>{hist}</table><div class="cap">Third-party valuation snapshot {src(9)}; one entry per daily issue.</div></div></section>'
    h=h.replace('<section id="dates">',cal+hs+'<section id="dates">',1)
    h=h.replace('<a href="#dates">','<a href="#cal">Calendar</a><a href="#hist">History</a><a href="#dates">',1)
    return h
def opps(d,url,p):
    h=_ORIG["opps"](d,url,p)
    for o in d["opportunities"]:
        sh=" → ".join(f'S{x["stage"]} ({x["date"][5:]})' for x in o["history"])
        mv='' if o["_ds"] is None or o["_ds"]==0 else (' <span class="dd up">⬆ moved up</span>' if o["_ds"]>0 else ' <span class="dd dn">⬇ moved down</span>')
        h=h.replace(f'<tr data-s="{o["stage"]}" data-r="{E(o["region"])}" data-c="{o["conv"]}"><td>{stb(o["stage"])}</td><td><b>{E(o["name"])}</b></td>',
            f'<tr data-s="{o["stage"]}" data-r="{E(o["region"])}" data-c="{o["conv"]}" data-f="{o["first_seen"]}" data-u="{o["last_updated"]}" data-f-new="{int(o["first_seen"]==d["date"])}"><td>{stb(o["stage"])}{mv}<div class="meta">{sh}</div></td><td><b>{E(o["name"])}</b><div class="meta">Added {o["first_seen"]}{" 🆕" if o["first_seen"]==d["date"] else ""}{(lambda n:f" <sup><a href=results.html#s{n}>[source {n}]</a></sup>" if n else "")(o.get("src"))}</div></td>',1)
    ups=[o for o in d["opportunities"] if (o["_ds"] or 0)>0]
    al=(f'<div class="card alert"><b>🚀 Moved up since {d["_prev"]}:</b> '+", ".join(f'{E(o["name"])} (S{o["stage"]-o["_ds"]}→S{o["stage"]})' for o in ups)+'</div>') if ups else (FIRST if not d["_prev"] else f'<div class="card">No stage moves since {d["_prev"]}.</div>')
    ds=sorted({o["first_seen"] for o in d["opportunities"]})
    df='<div class="tabs" data-k="fnew"><span class="meta">Added: </span><button class="on" onclick="fo(this)">All</button><button onclick="fo(this)" data-v="1">This issue</button><button onclick="fo(this)" data-v="0">Earlier</button></div>'
    h=h.replace('<div class="card tw"><table id="opp">',al+df+'<div class="card tw"><table id="opp">',1)
    h=h.replace('F[t.dataset.k]=b.textContent;','F[t.dataset.k]=b.dataset.v??b.textContent;',1).replace('<th>Company</th>','<th>Company (date added)</th>',1)
    h=h.replace('v=="All"||r.dataset[k]==v','v=="All"||r.dataset[k=="fnew"?"fNew":k]==v',1)
    return h
def archive(issues):
    evs={}
    for x in issues:evs[x["date"]]=(x,sum(1 for r in x["research"] if r["last_updated"]==x["date"])+sum(1 for o in x["opportunities"] if o["last_updated"]==x["date"]))
    st=_dt.date.fromisoformat(issues[0]["date"]);en=_dt.date.fromisoformat(issues[-1]["date"])
    mx=max(v[1] for v in evs.values()) or 1;out=[];y,m=st.year,st.month
    while (y,m)<=(en.year,en.month):
        f=_dt.date(y,m,1);nd=(_dt.date(y+(m==12),m%12+1,1)-f).days;cells=['<span></span>']*f.weekday()
        for dd in range(1,nd+1):
            k=f"{y}-{m:02d}-{dd:02d}"
            if k in evs:
                x,n=evs[k];lv=1+int(3*n/mx-1e-9)
                cells.append(f'<a class="hm l{lv}" href="{x["slug"]}/research.html" title="{k}: {n} new/updated items" aria-label="{k}: {n} new or updated items">{dd}</a>')
            else: cells.append(f'<span class="hm l0" title="{k}: no issue">{dd}</span>')
        out.append(f'<div class="mcal"><b>{f.strftime("%B %Y")}</b><div class="mg">'+"".join(f'<i>{w}</i>' for w in "MTWTFSS")+"".join(cells)+'</div></div>')
        y,m=(y+1,1) if m==12 else (y,m+1)
    rows="".join(f'<tr><td><b>{x["date"]}</b></td><td>{E(x["title"])}</td><td>{evs[x["date"]][1]}</td><td><a href="{x["slug"]}/research.html">Research</a> · <a href="{x["slug"]}/results.html">Results</a> · <a href="{x["slug"]}/opportunities.html">Opportunities</a></td></tr>' for x in reversed(issues))
    L=issues[-1]
    hh=head("Archive: every daily issue on a calendar","Browse every FrontierRadar daily issue on a calendar heatmap. Darker days had more new or updated research items.",BASE+"archive.html")+nav()
    hh+=f'<div class="hero"><div style="max-width:1200px;margin:0 auto"><span class="pill">🗓 Archive</span><h1>Every issue, day by day</h1><p class="hook">Darker squares = more new or updated papers, patents and opportunities that day. Tap a day to open it.</p></div></div>'
    hh+=f'<main style="max-width:1100px;margin:0 auto;padding:20px">{FIRST if len(issues)==1 else ""}<div class="card"><div class="cals">{"".join(out)}</div><div class="cap">Legend: <span class="hm l0">·</span> no issue <span class="hm l1">·</span> few <span class="hm l3">·</span> many changes</div></div><h2>All issues</h2><div class="card tw"><table><tr><th>Date</th><th>Title</th><th>New/updated</th><th>Open</th></tr>{rows}<tr><td><b>2026-10-28</b></td><td>5 AI-chip breakthroughs (original first issue)</td><td>5</td><td><a href="breakthroughs.html">Open</a></td></tr></table></div></main><footer>Not investment advice. © 2026 FrontierRadar. · <a href="feed.xml">RSS</a></footer><script>{JS}{JS3}{JS4}</script></body></html>'
    open("archive.html","w").write(hh)
CSS3+=""".datebar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;max-width:1200px;margin:14px auto 0;padding:0 20px}.datebar select,.datebar input,.fbar input,.fbar select{background:#0c1422;color:var(--tx);border:1px solid var(--bd);border-radius:8px;padding:6px;font:inherit;min-height:36px}
.dbn{border:1px solid var(--bd);border-radius:99px;padding:6px 12px;color:var(--tx);text-decoration:none;min-height:24px}.dbn.off{opacity:.45}.wn{max-width:1160px;margin:10px auto 0;display:none}.wn.show{display:block}
.dd{font-weight:700;font-size:.85em;margin-left:4px}.dd.up{color:#2ecc71}.dd.dn{color:#ff7b7b}.dd.eq{color:#9fb4d0}.dd.nw0{color:#f5c542}.newt{background:#2ecc7133;color:#2ecc71}.ri.nv{outline:2px solid #f5c542}
.dline{margin:6px 0}.fbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:10px 0}.tl{border-left:2px solid var(--bd);padding-left:18px}.tl li{margin:6px 0}.alert{border-left:4px solid #2ecc71;margin:10px 0}.fi{margin:10px 0}
.cals{display:flex;flex-wrap:wrap;gap:18px}.mcal{min-width:220px}.mg{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-top:6px}.mg i{font-style:normal;color:var(--tx3);font-size:.75em;text-align:center}.mg span,.mg a{text-align:center;font-size:.8em;padding:5px 0;border-radius:5px;background:#0f1a2b;color:var(--tx2);text-decoration:none}
.cd1.ev{background:#4da3ff;color:#04111f;font-weight:800}.hm.l0{background:#0f1a2b}.hm.l1{background:#1d5c3a;color:#fff}.hm.l2{background:#25a05a;color:#fff}.hm.l3{background:#2ecc71;color:#04111f;font-weight:800}.hm{display:inline-block;min-width:22px}
@media(max-width:700px){.datebar{padding:0 12px}.datebar input[type=date]{display:none}}"""
JS4="""(function(){const w=document.getElementById('wn');if(!w)return;const K='lv_'+(location.pathname.split('/').pop()||'index.html'),iss=w.dataset.issue,lv=LS(K);let n=0;
document.querySelectorAll('[data-f]').forEach(x=>{const u=x.dataset.u||x.dataset.f;if(lv&&u>lv){x.classList.add('nv');n++}});
w.innerHTML=lv?(n?`✨ <b>What's new since your last visit (${lv}):</b> ${n} item${n>1?'s':''} new or updated — outlined in yellow.`:`✅ Nothing new on this page since your last visit (${lv}).`):`👋 <b>First visit?</b> We'll remember today and highlight what's new next time you come back.`;w.classList.add('show');
if(!lv||iss>lv)LS(K,iss)})();"""
def main():
    global ALL
    ALL=annotate(sorted((json.load(open(f)) for f in glob.glob("data/20[0-9][0-9]-*.json")),key=lambda d:d["date"]))
    _ORIG["main"]()
    archive(ALL)
    ix=open("index.html").read().replace('<h2 id="archive">🗂 Archive</h2>','<h2 id="archive">🗂 Archive <a class="dbn" style="font-size:.6em" href="archive.html">🗓 Calendar view</a></h2>',1)
    L=ALL[-1];nw=sum(1 for r in L["research"] if r["first_seen"]==L["date"])
    ix=ix.replace('<main style="max-width:1100px;margin:0 auto;padding:20px">',f'<main style="max-width:1100px;margin:0 auto;padding:20px"><div class="card wn" id="wn" data-issue="{L["date"]}" aria-live="polite"></div><p class="meta">Today ({L["date"]}): {nw} new research items{" — first issue, history starts today" if not L["_prev"] else ""} · <a href="archive.html">all issues</a></p>',1).replace('</body>',f'<script>{JS4}</script></body>',1)
    open("index.html","w").write(ix)
    sm=open("sitemap.xml").read().replace(f"<url><loc>{BASE}research.html</loc></url>",f"<url><loc>{BASE}archive.html</loc></url><url><loc>{BASE}research.html</loc></url>",1)
    open("sitemap.xml","w").write(sm)
    json.dump({x["date"]:{"research":{r["id"]:{k:r[k] for k in ("first_seen","last_updated","history")} for r in x["research"]},"opportunities":{o["id"]:{k:o[k] for k in ("first_seen","last_updated","history")} for o in x["opportunities"]}} for x in ALL},open("history.json","w"),indent=1)


# ---------- v5: methodology, bear case, track record, persona UX ----------
W={"evidence":55,"manufacturable":20,"supply_chain":10,"backing":10,"groups":5}
EPCT=[0,10,25,45,75,100]
ELAB=["Paper / simulation only","Lab demo","Working prototype chip","Customer samples / qualification","Volume production or orders","Revenue at scale"]
CRIT={"evidence":("Evidence level","How far along the proof is (TRL-style ladder).",ELAB),
 "manufacturable":("Manufacturability","0 = exotic materials no fab can make; 5 = runs on today's standard lines.",None),
 "supply_chain":("Supply chain","0 = tools/materials don't exist; 5 = mature suppliers ready.",None),
 "backing":("Corporate backing","0 = academic only; 2 = funded startup; 3 = big-company R&D; 5 = several big firms committing capex.",None),
 "groups":("Independent groups","1 = one lab; 5 = industry-wide effort.",None)}
YRS=["6-10","4-8","3-6","2-4","0-2","now"]
def score_item(r):
    sc=r["score"];E_=sc["evidence"]
    parts={k:round(W[k]*(EPCT[E_]/100 if k=="evidence" else sc[k]/5),1) for k in W}
    r["ready"]=round(sum(parts.values()));r["_parts"]=parts
    r["stage"]=1 if E_<=1 else 2 if E_<=3 else 3 if E_==4 else 4
    lo,hi=map(int,YRS[E_].split("-")) if "-" in YRS[E_] else (0,0)
    if E_<=2 and sc["manufacturable"]<=1: lo,hi=lo+2,hi+2
    if E_<=2 and sc["manufacturable"]>=4: lo,hi=max(0,lo-2),max(1,hi-2)
    r["years"]=YRS[E_] if E_==5 else f"{lo}-{hi}"
    r["hype"]=10*sc["claim_boldness"]+10*sc["attention"]
    ipx=(sc["ip_crowding"]+sc["ip_litigation"])/2;r["_ipl"]="High" if ipx>=3.5 else "Medium" if ipx>=2 else "Low"
def score_opp(o,R):
    rs=[R[l]["ready"] for l in o["links"]];avg=sum(rs)/len(rs);sc=o["score"]
    v=round(0.4*avg+0.4*20*sc["exposure"]+0.2*20*sc["execution"]);o["_cs"]=v;o["_avg"]=round(avg)
    o["conv"]="Watch" if (not sc["investable"] or sc["exposure"]<=1) else "Speculative" if (sc["execution"]<=1 or v<45) else "High" if v>=65 else "Medium"
_annot4=annotate
def annotate(issues):
    for d in issues:
        for r in d["research"]:
            if "score" in r: score_item(r)
        R={r["id"]:r for r in d["research"]}
        for o in d["opportunities"]:
            if "score" in o: score_opp(o,R)
    return _annot4(issues)
GLX=[["CPO","Co-packaged optics: putting the light-based data link right next to the chip"],["photonics","Using light (photons) instead of electricity to move or compute data"],["neuromorphic","Chips wired like brain cells (neurons) that fire only when needed"],["substrate","The base board a chip sits on"],["chiplets","Small chips combined into one package like Lego blocks"],["analog","Computing with continuous signals instead of 0s and 1s"]]
def _gl(d,h):
    G=list(d["glossary"])+GLX
    i=h.find('<main');head_,body=h[:i],h[i:]
    for t,dfn in G:
        parts=re.split(r'(<[^>]+>)',body);done=False;skip=0
        for j,pt in enumerate(parts):
            if pt.startswith('<'):
                if re.match(r'<(a|h[1-6]|button|summary|option|script|style|abbr|th|label)\b',pt):skip+=1
                elif re.match(r'</(a|h[1-6]|button|summary|option|script|style|abbr|th|label)>',pt):skip=max(0,skip-1)
                continue
            if done or skip: continue
            m=re.search(rf'\b{re.escape(t)}\b',pt,re.I)
            if m:parts[j]=pt[:m.start()]+f'<abbr class="gl" tabindex="0" title="{E(dfn)}" data-d="{E(dfn)}">{m.group(0)}</abbr>'+pt[m.end():];done=True
        body="".join(parts)
    return head_+body
def _rt(h,sec):
    m=re.search(rf'<section id="{sec}"(.*?)</section>',h,re.S)
    if not m:return h
    w=len(re.sub(r'<[^>]+>',' ',m.group(1)).split());mins=max(1,round(w/200))
    return h.replace(f'<section id="{sec}">',f'<section id="{sec}"><span class="rt">⏱ {mins} min read</span>',1)
def bearhtml(items,p):
    return "".join(f'<li>{E(t)}'+(f' <a href="{u}" target="_blank" rel="noopener">source</a>' if u else ' <span class="meta">(judgment)</span>')+'</li>' for t,u in items)
WN='<p class="kv"><b>👀 What to watch next:</b>'
_res4=research
def research(d,url,p):
    h=_res4(d,url,p);O=d["opportunities"]
    for r in d["research"]:
        pr=r.get("prev_scores",{});pa=r.get("_parts",{})
        if not pa: continue
        rows="".join(f'<tr><td>{CRIT[k][0]}</td><td>{r["score"][k]}/5'+(f' — {ELAB[r["score"][k]]}' if k=="evidence" else '')+f'</td><td>{W[k]}%</td><td><b>{pa[k]}</b></td></tr>' for k in W)
        chg=(f'<p class="meta">Re-scored 2026-10-29 with the formula: readiness {pr["ready"]} → <b>{r["ready"]}</b>, hype {pr["hype"]} → <b>{r["hype"]}</b>, years {E(pr["years"])} → <b>{E(r["years"])}</b>.</p>' if pr and (pr["ready"]!=r["ready"] or pr["hype"]!=r["hype"] or pr["years"]!=r["years"]) else '')
        how=(f'<details class="how"><summary>📐 How we scored this</summary><div class="tw"><table><tr><th>Criterion</th><th>Score</th><th>Weight</th><th>Points</th></tr>{rows}<tr><td colspan=3><b>Readiness</b></td><td><b>{r["ready"]}/100</b></td></tr></table></div>'
             f'<p class="meta">Hype = 10×claim boldness ({r["score"]["claim_boldness"]}/5) + 10×attention ({r["score"]["attention"]}/5) = {r["hype"]}. Patent/IP risk: <b>{r["_ipl"]}</b> (crowding {r["score"]["ip_crowding"]}/5, litigation {r["score"]["ip_litigation"]}/5). Sub-scores are our judgment from the linked sources. <a href="{p}methodology.html">Full method</a></p>{chg}</details>')
        opp=[o["name"] for o in O if r["id"] in o["links"]]
        sw=f'<p class="sowhat">💰 <b>So what for investors:</b> {"Companies tied to this: "+", ".join(E(x) for x in opp[:4])+"." if opp else "No listed company is directly tied yet."} {"Too early for revenue — a watch-list item." if r["stage"]<=1 else "Proof is building; watch for customer orders." if r["stage"]==2 else "Orders and factories exist; this can show up in results within ~2 years."} <span class="meta">(our judgment, not advice)</span></p>'
        bb=f'<div class="bb"><div class="bull"><b>🐂 Bull case</b><p>{E(r["found"].split(". ")[0].rstrip("."))}.</p><p class="meta">Who could win: {E(", ".join(r["win"][:3]))}</p></div><div class="bear"><b>🐻 What could go wrong</b><ul>{bearhtml(r.get("bear",[]),p)}</ul></div></div>'
        m=re.search(rf'<article class="card ri" id="{r["id"]}".*?'+re.escape(WN),h,re.S)
        if m:
            seg=m.group(0);h=h.replace(seg,seg[:-len(WN)]+sw+bb+how+WN,1)
    for sec in ("pipe","map","timeline","items","poll","dates"):h=_rt(h,sec)
    return _gl(d,h)
_opp4=opps
def opps(d,url,p):
    h=_opp4(d,url,p)
    for o in d["opportunities"]:
        if "_cs" not in o: continue
        sc=o["score"];chg=f' (was {o["prev_conv"]})' if o.get("prev_conv") and o["prev_conv"]!=o["conv"] else ''
        x=(f'<details class="how"><summary>🐂 vs 🐻 + score</summary><p><b>🐂</b> {E(o["catalyst"])}.</p><ul>{bearhtml(o.get("bear",[]),p)}</ul>'
           f'<p class="meta">Conviction score {o["_cs"]} = 0.4×linked readiness {o["_avg"]} + 0.4×20×exposure {sc["exposure"]}/5 + 0.2×20×execution {sc["execution"]}/5 → {o["conv"]}{chg}. {"Not directly investable → Watch. " if not sc["investable"] else ""}Our judgment.</p></details>')
        h=re.sub(rf'(<tr data-s="{o["stage"]}" data-r="{re.escape(E(o["region"]))}" data-c="{o["conv"]}" data-f="[^"]*" data-u="[^"]*" data-f-new="\d"><td>.*?<b>{re.escape(E(o["name"]))}</b>.*?)(<td style="color:#ff9b9b">[^<]*)(</td>)',lambda m:m.group(1)+m.group(2)+x+m.group(3),h,count=1,flags=re.S)
    return _gl(d,_rt(h,"table"))
_res_r4=results
def results(d,url,p): return _gl(d,_res_r4(d,url,p))
BNAV=[("index.html","🏠","Home"),("research.html","🔬","Research"),("results.html","📊","Results"),("opportunities.html","🎯","Opps"),("methodology.html","📐","Method")]
def ux(h,p,on):
    bn='<nav class="bnav" aria-label="Main (mobile)">'+"".join(f'<a href="{p}{f}"{" class=on aria-current=page" if f==on else ""}><span>{i}</span>{t}</a>' for f,i,t in BNAV)+'</nav><a href="#" class="totop" aria-label="Back to top" onclick="scrollTo({top:0,behavior:\'smooth\'});return false">↑</a>'
    h=re.sub(r'(<nav class="mn">.*?)(</nav>)',lambda m:m.group(1)+f'<a class="m x{" on" if on=="methodology.html" else ""}" href="{p}methodology.html">📐 Method</a><a class="m x{" on" if on=="track-record.html" else ""}" href="{p}track-record.html">📈 Track record</a>'+m.group(2),h,count=1,flags=re.S)
    h=re.sub(r'(<nav class="mn">.*?</nav>)',lambda m:re.sub(r'href="(research|results|opportunities)\.html"',lambda k:f'href="{p if p else ""}{k.group(1)}.html"' if False else k.group(0),m.group(1)),h,count=1,flags=re.S)
    return h.replace('</body>',bn+'</body>',1)
_shell4=shell
def shell(d,url,p,on,title,hero,body,toc):
    return ux(_shell4(d,url,p,on,title,hero,body,toc),p,on)
def page(fn,title,desc,hero,body):
    h=head(title,desc,BASE+fn)+nav("",fn)+f'<div class="hero"><div style="max-width:1100px;margin:0 auto">{hero}</div></div><main style="max-width:1000px;margin:0 auto;padding:20px">{body}</main><footer>Not investment advice. Scores are FrontierRadar editorial judgment using the published method. © 2026 FrontierRadar.</footer><script>{JS}{JS3}</script></body></html>'
    return ux(h,"",fn)
def methodology(L):
    ex=[r for r in L["research"] if r["id"]=="hybridbond"][0];pa=ex["_parts"]
    crit="".join(f'<tr><td><b>{CRIT[k][0]}</b></td><td>{W[k]}%</td><td>{E(CRIT[k][1])}</td></tr>' for k in W)
    lad="".join(f'<li><b>{x}</b> → {EPCT[i]}% of the evidence weight · Stage {1 if i<=1 else 2 if i<=3 else 3 if i==4 else 4} · years-to-market {YRS[i]}</li>' for i,x in enumerate(ELAB))
    chg="".join(f'<tr><td>{E(r["title"][:52])}</td><td>{r["prev_scores"]["ready"]} → <b>{r["ready"]}</b></td><td>{r["prev_scores"]["hype"]} → <b>{r["hype"]}</b></td><td>{E(r["prev_scores"]["years"])} → <b>{E(r["years"])}</b></td><td>S{r["prev_scores"]["stage"]} → S{r["stage"]}</td></tr>' for r in L["research"] if "prev_scores" in r)
    oc="".join(f'<tr><td>{E(o["name"])}</td><td>{o["prev_conv"]} → <b>{o["conv"]}</b></td><td>{o["_cs"]}</td></tr>' for o in L["opportunities"] if o.get("prev_conv") and o["prev_conv"]!=o["conv"])
    body=f"""<section id="why"><h2>Why a formula?</h2><p class="lead">So you can check our work. Every score on this site comes from the same recipe below. Anyone with the sources can reproduce it, and argue with our inputs.</p></section>
<section id="ready"><h2>1. Readiness (0-100): how close to making money</h2><div class="card tw"><table><tr><th>Criterion</th><th>Weight</th><th>How we score it (0-5)</th></tr>{crit}</table></div>
<h3>Evidence ladder (the biggest weight)</h3><ol start="0" class="card" style="padding-left:34px">{lad}</ol><p class="meta">Readiness = sum of weight × (sub-score ÷ 5). Evidence uses the ladder % instead, because going from samples to volume is a far bigger jump than from paper to demo.</p></section>
<section id="other"><h2>2. Other scores</h2><div class="grid">
<div class="card"><b>🧪 Stage</b><p>Set by evidence only: 0-1 → Stage 1 Paper, 2-3 → Stage 2 Prototype, 4 → Stage 3 Factories & orders, 5 → Stage 4 Revenue.</p></div>
<div class="card"><b>⏳ Years to market</b><p>From the evidence ladder. Early items (evidence 0-2) get +2 years if manufacturability is 0-1, or −2 years if it already runs on standard lines (4-5).</p></div>
<div class="card"><b>🎢 Hype vs Reality</b><p>Hype = 10 × claim boldness (0-5; "1000× faster" = 5) + 10 × attention (0-5: press, funding, famous backers). Gap = Hype − Readiness: up to 10 = reality catching up, up to 35 = some hype, more = mostly hype.</p></div>
<div class="card"><b>⚖️ Patent / IP risk</b><p>Average of crowding (how many patent holders, 0-5) and litigation history (0-5): 3.5+ High, 2+ Medium, else Low. Not legal advice.</p></div>
<div class="card"><b>🎯 Conviction (opportunities)</b><p>Score = 0.4 × average readiness of linked research + 0.4 × 20 × exposure (share of the business riding on it, 0-5) + 0.2 × 20 × execution (track record, balance sheet, 0-5). 65+ High, 45-64 Medium, under 45 Speculative. Not directly investable, or exposure 0-1 → Watch. Execution 0-1 (e.g. pre-profit, funding risk) caps it at Speculative.</p></div></div></section>
<section id="example"><h2>3. Worked example: {E(ex["title"])}</h2><div class="card tw"><table><tr><th>Criterion</th><th>Sub-score</th><th>Points</th></tr>{"".join(f'<tr><td>{CRIT[k][0]}</td><td>{ex["score"][k]}/5</td><td>{pa[k]}</td></tr>' for k in W)}<tr><td colspan=2><b>Readiness</b></td><td><b>{ex["ready"]}</b></td></tr></table><p class="meta">Evidence 4 ("{ELAB[4]}"): Applied Materials is raising its Besi stake and hybrid-bonding tools are being ordered, but SK hynix says the method is not ready for HBM4E memory, so we stop short of 5. Result: Stage 3, {ex["years"]} years. Hype {ex["hype"]} vs readiness {ex["ready"]}: reality is ahead of the hype.</p></div></section>
<section id="changes"><h2>4. Re-score on 2026-10-29: what changed</h2><p class="lead">Our first issue used expert judgment directly. Re-running every item through this formula moved these numbers. {"Stage changes: "+", ".join(E(r["area"])+" S"+str(r["prev_scores"]["stage"])+"→S"+str(r["stage"]) for r in L["research"] if r["prev_scores"]["stage"]!=r["stage"])+"." if any(r["prev_scores"]["stage"]!=r["stage"] for r in L["research"]) else "No stage changed."}</p><div class="card tw"><table><tr><th>Item</th><th>Readiness</th><th>Hype</th><th>Years</th><th>Stage</th></tr>{chg}</table></div>
<h3>Conviction changes</h3><div class="card tw"><table><tr><th>Company</th><th>Conviction</th><th>Score</th></tr>{oc or '<tr><td colspan=3>None</td></tr>'}</table></div></section>
<section id="data"><h2>5. Data sources & update cadence</h2><ul class="card"><li>Papers: Nature-family journals, arXiv, AIP and conference proceedings (IEDM, ISSCC).</li><li>Patents: Google Patents and patent-analytics sites.</li><li>Company facts: SEC filings, investor-relations releases, earnings reports.</li><li>Counter-evidence: trade press, reviews and company filings, always linked in each "What could go wrong" box.</li><li>Cadence: one issue per day when there is news. Each item keeps first-seen, last-updated and history, and every call is logged on the <a href="track-record.html">Track record</a>.</li></ul></section>
<section id="limits"><h2>6. Limitations (please read)</h2><ul class="card"><li>Sub-scores are human judgment. Two careful analysts could differ by ±1 on any criterion (about ±10 readiness points).</li><li>Weights are our choice, not a statistically validated model. Any change to them will be published here.</li><li>Press releases overstate; papers under-report failures. A missing bear source does not mean low risk.</li><li>We have no access to private company data, customer contracts or patent claim charts.</li><li>Conviction is about the research-to-revenue story, not share price or valuation.</li></ul><p class="warn">⚠️ Not investment, legal or financial advice. Do your own research and consult a registered adviser.</p></section>"""
    open("methodology.html","w").write(page("methodology.html","Methodology: how we score every breakthrough","The transparent, repeatable formula behind FrontierRadar readiness, hype, stage, IP risk and conviction scores.",'<span class="pill">📐 Methodology</span><h1>How we score: open recipe, no black box</h1><p class="hook">Every number on FrontierRadar comes from one published formula. Here it is, with a worked example and its limits.</p>',body))
def track(issues):
    fn="data/track_record.json";T=json.load(open(fn)) if os.path.exists(fn) else []
    seen={(t["date"],t["kind"],t["id"]) for t in T}
    for d in issues:
        for r in d["research"]:
            k=(d["date"],"research",r["id"])
            if k not in seen:T.append({"date":d["date"],"kind":"research","id":r["id"],"name":r["title"],"stage":r["stage"],"ready":r["ready"],"call":f'Readiness {r["ready"]}, {r["years"]} yrs to market',"outcome":"pending"});seen.add(k)
        for o in d["opportunities"]:
            k=(d["date"],"opp",o["id"])
            if k not in seen:T.append({"date":d["date"],"kind":"opp","id":o["id"],"name":o["name"],"stage":o["stage"],"ready":o.get("_avg"),"call":f'{o["conv"]} conviction',"outcome":"pending"});seen.add(k)
    json.dump(T,open(fn,"w"),indent=1,ensure_ascii=False)
    rows="".join(f'<tr data-k="{t["kind"]}"><td>{t["date"]}</td><td>{"🔬" if t["kind"]=="research" else "🎯"} {E(t["name"])}</td><td>S{t["stage"]}</td><td>{t["ready"] if t["ready"] is not None else "—"}</td><td>{E(t["call"])}</td><td><span class="pill">{E(t["outcome"])}</span></td></tr>' for t in sorted(T,key=lambda t:(t["date"],t["kind"]),reverse=True))
    st=min(t["date"] for t in T)
    body=f'<div class="warn fi">📈 <b>Tracking starts {_dt.date.fromisoformat(st).strftime("%b %-d, %Y")}.</b> {len(T)} calls logged so far. Outcomes stay "pending" until a stage move, launch, result or miss can be checked against a source. Misses will be shown as prominently as hits.</div><div class="grid"><div class="card kpi"><div class="v">{len(T)}</div>calls logged</div><div class="card kpi"><div class="v">0</div>resolved so far</div><div class="card kpi"><div class="v">—</div>hit rate (needs resolved calls)</div></div><h2>All calls</h2><div class="tabs"><button class="on" onclick="tk(this,\'\')">All</button><button onclick="tk(this,\'research\')">Research</button><button onclick="tk(this,\'opp\')">Opportunities</button></div><div class="card tw"><table id="trk"><tr><th>Date</th><th>Call on</th><th>Stage</th><th>Readiness</th><th>Our call</th><th>Outcome</th></tr>{rows}</table></div><p class="meta">Grading rule: a research call is a <b>hit</b> if the item reaches the next stage inside our years-to-market window, a <b>miss</b> if the window passes. Logged automatically by the daily build; never edited after the fact.</p><script>function tk(b,k){{b.parentNode.querySelectorAll("button").forEach(x=>x.classList.remove("on"));b.classList.add("on");document.querySelectorAll("#trk tr[data-k]").forEach(r=>r.style.display=!k||r.dataset.k==k?"":"none")}}</script>'
    open("track-record.html","w").write(page("track-record.html","Track record: every call we make, graded later","Every FrontierRadar call is logged with date, stage and readiness, then graded against what actually happened.",'<span class="pill">📈 Track record</span><h1>Every call, on the record</h1><p class="hook">Anyone can make predictions. We log ours with a date, so you can check later whether we were right.</p>',body))
START="""<section id="start" class="card start"><h2 style="margin-top:0">⚡ Start here: FrontierRadar in 60 seconds</h2><ol><li><b>Big money follows a path:</b> lab paper → prototype → factory orders → company profits. Share prices usually move at the end.</li><li><b>We read the start of the path</b> (new papers and patents) and explain each in plain English.</li><li><b>Every idea gets a Readiness score (0-100)</b> from an <a href="methodology.html">open formula</a>, plus a bull and a bear case.</li><li><b>We link ideas to companies</b> on the Opportunities page and log every call on our <a href="track-record.html">Track record</a>.</li></ol></section>
<section id="paths"><h2>Pick your path</h2><div class="grid"><a class="card path" href="research.html#items"><span class="pi">🤔</span><b>I'm curious</b><p>Plain-English breakthroughs. Tap "Explain like I'm 10".</p><span class="go">Start reading →</span></a><a class="card path" href="opportunities.html"><span class="pi">💹</span><b>I invest</b><p>Companies tied to each idea, with bull vs bear and risks.</p><span class="go">See opportunities →</span></a><a class="card path" href="methodology.html"><span class="pi">🧠</span><b>I'm a pro</b><p>Scoring formula, sub-scores, sources and the call log.</p><span class="go">Check the method →</span></a></div></section>"""
def home_ux():
    ix=open("index.html").read().replace('<div class="card wn" id="wn"',START+'<div class="card wn" id="wn"',1)
    open("index.html","w").write(ux(ix,"","index.html"))
CSS3+=""".rt{float:right;font-size:.78em;color:var(--tx3);margin-top:6px}.bb{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}.bull{border-left:4px solid #2ecc71;padding:8px 12px;background:#2ecc7112;border-radius:8px}.bear{border-left:4px solid #ff5c5c;padding:8px 12px;background:#ff5c5c12;border-radius:8px}.bear ul,.how ul{margin:6px 0;padding-left:18px}.bull p{margin:6px 0}
.sowhat{background:#4da3ff14;border-radius:8px;padding:8px 12px}.how table{font-size:.85em}.how{color:var(--tx)}abbr.gl{text-decoration:underline dotted #4da3ff;cursor:help;position:relative}abbr.gl:focus::after,abbr.gl:hover::after{content:attr(data-d);position:absolute;left:0;top:1.6em;z-index:30;background:#0c1422;border:1px solid var(--bd);color:var(--tx);padding:6px 8px;border-radius:8px;width:220px;font-size:.8rem;font-weight:400;white-space:normal}
.bnav{display:none}.totop{position:fixed;right:14px;bottom:70px;width:40px;height:40px;border-radius:50%;background:#1a2638;color:var(--tx);display:flex;align-items:center;justify-content:center;text-decoration:none;border:1px solid var(--bd);z-index:40;font-size:1.2em}
.start ol li{margin:6px 0}.path{text-decoration:none;color:inherit;display:block}.path .pi{font-size:2em;display:block}.path .go{color:var(--g);font-weight:700}
@media(max-width:700px){.bb{grid-template-columns:1fr}.mn .x{display:none}.bnav{display:flex;position:fixed;bottom:0;left:0;right:0;z-index:50;background:#070b12f2;border-top:1px solid var(--bd);backdrop-filter:blur(8px)}.bnav a{flex:1;text-align:center;font-size:.7em;color:var(--tx2);text-decoration:none;padding:6px 0 8px}.bnav a span{display:block;font-size:1.4em}.bnav a.on{color:var(--g)}body{padding-bottom:64px}.switch{bottom:76px!important}.badge{bottom:76px!important}.totop{bottom:128px}abbr.gl:focus::after{width:180px}}"""
_main4=main
def main():
    _main4();methodology(ALL[-1]);track(ALL);home_ux()
    sm=open("sitemap.xml").read().replace("</urlset>",f"<url><loc>{BASE}methodology.html</loc></url><url><loc>{BASE}track-record.html</loc></url></urlset>")
    open("sitemap.xml","w").write(sm)
    for d in ALL:
        fn=f'data/{d["date"]}.json';raw=json.load(open(fn))
        RR={r["id"]:r for r in d["research"]};OO={o["name"]:o for o in d["opportunities"]}
        for r in raw["research"]:
            if r["id"] in RR and "score" in r:
                c=RR[r["id"]];r.update(ready=c["ready"],hype=c["hype"],years=c["years"],stage=c["stage"]);r["score_points"]=c["_parts"];r["ip_level"]=c["_ipl"]
        for o in raw["opportunities"]:
            if o["name"] in OO and "score" in o:o["conv"]=OO[o["name"]]["conv"];o["conv_score"]=OO[o["name"]]["_cs"]
        json.dump(raw,open(fn,"w"),indent=1,ensure_ascii=False)
if __name__=="__main__":main()
