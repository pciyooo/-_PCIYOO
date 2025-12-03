import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
import shutil
import subprocess
import glob
import sys  # 新增：用于获取当前Python路径，确保build能运行

CONFIG_FILE = "config.json"
DIRECTORIES = ["assets", "projects", "flipbooks", "compositing", "illustrations", "videos"]

class PortfolioManager:
    def __init__(self, root):
        self.root = root
        self.root.title("作品集管家 V5.0 (原画视频支持版)")
        self.root.geometry("950x880")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.ensure_dirs()
        self.config_data = self.load_config()
        
        # --- 1. 个人信息 ---
        self.page_info = ttk.Frame(self.notebook)
        self.notebook.add(self.page_info, text=" 📝 个人信息 ")
        self.build_info_page()
        
        # --- 2. 核心展示 (项目 + 原画) ---
        self.page_main = ttk.Frame(self.notebook)
        self.notebook.add(self.page_main, text=" 🎬 项目与原画镜头 ")
        self.build_main_page()

        # --- 3. 合成对比 ---
        self.page_comp = ttk.Frame(self.notebook)
        self.notebook.add(self.page_comp, text=" ⚔️ 合成对比 ")
        self.build_comp_tool()
        
        # --- 4. 基础资源 ---
        self.page_files = ttk.Frame(self.notebook)
        self.notebook.add(self.page_files, text=" 📂 画廊与其他 ")
        self.build_files_page()

        # 底部按钮
        frame_btn = ttk.Frame(root, padding=15)
        frame_btn.pack(fill=tk.X)
        
        # 使用大号字体强调
        btn_style = ttk.Style()
        btn_style.configure("Big.TButton", font=("微软雅黑", 10, "bold"))
        
        ttk.Button(frame_btn, text="💾 保存配置 (Save)", style="Big.TButton", command=self.save_config).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(frame_btn, text="🚀 生成网页 (Build)", style="Big.TButton", command=self.run_build).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(frame_btn, text="🌏 浏览器预览 (Preview)", style="Big.TButton", command=self.open_browser).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    def ensure_dirs(self):
        for d in DIRECTORIES:
            if not os.path.exists(d): os.makedirs(d)

    def load_config(self):
        default = {"profile": {}, "social_links": [], "projects": []}
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**default, **json.load(f)}
        except: return default

    # --- 1. 个人信息页 ---
    def build_info_page(self):
        f = ttk.Frame(self.page_info, padding=20)
        f.pack(fill=tk.BOTH, expand=True)
        
        # 左：基础信息
        left = ttk.Frame(f)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
        
        fr_base = ttk.LabelFrame(left, text="基础资料", padding=10)
        fr_base.pack(fill=tk.X)
        
        self.entries = {}
        fields = [("姓名", "name"), ("职位", "role"), ("邮箱", "email"), ("微信", "wechat"), ("QQ", "qq")]
        for i, (lbl, key) in enumerate(fields):
            ttk.Label(fr_base, text=lbl).grid(row=i, column=0, sticky="w", pady=5)
            e = ttk.Entry(fr_base, width=35)
            e.grid(row=i, column=1, sticky="w", padx=5)
            e.insert(0, self.config_data["profile"].get(key, ""))
            self.entries[key] = e
            
        ttk.Label(fr_base, text="简介").grid(row=5, column=0, sticky="nw", pady=5)
        self.txt_bio = tk.Text(fr_base, height=5, width=35, font=("微软雅黑", 9))
        self.txt_bio.grid(row=5, column=1, padx=5)
        self.txt_bio.insert("1.0", self.config_data["profile"].get("bio", ""))
        
        # 资源
        fr_asset = ttk.LabelFrame(left, text="核心图片", padding=10)
        fr_asset.pack(fill=tk.X, pady=10)
        ttk.Button(fr_asset, text="📂 上传头像 (Avatar)", command=lambda: self.up_asset("avatar")).pack(fill=tk.X, pady=2)
        ttk.Button(fr_asset, text="📂 上传背景图 (Banner)", command=lambda: self.up_asset("banner")).pack(fill=tk.X, pady=2)

        # 右：社交链接
        right = ttk.LabelFrame(f, text="社交链接", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.tree_social = ttk.Treeview(right, columns=("name", "url"), show="headings")
        self.tree_social.heading("name", text="平台名称")
        self.tree_social.heading("url", text="链接地址")
        self.tree_social.column("name", width=80)
        self.tree_social.pack(fill=tk.BOTH, expand=True)
        
        btn_box = ttk.Frame(right)
        btn_box.pack(fill=tk.X, pady=5)
        ttk.Button(btn_box, text="➕ 添加", command=self.add_social).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_box, text="✏️ 编辑", command=self.edit_social).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_box, text="❌ 删除", command=self.del_social).pack(side=tk.LEFT, padx=2)
        self.refresh_social()

    # --- 2. 项目与原画 (支持视频了！) ---
    def build_main_page(self):
        f = ttk.Frame(self.page_main, padding=20)
        f.pack(fill=tk.BOTH, expand=True)
        
        # A. 参与项目 (Bento)
        fr_proj = ttk.LabelFrame(f, text="1. 重点参与项目 (Bento Grid)", padding=10)
        fr_proj.pack(fill=tk.BOTH, expand=True)
        
        self.list_proj = tk.Listbox(fr_proj, height=5)
        self.list_proj.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_proj.bind('<<ListboxSelect>>', self.load_proj_detail)
        
        fr_proj_edit = ttk.Frame(fr_proj, padding=(10,0))
        fr_proj_edit.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.p_title = tk.StringVar()
        self.p_role = tk.StringVar()
        self.p_cover = tk.StringVar()
        self.p_video = tk.StringVar()
        self.curr_p_idx = -1
        
        ttk.Label(fr_proj_edit, text="项目名:").pack(anchor="w")
        ttk.Entry(fr_proj_edit, textvariable=self.p_title).pack(fill=tk.X)
        ttk.Label(fr_proj_edit, text="担任职责:").pack(anchor="w")
        ttk.Entry(fr_proj_edit, textvariable=self.p_role).pack(fill=tk.X)
        
        b1 = ttk.Frame(fr_proj_edit)
        b1.pack(fill=tk.X, pady=2)
        ttk.Entry(b1, textvariable=self.p_cover).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(b1, text="选封面", width=8, command=lambda: self.pick_file(self.p_cover, "*.jpg *.png", "projects")).pack(side=tk.RIGHT)
        
        b2 = ttk.Frame(fr_proj_edit)
        b2.pack(fill=tk.X, pady=2)
        ttk.Entry(b2, textvariable=self.p_video).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(b2, text="选视频", width=8, command=lambda: self.pick_file(self.p_video, "*.mp4", "projects")).pack(side=tk.RIGHT)
        
        bp = ttk.Frame(fr_proj_edit)
        bp.pack(fill=tk.X, pady=5)
        ttk.Button(bp, text="新建", command=self.new_proj).pack(side=tk.LEFT)
        ttk.Button(bp, text="保存修改", command=self.save_proj).pack(side=tk.LEFT, padx=5)
        ttk.Button(bp, text="删除", command=self.del_proj).pack(side=tk.LEFT)
        
        self.refresh_proj_list()
        
        # B. 原画/镜头 (Flipbook + Video)
        fr_flip = ttk.LabelFrame(f, text="2. 原画与镜头展示 (支持序列帧与视频)", padding=10)
        fr_flip.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 操作区
        op_frame = ttk.Frame(fr_flip)
        op_frame.pack(fill=tk.X, pady=5)

        # 序列帧操作
        fr_seq = ttk.Labelframe(op_frame, text="添加序列帧翻页书 (Flipbook)", padding=5)
        fr_seq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5))
        
        self.flip_src = tk.StringVar()
        self.flip_name = tk.StringVar()
        
        r1 = ttk.Frame(fr_seq); r1.pack(fill=tk.X)
        ttk.Entry(r1, textvariable=self.flip_src).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(r1, text="选文件夹", command=lambda: self.flip_src.set(filedialog.askdirectory())).pack(side=tk.LEFT)
        
        r2 = ttk.Frame(fr_seq); r2.pack(fill=tk.X, pady=2)
        ttk.Label(r2, text="命名:").pack(side=tk.LEFT)
        ttk.Entry(r2, textvariable=self.flip_name, width=10).pack(side=tk.LEFT)
        ttk.Button(r2, text="生成", command=self.gen_flip).pack(side=tk.LEFT, padx=5)

        # 视频操作
        fr_vid = ttk.Labelframe(op_frame, text="添加原画/Layout视频 (.mp4)", padding=5)
        fr_vid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Button(fr_vid, text="➕ 选择视频文件并添加", command=self.add_genga_video).pack(fill=tk.BOTH, expand=True, pady=10)

        # 列表
        ttk.Label(fr_flip, text="已添加的内容 (文件夹=序列帧 / .mp4=视频):").pack(anchor="w")
        self.list_flips = tk.Listbox(fr_flip, height=4)
        self.list_flips.pack(fill=tk.X, pady=2)
        ttk.Button(fr_flip, text="删除选中项", command=self.del_flip).pack(anchor="w")
        self.refresh_flips()

    # --- 3. 合成工具 ---
    def build_comp_tool(self):
        f = ttk.Frame(self.page_comp, padding=20)
        f.pack(fill=tk.BOTH)
        
        self.c_before = tk.StringVar()
        self.c_after = tk.StringVar()
        self.c_name = tk.StringVar()
        
        fr = ttk.LabelFrame(f, text="合成前后对比 (支持图/视频)", padding=15)
        fr.pack(fill=tk.X)
        
        for lbl, var in [("Before (Raw/Green)", self.c_before), ("After (Final Comp)", self.c_after)]:
            r = ttk.Frame(fr)
            r.pack(fill=tk.X, pady=5)
            ttk.Label(r, text=lbl, width=18).pack(side=tk.LEFT)
            ttk.Entry(r, textvariable=var).pack(side=tk.LEFT, fill=tk.X, expand=True)
            ttk.Button(r, text="浏览", width=6, command=lambda v=var: v.set(filedialog.askopenfilename())).pack(side=tk.LEFT)
            
        r = ttk.Frame(fr)
        r.pack(fill=tk.X, pady=15)
        ttk.Label(r, text="镜头命名 (如 sc01)", width=18).pack(side=tk.LEFT)
        ttk.Entry(r, textvariable=self.c_name).pack(side=tk.LEFT)
        ttk.Button(r, text="✨ 添加配对", command=self.do_comp).pack(side=tk.LEFT, padx=10)

    # --- 4. 基础文件 ---
    def build_files_page(self):
        f = ttk.Frame(self.page_files, padding=20)
        f.pack(fill=tk.BOTH)
        
        ttk.Label(f, text="快速添加素材到画廊或作品流").pack(pady=10)
        ttk.Button(f, text="📂 批量添加 插画图片 (Illustrations)", command=lambda: self.add_bulk("illustrations", "*.jpg *.png")).pack(fill=tk.X, pady=5)
        ttk.Button(f, text="📂 批量添加 其他视频 (Videos)", command=lambda: self.add_bulk("videos", "*.mp4 *.mov")).pack(fill=tk.X, pady=5)

    # --- 逻辑 ---
    
    def add_genga_video(self):
        f = filedialog.askopenfilename(filetypes=[("MP4 Video", "*.mp4")])
        if f:
            name = simpledialog.askstring("命名", "请输入镜头名称 (例如 cut01):")
            if name:
                dest = f"flipbooks/{name}.mp4"
                shutil.copy(f, dest)
                self.refresh_flips()
                messagebox.showinfo("成功", "视频已添加！")

    def refresh_flips(self):
        self.list_flips.delete(0, tk.END)
        if os.path.exists("flipbooks"):
            # 列出文件夹和mp4文件
            items = os.listdir("flipbooks")
            for i in sorted(items):
                if os.path.isdir(f"flipbooks/{i}") or i.endswith(".mp4"):
                    self.list_flips.insert(tk.END, i)

    def del_flip(self):
        sel = self.list_flips.curselection()
        if sel:
            name = self.list_flips.get(sel[0])
            path = f"flipbooks/{name}"
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.refresh_flips()

    # 其余逻辑保持不变
    def refresh_social(self):
        for i in self.tree_social.get_children(): self.tree_social.delete(i)
        for s in self.config_data.get("social_links", []): self.tree_social.insert("", tk.END, values=(s["name"], s["url"]))
            
    def social_dialog(self, name="", url=""):
        t = tk.Toplevel(self.root); t.geometry("300x150"); t.title("编辑")
        res = {}
        ttk.Label(t, text="平台:").pack(); e1=ttk.Entry(t, width=30); e1.pack(); e1.insert(0, name)
        ttk.Label(t, text="链接:").pack(); e2=ttk.Entry(t, width=30); e2.pack(); e2.insert(0, url)
        def ok(): res['name'],res['url']=e1.get(),e2.get(); t.destroy()
        ttk.Button(t, text="OK", command=ok).pack(pady=10)
        self.root.wait_window(t)
        return res

    def add_social(self):
        r = self.social_dialog()
        if r.get("name"): self.config_data["social_links"].append(r); self.refresh_social()
    
    def edit_social(self):
        s = self.tree_social.selection()
        if s:
            idx = self.tree_social.index(s[0])
            old = self.config_data["social_links"][idx]
            r = self.social_dialog(old["name"], old["url"])
            if r.get("name"): self.config_data["social_links"][idx] = r; self.refresh_social()

    def del_social(self):
        s = self.tree_social.selection()
        if s: del self.config_data["social_links"][self.tree_social.index(s[0])]; self.refresh_social()

    def refresh_proj_list(self):
        self.list_proj.delete(0, tk.END)
        for p in self.config_data["projects"]: self.list_proj.insert(tk.END, f"{p.get('title')} ({p.get('role')})")
    
    def load_proj_detail(self, e):
        s = self.list_proj.curselection()
        if s:
            self.curr_p_idx = s[0]
            p = self.config_data["projects"][s[0]]
            self.p_title.set(p.get("title","")); self.p_role.set(p.get("role",""))
            self.p_cover.set(p.get("cover","")); self.p_video.set(p.get("video",""))

    def new_proj(self): self.config_data["projects"].append({"title":"New","role":"-","cover":"","video":""}); self.refresh_proj_list()
    
    def save_proj(self):
        if self.curr_p_idx >= 0:
            self.config_data["projects"][self.curr_p_idx] = {"title":self.p_title.get(),"role":self.p_role.get(),"cover":self.p_cover.get(),"video":self.p_video.get()}
            self.refresh_proj_list()
            
    def del_proj(self):
        if self.curr_p_idx>=0: del self.config_data["projects"][self.curr_p_idx]; self.refresh_proj_list(); self.curr_p_idx=-1

    def gen_flip(self):
        src, name = self.flip_src.get(), self.flip_name.get()
        if src and name:
            dst = f"flipbooks/{name}"
            if os.path.exists(dst): shutil.rmtree(dst)
            shutil.copytree(src, dst)
            for f in os.listdir(dst): 
                if not f.lower().endswith(('.jpg','.png')): os.remove(os.path.join(dst,f))
            self.refresh_flips(); messagebox.showinfo("OK", "翻页书已生成")

    def do_comp(self):
        p1,p2,n = self.c_before.get(), self.c_after.get(), self.c_name.get()
        if p1 and p2 and n:
            e1, e2 = os.path.splitext(p1)[1], os.path.splitext(p2)[1]
            shutil.copy(p1, f"compositing/{n}_before{e1}"); shutil.copy(p2, f"compositing/{n}_after{e2}")
            messagebox.showinfo("OK", "配对已添加")

    def pick_file(self, var, t, f):
        x = filedialog.askopenfilename(filetypes=[("File", t)])
        if x: shutil.copy(x, f"{f}/{os.path.basename(x)}"); var.set(f"{f}/{os.path.basename(x)}")
    
    def up_asset(self, n):
        x = filedialog.askopenfilename(filetypes=[("Img", "*.jpg *.png")])
        if x:
            for o in glob.glob(f"assets/{n}.*"): os.remove(o)
            shutil.copy(x, f"assets/{n}{os.path.splitext(x)[1]}")

    def add_bulk(self, d, t):
        fs = filedialog.askopenfilenames(filetypes=[("File", t)])
        for f in fs: shutil.copy(f, d)
        if fs: messagebox.showinfo("OK", f"已添加 {len(fs)} 个文件")

    def save_config(self):
        for k, e in self.entries.items(): self.config_data["profile"][k] = e.get()
        self.config_data["profile"]["bio"] = self.txt_bio.get("1.0", "end-1c")
        with open(CONFIG_FILE, "w", encoding="utf-8") as f: json.dump(self.config_data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("OK", "配置已保存!")

    def run_build(self):
        self.save_config()
        try:
            # 关键修复：使用 sys.executable 确保调用正确的 python 环境
            subprocess.run([sys.executable, "build.py"], check=True)
            messagebox.showinfo("成功", "网页生成成功！请点击预览。")
        except Exception as e:
            messagebox.showerror("错误", f"生成失败: {str(e)}")

    def open_browser(self):
        if os.path.exists("index.html"): os.startfile("index.html")
        else: messagebox.showwarning("提示", "请先点击生成网页")

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioManager(root)
    root.mainloop()
