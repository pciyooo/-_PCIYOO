import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import shutil
import subprocess
import glob # 确保 glob 导入

CONFIG_FILE = "config.json"
ASSETS_DIR = "assets"

class PortfolioManager:
    def __init__(self, root):
        self.root = root
        self.root.title("作品集管家 V3.0 (含社交链接管理)")
        # 调整尺寸适应更长的列表
        self.root.geometry("750x780") 
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.config_data = self.load_config()
        
        # --- 1. 个人信息与链接 (重构) ---
        self.page_info = ttk.Frame(self.notebook)
        self.notebook.add(self.page_info, text=" 📝 个人信息与链接 ")
        self.build_info_page()
        
        # --- 2. 合成配对神器 ---
        self.page_comp = ttk.Frame(self.notebook)
        self.notebook.add(self.page_comp, text=" ⚔️ 合成图配对神器 ")
        self.build_comp_tool()
        
        # --- 3. 普通文件添加 ---
        self.page_files = ttk.Frame(self.notebook)
        self.notebook.add(self.page_files, text=" 📂 添加视频/插画 ")
        self.build_files_page()

        # 底部按钮
        frame_btn = ttk.Frame(root, padding=10)
        frame_btn.pack(fill=tk.X)
        ttk.Button(frame_btn, text="💾 保存所有配置", command=self.save_config).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(frame_btn, text="🚀 生成网页", command=self.run_build).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(frame_btn, text="🌏 预览", command=self.open_browser).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f: 
                data = json.load(f)
                if "social_links" not in data:
                    data["social_links"] = []
                return data
        except: return {"social_links": []}

    # --- 页面构建 ---

    def build_info_page(self):
        f = ttk.Frame(self.page_info, padding=20)
        f.pack(fill=tk.BOTH, expand=True)
        
        # --- 1. 基础信息 ---
        frame_base = ttk.LabelFrame(f, text="基础信息", padding=15)
        frame_base.pack(fill=tk.X, pady=10)

        data = self.config_data.get("profile", {})
        
        # 行 0: 名字
        ttk.Label(frame_base, text="名字:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_name = ttk.Entry(frame_base, width=40)
        self.entry_name.grid(row=0, column=1, sticky="w")
        self.entry_name.insert(0, data.get("name", ""))
        
        # 行 1: 职位
        ttk.Label(frame_base, text="职位:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_role = ttk.Entry(frame_base, width=40)
        self.entry_role.grid(row=1, column=1, sticky="w")
        self.entry_role.insert(0, data.get("role", ""))

        # 行 2: 邮箱
        ttk.Label(frame_base, text="邮箱:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(frame_base, width=40)
        self.entry_email.grid(row=2, column=1, sticky="w")
        self.entry_email.insert(0, data.get("email", ""))
        
        # 行 3: 微信号
        ttk.Label(frame_base, text="微信号:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_wechat = ttk.Entry(frame_base, width=40)
        self.entry_wechat.grid(row=3, column=1, sticky="w")
        self.entry_wechat.insert(0, data.get("wechat", ""))
        
        # 行 4: QQ号
        ttk.Label(frame_base, text="QQ号:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_qq = ttk.Entry(frame_base, width=40)
        self.entry_qq.grid(row=4, column=1, sticky="w")
        self.entry_qq.insert(0, data.get("qq", ""))

        # 行 5: 个人简介
        ttk.Label(frame_base, text="个人简介:").grid(row=5, column=0, sticky="nw", pady=5)
        self.text_bio = tk.Text(frame_base, height=4, width=40, font=('TkDefaultFont', 9))
        self.text_bio.grid(row=5, column=1, sticky="w")
        self.text_bio.insert("1.0", data.get("bio", ""))
        
        # --- 2. 社交链接表格 ---
        frame_social = ttk.LabelFrame(f, text="社交平台链接管理", padding=15)
        frame_social.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview (表格)
        self.tree_social = ttk.Treeview(frame_social, columns=("name", "url"), show="headings", selectmode="browse")
        self.tree_social.heading("name", text="平台名称 (例如: Bilibili)")
        self.tree_social.heading("url", text="链接地址 (URL)")
        self.tree_social.column("name", width=150, anchor="w")
        self.tree_social.column("url", width=350, anchor="w")
        self.tree_social.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        vsb = ttk.Scrollbar(frame_social, orient="vertical", command=self.tree_social.yview)
        vsb.pack(side=tk.RIGHT, fill="y")
        self.tree_social.configure(yscrollcommand=vsb.set)
        
        # 填充数据
        self.refresh_social_tree()

        # 链接管理按钮
        frame_social_btns = ttk.Frame(frame_social)
        frame_social_btns.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(frame_social_btns, text="➕ 添加新链接", command=self.add_social_link).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_social_btns, text="✏️ 编辑选中链接", command=self.edit_social_link).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_social_btns, text="❌ 删除选中链接", command=self.delete_social_link).pack(side=tk.LEFT, padx=5)

        # --- 3. 资源上传 ---
        frame_asset = ttk.LabelFrame(f, text="头像与背景图", padding=15)
        frame_asset.pack(fill=tk.X, pady=10)
        ttk.Button(frame_asset, text="📂 更换头像 (avatar.jpg/png)", command=lambda: self.up_asset("avatar")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(frame_asset, text="📂 更换背景 (banner.jpg/png)", command=lambda: self.up_asset("banner")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def refresh_social_tree(self):
        # 清空现有条目
        for i in self.tree_social.get_children():
            self.tree_social.delete(i)
        # 重新插入数据
        for item in self.config_data["social_links"]:
            self.tree_social.insert("", tk.END, values=(item.get("name", ""), item.get("url", "")))

    def show_social_edit_dialog(self, title, initial_name="", initial_url=""):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x180")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_set()
        
        result = {}

        ttk.Label(dialog, text="平台名称:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        name_entry.insert(0, initial_name)

        ttk.Label(dialog, text="链接 URL:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        url_entry = ttk.Entry(dialog, width=40)
        url_entry.grid(row=1, column=1, padx=10, pady=10)
        url_entry.insert(0, initial_url)
        
        def save_and_close():
            result['name'] = name_entry.get()
            result['url'] = url_entry.get()
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="确定", command=save_and_close).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

        self.root.wait_window(dialog)
        return result if 'name' in result else None

    def add_social_link(self):
        data = self.show_social_edit_dialog("添加新社交链接")
        if data and data['name'] and data['url']:
            self.config_data["social_links"].append({"name": data['name'], "url": data['url']})
            self.refresh_social_tree()
            messagebox.showinfo("提示", "新链接已添加，请记得点击【保存所有配置】。")

    def edit_social_link(self):
        selected = self.tree_social.focus()
        if not selected:
            messagebox.showwarning("警告", "请先在表格中选择一个链接条目。")
            return
        
        selected_index = self.tree_social.index(selected)
        original_data = self.config_data["social_links"][selected_index]
        
        data = self.show_social_edit_dialog("编辑社交链接", original_data['name'], original_data['url'])
        
        if data and data['name'] and data['url']:
            self.config_data["social_links"][selected_index] = {"name": data['name'], "url": data['url']}
            self.refresh_social_tree()
            messagebox.showinfo("提示", "链接已修改，请记得点击【保存所有配置】。")

    def delete_social_link(self):
        selected = self.tree_social.focus()
        if not selected:
            messagebox.showwarning("警告", "请先在表格中选择一个链接条目。")
            return

        if messagebox.askyesno("确认删除", "确定要删除选中的社交链接吗？"):
            selected_index = self.tree_social.index(selected)
            self.config_data["social_links"].pop(selected_index)
            self.refresh_social_tree()
            messagebox.showinfo("提示", "链接已删除，请记得点击【保存所有配置】。")


    def build_comp_tool(self):
        f = ttk.Frame(self.page_comp, padding=20)
        f.pack(fill=tk.BOTH)
        
        ttk.Label(f, text="不用手动改名！选择两张图，起个名，自动搞定。", foreground="#666").pack(pady=(0, 20))
        
        self.path_before = tk.StringVar()
        self.path_after = tk.StringVar()
        
        fr_a = ttk.LabelFrame(f, text="1. 选择 Before (线稿/原片)", padding=10)
        fr_a.pack(fill=tk.X, pady=5)
        ttk.Entry(fr_a, textvariable=self.path_before).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(fr_a, text="浏览...", command=lambda: self.path_before.set(filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")]))).pack(side=tk.LEFT, padx=5)
        
        fr_b = ttk.LabelFrame(f, text="2. 选择 After (成片)", padding=10)
        fr_b.pack(fill=tk.X, pady=5)
        ttk.Entry(fr_b, textvariable=self.path_after).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(fr_b, text="浏览...", command=lambda: self.path_after.set(filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")]))).pack(side=tk.LEFT, padx=5)
        
        fr_name = ttk.Frame(f, padding=10)
        fr_name.pack(fill=tk.X, pady=10)
        ttk.Label(fr_name, text="3. 命名 (例如 scene01): ").pack(side=tk.LEFT)
        self.entry_comp_name = ttk.Entry(fr_name, width=20)
        self.entry_comp_name.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(f, text="✨ 自动改名并添加到作品集", command=self.process_comp).pack(fill=tk.X, pady=10)

    def build_files_page(self):
        f = ttk.Frame(self.page_files, padding=30)
        f.pack(fill=tk.BOTH)
        ttk.Button(f, text="➕ 添加 MP4 视频", command=lambda: self.add_files("videos", "*.mp4")).pack(fill=tk.X, pady=10)
        ttk.Button(f, text="➕ 添加 插画图片", command=lambda: self.add_files("illustrations", "*.jpg *.png")).pack(fill=tk.X, pady=10)

    # --- 逻辑处理 ---

    def up_asset(self, name):
        path = filedialog.askopenfilename(filetypes=[("Img", "*.jpg *.png")])
        if path:
            if not os.path.exists("assets"): os.makedirs("assets")
            ext = os.path.splitext(path)[1]
            for old in glob.glob(os.path.join("assets", f"{name}.*")):
                os.remove(old)
            shutil.copy(path, f"assets/{name}{ext}")
            messagebox.showinfo("OK", f"{name} 已更新")

    def process_comp(self):
        p1, p2 = self.path_before.get(), self.path_after.get()
        name = self.entry_comp_name.get().strip()
        
        if not (p1 and p2 and name):
            messagebox.showwarning("提示", "请把两个文件都选上，并输入名字")
            return
            
        target_dir = "compositing"
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        
        ext1 = os.path.splitext(p1)[1]
        ext2 = os.path.splitext(p2)[1]
        
        try:
            shutil.copy(p1, os.path.join(target_dir, f"{name}_before{ext1}"))
            shutil.copy(p2, os.path.join(target_dir, f"{name}_after{ext2}"))
            
            self.path_before.set("")
            self.path_after.set("")
            self.entry_comp_name.delete(0, tk.END)
            messagebox.showinfo("成功", f"已生成:\n{name}_before{ext1}\n{name}_after{ext2}\n并存入 compositing 文件夹！")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_files(self, folder, types):
        files = filedialog.askopenfilenames(filetypes=[("Files", types)])
        if files:
            if not os.path.exists(folder): os.makedirs(folder)
            count = 0
            for f in files: 
                shutil.copy(f, folder)
                count += 1
            messagebox.showinfo("OK", f"添加了 {count} 个文件到 {folder} 文件夹。")

    def save_config(self):
        if "profile" not in self.config_data: self.config_data["profile"] = {}
        
        self.config_data["profile"]["name"] = self.entry_name.get()
        self.config_data["profile"]["role"] = self.entry_role.get()
        self.config_data["profile"]["email"] = self.entry_email.get()
        self.config_data["profile"]["wechat"] = self.entry_wechat.get()
        self.config_data["profile"]["qq"] = self.entry_qq.get()
        self.config_data["profile"]["bio"] = self.text_bio.get("1.0", "end-1c")
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("OK", "所有配置已保存到 config.json!")

    def run_build(self):
        try:
            # 确保保存，防止用户忘记
            self.save_config() 
            subprocess.run(["python", "build.py"], check=True)
            messagebox.showinfo("OK", "网页已成功生成！")
        except Exception as e:
            messagebox.showerror("生成失败", str(e))

    def open_browser(self):
        if os.path.exists("index.html"):
            os.startfile("index.html")
        else:
            messagebox.showwarning("提示", "请先点击【生成网页】")

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioManager(root)
    root.mainloop()
