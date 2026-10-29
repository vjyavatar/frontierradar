"""Top 5 & Inferences page – generated from data/*.json every build. Our judgment; not financial advice."""
import json,glob,re,html,datetime as dt
E=lambda s:html.escape(str(s or ""))
_TI={"Chips":"💾","Quantum":"⚛️","Medical":"💉","Neuro":"🧠","AI":"🤖","Materials":"🔋","DNA":"🧬","Space":"🚀"}
class _I(dict):
    def get(self,t,d=""):
        t=str(t or "Chips")
        for k,v in _TI.items():
            if k.lower() in t.lower():return v
        return {"Medical":"💉","Biotech":"💉","Neuro":"🧠","Material":"🔋","Energy":"🔋"}.get(next((k for k in ["Medical","Biotech","Neuro","Material","Energy"] if k.lower() in t.lower()),""),d or "🔬")
TOPIC_ICON=_I()
WIN=[("Daily",1),("Weekly",7),("Monthly",30),("Quarterly",91),("Half-yearly",182),("Yearly",365)]
def load():
    D={}
    for f in sorted(glob.glob("data/20*.json")):
        d=json.load(open(f));D[d["date"]]=d
    return D
def tickers(d,iid):
    return [o for o in d.get("opportunities",[]) if iid in (o.get("links") or [])]
def rank(D,date):
    d=D[date];prev={}
    for k in sorted(D):
        if k<date:
            for r in D[k]["research"]:prev[r["id"]]=r.get("ready",0)
    out=[]
    for r in d["research"]:
        s=r.get("score",{});mom=r.get("ready",0)-prev.get(r["id"],r.get("ready",0))
        tk=tickers(d,r["id"]);pull=min(5,len(tk)*2+s.get("backing",0))
        sc=0.5*r.get("ready",0)+6*s.get("evidence",0)+3*pull+2*mom
        out.append(dict(r=r,score=round(sc,1),mom=mom,tk=tk,pull=pull))
    out.sort(key=lambda x:-x["score"])
    # diversity: at most 2 per topic
    pick,c=[],{}
    for x in out:
        t=x["r"].get("topic","Chips")
        if c.get(t,0)<2:pick.append(x);c[t]=c.get(t,0)+1
        if len(pick)==5:break
    return pick
def window(D,date,days):
    end=dt.date.fromisoformat(date);start=end-dt.timedelta(days=days-1)
    ks=[k for k in sorted(D) if start<=dt.date.fromisoformat(k)<=end]
    latest={}
    first={}
    for k in ks:
        for r in D[k]["research"]:
            first.setdefault(r["id"],r.get("ready",0));latest[r["id"]]=(r,k)
    T={}
    for iid,(r,k) in latest.items():
        t=r.get("topic","Chips");T.setdefault(t,[]).append((r,r.get("ready",0)-first[iid],k))
    rows=[]
    for t,L in T.items():
        avg=sum(r.get("ready",0) for r,_,_ in L)/len(L);mom=sum(m for _,m,_ in L)/len(L)
        adv=sum(1 for r,_,_ in L if r.get("stage",1)>=3)
        rows.append(dict(t=t,n=len(L),avg=round(avg),mom=round(mom,1),adv=adv,best=max(L,key=lambda z:z[0].get("ready",0))[0],sc=avg+5*mom+8*adv))
    rows.sort(key=lambda x:-x["sc"])
    return ks,rows
def card(x,i,d):
    r=x["r"];tk=x["tk"]
    tks=" ".join(f'<span class="pill">{E(o["ticker"])} · {E(o["name"])}</span>' for o in tk if o.get("ticker")) or '<span class="pill">No listed pure-play linked · developer likely private or a small part of a big company</span>'
    bear=(r.get("bear") or [["Not yet independently confirmed",None]])[0][0]
    mom=f'{"+" if x["mom"]>0 else ""}{x["mom"]}' if x["mom"] else "new / flat"
    return f'''<details class="card t5" {"open" if i==0 else ""}><summary><b>#{i+1} {TOPIC_ICON.get(r.get("topic"),"🔬")} {E(r["title"])}</b> <span class="meta">readiness {r.get("ready")} · momentum {mom} · {E(r.get("plan","Watch"))}</span></summary>
<p>{E(r.get("eli10",""))}</p><p><i>Analogy:</i> {E(r.get("analogy",""))}</p>
<div class="g2"><div><b>⏳ Timeline to materialise</b><br>{E(r.get("years",""))} yrs (our judgment)</div><div><b>🎯 Plan</b><br>{E(r.get("plan","Watch"))} — our judgment, not financial advice</div>
<div><b>✅ Catalyst to watch</b><br>{E(r.get("watch",""))}</div><div style="color:#ff9b9b"><b>❌ Kill signal</b><br>{E(bear)}</div></div>
<p><b>Related listed names:</b> {tks}</p><p class="meta">Rank score {x["score"]} = ½·readiness + 6·evidence + 3·commercial pull + 2·momentum (max 2 per topic). <a href="research.html#{E(r["id"])}">Full card →</a></p></details>'''
def inf(D,date,name,days):
    ks,rows=window(D,date,days)
    if not rows:return "<p>No data.</p>"
    honest=f'Based on <b>{len(ks)} day{"s" if len(ks)!=1 else ""} of data</b> ({ks[0]} → {ks[-1]})'+(f' — the {name.lower()} window wants {days} days, so treat this as early and thin.' if len(ks)<days else ".")
    top=rows[:3]
    dirs="".join(f'<li><b>{TOPIC_ICON.get(t["t"],"")} {E(t["t"])}</b>: {t["n"]} items, avg readiness {t["avg"]}, momentum {t["mom"]:+}, {t["adv"]} at Stage 3+. Lead item: <a href="research.html#{E(t["best"]["id"])}">{E(t["best"]["title"])}</a>.</li>' for t in top)
    d=D[date];rev=[]
    for t in rows:
        for r in [t["best"]]:
            for o in tickers(d,r["id"]):
                if o.get("ticker"):rev.append(f'{E(o["ticker"])} ({E(t["t"])}: {E(o.get("catalyst",""))})')
    rev=rev[:4]
    conf="".join(f'<li>{E(t["best"].get("watch",""))}</li>' for t in top)
    stage3=[t for t in rows if t["adv"]]
    revtxt=("Where money is closest: "+", ".join(E(t["t"]) for t in stage3)+" already have Stage 3+ items (selling or shipping). ") if stage3 else "Nothing here is at Stage 3+ yet, so revenue is mostly years away. "
    return f'''<p class="meta">{honest}</p><h3>Strongest directions</h3><ol>{dirs}</ol>
<h3>💰 Revenue angle</h3><p>{revtxt}{("Listed names tied to the leaders: "+"; ".join(rev)+".") if rev else ""} <i>Think of it like a farm: Stage 3+ is the crop already at market; Stage 1–2 is seeds in the ground.</i></p>
<h3>🔎 Confirming signals to watch</h3><ul>{conf}</ul><p class="meta">Our judgment · Not financial advice.</p>'''
def scorecard(D,date,trf="data/track_record.json"):
    tr=json.load(open(trf));top=rank(D,date)
    have={(e["date"],e["id"]) for e in tr if e.get("kind")=="top5"}
    for i,x in enumerate(top):
        if (date,x["r"]["id"]) not in have:
            tr.append(dict(date=date,kind="top5",id=x["r"]["id"],name=x["r"]["title"],rank=i+1,stage=x["r"].get("stage"),ready=x["r"].get("ready"),call=f'Top-5 #{i+1}: {x["r"].get("plan","Watch")}, {x["r"].get("years")} yrs',outcome="pending"))
    json.dump(tr,open(trf,"w"),indent=1)
    now={}
    for k in sorted(D):
        for r in D[k]["research"]:now[r["id"]]=r.get("ready",0)
    rows="".join(f'<tr><td>{e["date"]}</td><td>#{e.get("rank")}</td><td><a href="research.html#{E(e["id"])}">{E(e["name"])}</a></td><td>{e["ready"]}</td><td>{now.get(e["id"],"–")}</td><td style="color:{"#2ecc71" if now.get(e["id"],0)>e["ready"] else ("#ff5c5c" if now.get(e["id"],0)<e["ready"] else "inherit")}">{now.get(e["id"],0)-e["ready"]:+}</td><td>{E(e["outcome"])}</td></tr>' for e in sorted([e for e in tr if e.get("kind")=="top5"],key=lambda e:(e["date"],e["rank"]),reverse=True))
    return f'<div style="overflow-x:auto"><table><tr><th>Picked</th><th>Rank</th><th>Item</th><th>Readiness then</th><th>Now</th><th>Change</th><th>Outcome</th></tr>{rows}</table></div><p class="meta">Every Top-5 pick is logged to the track record and graded later. Green = readiness rose since the pick, red = fell.</p>'
def build(page):
    D=load();dates=sorted(D);last=dates[-1]
    sc=scorecard(D,last)
    blocks=""
    for date in dates:
        t5="".join(card(x,i,D[date]) for i,x in enumerate(rank(D,date)))
        tabs="".join(f'<button class="it{" on" if j==0 else ""}" data-w="{j}">{n}</button>' for j,(n,_) in enumerate(WIN))
        pans="".join(f'<div class="ip" data-w="{j}"{"" if j==0 else " hidden"}>{inf(D,date,n,dd)}</div>' for j,(n,dd) in enumerate(WIN))
        blocks+=f'<div class="dblk" data-d="{date}"{"" if date==last else " hidden"}><div class="ptabs"><button class="pt on" data-p="t5">🏆 Top 5</button><button class="pt" data-p="inf">🧭 Inferences</button><button class="pt" data-p="sc">📈 Pick scorecard</button></div><section data-p="t5"><h2>Top 5 most promising — {date}</h2>{t5}</section><section data-p="inf" hidden><div class="itabs">{tabs}</div>{pans}</section><section data-p="sc" hidden>{sc}</section></div>'
    opts="".join(f'<option{" selected" if k==last else ""}>{k}</option>' for k in reversed(dates))
    css='<style>.ptabs,.itabs{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}.pt,.it{background:#151b26;color:#dfe6f0;border:1px solid #2a3344;border-radius:999px;padding:7px 14px;cursor:pointer}.pt.on,.it.on{background:#2ecc71;color:#06210f;border-color:#2ecc71}.t5 summary{cursor:pointer;line-height:1.5}.g2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0}@media(max-width:700px){.g2{grid-template-columns:1fr}.ptabs,.itabs{flex-wrap:nowrap;overflow-x:auto}}</style>'
    js='''<script>const $$=(s,e=document)=>[...e.querySelectorAll(s)];
document.getElementById("idate").onchange=e=>$$(".dblk").forEach(b=>b.hidden=b.dataset.d!=e.target.value);
$$(".dblk").forEach(b=>{$$(".pt",b).forEach(t=>t.onclick=()=>{$$(".pt",b).forEach(x=>x.classList.toggle("on",x==t));$$("section",b).forEach(s=>s.hidden=s.dataset.p!=t.dataset.p)});
$$(".it",b).forEach(t=>t.onclick=()=>{$$(".it",b).forEach(x=>x.classList.toggle("on",x==t));$$(".ip",b).forEach(s=>s.hidden=s.dataset.w!=t.dataset.w)})});</script>'''
    body=css+f'<div class="card" style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">📅 <label>Issue <select id="idate">{opts}</select></label><span class="meta">Our judgment · Not financial advice · Rebuilt automatically with every issue.</span></div>'+blocks+js
    hero='<span class="pill">🏆 Top 5 & Inferences</span><h1>The 5 most promising breakthroughs today, and what the trend says</h1><p class="hook">Like a weather forecast for technology: today\'s top picks, plus what the data so far suggests over a week, a month and longer.</p>'
    open("insights.html","w").write(page("insights.html","Top 5 & Inferences: the most promising breakthroughs","Daily Top 5 frontier breakthroughs across all topics, with rolling inferences. Our judgment, not financial advice.",hero,body))
