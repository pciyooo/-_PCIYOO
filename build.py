import os
import glob
import json

# --- 1. 配置加载 ---
def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f: return json.load(f)
    except: return {"profile": {}, "social_links": [], "projects": []}

CONF = load_config()
PROF = CONF.get("profile", {})

def find_asset(name):
    # 优先查找 assets 目录
    if os.path.exists(f"assets/{name}"): return f"assets/{name}"
    # 兼容旧逻辑
    for ext in [".jpg", ".png", ".jpeg", ".pdf"]:
        if os.path.exists(f"assets/{name}{ext}"): return f"assets/{name}{ext}"
    return ""

AVATAR = find_asset("avatar")
BANNER = find_asset("banner")
RESUME = find_asset("resume.pdf")

GALLERY_IMGS = []
if os.path.exists("illustrations"):
    GALLERY_IMGS = sorted([f"illustrations/{f}" for f in os.listdir("illustrations") if f.endswith(('.jpg','.png'))])
GALLERY_JSON = json.dumps(GALLERY_IMGS)

# --- 2. 定制图标库 ---
ICONS = {
    "menu": '<path d="M3 12h18M3 6h18M3 18h18"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "scroll": '<rect x="5" y="2" width="14" height="20" rx="7"/><line x1="12" y1="6" x2="12" y2="10"/>', # Mouse icon
    
    # Nav
    "film": '<rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',
    "home": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "email": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    
    # Custom Brand
    "wechat": '''<path d="M 13 4 C 7.486 4 3 7.813 3 12.5 C 3 14.089 3.511375 15.622891 4.484375 16.962891 L 3.9023438 21.515625 L 7.9238281 19.826172 C 9.2157664 20.473405 10.661622 20.845152 12.171875 20.951172 C 12.911761 23.89542 15.984593 26 19.5 26 C 20.952474 26 22.272207 25.588631 23.429688 24.96875 L 26.337891 26.601562 L 25.894531 22.833984 C 26.553846 21.884082 27 20.785589 27 19.582031 C 27 17.01804 25.280055 14.888016 22.853516 13.849609 C 22.940874 13.398313 23 12.947264 23 12.5 C 23 7.813 18.514 4 13 4 z M 9.5625 9.171875 C 10.3405 9.171875 10.96875 9.8001719 10.96875 10.576172 C 10.96875 11.352172 10.3395 11.984375 9.5625 11.984375 C 8.7855 11.984375 8.15625 11.354172 8.15625 10.576172 C 8.15625 9.8001719 8.7855 9.171875 9.5625 9.171875 z M 17.234375 9.171875 C 18.011375 9.171875 18.640625 9.8001719 18.640625 10.576172 C 18.640625 11.354172 18.011375 11.984375 17.234375 11.984375 C 16.455375 11.984375 15.828125 11.354172 15.828125 10.576172 C 15.828125 9.7991719 16.457375 9.171875 17.234375 9.171875 z M 19.5 15.166016 C 22.639675 15.166016 25 17.238427 25 19.582031 C 25 20.470335 24.677694 21.29295 24.091797 22.005859 L 23.822266 22.333984 L 23.871094 22.755859 L 23.892578 22.935547 L 23.449219 22.6875 L 22.941406 23.015625 C 22.007387 23.622187 20.813397 24 19.5 24 C 16.360325 24 14 21.925636 14 19.582031 C 14 17.239644 16.360511 15.166016 19.5 15.166016 z M 16.986328 17.429688 C 16.396328 17.429687 15.921875 17.906141 15.921875 18.494141 C 15.921875 19.082141 16.397328 19.560547 16.986328 19.560547 C 17.573328 19.560547 18.051734 19.082141 18.052734 18.494141 C 18.052734 17.906141 17.574328 17.429688 16.986328 17.429688 z M 22.033203 17.429688 C 21.446203 17.429687 20.96875 17.906141 20.96875 18.494141 C 20.96875 19.082141 21.445203 19.560547 22.033203 19.560547 C 22.622203 19.560547 23.101562 19.082141 23.101562 18.494141 C 23.101563 17.906141 22.622203 17.429688 22.033203 17.429688 z"/>''',
    "qq": '''<path d="M 12.601563 3.953125 C 17.574219 3.953125 17.824219 8.328125 18.101563 9.1875 C 18.101563 9.1875 18.492188 9.617188 18.585938 10.277344 C 18.644531 10.699219 18.398438 11.183594 18.398438 11.183594 C 18.398438 11.183594 19.988281 13.289063 19.988281 14.945313 C 19.988281 15.980469 19.679688 16.515625 19.316406 16.515625 C 18.957031 16.515625 18.425781 15.421875 18.425781 15.421875 C 18.425781 15.421875 17.597656 17.164063 17.183594 17.414063 C 16.769531 17.664063 18.675781 17.9375 18.675781 18.753906 C 18.675781 19.566406 17.160156 19.929688 15.917969 19.929688 C 14.675781 19.929688 12.695313 19.296875 12.695313 19.296875 L 11.984375 19.273438 C 11.984375 19.273438 11.429688 20.042969 9.152344 20.042969 C 6.875 20.042969 5.886719 19.433594 5.886719 18.707031 C 5.886719 17.730469 7.335938 17.597656 7.335938 17.597656 C 7.335938 17.597656 6.410156 17.34375 5.628906 15.1875 C 5.628906 15.1875 5.085938 16.351563 4.320313 16.351563 C 4.320313 16.351563 4 16.164063 4 15.105469 C 4 12.914063 5.597656 11.84375 6.285156 11.1875 C 6.285156 11.1875 6.171875 10.902344 6.230469 10.546875 C 6.300781 10.148438 6.535156 9.910156 6.535156 9.910156 C 6.535156 9.910156 6.449219 9.4375 6.78125 9.054688 C 6.851563 7.988281 7.632813 3.953125 12.601563 3.953125 M 12.625 1.996094 C 7.210938 1.996094 5.292969 5.820313 4.953125 8.386719 C 4.789063 8.699219 4.699219 9.023438 4.660156 9.324219 C 4.535156 9.566406 4.417969 9.863281 4.355469 10.214844 C 4.34375 10.304688 4.332031 10.390625 4.324219 10.476563 C 3.386719 11.328125 2.019531 12.777344 2.019531 15.214844 C 2.019531 16.90625 2.652344 17.628906 3.183594 17.9375 L 3.582031 18.171875 L 4.046875 18.171875 C 4.058594 18.171875 4.074219 18.171875 4.089844 18.171875 C 4.015625 18.410156 3.976563 18.667969 3.976563 18.945313 C 3.972656 19.664063 4.339844 22 9.050781 22 C 10.773438 22 11.851563 21.632813 12.511719 21.242188 C 13.207031 21.445313 14.828125 21.882813 16.054688 21.882813 C 18.820313 21.882813 20.605469 20.75 20.605469 18.996094 C 20.605469 18.683594 20.546875 18.402344 20.445313 18.160156 C 21.257813 17.792969 21.964844 16.855469 21.964844 15.054688 C 21.964844 13.472656 21.078125 11.816406 20.476563 10.871094 C 20.523438 10.601563 20.539063 10.300781 20.496094 9.988281 C 20.398438 9.285156 20.113281 8.730469 19.886719 8.382813 C 19.878906 8.351563 19.871094 8.316406 19.867188 8.285156 C 18.976563 4.113281 16.539063 1.996094 12.625 1.996094 Z"/>''',
    
    "bilibili": '<rect x="3" y="6" width="18" height="14" rx="2"/><path d="M8 3l3 3"/><path d="M16 3l-3 3"/><path d="M9 13v-2"/><path d="M15 11v2"/>',
    "youtube": '<path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02" fill="currentColor"/>',
    "artstation": '<path d="M9.3 6.8l-2.3 4.1 6.5-0.1 2.3-4-6.5 0zM14.3 12.4l-7.8 0-1.4 2.5 12.2 0 3.6-6.3-2.4 0zM5.1 16.3l1.4-2.5-3.9 0 1.4 2.5z" fill="currentColor"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>',
    "twitter": '<path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"/>',
    "x": '<path d="M4 4l16 16"/><path d="M4 20l16-16"/>',
    "weibo": '<path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm5 6c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm-5 12c-3.3 0-6-2.7-6-6s2.7-6 6-6 6 2.7 6 6-2.7 6-6 6z"/>',
    "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>'
}

def get_icon(name, size=24):
    k = name.lower().replace(" ", "")
    path = ICONS["link"]
    viewbox = "0 0 24 24"
    fill = "none"
    stroke = "currentColor"
    
    if "wechat" in k or "微信" in k: 
        path = ICONS["wechat"]; viewbox="0 0 30 30"; fill="currentColor"; stroke="none"
    elif "qq" in k: 
        path = ICONS["qq"]; viewbox="0 0 24 24"; fill="currentColor"; stroke="none"
    elif "youtube" in k or "youtu" in k: 
        path = ICONS["youtube"]; fill="currentColor"; stroke="none"
    elif "artstation" in k: 
        path = ICONS["artstation"]; fill="currentColor"; stroke="none"
    else:
        for key in ICONS:
            if key in k: path = ICONS[key]; break
            
    return f'<svg width="{size}" height="{size}" viewBox="{viewbox}" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'

# --- 3. HTML ---
HTML = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PROF.get('name')} | Portfolio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>
    <style>
        :root {{ 
            --bg: #0a0a0a; --sidebar: #111; --accent: #4f86f7; --text: #eee; 
            --w-sidebar: 280px; --w-sidebar-sm: 80px; 
            --font-en: 'Inter', sans-serif; --font-cn: 'Noto Sans SC', sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; outline: none; -webkit-tap-highlight-color: transparent; }}
        body {{ background-color: var(--bg); color: var(--text); font-family: var(--font-en), var(--font-cn); overflow-x: hidden; height: 100vh; overflow: hidden; }}
        
        /* --- CINEMATIC LOADER --- */
        #loader {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 9999; 
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: transform 1s cubic-bezier(0.77, 0, 0.175, 1);
        }}
        #loader.hide {{ transform: translateY(-100%); }}
        
        .typewriter {{
            font-size: 3rem; font-weight: 800; color: #fff;
            border-right: 2px solid var(--accent); white-space: nowrap; overflow: hidden;
            animation: cursor 0.75s step-end infinite;
        }}
        @keyframes cursor {{ from, to {{ border-color: transparent; }} 50% {{ border-color: var(--accent); }} }}
        
        .scroll-hint {{
            margin-top: 20px; opacity: 0; transition: opacity 1s; font-size: 0.8rem; letter-spacing: 3px; color: #666;
            display: flex; flex-direction: column; align-items: center; gap: 10px;
        }}
        .scroll-hint.show {{ opacity: 1; animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} }}
        
        /* --- Main Styles --- */
        #particles {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; }}
        .particle {{ position: absolute; background: white; border-radius: 50%; opacity: 0.3; animation: floatUp linear infinite; }}
        @keyframes floatUp {{ from {{ transform: translateY(100vh); }} to {{ transform: translateY(-10vh); }} }}

        aside {{ 
            width: var(--w-sidebar); height: 100vh; position: fixed; top:0; left:0; z-index: 50;
            background: var(--sidebar); border-right: 1px solid #222;
            display: flex; flex-direction: column; padding: 20px;
            transition: width 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); overflow: hidden;
        }}
        aside.collapsed {{ width: var(--w-sidebar-sm); padding: 20px 10px; }}
        
        .menu-toggle {{ 
            cursor: pointer; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;
            border-radius: 8px; transition: 0.2s; color: #888; align-self: flex-end; margin-bottom: 20px;
        }}
        aside.collapsed .menu-toggle {{ align-self: center; }}
        .menu-toggle:hover {{ background: #222; color: #fff; }}

        .profile-box {{ display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 30px; transition: 0.2s; }}
        aside.collapsed .profile-box {{ transform: scale(0.8); margin-bottom: 10px; }}
        .avatar {{ width: 100px; height: 100px; border-radius: 50%; border: 2px solid var(--accent); margin-bottom: 15px; object-fit: cover; transition: 0.3s; }}
        aside.collapsed .avatar {{ width: 40px; height: 40px; border-width: 1px; margin-bottom: 5px; }}
        
        .info-text {{ transition: opacity 0.2s; }}
        aside.collapsed .info-text {{ opacity: 0; height: 0; overflow: hidden; }}
        .name {{ font-size: 1.5rem; font-weight: 800; margin-bottom: 5px; white-space: nowrap; letter-spacing: -0.5px; }}
        .role {{ color: var(--accent); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}

        .contact-row {{ display: flex; gap: 10px; justify-content: center; margin-bottom: 30px; transition: 0.2s; }}
        aside.collapsed .contact-row {{ flex-direction: column; gap: 15px; align-items: center; }}
        
        .c-icon {{ 
            width: 36px; height: 36px; background: #222; border-radius: 50%; 
            display: flex; align-items: center; justify-content: center; 
            cursor: pointer; transition: 0.2s; color: #aaa; position: relative;
        }}
        .c-icon:hover {{ background: var(--accent); color: #fff; transform: translateY(-3px); }}
        
        /* Resume Btn */
        .resume-btn {{
            margin-top: auto; display: flex; align-items: center; justify-content: center; gap: 10px;
            padding: 12px; background: #222; border-radius: 8px; color: #fff; text-decoration: none;
            transition: 0.2s; font-size: 0.9rem; font-weight: 600; border: 1px solid #333;
        }}
        aside.collapsed .resume-btn span {{ display: none; }}
        .resume-btn:hover {{ background: var(--accent); border-color: var(--accent); }}

        /* Toast */
        #toast {{
            position: fixed; top: 30px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.9); color: #fff; padding: 10px 20px; border-radius: 30px;
            font-size: 14px; z-index: 9999; pointer-events: none;
            opacity: 0; transition: opacity 0.3s, top 0.3s; box-shadow: 0 5px 20px rgba(0,0,0,0.5);
            display: flex; align-items: center; gap: 8px; border: 1px solid #333; font-weight: 500;
        }}
        #toast.show {{ opacity: 1; top: 40px; }}

        .nav {{ display: flex; flex-direction: column; gap: 5px; width: 100%; }}
        .nav-item {{ 
            display: flex; align-items: center; gap: 15px; padding: 12px 15px; 
            color: #888; text-decoration: none; border-radius: 8px; transition: 0.2s; overflow: hidden; font-weight: 500;
        }}
        .nav-item svg {{ flex-shrink: 0; }}
        .nav-item span {{ white-space: nowrap; transition: opacity 0.2s; }}
        aside.collapsed .nav-item span {{ opacity: 0; }}
        aside.collapsed .nav-item {{ justify-content: center; padding: 12px 0; }}
        .nav-item:hover, .nav-item.active {{ background: #222; color: #fff; }}
        .nav-item.active {{ color: var(--accent); }}

        /* FAB */
        .fab-container {{ position: fixed; bottom: 40px; right: 40px; z-index: 90; }}
        .fab-main {{
            width: 60px; height: 60px; background: var(--accent); border-radius: 50%;
            display: flex; align-items: center; justify-content: center; color: #fff;
            box-shadow: 0 5px 20px rgba(79, 134, 247, 0.4); cursor: pointer; transition: 0.3s; font-size: 24px;
        }}
        .fab-main:hover {{ transform: scale(1.1) rotate(90deg); }}
        
        .fab-list {{
            position: absolute; bottom: 70px; right: 5px; 
            display: flex; flex-direction: column; gap: 10px; align-items: center;
            opacity: 0; pointer-events: none; transform: translateY(20px); transition: 0.3s;
        }}
        .fab-container:hover .fab-list {{ opacity: 1; pointer-events: auto; transform: translateY(0); }}
        
        .fab-item {{
            width: 45px; height: 45px; background: #333; border-radius: 50%;
            display: flex; align-items: center; justify-content: center; color: #fff; text-decoration: none;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: 0.2s; font-size: 12px;
        }}
        .fab-item:hover {{ background: #fff; color: #000; transform: translateX(-5px); }}
        .fab-item::after {{
            content: attr(data-label); position: absolute; right: 55px; 
            background: rgba(0,0,0,0.8); padding: 4px 8px; border-radius: 4px; font-size: 12px; color: #fff;
            opacity: 0; transition: 0.2s; white-space: nowrap; pointer-events: none;
        }}
        .fab-item:hover::after {{ opacity: 1; right: 60px; }}

        /* Main */
        main {{ 
            margin-left: var(--w-sidebar); width: calc(100% - var(--w-sidebar)); 
            transition: margin-left 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), width 0.4s;
            min-height: 100vh; position: relative;
        }}
        main.expanded {{ margin-left: var(--w-sidebar-sm); width: calc(100% - var(--w-sidebar-sm)); }}
        
        .hero {{ height: 350px; background: url('{BANNER}') center/cover; position: relative; display: flex; align-items: flex-end; padding: 40px 60px; }}
        .hero::after {{ content:""; position:absolute; bottom:0; left:0; width:100%; height:100%; background: linear-gradient(to top, var(--bg), transparent); }}
        .hero h1 {{ position: relative; z-index: 2; font-size: 4rem; font-weight: 800; letter-spacing: -2px; text-shadow: 0 2px 10px black; }}
        
        section {{ padding: 60px 0; border-bottom: 1px solid #222; }}
        h2 {{ font-size: 1.5rem; margin-bottom: 30px; border-left: 4px solid var(--accent); padding-left: 15px; margin-left: 60px; font-weight: 700; letter-spacing: -0.5px; }}

        /* Movie Wall */
        .wall-wrap {{ position: relative; width: 100%; overflow: hidden; padding: 20px 0; mask-image: linear-gradient(to right, transparent 0%, black 5%, black 95%, transparent 100%); }}
        .wall-track {{ display: flex; width: max-content; gap: 30px; animation: scrollLeft 40s linear infinite; }}
        .wall-track:hover {{ animation-play-state: paused; }}
        @keyframes scrollLeft {{ to {{ transform: translateX(-50%); }} }}
        .wall-card {{ position: relative; width: 320px; aspect-ratio: 16/9; border-radius: 12px; overflow: hidden; transition: 0.4s; cursor: pointer; flex-shrink: 0; }}
        .wall-card:hover {{ transform: scale(1.15); z-index: 10; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }}
        .wall-track:hover .wall-card:not(:hover) {{ opacity: 0.5; filter: blur(2px); }}
        .wall-card img, .wall-card video {{ width: 100%; height: 100%; object-fit: cover; }}
        .wall-card video {{ position: absolute; top:0; left:0; opacity: 0; transition: opacity 0.4s; }}
        .wall-card:hover video {{ opacity: 1; }}
        .wall-info {{ position: absolute; bottom: 0; left: 0; width: 100%; padding: 20px; background: linear-gradient(to top, rgba(0,0,0,0.95), transparent); transform: translateY(100%); transition: transform 0.3s ease; }}
        .wall-card:hover .wall-info {{ transform: translateY(0); }}
        .wall-info h3 {{ font-size: 1.1rem; color: #fff; font-weight: 700; }}
        
        /* Grids */
        .genga-grid {{ display: flex; flex-wrap: wrap; gap: 30px; padding: 0 60px; }}
        .genga-item {{ flex: 1 1 400px; }}
        .flip-viewer {{ width: 100%; aspect-ratio: 16/9; background: #111; position: relative; overflow: hidden; border-radius: 8px; cursor: ew-resize; border: 1px solid #333; }}
        .flip-frame {{ width: 100%; height: 100%; object-fit: contain; display: none; }}
        .flip-frame.active {{ display: block; }}
        .genga-video {{ width: 100%; aspect-ratio: 16/9; border-radius: 8px; background: #000; object-fit: contain; }}

        .comp-wrapper {{ padding: 0 60px; }}
        .comp-box {{ position: relative; aspect-ratio: 16/9; margin-bottom: 40px; overflow: hidden; border-radius: 8px; }}
        .comp-layer {{ position: absolute; top:0; left:0; width:100%; height:100%; object-fit: cover; }}
        .comp-over {{ position: absolute; top:0; left:0; width:50%; height:100%; overflow: hidden; border-right: 2px solid white; }}
        .comp-over .comp-layer {{ width: 100vw; max-width: none; }} 

        .masonry {{ column-count: 3; column-gap: 20px; padding: 0 60px; }}
        .art {{ width: 100%; margin-bottom: 20px; border-radius: 8px; transition: 0.3s; cursor: zoom-in; }}
        .art:hover {{ opacity: 0.8; transform: scale(1.02); }}

        /* Lightbox */
        .lb-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 1000; display: none; opacity: 0; transition: opacity 0.4s ease; }}
        .lb-overlay.visible {{ display: block; opacity: 1; }}
        .lb-stage {{ position: absolute; top: 50%; left: 50%; width: 100%; height: 80vh; transform: translate(-50%, -50%); touch-action: pan-y; }}
        .lb-slide {{ position: absolute; top: 50%; left: 50%; height: 100%; width: auto; aspect-ratio: auto; transform: translate(-50%, -50%); opacity: 0; transition: 0.4s; border-radius: 8px; }}
        .lb-slide img {{ height: 100%; display: block; border-radius: 8px; }}
        .lb-slide.center {{ opacity: 1; z-index: 10; }}
        .lb-slide.left {{ transform: translate(-140%, -50%) scale(0.8); opacity: 0.4; }}
        .lb-slide.right {{ transform: translate(40%, -50%) scale(0.8); opacity: 0.4; }}
        .lb-close {{ position: absolute; top: 30px; right: 30px; font-size: 3rem; color: #666; cursor: pointer; z-index: 20; }}
        .zoom-helper {{ position: fixed; z-index: 2000; transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); transform-origin: top left; pointer-events: none; border-radius: 8px; }}

        @media (max-width: 768px) {{
            .layout {{ flex-direction: column; }}
            aside {{ width: 100%; height: auto; position: relative; padding-bottom: 60px; }}
            main {{ margin: 0; width: 100%; }}
            .masonry {{ column-count: 1; }}
            .wall-card {{ width: 260px; }}
            .genga-grid, .comp-wrapper, .masonry {{ padding: 0 20px; }}
            h2 {{ margin-left: 20px; }}
            .menu-toggle {{ display: none; }}
            .hero h1 {{ font-size: 2.5rem; }}
        }}
    </style>
</head>
<body>
    <!-- Cinematic Loader -->
    <div id="loader">
        <div class="typewriter" id="tw-text"></div>
        <div class="scroll-hint" id="s-hint">
            {get_icon('scroll', 30)}
            <span>SCROLL TO ENTER</span>
        </div>
    </div>

    <div id="particles"></div>
    <div id="toast"></div>
    
    <!-- Sidebar -->
    <aside id="sidebar">
        <div class="menu-toggle" onclick="toggleSidebar()">{get_icon('menu')}</div>
        
        <div class="profile-box">
            <img src="{AVATAR}" class="avatar">
            <div class="info-text">
                <div class="name">{PROF.get('name')}</div>
                <div class="role">{PROF.get('role')}</div>
            </div>
        </div>
        
        <div class="contact-row">
            <div class="c-icon" onclick="copy('{PROF.get('email')}', 'Email')">{get_icon('email')}</div>
            <div class="c-icon" onclick="copy('{PROF.get('wechat')}', 'WeChat')">{get_icon('wechat')}</div>
            <div class="c-icon" onclick="copy('{PROF.get('qq')}', 'QQ')">{get_icon('qq')}</div>
        </div>
        
        <nav class="nav">
            <a href="#projects" class="nav-item">{get_icon('film')} <span>参与项目</span></a>
            <a href="#genga" class="nav-item">{get_icon('layers')} <span>原画与镜头</span></a>
            <a href="#comp" class="nav-item">{get_icon('image')} <span>合成对比</span></a>
            <a href="#gallery" class="nav-item">{get_icon('home')} <span>美术画廊</span></a>
        </nav>
        
        {'<a href="' + RESUME + '" target="_blank" class="resume-btn">' + get_icon('download', 18) + '<span>Download Resume</span></a>' if RESUME else ''}
    </aside>
    
    <!-- FAB -->
    <div class="fab-container">
        <div class="fab-list">
            {''.join([f'<a href="{s["url"]}" target="_blank" class="fab-item" data-label="{s["name"]}">{get_icon(s["name"], 16)}</a>' for s in CONF.get("social_links", [])])}
        </div>
        <div class="fab-main">{get_icon('share', 24)}</div>
    </div>
    
    <main id="main">
        <div class="hero"><h1>PORTFOLIO</h1></div>
        
        <section id="projects">
            <h2>参与项目</h2>
            <div class="wall-wrap">
                <div class="wall-track">
'''

# 内容生成
def get_projects():
    raw_items = CONF.get("projects", [])
    if not raw_items: return "</div></div></section>"
    items = raw_items * 4 if len(raw_items) < 5 else raw_items * 2
    h = ""
    for p in items:
        h += f'''
        <div class="wall-card">
            <img src="{p.get('cover')}">
            <video src="{p.get('video')}" muted loop playsinline onmouseover="this.play()" onmouseout="this.pause()"></video>
            <div class="wall-info">
                <h3>{p.get('title')}</h3>
                <p>{p.get('role')}</p>
            </div>
        </div>'''
    return h + "</div></div></section>"

def get_genga():
    h = '<section id="genga"><h2>原画与镜头</h2><div class="genga-grid">'
    if os.path.exists("flipbooks"):
        for item in sorted(os.listdir("flipbooks")):
            path = f"flipbooks/{item}"
            if os.path.isdir(path):
                imgs = sorted([f for f in os.listdir(path) if f.endswith(('.jpg','.png'))])
                if imgs:
                    frames = "".join([f'<img src="{path}/{i}" class="flip-frame {"active" if idx==0 else ""}">' for idx, i in enumerate(imgs)])
                    h += f'<div class="genga-item"><div class="flip-viewer" onmousemove="doFlip(event, this)">{frames}</div><p style="margin-top:10px; color:#888">📒 {item}</p></div>'
            elif item.endswith(".mp4"):
                h += f'<div class="genga-item"><video src="{path}" class="genga-video" controls loop playsinline></video><p style="margin-top:10px; color:#888">🎬 {item[:-4]}</p></div>'
    return h + "</div></section>"

def get_comp():
    h = '<section id="comp"><h2>合成拆解</h2><div class="comp-wrapper">'
    if os.path.exists("compositing"):
        files = os.listdir("compositing")
        pairs = {}
        for f in files:
            if "_after" in f: pairs[f.split("_after")[0]] = {"after": f}
        for k, v in pairs.items():
            for f in files:
                if f.startswith(k+"_before"): v["before"] = f
            if "before" in v:
                tag = "video" if v["after"].endswith(".mp4") else "img"
                attrs = "autoplay muted loop playsinline" if tag == "video" else ""
                h += f'<div class="comp-box" onmousemove="doComp(event, this)"><{tag} src="compositing/{v["after"]}" class="comp-layer" {attrs}></{tag}><div class="comp-over"><{tag} src="compositing/{v["before"]}" class="comp-layer" {attrs}></{tag}></div></div>'
    return h + "</div></section>"

def get_gallery():
    h = '<section id="gallery"><h2>美术画廊</h2><div class="masonry">'
    if os.path.exists("illustrations"):
        for i, f in enumerate(sorted(os.listdir("illustrations"))):
            if f.endswith(('.jpg','.png')):
                h += f'<img id="art-{i}" src="illustrations/{f}" class="art" onclick="launchGallery({i})">'
    return h + "</div></section>"

HTML_END = f'''
        </main>
    </div>

    <div class="lb-overlay" id="lb-overlay" onclick="closeGallery()">
        <div class="lb-close">&times;</div>
        <div class="lb-stage" id="lb-stage"></div>
    </div>

    <script>
        // Typewriter & Intro
        const nameText = "{PROF.get('name', 'PORTFOLIO')}";
        let i = 0;
        function typeWriter() {{
            if (i < nameText.length) {{
                document.getElementById("tw-text").innerHTML += nameText.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }} else {{
                document.getElementById("s-hint").classList.add("show");
                // Enable scroll unlock
                window.addEventListener('wheel', unlockLoader, {{once:true}});
                window.addEventListener('touchstart', unlockLoader, {{once:true}});
            }}
        }}
        
        function unlockLoader() {{
            document.getElementById('loader').classList.add('hide');
            document.body.style.overflow = 'auto'; // unlock scroll
        }}
        
        window.addEventListener('load', () => {{
            setTimeout(typeWriter, 500);
        }});

        const lenis = new Lenis({{duration: 1.2}});
        function raf(time) {{ lenis.raf(time); requestAnimationFrame(raf); }}
        requestAnimationFrame(raf);

        const pc = document.getElementById('particles');
        for(let i=0; i<30; i++) {{
            let p = document.createElement('div'); p.className = 'particle';
            let size = Math.random()*4;
            p.style.width = size+'px'; p.style.height = size+'px';
            p.style.left = Math.random()*100+'vw';
            p.style.animationDuration = (Math.random()*10+10)+'s';
            p.style.animationDelay = (Math.random()*5)+'s';
            pc.appendChild(p);
        }}

        function toggleSidebar() {{
            document.getElementById('sidebar').classList.toggle('collapsed');
            document.getElementById('main').classList.toggle('expanded');
        }}

        function copy(txt, type) {{
            if(!txt || txt === 'None') return;
            navigator.clipboard.writeText(txt);
            const t = document.getElementById('toast');
            t.innerHTML = `<span style="color:#4f86f7">✓</span> 已复制 ${{type}} : ${{txt}}`;
            t.classList.add('show');
            setTimeout(() => {{ t.classList.remove('show'); }}, 2500);
        }}

        function doFlip(e, box) {{
            let frames = box.querySelectorAll('.flip-frame');
            let x = Math.max(0, Math.min(1, (e.clientX - box.getBoundingClientRect().left)/box.offsetWidth));
            let idx = Math.floor(x * (frames.length-1));
            frames.forEach(f => f.classList.remove('active'));
            frames[idx].classList.add('active');
        }}

        function doComp(e, box) {{
            let w = e.clientX - box.getBoundingClientRect().left;
            box.querySelector('.comp-over').style.width = w + 'px';
            box.querySelector('.comp-over .comp-layer').style.width = box.offsetWidth + 'px';
        }}
        
        const gallery = {GALLERY_JSON};
        let curIdx = 0;
        const overlay = document.getElementById('lb-overlay');
        const stage = document.getElementById('lb-stage');
        
        function renderStage() {{
            stage.innerHTML = '';
            let prevIdx = (curIdx - 1 + gallery.length) % gallery.length;
            let nextIdx = (curIdx + 1) % gallery.length;
            createSlide(prevIdx, 'left');
            createSlide(curIdx, 'center');
            createSlide(nextIdx, 'right');
        }}
        
        function createSlide(idx, posClass) {{
            let div = document.createElement('div');
            div.className = `lb-slide ${{posClass}}`;
            div.onclick = (e) => {{ e.stopPropagation(); if(posClass==='left') slide(-1); if(posClass==='right') slide(1); }};
            let img = document.createElement('img'); img.src = gallery[idx];
            div.appendChild(img); stage.appendChild(div);
        }}

        function launchGallery(idx) {{
            curIdx = idx;
            const thumb = document.getElementById('art-'+idx);
            const rect = thumb.getBoundingClientRect();
            const ghost = document.createElement('img');
            ghost.src = gallery[idx]; ghost.className = 'zoom-helper';
            ghost.style.top = rect.top+'px'; ghost.style.left = rect.left+'px';
            ghost.style.width = rect.width+'px'; ghost.style.height = rect.height+'px';
            document.body.appendChild(ghost); ghost.offsetHeight; 
            ghost.style.top = '50%'; ghost.style.left = '50%';
            ghost.style.width = 'auto'; ghost.style.height = '80vh';
            ghost.style.transform = 'translate(-50%, -50%)';
            overlay.classList.add('visible');
            setTimeout(() => {{ renderStage(); ghost.remove(); }}, 450);
        }}
        
        function slide(dir) {{ curIdx = (curIdx + dir + gallery.length) % gallery.length; renderStage(); }}
        function closeGallery() {{ overlay.classList.remove('visible'); stage.innerHTML = ''; }}
        
        // Touch Swipe
        let touchStartX = 0;
        stage.addEventListener('touchstart', e => {{ touchStartX = e.changedTouches[0].screenX; }});
        stage.addEventListener('touchend', e => {{
            let touchEndX = e.changedTouches[0].screenX;
            if(touchEndX < touchStartX - 50) slide(1);
            if(touchEndX > touchStartX + 50) slide(-1);
        }});

        document.addEventListener('keydown', (e) => {{
            if(overlay.classList.contains('visible')) {{
                if(e.key === 'ArrowLeft') slide(-1);
                if(e.key === 'ArrowRight') slide(1);
                if(e.key === 'Escape') closeGallery();
            }}
        }});
        
        window.addEventListener('resize', () => {{
             document.querySelectorAll('.comp-box').forEach(b => {{
                b.querySelector('.comp-over .comp-layer').style.width = b.getBoundingClientRect().width + 'px';
            }});
        }});
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML + get_projects() + get_genga() + get_comp() + get_gallery() + HTML_END)
    print("Success! V10.0 Cinematic Build Complete.")
