import os
import glob
import json

# --- 社交平台图标映射表 ---
SOCIAL_ICONS = {
    "Bilibili": "📺", "YouTube": "▶", "Instagram": "📸", "ArtStation": "🎨",
    "Twitter": "🐦", "X": "✖️", "GitHub": "💻", "微博": "💬", "TikTok": "🎵", "Pinterest": "📌",
}

# --- 读取配置 ---
def load_config():
    default = {
        "profile": {"name": "My Name", "role": "Artist", "bio": "Bio here", "email": "me@example.com", "wechat": "", "qq": ""},
        "social_links": [],
        "sections": {"animation": "Animation", "compositing": "Compositing", "illustration": "Illustration"}
    }
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f: 
                data = json.load(f)
                if "social_links" not in data: data["social_links"] = []
                data["profile"] = data.get("profile", {})
                if "wechat" not in data["profile"]: data["profile"]["wechat"] = ""
                if "qq" not in data["profile"]: data["profile"]["qq"] = ""
                return data
        except: pass
    return default

CONFIG = load_config()

# --- 资源检查 ---
def get_asset(name):
    path = os.path.join("assets", name)
    return path.replace(os.sep, '/') if os.path.exists(path) else None

AVATAR = get_asset("avatar.jpg") or get_asset("avatar.png")
BANNER = get_asset("banner.jpg") or get_asset("banner.png")

# --- 联系方式 HTML 生成器 ---
def get_contact_html(type, icon, value):
    if not value or value.strip() == "":
        return "" 
    
    container_id = f"contact-{type}" 
    
    html = f'''
    <div class="contact-container" id="{container_id}">
        <div class="contact-btn" onclick="copyContact('{value}', '{container_id}')">
           {icon} {type.capitalize()}
        </div>
        <div class="contact-popup">
            {value} <br><span style="font-size:0.7rem; opacity:0.7">(点击已复制)</span>
        </div>
    </div>
    '''
    return html

# --- 辅助函数：生成社交链接 HTML ---
def get_social_links_html(config):
    links_html = []
    for s in config.get('social_links', []):
        name = s.get('name', '').strip()
        url = s.get('url', '').strip()
        
        if not url or not name:
            continue
            
        icon_char = SOCIAL_ICONS.get(name)
        icon_html = f'<span class="social-icon" role="img" aria-label="{name} icon">{icon_char}</span>' if icon_char else ''

        links_html.append(
            f'<a href="{url}" target="_blank" class="social-btn">'
            f'{icon_html}'
            f'<span>{name}</span>'
            f'</a>'
        )
    return ''.join(links_html)


# --- 辅助函数：文件获取 (用于内容生成和 JS 传递) ---
def get_files(folder, exts):
    if not os.path.exists(folder): return []
    files = []
    for ext in exts: files.extend(glob.glob(os.path.join(folder, f"*{ext}")))
    return [f.replace(os.sep, '/') for f in sorted(files)]

# 预先获取插画文件列表，供 Lightbox JS 使用
ART_FILES = get_files('illustrations', ['.jpg', '.png', '.gif'])
# 将 Python 列表转换为 JSON 字符串嵌入到 JS 中
ART_FILES_JSON = json.dumps(ART_FILES, ensure_ascii=False)


# --- HTML 核心（包含 CSS 和结构） ---
profile_data = CONFIG['profile']

html = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{profile_data['name']} | Portfolio</title>
    <style>
        :root {{ 
            --bg: #121212; 
            --sidebar-bg-blend: rgba(0, 0, 0, 0.7); 
            --content-panel-bg-blend: rgba(255, 255, 255, 0.1); 
            --text: #e0e0e0; --text-sub: #888; 
            --accent: #4f86f7; --border: #2a2a2a;
            --sidebar-width: 300px;
        }}
        
        /* 粒子垂直运动的关键帧 */
        @keyframes flow {{ 0% {{ transform: translateY(0) scale(1); opacity: 1; }} 100% {{ transform: translateY(-100vh) scale(0.5); opacity: 0; }} }}
        
        * {{ box-sizing: border-box; }}
        body {{ 
            margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            background: var(--bg); color: var(--text); 
            display: flex; min-height: 100vh;
        }}
        a {{ color: inherit; text-decoration: none; transition: 0.2s; }}
        
        /* 悬停放大效果基础类 */
        .hover-scale {{
            transition: transform 0.3s ease-out, box-shadow 0.3s;
            will-change: transform;
        }}
        .hover-scale:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        }}
        
        /* --- 1. 固定底层背景 (模糊和色延伸基础) --- */
        .color-adapt-base {{
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background-image: {f"url('{BANNER}')" if BANNER else "linear-gradient(to right, #222, #111)"};
            background-size: cover; background-position: center;
            background-repeat: no-repeat;
            z-index: -2; 
            transform: scale(1.1); 
            filter: blur(10px); 
        }}

        /* --- 2. 粒子容器 (z-index:-1 确保它在最底层背景之上，内容之下) --- */
        .particles {{ 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            z-index: -1; 
            pointer-events: none; overflow: hidden;
            opacity: 0.9;
        }}
        .particle {{ 
            position: absolute; 
            border-radius: 50%;
            animation-name: flow; 
            animation-timing-function: linear; 
            animation-iteration-count: infinite; 
            will-change: transform, opacity; 
            /* V4.8: 移除默认背景，由 JS 注入纯白背景和透明度 */
        }}

        /* --- 3. 左侧固定侧边栏 (深色半透明模拟色延伸) --- */
        aside {{
            width: var(--sidebar-width); 
            background: var(--sidebar-bg-blend); 
            backdrop-filter: blur(5px); 
            border-right: 1px solid rgba(255, 255, 255, 0.1); 
            position: fixed; top: 0; bottom: 0; left: 0;
            padding: 40px 30px; display: flex; flex-direction: column; z-index: 10; 
            box-shadow: 2px 0 20px rgba(0,0,0,0.8); 
        }}
        
        /* 头像修复及优化 */
        .profile-header {{ margin-bottom: 40px; }}
        .avatar-wrapper {{ 
            display: inline-block; margin-bottom: 20px; 
            transition: transform 0.3s ease-out, box-shadow 0.3s; 
        }}
        .avatar {{ 
            width: 100px; height: 100px; border-radius: 50%; object-fit: cover; 
            border: 3px solid rgba(255, 255, 255, 0.2);
            transition: border-color 0.3s;
        }}
        .avatar-wrapper:hover {{
            transform: scale(1.1); 
            box-shadow: 0 0 20px rgba(79, 134, 247, 0.6); 
        }}
        .avatar-wrapper:hover .avatar {{
            border-color: var(--accent);
        }}
        
        /* 标题阴影 */
        .name {{ 
            font-size: 1.8rem; font-weight: 800; margin: 0 0 5px 0; color: #fff; 
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8), 0 0 5px rgba(0, 0, 0, 0.5); 
        }}
        .role {{ font-size: 0.9rem; color: var(--text-sub); text-transform: uppercase; letter-spacing: 1px; }}
        .bio {{ margin-top: 20px; font-size: 0.9rem; color: #aaa; line-height: 1.5; }}
        
        /* 侧边栏导航优化 (只放大文本) */
        nav {{ display: flex; flex-direction: column; gap: 5px; flex: 1; }}
        .nav-item {{ 
            padding: 10px 0; font-weight: 500; display: flex; justify-content: space-between; align-items: center; 
            transition: color 0.2s, transform 0.2s; 
        }}
        .nav-item:hover {{ color: var(--accent); transform: translateX(5px); }}
        .nav-item span {{ transition: font-size 0.2s; }}
        .nav-item:hover span {{ font-size: 1.05em; }} 

        /* 联系方式 (弹窗修复) */
        .contact-group {{ margin-top: 10px; }}
        .contact-container {{ position: relative; display: block; margin: 5px 0; }}
        .contact-btn {{ 
            color: var(--accent); cursor: pointer; font-weight: bold; 
            display: inline-flex; align-items: center; gap: 5px; padding: 5px 0; 
            transition: color 0.2s, font-size 0.2s;
        }}
        .contact-btn:hover {{ font-size: 1.05em; color: #fff; }}

        .contact-popup {{ 
            visibility: hidden; opacity: 0; position: absolute; top: 50%; left: 100%; 
            transform: translateY(-50%); background: #333; color: #fff; padding: 8px 12px; 
            border-radius: 6px; font-size: 0.85rem; white-space: nowrap; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.5); transition: opacity 0.2s, left 0.2s; 
            pointer-events: none; z-index: 9999; 
        }}
        .contact-popup::after {{ 
            content: ""; position: absolute; top: 50%; left: -10px; margin-top: -5px; 
            border-width: 5px; border-style: solid; border-color: transparent #333 transparent transparent; 
        }}
        .contact-container.active .contact-popup {{ visibility: visible; opacity: 1; left: calc(100% + 10px); }}

        /* 社交链接优化 (只放大文本/图标) */
        .footer-links {{ margin-top: 40px; display: flex; flex-wrap: wrap; gap: 10px; }}
        .social-btn {{ 
            font-size: 0.85rem; color: var(--text-sub); padding: 5px 10px; border: 1px solid #333; border-radius: 20px;
            display: flex; align-items: center; gap: 5px; transition: border-color 0.2s, color 0.2s, transform 0.2s;
        }}
        .social-btn:hover {{ border-color: var(--accent); color: #fff; }}
        .social-icon {{ font-size: 1.1em; line-height: 1; opacity: 0.7; transition: font-size 0.2s, opacity 0.2s; }}
        .social-btn:hover .social-icon {{ font-size: 1.3em; opacity: 1; }}


        /* --- 4. 右侧主要内容区 --- */
        main {{ 
            margin-left: var(--sidebar-width); flex: 1; padding: 0; 
            position: relative; 
        }}
        
        /* 浅色内容面板：最大模糊 + 浅色蒙版 */
        .content-panel {{
            background: var(--content-panel-bg-blend); 
            min-height: 100vh;
            backdrop-filter: blur(10px); 
            -webkit-backdrop-filter: blur(10px);
        }}
        
        /* 头部 Banner (清晰) */
        .hero-banner {{
            height: 300px; width: 100%; 
            background-image: {f"url('{BANNER}')" if BANNER else "none"};
            background-size: cover; background-position: center;
            position: relative; margin-bottom: 0; 
            z-index: 1; 
        }}

        /* 渐变蒙版，完美衔接 Banner 和内容面板 (优化) */
        .hero-banner::after {{
            content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 100px;
            /* 使用更柔和的渐变过渡 */
            background: linear-gradient(to top, var(--content-panel-bg-blend) 50%, transparent 100%);
            z-index: 2; 
        }}
        
        .content-wrapper {{ padding: 0 60px 100px; max-width: 1400px; margin: 0 auto; position: relative; z-index: 3; }}
        
        section {{ margin-bottom: 100px; scroll-margin-top: 40px; }}
        h2 {{ 
            font-size: 2rem; margin-bottom: 30px; border-bottom: 1px solid #222; padding-bottom: 15px; color: #fff; 
            /* 主内容区标题阴影 */
            text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
        }}
        
        /* --- 布局安全修正 (V4.5) --- */
        .item, .art-item {{ 
            box-sizing: border-box; 
            max-width: 100%; 
            background: rgba(0,0,0,0.3); border-radius: 8px; overflow: hidden; transition: 0.3s; 
        }} 
        .art-item img, .comp-media, video {{ 
            max-width: 100%; 
            width: 100%; display: block; 
        }}
        /* --- 布局安全修正结束 --- */
        
        /* 视频/合成 Grid 样式 */
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 30px; }}
        .grid.single-col-comp {{ grid-template-columns: 1fr; max-width: 800px; margin: 0 auto; }}

        .item:hover {{ transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        
        /* --- Illustration/Art 区 Masonry 样式 --- */
        .masonry {{ column-count: 3; column-gap: 25px; }}
        .masonry.single-col {{ column-count: 1; max-width: 800px; margin: 0 auto; }}

        .art-item {{ margin-bottom: 25px; cursor: pointer; }}
        .art-item:hover {{ transform: scale(1.03); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }} 
        
        @media (max-width: 768px) {{ .masonry {{ column-count: 1; }} }}

        /* --- 合成对比修复 --- */
        .comp-wrapper {{ position: relative; aspect-ratio: 16/9; overflow: hidden; cursor: ew-resize; }}
        .comp-media {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; pointer-events: none; }}
        .comp-wrapper video {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; pointer-events: none; }}

        .slider-input {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; z-index: 10; margin: 0; cursor: ew-resize; }}
        .handle {{ position: absolute; top: 0; bottom: 0; left: 50%; width: 2px; background: #fff; z-index: 5; pointer-events: none; box-shadow: 0 0 10px rgba(0,0,0,0.5); }}
        .handle::after {{ content: "↔"; position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); width: 30px; height: 30px; background: #fff; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
        
        /* --- Lightbox 浮动模态框修复 (V4.7) --- */
        .lightbox {{ 
            background: rgba(0,0,0,0.85); 
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            z-index: 1000; justify-content: center; align-items: center; 
        }}
        
        .lightbox-viewer {{
            max-width: 90vw; max-height: 90vh;
            background: var(--bg); 
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            position: relative; 
            display: flex; align-items: center; justify-content: center;
        }}
        
        .lightbox-viewer img {{
            max-width: 100%; 
            max-height: 90vh; 
            object-fit: contain;
            transition: opacity 0.3s;
            display: block;
            padding: 20px; 
        }}

        .nav-btn {{
            position: absolute; 
            top: 50%; transform: translateY(-50%);
            background: rgba(0,0,0,0.4); 
            color: #fff; border: none;
            padding: 10px 15px; 
            font-size: 3rem; 
            cursor: pointer;
            z-index: 1010; 
            transition: background 0.2s, opacity 0.2s;
            width: 50px; 
            display: flex; align-items: center; justify-content: center;
            opacity: 0; 
            border-radius: 8px; 
        }}
        
        .lightbox-viewer:hover .nav-btn {{
            opacity: 1; 
        }}
        .nav-btn:hover {{ 
            background: rgba(0,0,0,0.7); 
            opacity: 1; 
        }}
        .nav-btn.prev {{ left: 0; border-radius: 12px 0 0 12px; height: calc(100% - 40px); }} 
        .nav-btn.next {{ right: 0; border-radius: 0 12px 12px 0; height: calc(100% - 40px); }}

        .lightbox-close {{ 
            position: absolute; 
            top: 15px; right: 20px; 
            color: #fff; 
            font-size: 2rem; cursor: pointer; z-index: 1020; opacity: 0.8; 
            transition: opacity 0.2s, transform 0.2s; 
            padding: 5px; 
        }}
        .lightbox-close:hover {{ opacity: 1; transform: scale(1.1); }}
    </style>
</head>
<body>
'''

# --- 侧边栏 HTML (内容) ---
html += f'''
    <aside>
        <div class="profile-header">
            {f'<div class="avatar-wrapper"><img src="{AVATAR}" class="avatar"></div>' if AVATAR else ''}
            <h1 class="name">{profile_data['name']}</h1>
            <div class="role">{profile_data['role']}</div>
            <div class="bio">{profile_data['bio']}</div>
            
            <div class="contact-group">
                {get_contact_html("Email", "✉️", profile_data['email'])}
                {get_contact_html("Wechat", "💬", profile_data['wechat'])}
                {get_contact_html("QQ", "🐧", profile_data['qq'])}
            </div>
        </div>
        
        <nav>
            <a href="#animation" class="nav-item">
                {CONFIG['sections']['animation']} 
                <span class="nav-count">VIDEO</span>
            </a>
            <a href="#compositing" class="nav-item">
                {CONFIG['sections']['compositing']}
                <span class="nav-count">COMP</span>
            </a>
            <a href="#illustration" class="nav-item">
                {CONFIG['sections']['illustration']}
                <span class="nav-count">ART</span>
            </a>
        </nav>

        <div class="footer-links">
            {get_social_links_html(CONFIG)}
        </div>
    </aside>

    <main>
        <div class="content-panel"> <div class="hero-banner">
                </div>
            
            <div class="content-wrapper">
'''

# --- 内容生成函数 (保持 V4.6 逻辑) ---
def section_vid():
    html = f'<section id="animation"><h2>{CONFIG["sections"]["animation"]}</h2><div class="grid">'
    files = get_files('videos', ['.mp4', '.mov', '.webm'])
    for f in files:
        html += f'<div class="item"><video controls loop playsinline><source src="{f}" type="video/mp4"></video></div>'
    return html + '</div></section>'

def section_comp():
    all_exts = ['.jpg', '.png', '.mp4', '.mov', '.webm']
    files = get_files('compositing', all_exts)
    pairs = {}
    
    for f in files:
        if '_after' in f:
            base_name_ext = f.replace('_after', '')
            base = os.path.dirname(f) + '/' + os.path.splitext(os.path.basename(base_name_ext))[0]
            ext = os.path.splitext(f)[1]
            
            is_video = ext.lower() in ['.mp4', '.mov', '.webm']
            
            if base not in pairs:
                comp_id = "comp-" + os.path.basename(base).split('/')[-1].replace('.', '-')
                pairs[base] = {'type': 'video' if is_video else 'image', 'after': f, 'before': None, 'id': comp_id}
            else:
                pairs[base]['after'] = f
    
    valid_pairs = {}
    for base, data in pairs.items():
        ext = os.path.splitext(data['after'])[1] 
        base_filename_no_ext = os.path.splitext(os.path.basename(data['after']).replace('_after', ''))[0]
        before_name_full_path = os.path.join(os.path.dirname(data['after']), f"{base_filename_no_ext}_before{ext}")
        
        if before_name_full_path.replace(os.sep, '/') in files:
            data['before'] = before_name_full_path.replace(os.sep, '/')
            valid_pairs[base] = data
            
    num_pairs = len(valid_pairs)
    grid_class = 'grid'
    if num_pairs == 1:
        grid_class = 'grid single-col-comp'

    html = f'<section id="compositing"><h2>{CONFIG["sections"]["compositing"]}</h2><div class="{grid_class}">'
            
    for base, data in valid_pairs.items():
        comp_id = data['id']
        
        if data['type'] == 'video':
            content = f'''
                <video id="{comp_id}-before" src="{data['before']}" class="comp-media" loop playsinline muted></video>
                <video id="{comp_id}-after" src="{data['after']}" class="comp-media" style="clip-path: inset(0 50% 0 0);" loop playsinline muted></video>
            '''
            item_html = f'''
            <div class="item video-comp" onclick="toggleVideoPlay('{comp_id}')">
                <div class="comp-wrapper">
                    {content}
                    <div class="handle"></div>
                    <input type="range" min="0" max="100" value="50" class="slider-input" 
                        oninput="this.previousElementSibling.style.left=this.value+'%'; this.previousElementSibling.previousElementSibling.style.clipPath='inset(0 '+(100-this.value)+'% 0 0)'">
                </div>
            </div>'''
        else:
            content = f'''
                <img src="{data['before']}" class="comp-media">
                <img src="{data['after']}" class="comp-media" style="clip-path: inset(0 50% 0 0);">
            '''
            item_html = f'''
            <div class="item image-comp">
                <div class="comp-wrapper">
                    {content}
                    <div class="handle"></div>
                    <input type="range" min="0" max="100" value="50" class="slider-input" 
                        oninput="this.previousElementSibling.style.left=this.value+'%'; this.previousElementSibling.previousElementSibling.style.clipPath='inset(0 '+(100-this.value)+'% 0 0)'">
                </div>
            </div>'''
        
        html += item_html
            
    return html + '</div></section>'

def section_art():
    masonry_class = 'masonry'
    if len(ART_FILES) == 1:
        masonry_class = 'masonry single-col'
    
    html = f'<section id="illustration"><h2>{CONFIG["sections"]["illustration"]}</h2><div class="{masonry_class}">'
    for i, f in enumerate(ART_FILES):
        html += f'<div class="art-item" onclick="openL({i})"><img src="{f}" loading="lazy"></div>'
    return html + '</div></section>'

# --- 脚本与固定元素 HTML ---
scripts = f'''
            </div> </div> </main>

    <div class="lightbox" id="lightbox" onclick="closeL()">
        <div class="lightbox-viewer" onclick="event.stopPropagation()">
            <span class="lightbox-close" onclick="closeL()">&times;</span>
            <button class="nav-btn prev" onclick="navigateL(-1)">❮</button>
            <img id="l-img" src="" alt="Artwork">
            <button class="nav-btn next" onclick="navigateL(1)">❯</button>
        </div>
    </div>
    
    <div class="particles" id="particles-js"></div> <div class="color-adapt-base"></div> <script>
        // 将 Python 列表转为 JS 数组
        const ARTWORK_PATHS = {ART_FILES_JSON};
        let currentArtIndex = 0;

        // 打开 Lightbox 并定位到指定索引
        function openL(index) {{ 
            if (ARTWORK_PATHS.length === 0) return;
            currentArtIndex = index;
            document.getElementById('l-img').src = ARTWORK_PATHS[currentArtIndex];
            document.getElementById('lightbox').style.display = 'flex';
        }}
        
        // 关闭 Lightbox
        function closeL() {{
            document.getElementById('lightbox').style.display = 'none';
        }}

        // Lightbox 翻页功能
        function navigateL(direction) {{
            event.stopPropagation(); 
            
            currentArtIndex += direction;
            
            // 循环翻页逻辑
            if (currentArtIndex < 0) {{
                currentArtIndex = ARTWORK_PATHS.length - 1;
            }} else if (currentArtIndex >= ARTWORK_PATHS.length) {{
                currentArtIndex = 0;
            }}
            
            // 更新图片，使用淡入效果优化切换体验
            const img = document.getElementById('l-img');
            img.style.opacity = 0;
            setTimeout(() => {{
                img.src = ARTWORK_PATHS[currentArtIndex];
                img.style.opacity = 1;
            }}, 150);
        }}
        
        // 键盘导航 (ESC 关闭, 左右箭头翻页)
        document.addEventListener('keydown', (e) => {{
            if (document.getElementById('lightbox').style.display === 'flex') {{
                if (e.key === 'Escape') {{
                    closeL();
                }} else if (e.key === 'ArrowLeft') {{
                    navigateL(-1);
                }} else if (e.key === 'ArrowRight') {{
                    navigateL(1);
                }}
            }}
        }});

        // 视频对比同步播放功能 
        function toggleVideoPlay(id_prefix) {{
            const vidA = document.getElementById(id_prefix + '-before');
            const vidB = document.getElementById(id_prefix + '-after');
            
            if (vidA && vidB) {{
                if (!vidA.paused) {{
                    vidA.pause();
                    vidB.pause();
                }} else {{
                    vidA.currentTime = vidB.currentTime;
                    vidA.play();
                    vidB.play();
                }}
            }}
        }}

        // 通用联系方式复制功能 
        function copyContact(content, boxId) {{
            const box = document.getElementById(boxId);

            document.querySelectorAll('.contact-container').forEach(el => el.classList.remove('active'));

            if (navigator.clipboard) {{
                navigator.clipboard.writeText(content).then(() => {{
                    box.classList.add('active');
                    setTimeout(() => {{ box.classList.remove('active'); }}, 2000);
                }}).catch(err => {{
                    console.error('Copy failed:', err);
                    alert('复制失败，请手动复制: ' + content);
                }});
            }} else {{
                alert('您的浏览器不支持自动复制功能，请手动复制: ' + content);
            }}
        }}
        
        // 浮动粒子生成脚本 - 实现景深和视差 (V4.8 增强版)
        (function generateParticles() {{
            const container = document.getElementById('particles-js');
            const numParticles = 80; // 数量翻倍
            
            for (let i = 0; i < numParticles; i++) {{
                const p = document.createElement('div');
                const depth = Math.random(); 
                
                let size;
                let opacity; 

                if (depth < 0.3) {{ // 远景：小、淡、慢
                    opacity = Math.random() * 0.2 + 0.3; // 最小 0.3
                    size = Math.random() * 1 + 3; 
                }} else if (depth < 0.7) {{ // 中景：中速、中等 
                    opacity = Math.random() * 0.4 + 0.5; // 最小 0.5
                    size = Math.random() * 2 + 5; 
                }} else {{ // 近景：快、大、亮
                    opacity = Math.random() * 0.5 + 0.5; // 最小 0.5，最大 1.0
                    size = Math.random() * 3 + 7; 
                }}

                p.className = 'particle';

                p.style.left = Math.random() * 100 + 'vw';
                p.style.top = Math.random() * 100 + 'vh';
                
                p.style.width = p.style.height = size + 'px';
                p.style.background = '#fff'; // 确保粒子颜色是白色
                p.style.opacity = opacity; // 使用 JS 确定的透明度

                const duration = Math.random() * 15 + 10; 
                p.style.animationDuration = duration + 's'; 
                p.style.animationDelay = -Math.random() * duration + 's';
                
                container.appendChild(p);
            }}
        }})();
    </script>
</body></html>
'''

# --- 文件写入 ---
print("正在生成网页...")
content = html + section_vid() + section_comp() + section_art() + scripts
try:
    with open("index.html", "w", encoding="utf-8") as f: 
        f.write(content)
    print("✅ 成功！index.html 已生成。")
except Exception as e:
    print(f"❌ 写入文件时发生错误: {e}")

# --- 运行提示 ---
if __name__ == "__main__":
    print("\n--------------------------------------------------------------------------------")
    print("请使用命令行运行此文件（py build.py），以生成最新的 index.html 文件。")
    print("--------------------------------------------------------------------------------")
