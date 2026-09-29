from flask import Flask, request, send_from_directory, redirect
import os, json, time
app = Flask(__name__)
os.makedirs('videos', exist_ok=True)
DB='videos/data.json'
if not os.path.exists(DB): open(DB,'w').write('[]')
def load():
    try: return json.load(open(DB))
    except: return []
def save(d): json.dump(d, open(DB,'w'))

PAGE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#fff;color:#000;padding-bottom:60px}
.top{height:50px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;position:sticky;top:0;background:#fff;z-index:100}
.logo{font-size:20px;font-weight:900;display:flex;align-items:center} .logo i{background:red;color:white;padding:2px 6px;border-radius:4px;margin-right:4px;font-style:normal;font-size:14px}
.icons{font-size:22px;display:flex;gap:18px}
.tabs{display:flex;gap:8px;padding:8px 12px;overflow-x:auto;white-space:nowrap;border-bottom:1px solid #eee;position:sticky;top:50px;background:#fff;z-index:99}
.tabs::-webkit-scrollbar{display:none}
.chip{padding:7px 12px;background:#f2f2f2;border-radius:8px;font-size:14px;font-weight:500} .chip.active{background:#0f0f0f;color:#fff}
.video-card{padding:0 0 12px 0}
.thumb{width:100%;aspect-ratio:16/9;background:#000;position:relative} .thumb video{width:100%;height:100%;object-fit:cover}
.info{padding:8px 12px;display:flex;gap:10px}
.avatar{width:36px;height:36px;border-radius:50%;background:#e5e5e5;flex-shrink:0}
.title{font-size:15px;font-weight:600;line-height:1.3} .meta{font-size:12px;color:#606060;margin-top:3px}
.ad-badge{background:#ffcc00;font-size:10px;padding:1px 4px;border-radius:2px}
.shorts-head{padding:12px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #eee;border-bottom:1px solid #eee}
.shorts-row{display:flex;gap:10px;overflow-x:auto;padding:12px} .shorts-row::-webkit-scrollbar{display:none}
.s-card{width:160px;flex-shrink:0} .s-thumb{width:100%;height:260px;background:#000;border-radius:12px;overflow:hidden;position:relative} .s-thumb video{width:100%;height:100%;object-fit:cover}
.bottom{position:fixed;bottom:0;left:0;right:0;height:55px;background:#fff;border-top:1px solid #ddd;display:flex;justify-content:space-around;align-items:center;z-index:200}
.b-item{text-align:center;font-size:10px} .b-plus{width:30px;height:24px;background:#000;color:#fff;display:flex;align-items:center;justify-content:center;border-radius:4px;font-size:20px}
</style></head><body>
<div class="top"><div class="logo"><i>▶</i> YouTube</div><div class="icons">🔔 ⌕</div></div>
<div class="tabs"><div class="chip active">Home</div><div class="chip">Subscriptions</div><div class="chip">Music</div><div class="chip">Live</div><div class="chip">Gaming</div></div>
"""

BOTTOM = """<div class="bottom">
<div class="b-item" onclick="location.href='/'">🏠<br>Home</div>
<div class="b-item">▶<br>Shorts</div>
<div class="b-item" onclick="location.href='/upload'"><div class="b-plus">+</div></div>
<div class="b-item">⦿<br>Subs</div>
<div class="b-item">👤<br>You</div>
</div></body></html>"""

@app.route('/')
def home():
    vids = load()[::-1]
    html = PAGE
    if not vids:
        html += '<div style="padding:60px 20px;text-align:center;color:#888">Koi video nahi hai<br><br><a href="/upload" style="background:red;color:white;padding:10px 20px;border-radius:20px;text-decoration:none">+ Pehli Video Upload Karo</a></div>'
    else:
        for v in vids:
            html += f"""
            <div class="video-card" onclick="location.href='/watch/{v['file']}'">
                <div class="thumb"><video src="/videos/{v['file']}" muted></video><span style="position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,0.8);color:white;font-size:11px;padding:2px 4px;border-radius:4px">{v['time']}</span></div>
                <div class="info"><div class="avatar"></div><div><div class="title">{v['title']}</div><div class="meta">Mera Channel • {v['views']} views • 2 days ago</div></div><div>⋮</div></div>
            </div>"""
        # Shorts section
        html += '<div class="shorts-head"><b>▶ Shorts</b><span>⋮</span></div><div class="shorts-row">'
        for v in vids[:10]:
            html += f'<div class="s-card" onclick="location.href=\'/watch/{v["file"]}\'"><div class="s-thumb"><video src="/videos/{v["file"]}"></video></div><div style="font-size:12px;padding:5px 0">{v["title"][:30]}...</div></div>'
        html += '</div>'
    return html + BOTTOM

@app.route('/upload', methods=['GET','POST'])
def up():
    if request.method=='POST':
        f=request.files['video']; title=request.form['title']
        fname=str(int(time.time()))+"_"+f.filename.replace(" ","_")
        f.save(os.path.join('videos', fname))
        d=load(); d.append({"file":fname,"title":title,"views":0,"time":"0:30"}); save(d)
        return redirect('/')
    return PAGE + """
    <div style="padding:30px 15px;text-align:center">
    <h2>Upload Video</h2><br>
    <form method="POST" enctype="multipart/form-data">
    <input name="title" required placeholder="Title likh - Mera Vlog" style="width:100%;padding:12px;border:1px solid #ccc;border-radius:8px"><br><br>
    <input type="file" name="video" accept="video/*" required><br><br>
    <button style="width:100%;padding:12px;background:red;color:white;border:none;border-radius:8px;font-weight:bold;font-size:16px">UPLOAD</button>
    </form></div>""" + BOTTOM

@app.route('/watch/<name>')
def watch(name):
    d=load(); v=next((x for x in d if x['file']==name), None)
    if v: v['views']+=1; save(d)
    return PAGE + f"""
    <div class="thumb" style="position:sticky;top:0"><video src="/videos/{name}" controls autoplay style="width:100%;height:100%"></video></div>
    <div class="info"><div style="flex:1"><div class="title" style="font-size:16px">{v['title'] if v else name}</div><div class="meta">{v['views'] if v else 0} views • Sponsored • 4.3★ FREE</div>
    <div style="display:flex;gap:8px;margin-top:10px;overflow-x:auto"><span style="padding:6px 12px;background:#f2f2f2;border-radius:20px">👍 12K</span><span style="padding:6px 12px;background:#f2f2f2;border-radius:20px">Share</span><span style="padding:6px 12px;background:#f2f2f2;border-radius:20px">Download</span></div>
    </div></div>""" + BOTTOM

@app.route('/videos/<n>')
def vid(n): return send_from_directory('videos', n)

app.run(host='0.0.0.0', port=5000)

