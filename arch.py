import subprocess, os, glob, tkinter as tk, tkinter.font as tkfont
import time, threading, psutil, datetime, random, json, math, hashlib
import urllib.request, urllib.parse, re, base64, calendar as cal_mod
import socket, struct, zipfile, difflib, colorsys, sys

# ── Config ─────────────────────────────────────────────────────────────────────
# When frozen as a PyInstaller exe, __file__ points inside the exe bundle.
# sys.executable gives the actual exe path, so we save config next to the exe.
if getattr(sys, "frozen", False):
    _BASE_DIR = os.path.dirname(sys.executable)
else:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(_BASE_DIR, "arch_config.json")

DEFAULT_CONFIG = {
    "theme": "green",
    "favorites": ["chrome", "vscode", "spotify", "discord", "terminal"],
    "aliases": {
        "yt":   "https://youtube.com",
        "gh":   "https://github.com",
        "gpt":  "https://chatgpt.com",
        "maps": "https://maps.google.com",
        "mail": "https://mail.google.com",
    },
    "notes": [],
    "todos": [],
    "lock_hash": "",
    "vault": {},
    "hotkey": "ctrl+space",
    "ai_history": [],
    "scripts_dir": "",
    "splash_quotes": [],
    "inactivity_screensaver": 300,
    "custom_themes": {},
    "prompt_text": "arch~$ ",
    "profiles": {},
    "active_profile": "",
    "autoclose": False,
    "font_size": 13,
    "opacity": 100,
    "topmost": False,
    "motd": "",
    "cron_jobs": [],
    "launch_log": [],
    "templates": {},
    "mood": "",
    "bg_image": "",
    "gemini_api_key": "",
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
            for k, v in DEFAULT_CONFIG.items():
                cfg.setdefault(k, v)
            return cfg
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)

def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

CFG = load_config()

# ── Themes ─────────────────────────────────────────────────────────────────────
BUILTIN_THEMES = {
    "green":  {"bg":"#0d0d0d","fg":"#00ff88","dim":"#005533","err":"#ff4444","info":"#44aaff","bar":"#111111","graph":"#00ff88"},
    "amber":  {"bg":"#0d0900","fg":"#ffb000","dim":"#554400","err":"#ff4444","info":"#ffdd88","bar":"#1a1200","graph":"#ffb000"},
    "blue":   {"bg":"#00050d","fg":"#00aaff","dim":"#003355","err":"#ff4444","info":"#88ddff","bar":"#001122","graph":"#00aaff"},
    "white":  {"bg":"#0d0d0d","fg":"#ffffff","dim":"#555555","err":"#ff4444","info":"#aaaaff","bar":"#1a1a1a","graph":"#ffffff"},
    "matrix": {"bg":"#000000","fg":"#00ff00","dim":"#004400","err":"#ff0000","info":"#00ff88","bar":"#001100","graph":"#00ff00"},
    "red":    {"bg":"#0d0000","fg":"#ff4455","dim":"#550011","err":"#ff8800","info":"#ffaaaa","bar":"#1a0000","graph":"#ff4455"},
    "cyan":   {"bg":"#000d0d","fg":"#00ffee","dim":"#004444","err":"#ff4444","info":"#88ffee","bar":"#001111","graph":"#00ffee"},
    "purple": {"bg":"#05000d","fg":"#cc88ff","dim":"#330055","err":"#ff4444","info":"#ff88dd","bar":"#0d0022","graph":"#cc88ff"},
}

def get_themes():
    t = dict(BUILTIN_THEMES)
    t.update(CFG.get("custom_themes", {}))
    return t

THEMES = get_themes()
THEME_NAMES = list(THEMES.keys())

FONT  = ("Courier New", CFG.get("font_size", 13))
FONTS = ("Courier New", 10, "bold")

ASCII_LOGO = [
    "  █████╗ ██████╗  ██████╗██╗  ██╗",
    " ██╔══██╗██╔══██╗██╔════╝██║  ██║",
    " ███████║██████╔╝██║     ███████║",
    " ██╔══██║██╔══██╗██║     ██╔══██║",
    " ██║  ██║██║  ██║╚██████╗██║  ██║",
    " ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝",
]

BIG = {
    'A':["  /\\  "," /  \\ ","/----\\"," /  \\ "],
    'B':["|\\ ","| >","| >","|/ "],
    'C':["  /","  |","  |","  \\"],
    'D':["|\\ "," \\ "," / ","|/ "],
    'E':["|===","|== ","|   ","|==="],
    'F':["|===","|== ","|   ","|   "],
    'G':["  /","  | __","  |   |","  \\__/"],
    'H':["|  |","|__|","|  |","|  |"],
    'I':["=|=","  |  ","  |  ","=|="],
    'J':["   |","   |","   |","\\__/"],
    'K':["|  /","| / ","| \\ ","|  \\"],
    'L':["|   ","|   ","|   ","|___"],
    'M':["|\\  /|","| \\/ |","|    |","|    |"],
    'N':["|\\  |","| \\ |","|  \\|","|   |"],
    'O':["  /\\  ","/    \\","\\    /","  \\/  "],
    'P':["|\\","| >","| /","|  "],
    'Q':["  /\\  ","/    \\","\\  \\ /","  \\/\\ "],
    'R':["|\\","| >","| \\","|  \\"],
    'S':["  ___"," /   "," \\__ ","    \\"],
    'T':["=====","  |  ","  |  ","  |  "],
    'U':["|   |","|   |","|   |","\\___/"],
    'V':["|   |","|   |"," \\ / ","  V  "],
    'W':["|   |","|   |","| | |","\\/ \\/"],
    'X':["\\ /","  X  "," / \\","     "],
    'Y':["\\ /","  Y  ","  |  ","  |  "],
    'Z':["====","   /","  / ","===="],
    ' ':["    ","    ","    ","    "],
}

def make_banner(text):
    rows = ["","","",""]
    for ch in text.upper():
        pat = BIG.get(ch, BIG[' '])
        for i in range(4):
            rows[i] += (pat[i] if i < len(pat) else "    ") + " "
    return rows

def fuzzy_match(query, candidates):
    q = query.lower()
    results = []
    for c in candidates:
        cl = c.lower()
        if cl.startswith(q):
            results.insert(0, c); continue
        idx = 0
        for ch in q:
            idx = cl.find(ch, idx)
            if idx == -1: break
            idx += 1
        else:
            results.append(c)
    return results

# ── Vault encryption ───────────────────────────────────────────────────────────
def _vault_key(password_hash):
    return (password_hash[:32]).encode().ljust(32, b"0")

def vault_encrypt(plaintext, password_hash):
    key  = _vault_key(password_hash)
    data = plaintext.encode()
    enc  = bytes([b ^ key[i % 32] for i, b in enumerate(data)])
    return base64.b64encode(enc).decode()

def vault_decrypt(ciphertext, password_hash):
    key  = _vault_key(password_hash)
    data = base64.b64decode(ciphertext.encode())
    dec  = bytes([b ^ key[i % 32] for i, b in enumerate(data)])
    return dec.decode()

# ── Clipboard history ──────────────────────────────────────────────────────────
CLIP_HISTORY   = []
MAX_CLIP       = 15
_last_clip_val = None

def _poll_clipboard(root):
    global _last_clip_val
    try:
        val = root.clipboard_get()
        if val and val != _last_clip_val:
            _last_clip_val = val
            if val not in CLIP_HISTORY:
                CLIP_HISTORY.append(val)
            if len(CLIP_HISTORY) > MAX_CLIP:
                CLIP_HISTORY.pop(0)
    except Exception:
        pass
    root.after(1500, lambda: _poll_clipboard(root))

# ── App scanner ────────────────────────────────────────────────────────────────
def find_apps():
    apps = {}
    known = {
        "chrome":  [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"],
        "firefox": [r"C:\Program Files\Mozilla Firefox\firefox.exe"],
        "vscode":  [os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
        "spotify": [os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe")],
        "discord": [os.path.expandvars(r"%LOCALAPPDATA%\Discord\app-*\Discord.exe")],
        "steam":   [r"C:\Program Files (x86)\Steam\steam.exe", r"C:\Program Files\Steam\steam.exe"],
        "obs":     [r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"],
        "vlc":     [r"C:\Program Files\VideoLAN\VLC\vlc.exe"],
        "slack":   [os.path.expandvars(r"%LOCALAPPDATA%\slack\slack.exe")],
        "zoom":    [os.path.expandvars(r"%APPDATA%\Zoom\bin\Zoom.exe")],
        "figma":   [os.path.expandvars(r"%LOCALAPPDATA%\Figma\Figma.exe")],
        "cursor":  [os.path.expandvars(r"%LOCALAPPDATA%\Programs\cursor\Cursor.exe")],
        "git":     [r"C:\Program Files\Git\git-bash.exe"],
        "blender": [r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"],
        "postman": [os.path.expandvars(r"%LOCALAPPDATA%\Postman\Postman.exe")],
    }
    builtin = {
        "notepad":"notepad.exe","explorer":"explorer.exe","cmd":"cmd.exe",
        "terminal":"wt.exe","calc":"calc.exe","taskmanager":"taskmgr.exe",
        "task":"taskmgr.exe","paint":"mspaint.exe","snip":"snippingtool.exe",
        "docs":os.path.expandvars(r"%USERPROFILE%\Documents"),
        "downloads":os.path.expandvars(r"%USERPROFILE%\Downloads"),
        "desktop":os.path.expandvars(r"%USERPROFILE%\Desktop"),
    }
    apps.update(builtin)
    for name, paths in known.items():
        for path in paths:
            matches = glob.glob(os.path.expandvars(path))
            if matches: apps[name] = matches[0]; break
            elif os.path.exists(os.path.expandvars(path)): apps[name] = path; break
    for sm in [r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
               os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")]:
        if os.path.exists(sm):
            for lnk in glob.glob(os.path.join(sm,"**","*.lnk"), recursive=True):
                name = os.path.splitext(os.path.basename(lnk))[0].lower().replace(" ","").replace("-","")[:14]
                if name and name not in apps: apps[name] = lnk
    return apps

RECENT     = []
MAX_RECENT = 10

# ══════════════════════════════════════════════════════════════════════════════
class Launcher:
    _ai_session = []

    def __init__(self):
        self.root = tk.Tk.__new__(tk.Tk)
        tk.Tk.__init__(self.root)
        self.root.title("ARCH")
        self.root.attributes("-fullscreen", True)
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        self.root.bind("<Escape>", lambda e: self._try_close())
        self.root.bind("<Button-1>", lambda e: self.entry.focus_force())

        self.history, self.hidx = [], -1
        self.matrix_running  = False
        self.dash_running    = False
        self.locked          = bool(CFG.get("lock_hash"))
        self.stars           = []
        self.cpu_history     = [0]*60
        self.ram_history     = [0]*60
        self._graph_after    = None
        self._last_activity  = time.time()
        self._screensaver_on = False
        self._sticky_win     = None
        self._pomodoro_running = False
        self._stopwatch_start  = None
        self._stopwatch_laps   = []
        self._macro_recording  = False
        self._macro_buffer     = []
        self._macros           = {}
        self._cron_jobs        = []

        self.t = CFG["theme"] if CFG["theme"] in get_themes() else "green"
        self._apply_theme(self.t)
        self._build_ui()
        self._apply_font_size(CFG.get("font_size", 13))
        self._apply_opacity(CFG.get("opacity", 100))
        if CFG.get("topmost", False):
            self.root.attributes("-topmost", True)

        if self.locked:
            self._lock_screen()
        else:
            self._boot()

        self._start_hotkey_listener()
        _poll_clipboard(self.root)
        self._inactivity_watch()
        self._start_cron()
        self.root.mainloop()

    # ── Theme ──────────────────────────────────────────────────────────────────
    def _apply_theme(self, name):
        self.t = name
        themes = get_themes()
        th = themes.get(name, BUILTIN_THEMES["green"])
        self.BG   = th["bg"];   self.FG   = th["fg"]
        self.DIM  = th["dim"];  self.ERR  = th["err"]
        self.INFO = th["info"]; self.BAR  = th["bar"]
        self.GRAPH= th["graph"]

    # ── UI ─────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.root.configure(bg=self.BG)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.star_canvas = tk.Canvas(self.root, bg=self.BG, highlightthickness=0)
        self.star_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.after(200, self._init_stars)

        self.bar = tk.Frame(self.root, bg=self.BAR, height=32)
        self.bar.grid(row=0, column=0, sticky="ew")
        self.bar.grid_columnconfigure(1, weight=1)
        tk.Label(self.bar, text="  ◈ ARCH  v4.52", bg=self.BAR, fg=self.FG,
                 font=FONTS).grid(row=0, column=0, sticky="w", padx=4)
        self.clock_lbl = tk.Label(self.bar, text="", bg=self.BAR, fg=self.DIM,
                                   font=("Courier New", 10))
        self.clock_lbl.grid(row=0, column=1, sticky="e", padx=12)
        self.mood_lbl = tk.Label(self.bar, text="", bg=self.BAR, fg=self.INFO,
                                  font=("Courier New", 11))
        self.mood_lbl.grid(row=0, column=2, sticky="e", padx=4)
        self.stat_lbl = tk.Label(self.bar, text="", bg=self.BAR, fg=self.DIM,
                                  font=("Courier New", 10))
        self.stat_lbl.grid(row=0, column=3, sticky="e", padx=8)
        tk.Label(self.bar, text="[ESC]  ", bg=self.BAR, fg=self.DIM,
                 font=("Courier New", 10)).grid(row=0, column=4, sticky="e", padx=4)

        self.out = tk.Text(self.root, bg=self.BG, fg=self.FG, font=FONT,
                           insertbackground=self.FG, relief="flat",
                           padx=16, pady=10, state="disabled", cursor="arrow")
        self.out.grid(row=1, column=0, sticky="nsew")
        self.out.configure(bg=self.BG)
        self._retag()

        irow = tk.Frame(self.root, bg=self.BG)
        irow.grid(row=2, column=0, sticky="ew", padx=16, pady=10)
        self.prompt_lbl = tk.Label(irow, text=CFG.get("prompt_text","arch~$ "),
                                    bg=self.BG, fg=self.FG, font=FONT)
        self.prompt_lbl.pack(side="left")
        self.entry = tk.Entry(irow, bg=self.BG, fg=self.FG, font=FONT,
                              insertbackground=self.FG, relief="flat", width=60)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self._submit)
        self.entry.bind("<Up>",     self._hist_up)
        self.entry.bind("<Down>",   self._hist_dn)
        self.entry.bind("<Tab>",    self._autocomplete)
        self.cur = tk.Label(irow, text="█", bg=self.BG, fg=self.FG, font=FONT)
        self.cur.pack(side="left")
        if CFG.get("mood"):
            self.mood_lbl.config(text=CFG["mood"]+"  ")

    def _retag(self):
        self.out.tag_config("dim",  foreground=self.DIM)
        self.out.tag_config("err",  foreground=self.ERR)
        self.out.tag_config("info", foreground=self.INFO)
        self.out.tag_config("bold", foreground=self.FG, font=("Courier New", CFG.get("font_size",13), "bold"))
        self.out.tag_config("prmt", foreground=self.DIM)
        self.out.tag_config("logo", foreground=self.FG, font=("Courier New", 11, "bold"))
        self.out.tag_config("good", foreground="#00ff88")
        self.out.tag_config("ai",   foreground=self.INFO, font=("Courier New", CFG.get("font_size",13), "italic"))

    def _w(self, text, tag=None):
        self.out.config(state="normal")
        if tag: self.out.insert("end", text, tag)
        else:   self.out.insert("end", text)
        self.out.see("end")
        self.out.config(state="disabled")

    # ── Stars ──────────────────────────────────────────────────────────────────
    def _init_stars(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        self.stars = []
        for _ in range(80):
            x = random.randint(0, w); y = random.randint(0, h)
            size  = random.choice([1,1,1,2])
            speed = random.uniform(0.1, 0.4)
            self.stars.append([x, y, size, speed])
        self._animate_stars()

    def _animate_stars(self):
        c = self.star_canvas
        c.delete("star")
        w = self.root.winfo_width()
        for s in self.stars:
            x,y,sz,sp = s
            c.create_oval(x,y,x+sz,y+sz, fill=self.DIM, outline="", tags="star")
            s[0] -= sp
            if s[0] < 0: s[0] = w
        self.root.after(50, self._animate_stars)

    # ── Boot ───────────────────────────────────────────────────────────────────
    def _boot(self):
        self._animated_banner()
        motd = CFG.get("motd","")
        if motd:
            self._w(f"  {motd}\n\n","ai")
        self._show_splash_quote()
        self._w("  Scanning for apps", "dim")
        self.root.update()
        self.apps = find_apps()
        self._w(f" — found {len(self.apps)}\n\n", "info")
        self._show_favorites()
        self._w("  Type ", "dim"); self._w("help", "info"); self._w(" for all commands.\n\n", "dim")
        if not CFG.get("gemini_api_key"):
            self._w("  ⚠ AI features disabled (no API key). Use: ", "dim")
            self._w("apikey set <your-gemini-key>\n\n", "bold")
        self._blink()
        self._update_clock()
        self._update_bar_stats()
        self.entry.focus_force()
        self.root.bind("<Key>", self._reset_activity)

    def _animated_banner(self):
        for line in ASCII_LOGO:
            self._w(line + "\n", "logo")
            self.root.update()
            time.sleep(0.04)
        self._w("\n")

    def _show_splash_quote(self):
        quotes = CFG.get("splash_quotes", [])
        if quotes:
            quote = random.choice(quotes)
            self._w(f"  ✨ {quote}\n\n", "info")

    def _show_favorites(self):
        favs = CFG["favorites"]
        self._w("  Favorites: ", "dim")
        if favs:
            for f in favs: self._w(f"[{f}] ", "info")
        else:
            self._w("(none — use 'fav add <app>')", "dim")
        self._w("\n\n")

    # ── Clock & stats ──────────────────────────────────────────────────────────
    def _update_clock(self):
        now = datetime.datetime.now().strftime("%a %b %d  %H:%M:%S")
        self.clock_lbl.config(text=now)
        self.root.after(1000, self._update_clock)

    def _update_bar_stats(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.stat_lbl.config(text=f"CPU {cpu:4.1f}%  RAM {ram:4.1f}%  ")
            self.cpu_history.append(cpu);  self.cpu_history.pop(0)
            self.ram_history.append(ram);  self.ram_history.pop(0)
        except Exception:
            pass
        self.root.after(2000, self._update_bar_stats)

    # ── Lock screen ────────────────────────────────────────────────────────────
    def _lock_screen(self):
        self._block_keys()
        self.lock_frame = tk.Frame(self.root, bg=self.BG)
        self.lock_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.lock_frame.lift()
        self.root.attributes("-topmost", True)
        self._lock_focus_guard()
        inner = tk.Frame(self.lock_frame, bg=self.BG)
        inner.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(inner, text="🔒  ARCH is locked", bg=self.BG,
                 fg=self.FG, font=("Courier New", 22, "bold")).pack(pady=20)
        tk.Label(inner, text="Enter password:", bg=self.BG,
                 fg=self.DIM, font=FONT).pack()
        self.lock_entry = tk.Entry(inner, show="*", bg=self.BAR,
                                   fg=self.FG, font=("Courier New", 16),
                                   relief="flat", width=24,
                                   insertbackground=self.FG)
        self.lock_entry.pack(pady=10, ipady=6)
        self.lock_msg = tk.Label(inner, text="", bg=self.BG,
                                  fg=self.ERR, font=FONT)
        self.lock_msg.pack()
        tk.Label(inner, text="press Enter to unlock  |  use recovery key if forgotten", bg=self.BG,
                 fg=self.DIM, font=("Courier New", 10)).pack(pady=(8,0))
        self.lock_entry.bind("<Return>", self._check_password)
        self.lock_frame.bind("<Button-1>", lambda e: self.lock_entry.focus_force())
        self.lock_frame.bind("<Key>", lambda e: "break")
        self.root.bind("<Escape>",   lambda e: "break")
        self.root.bind("<Alt_L>",    lambda e: "break")
        self.root.bind("<Alt_R>",    lambda e: "break")
        self.root.bind("<Tab>",      lambda e: "break")
        self.root.after(100, self.lock_entry.focus_force)

    def _block_keys(self):
        try:
            import keyboard
            keyboard.block_key("windows"); keyboard.block_key("left windows"); keyboard.block_key("right windows")
            keyboard.add_hotkey("alt+tab", lambda: None, suppress=True)
            keyboard.add_hotkey("alt+f4",  lambda: None, suppress=True)
            self._keys_blocked = True
        except Exception:
            self._keys_blocked = False

    def _unblock_keys(self):
        try:
            import keyboard
            keyboard.unhook_all_hotkeys()
            if getattr(self, "_keys_blocked", False):
                keyboard.unblock_key("windows"); keyboard.unblock_key("left windows"); keyboard.unblock_key("right windows")
            self._keys_blocked = False
        except Exception:
            pass

    def _lock_focus_guard(self):
        if self.locked:
            self.root.lift(); self.root.focus_force()
            if hasattr(self, "lock_entry"): self.lock_entry.focus_force()
            self.root.after(300, self._lock_focus_guard)

    def _check_password(self, _=None):
        pw = self.lock_entry.get()
        h  = hashlib.sha256(pw.encode()).hexdigest()
        is_password = h == CFG.get("lock_hash","")
        is_recovery = h == CFG.get("recovery_hash","")
        if is_password or is_recovery:
            if is_recovery:
                CFG["lock_hash"] = ""; CFG["recovery_hash"] = ""; save_config(CFG)
            self._unblock_keys()
            self.root.attributes("-topmost", CFG.get("topmost", False))
            self.root.unbind("<Alt_L>"); self.root.unbind("<Alt_R>"); self.root.unbind("<Tab>")
            self.lock_frame.destroy()
            self.locked = False
            self.root.bind("<Escape>", lambda e: self._try_close())
            self._boot()
            if is_recovery:
                self._w("  Recovery key accepted. Lock cleared.\n","good")
                self._w("  Use 'lock set <password>' to set a new one.\n\n","dim")
        else:
            self.lock_msg.config(text="  Wrong password. (or use your recovery key)")
            self.lock_entry.delete(0,"end")

    def _try_close(self):
        self.root.destroy()

    # ── Input ──────────────────────────────────────────────────────────────────
    def _submit(self, _=None):
        cmd = self.entry.get().strip()
        self.entry.delete(0, "end")
        if not cmd: return
        self.history.append(cmd); self.hidx = -1
        self._reset_activity()
        if self._macro_recording and cmd != "macro stop":
            self._macro_buffer.append(cmd)
        self._w(f"\n{CFG.get('prompt_text','arch~$ ')}", "prmt"); self._w(f"{cmd}\n")
        self._run(cmd.lower(), cmd)

    # ══════════════════════════════════════════════════════════════════════════
    def _run(self, cmd, raw):

        # ── apikey ──
        if cmd.startswith("apikey"):
            parts = cmd.split(None,2)
            sub   = parts[1] if len(parts)>1 else "status"
            if sub == "set" and len(parts)==3:
                CFG["gemini_api_key"] = parts[2]; save_config(CFG)
                self._w("\n  Anthropic API key set.\n\n","good"); return
            elif sub == "clear":
                CFG["gemini_api_key"] = ""; save_config(CFG)
                self._w("\n  API key cleared.\n\n","dim"); return
            else:
                has_key = bool(CFG.get("gemini_api_key"))
                self._w("\n  Anthropic API key: ","dim")
                self._w(("SET" if has_key else "NOT SET")+"\n\n","info" if has_key else "err")
            return

        # ── chain (&&) ──
        if " && " in raw:
            for part in raw.split(" && "):
                part = part.strip()
                if part: self._run(part.lower(), part)
            return

        # ── search ──
        if cmd.startswith("search "):
            q = urllib.parse.quote_plus(raw[7:].strip())
            url = f"https://www.google.com/search?q={q}"
            self._w(f"\n  Searching: ","dim"); self._w(raw[7:]+"\n\n","info")
            subprocess.Popen(f'start "" "{url}"', shell=True); return

        # ── open ──
        if cmd.startswith("open "):
            url = raw[5:].strip()
            self._w(f"\n  Opening ","dim"); self._w(url+"\n\n","info")
            subprocess.Popen(f'start "" "{url}"', shell=True); return

        # ── calc ──
        if cmd.startswith("calc "):
            expr = raw[5:].strip()
            try:
                result = eval(expr, {"__builtins__":{}}, {k: getattr(math,k) for k in dir(math)})
                self._w(f"\n  {expr} = ","dim"); self._w(f"{result}\n\n","bold")
            except Exception as e:
                self._w(f"\n  Calc error: {e}\n\n","err")
            return

        # ── unit converter ──
        if cmd.startswith("unit "):
            self._unit_convert(raw[5:].strip()); return

        # ── ip ──
        if cmd == "ip":
            def fetch():
                try:
                    ip = urllib.request.urlopen("https://api.ipify.org", timeout=4).read().decode()
                    self.root.after(0, lambda: self._w(f"\n  Public IP: ","dim"))
                    self.root.after(0, lambda: self._w(ip+"\n\n","info"))
                except Exception:
                    self.root.after(0, lambda: self._w("\n  Could not fetch IP.\n\n","err"))
            self._w("\n  Fetching IP...\n","dim")
            threading.Thread(target=fetch, daemon=True).start(); return

        # ── weather ──
        if cmd.startswith("weather"):
            city = urllib.parse.quote_plus(raw[7:].strip() or "auto")
            def fetch():
                try:
                    url = f"https://wttr.in/{city}?format=3"
                    res = urllib.request.urlopen(url, timeout=5).read().decode()
                    self.root.after(0, lambda: self._w(f"\n  {res}\n\n","info"))
                except Exception:
                    self.root.after(0, lambda: self._w("\n  Could not fetch weather.\n\n","err"))
            self._w("\n  Fetching weather...\n","dim")
            threading.Thread(target=fetch, daemon=True).start(); return

        # ── theme ──
        if cmd.startswith("theme"):
            parts = cmd.split(None, 2)
            sub   = parts[1] if len(parts)>1 else ""
            if sub == "create" and len(parts)==3:
                args = parts[2].split()
                if len(args) < 8:
                    self._w("\n  Usage: theme create <name> <bg> <fg> <dim> <err> <info> <bar> <graph>\n\n","err"); return
                name2 = args[0]
                keys  = ["bg","fg","dim","err","info","bar","graph"]
                new_theme = dict(zip(keys, args[1:8]))
                CFG["custom_themes"][name2] = new_theme; save_config(CFG)
                self._w(f"\n  Custom theme '{name2}' saved.\n\n","good"); return
            arg = sub
            if arg == "random": arg = random.choice(list(get_themes().keys()))
            themes = get_themes()
            if arg in themes:
                self._apply_theme(arg)
                self.root.configure(bg=self.BG)
                self.out.configure(bg=self.BG, fg=self.FG)
                self.entry.configure(bg=self.BG, fg=self.FG, insertbackground=self.FG)
                self.bar.configure(bg=self.BAR)
                for w in self.bar.winfo_children():
                    try: w.configure(bg=self.BAR)
                    except Exception: pass
                self._retag(); CFG["theme"] = arg; save_config(CFG)
                self._w(f"\n  Theme → ","dim"); self._w(arg+"\n\n","info")
            else:
                self._w(f"\n  Themes: ","dim"); self._w(" ".join(get_themes().keys())+"\n\n","info")
                self._w("  theme create <name> <bg> <fg> <dim> <err> <info> <bar> <graph>\n\n","dim")
            return

        # ── sys ──
        if cmd == "sys":
            cpu  = psutil.cpu_percent(interval=0.5)
            ram  = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            net  = psutil.net_io_counters()
            bat  = None
            try:
                b = psutil.sensors_battery()
                if b: bat = f"{b.percent:.0f}% {'🔌' if b.power_plugged else '🔋'}"
            except Exception: pass
            self._w("\n  ─── System Info ───────────────────\n","bold")
            self._w(f"  CPU:   {cpu}%\n","info")
            self._w(f"  RAM:   {ram.percent}% used  ({ram.used//1024**2} MB / {ram.total//1024**3} GB)\n","info")
            self._w(f"  Disk:  {disk.percent}% used  ({disk.used//1024**3} GB / {disk.total//1024**3} GB)\n","info")
            self._w(f"  Net:   ↑ {net.bytes_sent//1024**2} MB  ↓ {net.bytes_recv//1024**2} MB\n","info")
            if bat: self._w(f"  Bat:   {bat}\n","info")
            self._w("\n"); return

        # ── battery ──
        if cmd == "battery":
            try:
                b = psutil.sensors_battery()
                if b:
                    status = "Charging" if b.power_plugged else "Discharging"
                    secs   = b.secsleft
                    tleft  = f"{secs//3600}h {(secs%3600)//60}m" if secs != psutil.POWER_TIME_UNLIMITED and secs > 0 else "—"
                    self._w(f"\n  Battery: ","dim"); self._w(f"{b.percent:.0f}%  {status}  ({tleft} remaining)\n\n","info")
                else:
                    self._w("\n  No battery detected.\n\n","dim")
            except Exception as e:
                self._w(f"\n  Battery error: {e}\n\n","err")
            return

        # ── lock ──
        if cmd.startswith("lock"):
            parts = cmd.split(None, 1)
            sub   = parts[1] if len(parts)>1 else ""
            if sub.startswith("set "):
                pwd = sub[4:].strip()
                h = hashlib.sha256(pwd.encode()).hexdigest()
                CFG["lock_hash"] = h; save_config(CFG)
                self._w("\n  Lock enabled with password.\n\n","good"); return
            elif sub == "now":
                if CFG.get("lock_hash"):
                    self._w("\n  Locking screen...\n\n","info")
                    self.root.after(500, self._lock_screen)
                else:
                    self._w("\n  Lock not set. Use: lock set <password>\n\n","err")
            elif sub == "clear":
                CFG["lock_hash"] = ""; save_config(CFG)
                self._w("\n  Lock disabled.\n\n","good"); return
            else:
                self._w("\n  Usage: lock set <pwd> | lock now | lock clear\n\n","dim")
            return

        # ── font ──
        if cmd.startswith("font "):
            try:
                size = int(raw[5:].strip())
                CFG["font_size"] = max(8, min(32, size)); save_config(CFG)
                self._apply_font_size(size)
                self._w(f"\n  Font size → {size}\n\n","good"); return
            except: self._w("\n  Usage: font <size>\n\n","err"); return

        # ── opacity ──
        if cmd.startswith("opacity "):
            try:
                val = int(raw[8:].strip())
                CFG["opacity"] = max(20, min(100, val)); save_config(CFG)
                self._apply_opacity(val)
                self._w(f"\n  Opacity → {val}%\n\n","good"); return
            except: self._w("\n  Usage: opacity <0-100>\n\n","err"); return

        # ── topmost ──
        if cmd == "topmost":
            current = CFG.get("topmost", False)
            CFG["topmost"] = not current; save_config(CFG)
            self.root.attributes("-topmost", not current)
            self._w(f"\n  Topmost → {'ON' if not current else 'OFF'}\n\n","good"); return

        # ── prompt ──
        if cmd.startswith("prompt "):
            text = raw[7:].strip()
            CFG["prompt_text"] = text; save_config(CFG)
            self._w(f"\n  Prompt → {text}\n\n","good"); return

        # ── mood ──
        if cmd.startswith("mood "):
            mood = raw[5:].strip()
            CFG["mood"] = mood; save_config(CFG)
            self._w(f"\n  Mood → {mood}\n\n","good"); return

        # ── motd ──
        if cmd.startswith("motd"):
            parts = cmd.split(None, 1)
            text = parts[1] if len(parts)>1 else ""
            CFG["motd"] = text; save_config(CFG)
            self._w(f"\n  MOTD → {text or '(cleared)'}\n\n","good"); return

        # ── cursor ──
        if cmd.startswith("cursor "):
            style = raw[7:].strip().lower()
            valid = ["block","ibeam"]
            if style in valid:
                self._w(f"\n  Cursor → {style}\n\n","good"); return
            else: self._w(f"\n  Valid: {','.join(valid)}\n\n","err"); return

        # ── find ──
        if cmd.startswith("find "):
            path = raw[5:].strip()
            self._w(f"\n  Searching: {path}\n","dim")
            try:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        self._w(f"  {os.path.join(root,f)}\n","info")
            except: self._w("  (not found)\n","err")
            self._w("\n"); return

        # ── ls ──
        if cmd.startswith("ls"):
            path = (raw[2:].strip() or ".").replace("~", os.path.expanduser("~"))
            self._w(f"\n  Contents of {path}\n","dim")
            try:
                for item in os.listdir(path):
                    full = os.path.join(path, item)
                    self._w(f"  {'[D]' if os.path.isdir(full) else '[F]'} {item}\n","info")
            except: self._w("  (access denied)\n","err")
            self._w("\n"); return

        # ── tree ──
        if cmd.startswith("tree"):
            path = (raw[4:].strip() or ".").replace("~", os.path.expanduser("~"))
            self._w(f"\n  Tree: {path}\n","dim")
            try:
                for root, dirs, files in os.walk(path):
                    level = root.replace(path,"").count(os.sep)
                    indent = "  " * level
                    self._w(f"{indent}📁 {os.path.basename(root)}\n","info")
                    sub = "    " * (level+1)
                    for f in files[:5]: self._w(f"{sub}📄 {f}\n","dim")
                    if len(files)>5: self._w(f"{sub}... +{len(files)-5} more\n","dim")
            except: self._w("  (access denied)\n","err")
            self._w("\n"); return

        # ── cd ──
        if cmd.startswith("cd "):
            path = raw[3:].strip().replace("~", os.path.expanduser("~"))
            try:
                os.chdir(path)
                self._w(f"\n  → {os.getcwd()}\n\n","good"); return
            except: self._w(f"\n  Path not found: {path}\n\n","err"); return

        # ── run ──
        if cmd.startswith("run "):
            script = raw[4:].strip()
            try:
                subprocess.Popen(script, shell=True)
                self._w(f"\n  Running: {script}\n\n","good"); return
            except Exception as e: self._w(f"\n  Error: {e}\n\n","err"); return

        # ── recent ──
        if cmd == "recent":
            self._w("\n  Recent apps:\n","dim")
            for app in RECENT[-10:]:
                self._w(f"  • {app}\n","info")
            self._w("\n"); return

        # ── fav ──
        if cmd.startswith("fav "):
            parts = cmd.split(None, 2)
            sub = parts[1] if len(parts)>1 else "list"
            app = parts[2] if len(parts)>2 else ""
            if sub == "add" and app:
                if app not in CFG["favorites"]: CFG["favorites"].append(app)
                save_config(CFG)
                self._w(f"\n  Added to favorites: {app}\n\n","good"); return
            elif sub == "rm" and app:
                if app in CFG["favorites"]: CFG["favorites"].remove(app)
                save_config(CFG)
                self._w(f"\n  Removed from favorites: {app}\n\n","good"); return
            elif sub == "list":
                self._w(f"\n  Favorites: {', '.join(CFG['favorites']) or '(none)'}\n\n","info"); return
            else: self._w("\n  Usage: fav add/rm/list <app>\n\n","err"); return

        # ── ps ──
        if cmd == "ps":
            self._w("\n  Processes:\n","dim")
            for p in psutil.process_iter(['pid','name','memory_percent']):
                try: self._w(f"  {p.pid:6d} {p.name():30s} {p.memory_percent():.1f}%\n","info")
                except: pass
            self._w("\n"); return

        # ── kill ──
        if cmd.startswith("kill "):
            name = raw[5:].strip().lower()
            killed = 0
            for p in psutil.process_iter(['pid','name']):
                try:
                    if name.lower() in p.name().lower(): p.kill(); killed += 1
                except: pass
            self._w(f"\n  Killed {killed} process(es)\n\n","good" if killed else "dim"); return

        # ── graph ──
        if cmd == "graph": self._show_graph(); return

        # ── dash ──
        if cmd == "dash": self._show_dash(); return

        # ── size ──
        if cmd.startswith("size "):
            path = raw[5:].strip()
            try:
                if os.path.isfile(path): size = os.path.getsize(path)
                else: size = sum(os.path.getsize(os.path.join(d,f)) for d,_,fs in os.walk(path) for f in fs)
                self._w(f"\n  Size: {size/(1024**2):.2f} MB\n\n","info"); return
            except: self._w("\n  Error reading path\n\n","err"); return

        # ── dupes ──
        if cmd.startswith("dupes "):
            path = raw[6:].strip()
            seen = {}; dupes = []
            try:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        full = os.path.join(root, f)
                        h = hashlib.md5(open(full,'rb').read()).hexdigest()
                        if h in seen: dupes.append((f, seen[h]))
                        else: seen[h] = full
                self._w(f"\n  Found {len(dupes)} duplicate(s):\n","dim")
                for f, orig in dupes: self._w(f"  {f} ↔ {orig}\n","info")
                self._w("\n"); return
            except: self._w("\n  Error\n\n","err"); return

        # ── diff ──
        if cmd.startswith("diff "):
            parts = raw[5:].split()
            if len(parts)<2: self._w("\n  Usage: diff <file1> <file2>\n\n","err"); return
            try:
                with open(parts[0]) as f1, open(parts[1]) as f2:
                    diff = list(difflib.unified_diff(f1.readlines(), f2.readlines()))
                self._w(f"\n  Differences:\n","dim")
                for line in diff[:20]: self._w(f"  {line.rstrip()}\n","info" if line.startswith("+") else "err" if line.startswith("-") else "dim")
                self._w("\n"); return
            except: self._w("\n  Error\n\n","err"); return

        # ── zip ──
        if cmd.startswith("zip "):
            path = raw[4:].strip()
            try:
                with zipfile.ZipFile(path+".zip", 'w') as z:
                    for root, dirs, files in os.walk(path):
                        for f in files: z.write(os.path.join(root,f))
                self._w(f"\n  Zipped → {path}.zip\n\n","good"); return
            except: self._w("\n  Error\n\n","err"); return

        # ── unzip ──
        if cmd.startswith("unzip "):
            path = raw[6:].strip()
            try:
                with zipfile.ZipFile(path, 'r') as z: z.extractall()
                self._w(f"\n  Extracted\n\n","good"); return
            except: self._w("\n  Error\n\n","err"); return

        # ── preview ──
        if cmd.startswith("preview "):
            path = raw[8:].strip()
            try:
                with open(path) as f:
                    lines = f.readlines()[:10]
                    for line in lines: self._w(f"  {line.rstrip()}\n","info")
                self._w("\n"); return
            except: self._w("\n  Cannot preview\n\n","err"); return

        # ── ping ──
        if cmd.startswith("ping "):
            host = raw[5:].strip()
            def do_ping():
                try:
                    result = os.popen(f"ping -n 4 {host}").read()
                    self.root.after(0, lambda: self._w(f"\n{result}\n","info"))
                except: self.root.after(0, lambda: self._w("\n  Ping failed\n\n","err"))
            self._w("\n  Pinging...\n","dim")
            threading.Thread(target=do_ping, daemon=True).start(); return

        # ── dns ──
        if cmd.startswith("dns "):
            host = raw[4:].strip()
            def resolve():
                try:
                    ip = socket.gethostbyname(host)
                    self.root.after(0, lambda: self._w(f"\n  {host} → {ip}\n\n","info"))
                except: self.root.after(0, lambda: self._w("\n  Resolution failed\n\n","err"))
            threading.Thread(target=resolve, daemon=True).start(); return

        # ── whois ──
        if cmd.startswith("whois "):
            domain = raw[6:].strip()
            def lookup():
                try:
                    result = os.popen(f"whois {domain}").read()
                    self.root.after(0, lambda: self._w(f"\n{result[:500]}\n\n","info"))
                except: self.root.after(0, lambda: self._w("\n  Lookup failed\n\n","err"))
            threading.Thread(target=lookup, daemon=True).start(); return

        # ── tracert ──
        if cmd.startswith("tracert "):
            host = raw[8:].strip()
            def trace():
                try:
                    result = os.popen(f"tracert {host}").read()
                    self.root.after(0, lambda: self._w(f"\n{result}\n","info"))
                except: self.root.after(0, lambda: self._w("\n  Trace failed\n\n","err"))
            threading.Thread(target=trace, daemon=True).start(); return

        # ── ports ──
        if cmd.startswith("ports "):
            host = raw[6:].strip()
            self._w("\n  Checking ports...\n\n","dim")
            for port in [80, 443, 22, 3306, 5432, 8080]:
                try:
                    s = socket.socket(); s.settimeout(1)
                    s.connect((host, port))
                    self._w(f"  {port}: OPEN\n","info")
                    s.close()
                except: self._w(f"  {port}: closed\n","dim")
            self._w("\n"); return

        # ── speedtest ──
        if cmd == "speedtest":
            self._w("\n  Running speedtest (this may take a moment)...\n\n","dim")
            def test():
                try:
                    result = os.popen("speedtest-cli").read() if os.system("speedtest-cli --help > nul 2>&1")==0 else "speedtest-cli not installed"
                    self.root.after(0, lambda: self._w(f"\n{result}\n","info"))
                except: self.root.after(0, lambda: self._w("\n  Speedtest error\n\n","err"))
            threading.Thread(target=test, daemon=True).start(); return

        # ── headers ──
        if cmd.startswith("headers "):
            url = raw[8:].strip()
            def get_headers():
                try:
                    req = urllib.request.Request(url, method="HEAD")
                    with urllib.request.urlopen(req, timeout=5) as r:
                        for k, v in r.headers.items(): self.root.after(0, lambda: self._w(f"  {k}: {v}\n","info"))
                except: self.root.after(0, lambda: self._w("\n  Error\n\n","err"))
            threading.Thread(target=get_headers, daemon=True).start(); return

        # ── ask ──
        if cmd.startswith("ask "):
            question = raw[4:].strip()
            self._ask_ai(question); return

        # ── explain ──
        if cmd.startswith("explain "):
            app = raw[8:].strip()
            q = f"Briefly explain what {app} does in one sentence."
            self._ask_ai(q); return

        # ── suggest ──
        if cmd == "suggest":
            q = "Suggest a useful command I could run next."
            self._ask_ai(q); return

        # ── summarize ──
        if cmd.startswith("summarize "):
            url = raw[10:].strip()
            self._w("\n  Fetching...\n","dim")
            def fetch_sum():
                try:
                    text = urllib.request.urlopen(url, timeout=5).read().decode()
                    q = f"Summarize this text: {text[:500]}"
                    self._ask_ai(q)
                except: self.root.after(0, lambda: self._w("\n  Error fetching\n\n","err"))
            threading.Thread(target=fetch_sum, daemon=True).start(); return

        # ── tldr ──
        if cmd.startswith("tldr "):
            text = raw[5:].strip()
            q = f"Give a very brief summary (1-2 sentences) of: {text}"
            self._ask_ai(q); return

        # ── define ──
        if cmd.startswith("define "):
            word = raw[7:].strip()
            q = f"Define {word} in one sentence."
            self._ask_ai(q); return

        # ── translate ──
        if cmd.startswith("translate "):
            parts = raw[10:].split(None, 1)
            if len(parts)<2: self._w("\n  Usage: translate <lang> <text>\n\n","err"); return
            lang, text = parts
            q = f"Translate to {lang}: {text}"
            self._ask_ai(q); return

        # ── fortune ──
        if cmd == "fortune":
            q = "Tell me a random interesting fact."
            self._ask_ai(q); return

        # ── aiclear ──
        if cmd == "aiclear":
            self._ai_session = []
            self._w("\n  AI history cleared.\n\n","good"); return

        # ── timer ──
        if cmd.startswith("timer "):
            args = raw[6:].split()
            if not args: self._w("\n  Usage: timer <5s|10m|1h> [label]\n\n","err"); return
            time_str = args[0]
            label = " ".join(args[1:]) or "Timer"
            try:
                val = int(time_str[:-1])
                unit = time_str[-1]
                secs = val*{"s":1,"m":60,"h":3600}[unit]
                self._w(f"\n  ⏱ {label}: {time_str}\n","good")
                def done():
                    self.root.after(0, lambda: self._w(f"\n  ⏰ {label} done!\n\n","info"))
                self.root.after(int(secs*1000), done)
            except: self._w("\n  Invalid format\n\n","err")
            return

        # ── remind ──
        if cmd.startswith("remind "):
            args = raw[7:].split(None, 1)
            if len(args)<2: self._w("\n  Usage: remind <5s|10m|1h> <message>\n\n","err"); return
            time_str, msg = args
            try:
                val = int(time_str[:-1])
                unit = time_str[-1]
                secs = val*{"s":1,"m":60,"h":3600}[unit]
                def remind_msg():
                    self.root.after(0, lambda: self._w(f"\n  🔔 {msg}\n\n","info"))
                self.root.after(int(secs*1000), remind_msg)
                self._w(f"\n  Reminder set for {time_str}\n\n","good")
            except: self._w("\n  Invalid format\n\n","err")
            return

        # ── pomodoro ──
        if cmd == "pomodoro":
            self._pomodoro_running = True
            self._w("\n  🍅 Pomodoro (25m work + 5m break) started\n\n","good")
            def work_timer():
                self.root.after(1500000, lambda: self._w("\n  ⏰ Work time done! Break time...\n\n","info"))
                def break_timer():
                    self.root.after(300000, lambda: self._w("\n  ⏰ Break done! Ready for another?\n\n","info"))
                self.root.after(1500000, break_timer)
            work_timer(); return

        # ── stopwatch ──
        if cmd.startswith("stopwatch"):
            args = cmd.split()
            sub = args[1] if len(args)>1 else "start"
            if sub == "start":
                self._stopwatch_start = time.time()
                self._stopwatch_laps = []
                self._w("\n  ⏱ Stopwatch started\n\n","good"); return
            elif sub == "stop":
                if self._stopwatch_start:
                    elapsed = time.time() - self._stopwatch_start
                    self._w(f"\n  ⏱ Elapsed: {int(elapsed//60)}m {int(elapsed%60)}s\n\n","info")
                    self._stopwatch_start = None
                else: self._w("\n  Stopwatch not running\n\n","err")
                return
            elif sub == "lap":
                if self._stopwatch_start:
                    elapsed = time.time() - self._stopwatch_start
                    self._stopwatch_laps.append(elapsed)
                    self._w(f"\n  📍 Lap {len(self._stopwatch_laps)}: {int(elapsed//60)}m {int(elapsed%60)}s\n\n","info")
                else: self._w("\n  Stopwatch not running\n\n","err")
                return

        # ── note ──
        if cmd.startswith("note"):
            parts = cmd.split(None, 1)
            sub = parts[1] if len(parts)>1 else "list"
            if sub.startswith("list"):
                self._w(f"\n  Notes ({len(CFG['notes'])}):\n","dim")
                for i, n in enumerate(CFG["notes"]): self._w(f"  {i}. {n}\n","info")
                self._w("\n"); return
            elif sub == "clear":
                CFG["notes"] = []; save_config(CFG)
                self._w("\n  Notes cleared.\n\n","good"); return
            elif sub.startswith("del "):
                try:
                    idx = int(sub[4:])
                    CFG["notes"].pop(idx)
                    save_config(CFG)
                    self._w("\n  Note deleted.\n\n","good")
                except: self._w("\n  Invalid index.\n\n","err")
                return
            else:
                CFG["notes"].append(sub)
                save_config(CFG)
                self._w(f"\n  Note saved: {sub}\n\n","good"); return

        # ── todo ──
        if cmd.startswith("todo"):
            parts = cmd.split(None, 2)
            sub = parts[1] if len(parts)>1 else "list"
            item = parts[2] if len(parts)>2 else ""
            if sub == "list":
                self._w(f"\n  TODO ({len(CFG['todos'])}):\n","dim")
                for i, t in enumerate(CFG["todos"]): self._w(f"  {i}. {'✓' if t.get('done') else '○'} {t['text']}\n","info")
                self._w("\n"); return
            elif sub == "add":
                CFG["todos"].append({"text":item,"done":False}); save_config(CFG)
                self._w(f"\n  TODO added: {item}\n\n","good"); return
            elif sub == "done":
                try:
                    idx = int(item)
                    CFG["todos"][idx]["done"] = True
                    save_config(CFG)
                    self._w("\n  TODO marked done.\n\n","good")
                except: self._w("\n  Invalid index.\n\n","err")
                return
            elif sub == "del":
                try:
                    idx = int(item)
                    CFG["todos"].pop(idx)
                    save_config(CFG)
                    self._w("\n  TODO deleted.\n\n","good")
                except: self._w("\n  Invalid index.\n\n","err")
                return
            elif sub == "clear":
                CFG["todos"] = []; save_config(CFG)
                self._w("\n  TODOs cleared.\n\n","good"); return

        # ── sticky ──
        if cmd == "sticky":
            win = tk.Toplevel(self.root); win.title("Sticky Note"); win.geometry("300x200"); win.configure(bg=self.BG)
            txt = tk.Text(win, bg=self.BG, fg=self.FG, font=FONT)
            txt.pack(fill="both", expand=True, padx=10, pady=10)
            self._w("\n  Sticky note opened.\n\n","good"); return

        # ── clip ──
        if cmd == "clip":
            try:
                text = self.root.clipboard_get()
                self._w(f"\n  Clipboard:\n  {text[:100]}...\n\n","info"); return
            except: self._w("\n  (clipboard empty)\n\n","dim"); return

        # ── banner ──
        if cmd.startswith("banner"):
            text = (raw[6:].strip() or "ARCH").upper()
            self._w(f"\n  ─── {text} ───\n\n","bold"); return

        # ── matrix ──
        if cmd == "matrix":
            self._matrix_rain(); return

        # ── glitch ──
        if cmd == "glitch":
            self._glitch_effect(); return

        # ── splash ──
        if cmd == "splash":
            self._w("\n  ✨ ✨ ✨\n","info")
            self._show_splash_quote(); return

        # ── cal ──
        if cmd == "cal":
            now = datetime.datetime.now()
            self._w(f"\n  {cal_mod.month_name[now.month]} {now.year}\n\n","info")
            self._w(f"  {'Mo Tu We Th Fr Sa Su'}\n","dim")
            for week in cal_mod.monthcalendar(now.year, now.month):
                line = ""
                for day in week:
                    if day == 0: line += "    "
                    elif day == now.day: line += f" {day:2d}*"
                    else: line += f" {day:2d} "
                self._w(f"  {line}\n","info")
            self._w("\n"); return

        # ── color ──
        if cmd.startswith("color "):
            hex_color = raw[6:].strip()
            try:
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
                self._w(f"\n  HEX: {hex_color}  RGB: {rgb}  HSV: ({int(h*360)}, {int(s*100)}, {int(v*100)})\n\n","info"); return
            except: self._w("\n  Invalid hex color\n\n","err"); return

        # ── qr ──
        if cmd.startswith("qr "):
            text = raw[3:].strip()
            self._w(f"\n  QR code for: {text}\n","dim")
            self._w("  (requires qrcode library)\n\n","dim"); return

        # ── hash ──
        if cmd.startswith("hash "):
            text = raw[5:].strip()
            md5 = hashlib.md5(text.encode()).hexdigest()
            sha = hashlib.sha256(text.encode()).hexdigest()
            self._w(f"\n  MD5:  {md5}\n","info")
            self._w(f"  SHA: {sha}\n\n","info"); return

        # ── vault ──
        if cmd.startswith("vault"):
            parts = cmd.split(None, 2)
            sub = parts[1] if len(parts)>1 else "list"
            key = parts[2] if len(parts)>2 else ""
            if sub == "list":
                self._w(f"\n  Vault keys: {', '.join(CFG['vault'].keys()) or '(empty)'}\n\n","info"); return
            elif sub == "add" and key and len(parts)>3:
                val = parts[3] if len(parts)>3 else ""
                CFG["vault"][key] = val; save_config(CFG)
                self._w(f"\n  Vault item added: {key}\n\n","good"); return
            elif sub == "get" and key:
                val = CFG["vault"].get(key, "(not found)")
                self._w(f"\n  {key}: {val}\n\n","info"); return
            elif sub == "del" and key:
                CFG["vault"].pop(key, None); save_config(CFG)
                self._w(f"\n  Vault item deleted: {key}\n\n","good"); return

        # ── macro ──
        if cmd.startswith("macro"):
            parts = cmd.split(None, 1)
            sub = parts[1] if len(parts)>1 else ""
            if sub == "record":
                self._macro_recording = True
                self._macro_buffer = []
                self._w("\n  🔴 Recording macro (type 'macro stop' to end)\n\n","good"); return
            elif sub == "stop":
                self._macro_recording = False
                if len(self._macro_buffer)>1:
                    self._macros[self._macro_buffer[0]] = self._macro_buffer[1:]
                self._w(f"\n  Macro saved with {len(self._macro_buffer)-1} commands\n\n","good"); return
            elif sub.startswith("play "):
                macro_name = sub[5:].strip()
                if macro_name in self._macros:
                    for cmd_line in self._macros[macro_name]: self._run(cmd_line.lower(), cmd_line)
                    self._w(f"\n  Macro executed: {macro_name}\n\n","good")
                else: self._w("\n  Macro not found\n\n","err")
                return

        # ── cron ──
        if cmd.startswith("cron"):
            parts = cmd.split(None, 1)
            sub = parts[1] if len(parts)>1 else "list"
            if sub == "list":
                self._w(f"\n  Cron jobs: {len(CFG['cron_jobs'])}\n","dim")
                for job in CFG["cron_jobs"]: self._w(f"  • {job}\n","info")
                self._w("\n"); return
            elif sub.startswith("add "):
                job = sub[4:].strip()
                CFG["cron_jobs"].append(job); save_config(CFG)
                self._w(f"\n  Cron job added\n\n","good"); return
            elif sub.startswith("del "):
                try:
                    idx = int(sub[4:])
                    CFG["cron_jobs"].pop(idx)
                    save_config(CFG)
                    self._w("\n  Cron job deleted\n\n","good")
                except: self._w("\n  Invalid index\n\n","err")
                return

        # ── help ──
        if cmd == "help apps":
            self._w("\nAll detected apps:\n\n","info")
            for i,n in enumerate(sorted(self.apps.keys())):
                self._w(f"  {n:<22}","bold")
                if (i+1)%3==0: self._w("\n")
            self._w("\n\n"); return

        if cmd == "help":
            self._w("\n  ─── ARCH v4.52 Commands ───────────────────────────────\n\n","bold")
            sections = [
                ("CONFIG", [
                    ("apikey set/clear/status",         "manage your Gemini AI key"),
                    ("theme <name> / random",           "switch colour theme"),
                    ("font <size>",                     "change font size e.g. font 15"),
                    ("opacity <0-100>",                 "window transparency"),
                    ("topmost",                         "toggle always-on-top"),
                    ("prompt <text>",                   "customise the prompt text"),
                    ("mood <text>",                     "set mood emoji shown in bar"),
                    ("motd [text]",                     "message shown on startup"),
                ]),
                ("APPS & LAUNCH", [
                    ("search <q>",                      "google search in browser"),
                    ("open <url>",                      "open a URL in browser"),
                    ("find <file>",                     "search for a file by name"),
                    ("ls [path]",                       "list directory contents"),
                    ("tree [path]",                     "show folder tree"),
                    ("cd <path>",                       "change working directory"),
                    ("recent",                          "recently launched apps"),
                    ("fav add/rm/list",                 "manage favourite apps"),
                ]),
                ("SYSTEM", [
                    ("sys",                             "CPU, RAM, disk, network stats"),
                    ("battery",                         "battery status and time left"),
                    ("ps",                              "top 12 running processes"),
                    ("kill <name>",                     "kill a process by name"),
                    ("ip",                              "show your public IP address"),
                    ("weather [city]",                  "current weather conditions"),
                    ("graph",                           "live CPU/RAM graph window"),
                    ("dash",                            "system dashboard overview"),
                ]),
                ("FILES", [
                    ("size <path>",                     "calculate folder/file size"),
                    ("dupes <path>",                    "find duplicate files"),
                    ("diff <f1> <f2>",                  "compare two files side by side"),
                    ("zip <file>",                      "zip a file or folder"),
                    ("unzip <file>",                    "extract a zip archive"),
                    ("preview <file>",                  "preview text file contents"),
                ]),
                ("NETWORK", [
                    ("ping <host>",                     "ping a host"),
                    ("dns <host>",                      "DNS lookup"),
                    ("whois <domain>",                  "domain registration info"),
                    ("tracert <host>",                  "trace network route"),
                    ("ports <host>",                    "scan open ports"),
                    ("speedtest",                       "test internet speed"),
                    ("headers <url>",                   "show HTTP response headers"),
                ]),
                ("AI", [
                    ("ask <question>",                  "ask the AI anything"),
                    ("explain <app>",                   "what does this app do?"),
                    ("suggest",                         "get app suggestions"),
                    ("summarize <url>",                 "summarize a web page"),
                    ("tldr <text>",                     "summarize a block of text"),
                    ("define <word>",                   "define a word"),
                    ("translate <lang> <text>",         "translate text to a language"),
                    ("fortune",                         "get a random fortune"),
                    ("aiclear",                         "clear AI conversation memory"),
                ]),
                ("TIMERS", [
                    ("timer <n>s|m|h [label]",          "set a countdown timer"),
                    ("remind <n>s|m|h <msg>",           "set a reminder message"),
                    ("pomodoro",                        "start a 25min focus timer"),
                    ("stopwatch start/stop/lap",        "stopwatch with lap times"),
                ]),
                ("NOTES", [
                    ("note <text>",                     "add a quick note"),
                    ("note list/del/clear",             "manage your notes"),
                    ("todo add/done/del/list",          "manage to-do list"),
                    ("sticky",                          "open sticky notes window"),
                    ("clip",                            "show clipboard history"),
                ]),
                ("VISUAL", [
                    ("theme <name>",                    "change theme"),
                    ("banner <text>",                   "display big ASCII banner"),
                    ("matrix",                          "matrix rain effect"),
                    ("glitch",                          "glitch animation"),
                    ("splash",                          "show splash screen again"),
                    ("cal",                             "show calendar"),
                    ("color <hex>",                     "preview a hex colour"),
                    ("qr <text>",                       "generate a QR code"),
                ]),
                ("TOOLS", [
                    ("calc <expr>",                     "calculator e.g. calc 2**8"),
                    ("unit <val> <from> <to>",          "unit converter e.g. unit 5 km mi"),
                    ("hash <text>",                     "MD5/SHA256 hash of text"),
                    ("vault add/get/del/list",          "encrypted secret storage"),
                    ("macro record/stop/play <name>",   "record and replay commands"),
                    ("cron add/list/del",               "scheduled command jobs"),
                ]),
                ("SECURITY", [
                    ("lock set <pw>",                   "set a password lock"),
                    ("lock now",                        "lock the screen immediately"),
                    ("lock clear",                      "remove password lock"),
                ]),
                ("MISC", [
                    ("clear",                           "clear the screen"),
                    ("exit",                            "close ARCH"),
                ]),
            ]
            CMD_W = 36
            for title, cmds in sections:
                self._w(f"\n  {title}\n","info")
                for name, desc in cmds:
                    self._w(f"    {name:<{CMD_W}}","bold")
                    self._w(f"{desc}\n","dim")
            self._w(f"\n  Themes: ","dim"); self._w(" ".join(get_themes().keys())+"\n\n","info")
            return

        if cmd in ("exit","quit"):
            self.root.destroy(); return

        if cmd == "clear":
            self.out.config(state="normal"); self.out.delete("1.0","end"); self.out.config(state="disabled")
            self._animated_banner(); self._show_favorites(); return

        # ── app launch ──
        if cmd in self.apps:
            path = os.path.expandvars(self.apps[cmd])
            self._w(f"\n  Launching ","dim"); self._w(cmd,"bold"); self._w("...\n\n","dim")
            if cmd not in RECENT: RECENT.append(cmd)
            if len(RECENT)>MAX_RECENT: RECENT.pop(0)
            log_entry = {"app":cmd,"time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            CFG["launch_log"].append(log_entry)
            if len(CFG["launch_log"])>500: CFG["launch_log"].pop(0)
            save_config(CFG)
            try: subprocess.Popen(path, shell=True)
            except Exception as e: self._w(f"  Error: {e}\n","err")
            if CFG.get("autoclose"): self.root.withdraw()
            return

        # ── fuzzy fallback ──
        all_cmds = list(self.apps.keys())
        close    = fuzzy_match(cmd, all_cmds)
        self._w(f"\n  Unknown: '{cmd}'","err")
        if close: self._w(f"  — did you mean: ","dim"); self._w(", ".join(close[:4])+"\n\n","info")
        else: self._w("  Type ","dim"); self._w("help","info"); self._w(" to see all.\n\n","dim")

    # ── Unit converter ─────────────────────────────────────────────────────────
    def _unit_convert(self, text):
        conversions = {
            ("km","mi"):0.621371, ("mi","km"):1.60934,
            ("kg","lb"):2.20462,  ("lb","kg"):0.453592,
            ("m","ft"):3.28084,   ("ft","m"):0.3048,
            ("c","f"):None,       ("f","c"):None,
        }
        parts = text.lower().split()
        if len(parts)<3:
            self._w("\n  Usage: unit <value> <from> <to>\n\n","err"); return
        try: val = float(parts[0])
        except Exception: self._w("\n  Invalid value.\n\n","err"); return
        frm, to = parts[1], parts[2]
        if frm=="c" and to=="f": result = val*9/5+32
        elif frm=="f" and to=="c": result = (val-32)*5/9
        elif (frm,to) in conversions:
            result = val * conversions[(frm,to)]
        else:
            self._w(f"\n  Conversion not supported.\n\n","err"); return
        self._w(f"\n  {val} {frm} = ","dim"); self._w(f"{result:.4g} {to}\n\n","bold")

    # ── AI features (Gemini) ───────────────────────────────────────────────────
    def _ask_ai(self, question):
        api_key = CFG.get("gemini_api_key","")
        if not api_key:
            self._w("\n  ⚠ AI features disabled. Set API key: apikey set <your-gemini-key>\n","err")
            self._w("  Get a free key at: aistudio.google.com\n\n","dim"); return
        self._w("\n  ◈ Thinking...\n","dim")
        self._ai_session.append({"role":"user","content":question})
        def fetch():
            try:
                # Build Gemini contents format from session history
                contents = []
                for msg in self._ai_session[-20:]:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": msg["content"]}]})
                payload = json.dumps({
                    "system_instruction": {"parts": [{"text": "You are ARCH, a terminal assistant. Respond in plain text only — no markdown, no asterisks, no bullet symbols."}]},
                    "contents": contents,
                    "generationConfig": {"maxOutputTokens": 512, "temperature": 0.7}
                }).encode()
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                req = urllib.request.Request(url, data=payload, headers={"Content-Type":"application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read())
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                self._ai_session.append({"role":"assistant","content":text})
                def show():
                    self._w("\n")
                    for line in text.splitlines(): self._w(f"  {line}\n","ai")
                    self._w("\n")
                self.root.after(0, show)
            except Exception as e:
                self.root.after(0, lambda: self._w(f"\n  AI error: {str(e)[:80]}\n\n","err"))
        threading.Thread(target=fetch, daemon=True).start()

    # ── Font & opacity ─────────────────────────────────────────────────────────
    def _apply_font_size(self, size):
        new_font = ("Courier New", size)
        self.out.configure(font=new_font)
        self.entry.configure(font=new_font)
        self.prompt_lbl.configure(font=new_font)
        self.cur.configure(font=new_font)
        self._retag()

    def _apply_opacity(self, val):
        val = max(20, min(100, val))
        self.root.attributes("-alpha", val/100)

    # ── Graph ──────────────────────────────────────────────────────────────────
    def _show_graph(self):
        self._w("\n  Opening live graph...\n\n","info")
        win = tk.Toplevel(self.root); win.title("ARCH — Live Stats"); win.configure(bg=self.BG); win.geometry("600x220")
        canvas = tk.Canvas(win, bg=self.BG, highlightthickness=0, width=600, height=200)
        canvas.pack(fill="both", expand=True)
        running = [True]
        win.protocol("WM_DELETE_WINDOW", lambda: running.__setitem__(0,False) or win.destroy())
        def draw():
            if not running[0]: return
            canvas.delete("all"); W,H=600,200; margin=40; gw=W-margin*2; gh=(H-20)//2-10
            canvas.create_text(margin,10,text="CPU %",fill=self.FG,anchor="w",font=("Courier New",9,"bold"))
            for i,v in enumerate(self.cpu_history[-gw:]):
                x=margin+i; y=20+gh-int(v/100*gh); canvas.create_line(x,20+gh,x,y,fill=self.GRAPH)
            canvas.create_text(W-10,10,text=f"{self.cpu_history[-1]:.0f}%",fill=self.INFO,anchor="e",font=("Courier New",9))
            off=H//2
            canvas.create_text(margin,off,text="RAM %",fill=self.FG,anchor="w",font=("Courier New",9,"bold"))
            for i,v in enumerate(self.ram_history[-gw:]):
                x=margin+i; y=off+10+gh-int(v/100*gh); canvas.create_line(x,off+10+gh,x,y,fill=self.INFO)
            canvas.create_text(W-10,off,text=f"{self.ram_history[-1]:.0f}%",fill=self.INFO,anchor="e",font=("Courier New",9))
            win.after(1000, draw)
        draw()

    def _show_dash(self):
        self._w("\n  Opening dashboard...\n\n","info")
        win = tk.Toplevel(self.root); win.title("ARCH — Dashboard"); win.configure(bg=self.BG); win.geometry("700x300")
        now2  = datetime.datetime.now().strftime("%A, %B %d  %H:%M:%S")
        cpu   = psutil.cpu_percent(); ram = psutil.virtual_memory(); disk = psutil.disk_usage("/")
        tk.Label(win,text="◈ ARCH DASHBOARD",bg=self.BG,fg=self.FG,font=("Courier New",16,"bold")).pack(pady=(16,4))
        tk.Label(win,text=now2,bg=self.BG,fg=self.DIM,font=("Courier New",11)).pack(pady=(0,12))
        fr = tk.Frame(win,bg=self.BG); fr.pack(fill="x",padx=32)
        for label,val,color in [(f"CPU\n{cpu:.0f}%",cpu,self.GRAPH),(f"RAM\n{ram.percent:.0f}%",ram.percent,self.INFO),(f"DISK\n{disk.percent:.0f}%",disk.percent,self.DIM)]:
            col = tk.Frame(fr,bg=self.BAR,padx=16,pady=12); col.pack(side="left",expand=True,fill="both",padx=6)
            tk.Label(col,text=label,bg=self.BAR,fg=color,font=("Courier New",13,"bold")).pack()
        tk.Button(win,text="Close",bg=self.BAR,fg=self.DIM,font=FONTS,relief="flat",command=win.destroy).pack(pady=14)

    # ── Matrix ─────────────────────────────────────────────────────────────────
    def _matrix_rain(self):
        self._w("\n  Matrix mode — press any key to stop\n\n","info")
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*()"
        self.matrix_running = True
        def stop(_=None):
            self.matrix_running = False; self.root.unbind("<Key>"); self.entry.focus_force()
        self.root.bind("<Key>", stop)
        def rain():
            if not self.matrix_running: return
            self._w("  "+"".join(random.choice(chars) for _ in range(60))+"\n","bold")
            self.root.after(60, rain)
        rain()

    def _glitch_effect(self):
        self._w("\n","")
        chars = "!@#$%^&*<>?/\\|~`"
        glitches = [0]
        def tick():
            if glitches[0] >= 12: self._w("\n"); return
            self._w("  "+"".join(random.choice(chars) for _ in range(random.randint(10,60)))+"\n","err")
            glitches[0] += 1
            self.root.after(random.randint(30,120), tick)
        tick()

    # ── Hotkey listener ────────────────────────────────────────────────────────
    def _start_hotkey_listener(self):
        try:
            import keyboard
            hotkey = CFG.get("hotkey","ctrl+space")
            def listen():
                try:
                    keyboard.add_hotkey(hotkey, lambda: self.root.after(0, self._toggle_visibility))
                    keyboard.wait()
                except Exception:
                    pass
            threading.Thread(target=listen, daemon=True).start()
        except ImportError:
            pass

    def _toggle_visibility(self):
        if self.root.state()=="withdrawn":
            self.root.deiconify(); self.root.lift(); self.entry.focus_force()
        else:
            self.root.withdraw()

    # ── Autocomplete ───────────────────────────────────────────────────────────
    def _autocomplete(self, _=None):
        typed = self.entry.get().strip().lower()
        if not typed: return "break"
        all_cmds = list(self.apps.keys())
        matches  = fuzzy_match(typed, all_cmds)
        if len(matches)==1:
            self.entry.delete(0,"end"); self.entry.insert(0, matches[0])
        elif len(matches)>1:
            self._w(f"\n  {' '.join(matches[:10])}\n","dim")
        return "break"

    # ── History ────────────────────────────────────────────────────────────────
    def _hist_up(self, _):
        if not self.history: return
        self.hidx = min(self.hidx+1, len(self.history)-1)
        self.entry.delete(0,"end"); self.entry.insert(0, self.history[-(self.hidx+1)])

    def _hist_dn(self, _):
        if self.hidx<=0: self.hidx=-1; self.entry.delete(0,"end"); return
        self.hidx-=1; self.entry.delete(0,"end"); self.entry.insert(0, self.history[-(self.hidx+1)])

    # ── Blink ──────────────────────────────────────────────────────────────────
    def _blink(self):
        self.cur.config(fg=self.FG if self.cur.cget("fg")==self.BG else self.BG)
        self.root.after(500, self._blink)

    # ── Activity ───────────────────────────────────────────────────────────────
    def _reset_activity(self, _=None):
        self._last_activity = time.time()

    def _inactivity_watch(self):
        self.root.after(60000, self._inactivity_watch)

    def _start_cron(self):
        # Placeholder for cron job scheduler
        self.root.after(60000, self._start_cron)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        subprocess.run([sys.executable,"-m","pip","install","psutil"],check=True)
        import psutil
    
    Launcher()
