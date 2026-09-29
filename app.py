from flask import Flask, request, redirect, send_from_directory, render_template_string
import os
app = Flask(__name__)
VIDEO_FOLDER = 'videos'
os.makedirs(VIDEO_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html><head><title>MyTube</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Roboto}
body{background:#0f0f0f;color:#fff}
.header{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;background:#0f0f0f;position:sticky;top:0;z-index:10}
.logo{color:red;font-weight:900;font-size:22px}
.search{flex:1;max-width:500px;margin:0 15px;display:flex}
.search input{flex:1;background:#121212;border:1px solid #303030;padding:9px 14px;border-radius:20px 0 0 20px;color:#fff}
.search button{background:#222;border:1px solid #303030;padding:9px 16px;border-radius:0 20px 20px 0}
.upload{background:red;color:#fff;padding:7px 14px;border-radius:20px;text-decoration:none;font-weight:bold;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;padding:15px}
.thumb{height:170px;background:#222;border-radius:12px;display:flex;align-items:center;justify-content:center;position:relative}
.time{position:absolute;bottom:8px;right:8px;background:#000c;padding:2px 6px;border-radius:4px;font-size:12px}
.c-info{display:flex;gap:10px;margin-top:10px}
.avatar{width:36px;height:36px;background:#555;border-radius:50%}
.watch{display:grid;grid-template-columns:1fr 380px;gap:16px;padding:15px}
@media(max-width:900px){.watch{grid-template-columns:1fr}}
.player{width:100%;aspect-ratio:16/9;background:#000;border-radius:12px}
.btn{background:#272727;border:none;color:#fff;padding:8px 14px;border-radius:20px;margin-right:8px}
</style></head><body>
<div class="header">
<div class="logo">▶ MyTube</div>
<div class="search"><input id="q" placeholder="Search" onkeyup="filter()"><button>🔍</button></div>
<a class="upload" href="/upload">+ Upload</a>
</div>

{% if upload_page %}
<div style="max-width:500px;margin:40px auto;background:#212121;padding:20px;border-radius:12px">
<h2>Upload Video</h2><br>
<form method="POST" enctype="multipart/form-data" action="/upload">
<input type="file" name="file" accept="video/*" required style="width:100%;padding:10px;background:#111;color:#fff;border-radius:8px"><br><br>
<button class="upload" style="border:none;width:100%;padding:12px">Upload to MyTube</button>
</form>
</div>

{% elif play %}
<div class="watch">
<div>
<video class="player" controls autoplay src="/videos/{{play}}"></video>
<h3 style="margin:12px 0">{{play}}</h3>
<div><button class="btn">👍 12K</button><button class="btn">👎</button><button class="btn">Share</button><button class="btn">Download</button></div>
</div>
<div>{% for f in files %}<a href="/watch/{{f}}" style="color:#fff;text-decoration:none"><div style="display:flex;gap:8px;margin-bottom:10px"><div style="width:160px;height:90px;background:#222;border-radius:8px"></div><div style="font-size:13px">{{f}}</div></div></a>{% endfor %}</div>
</div>

{% else %}
<div class="grid" id="grid">
{% for f in files %}
<div class="card" data-name="{{f}}">
<a href="/watch/{{f}}" style="text-decoration:none;color:#fff">
<div class="thumb">▶<div class="time">10:21</div></div>
<div class="c-info"><div class="avatar"></div><div><div style="font-size:14px">{{f}}</div><div style="color:#aaa;font-size:12px">MyTube • 2.3M views</div></div></div>
</a>
</div>
{% endfor %}
</div>
<script>
function filter(){let q=document.getElementById('q').value.toLowerCase();document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.name.toLowerCase().includes(q)?'':'none'})}
</script>
{% endif %}
</body></html>
"""

@app.route('/')
def home():
    files=[f for f in os.listdir(VIDEO_FOLDER) if f.endswith(('.mp4','.webm','.mkv'))]
    return render_template_string(HTML, files=files, play=None, upload_page=False)

@app.route('/watch/<name>')
def watch(name):
    files=[f for f in os.listdir(VIDEO_FOLDER) if f.endswith(('.mp4','.webm','.mkv'))]
    return render_template_string(HTML, files=files, play=name, upload_page=False)

@app.route('/videos/<name>')
def serve(name):
    return send_from_directory(VIDEO_FOLDER, name)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['file']
        if f:
            f.save(os.path.join(VIDEO_FOLDER, f.filename))
            return redirect('/')
    return render_template_string(HTML, files=[], play=None, upload_page=True)

app.run(host='0.0.0.0', port=5000)

