#!/usr/bin/env python3
import threading
import time
import tkinter as tk
import urllib.error
import urllib.parse
import urllib.request
from tkinter import messagebox, scrolledtext, ttk

BG_COLOR = "#1e1e1e"
FG_COLOR = "#c0c0c0"
ENTRY_BG = "#2b2b2b"
BUTTON_BG = "#3c3c3c"
ACCENT = "#00adb5"


def probe(url, param, payload_base, delay, log):
    try:
        t0 = time.time()
        urllib.request.urlopen(f"{url}?{urllib.parse.urlencode({param: payload_base})}")
        base_time = time.time() - t0

        t0 = time.time()
        urllib.request.urlopen(
            f"{url}?{urllib.parse.urlencode({param: payload_base + f' and sleep({delay})'})}"
        )
        sleep_time = time.time() - t0

        delta = sleep_time - base_time
        if delta >= delay - 0.5:
            log(f"🔴 VULNERABLE: {delta:.1f}s delay")
        else:
            log(f"✅ Safe: delta {delta:.1f}s")
    except Exception as e:
        log(f"⚠️ Error: {e}")


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time-Blind SQLi Detector")
        self.geometry("680x460")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR)
        style.configure("TEntry", fieldbackground=ENTRY_BG, foreground=FG_COLOR, insertcolor=FG_COLOR)
        style.configure("TButton", background=BUTTON_BG, foreground=FG_COLOR)
        style.map("TButton", background=[("active", ACCENT)])

        frm = ttk.Frame(self)
        frm.pack(fill="x", padx=12, pady=12)

        ttk.Label(frm, text="URL:").grid(row=0, column=0, sticky="e", padx=4)
        self.url_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.url_var, width=50).grid(row=0, column=1, padx=4)

        ttk.Label(frm, text="Param:").grid(row=1, column=0, sticky="e", padx=4)
        self.param_var = tk.StringVar(value="id")
        ttk.Entry(frm, textvariable=self.param_var, width=15).grid(row=1, column=1, sticky="w", padx=4)

        ttk.Label(frm, text="Delay (s):").grid(row=2, column=0, sticky="e", padx=4)
        self.delay_var = tk.IntVar(value=5)
        ttk.Spinbox(frm, from_=3, to=15, textvariable=self.delay_var, width=4).grid(
            row=2, column=1, sticky="w", padx=4
        )

        ttk.Button(frm, text="Scan", command=self.start).grid(row=3, column=0, columnspan=2, pady=8)

        self.log = scrolledtext.ScrolledText(
            self,
            state="disabled",
            bg=ENTRY_BG,
            fg=FG_COLOR,
            insertbackground=FG_COLOR,
            font=("Consolas", 10),
        )
        self.log.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def log_msg(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.configure(state="disabled")
        self.log.yview("end")

    def start(self):
        url = self.url_var.get().strip()
        param = self.param_var.get().strip()
        delay = self.delay_var.get()
        if not url or not param:
            messagebox.showerror("Error", "Please fill URL and parameter")
            return
        self.log_msg(f"🔍 Testing {url}?{param}=...sleep({delay})")
        threading.Thread(
            target=probe, args=(url, param, "1", delay, self.log_msg), daemon=True
        ).start()


if __name__ == "__main__":
    GUI().mainloop()