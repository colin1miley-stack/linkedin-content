#!/usr/bin/env python3
"""
Colin Miley Revenue Systems — Prospect Intelligence Auditor GUI
Scrollable branded interface that fits any screen size.

Usage:
    python gui.py
    # Or double-click gui.py

Author: Colin Miley Revenue Systems
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import webbrowser
from pathlib import Path
from urllib.parse import urlparse

# Brand colors (colinmiley.com palette)
PRIMARY_BG = "#0B0D10"
ACCENT_LIME = "#C8F560"
TEXT_WHITE = "#F3F0E8"
TEXT_GRAY = "#9EA6AF"
CARD_BG = "#14171B"
INPUT_BG = "#1E2329"
SUCCESS_GREEN = "#73E6DF"  # signal cyan

class ScrollableFrame(tk.Frame):
    """A scrollable frame that works with any content height."""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self, bg=PRIMARY_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=PRIMARY_BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # Update canvas width when frame resizes
        self.canvas.bind('<Configure>', self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")


class RevenueRitualGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Colin Miley Revenue Systems — Prospect Auditor")
        self.root.geometry("680x650")
        self.root.configure(bg=PRIMARY_BG)
        self.root.minsize(600, 500)

        self.script_dir = Path(__file__).parent
        self.report_path = None
        self.build_ui()

    def build_ui(self):
        # Main scrollable container
        main_scroll = ScrollableFrame(self.root, bg=PRIMARY_BG)
        main_scroll.pack(fill=tk.BOTH, expand=True)

        container = main_scroll.scrollable_frame

        # Inner padding frame
        inner = tk.Frame(container, bg=PRIMARY_BG)
        inner.pack(fill=tk.BOTH, expand=True, padx=35, pady=25)

        # === HEADER ===
        logo = tk.Label(
            inner,
            text="COLIN MILEY",
            font=("Helvetica Neue", 26),
            fg=TEXT_WHITE,
            bg=PRIMARY_BG
        )
        logo.pack(anchor=tk.W)

        tagline = tk.Label(
            inner,
            text="Prospect Intelligence Auditor",
            font=("Helvetica Neue", 11),
            fg=ACCENT_LIME,
            bg=PRIMARY_BG
        )
        tagline.pack(anchor=tk.W, pady=(2, 0))

        tk.Label(
            inner,
            text="Find the signal. Fix the handoff. Build the ritual.",
            font=("Helvetica Neue", 10),
            fg=TEXT_GRAY,
            bg=PRIMARY_BG
        ).pack(anchor=tk.W, pady=(3, 0))

        # Separator
        tk.Frame(inner, height=1, bg=ACCENT_LIME).pack(fill=tk.X, pady=18)

        # === FORM ===
        # URL
        self._label(inner, "Website URL *")
        self.url_entry = self._input(inner, "https://example.com")
        self.url_entry.pack(fill=tk.X, pady=(0, 15))

        # Revenue
        self._label(inner, "Annual Revenue (€) - Optional")
        self.revenue_entry = self._input(inner, "e.g. 250000")
        self.revenue_entry.pack(fill=tk.X, pady=(0, 15))

        # Industry dropdown
        self._label(inner, "Industry - Optional")
        self.industry_var = tk.StringVar(value="Auto-detect")
        industries = [
            "Auto-detect",
            "Wedding Services",
            "Professional Services",
            "E-commerce",
            "SaaS / Tech",
            "Health & Wellness",
            "Hospitality",
            "Retail",
            "General Business",
        ]

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox",
                        fieldbackground=INPUT_BG,
                        background=INPUT_BG,
                        foreground=TEXT_WHITE,
                        arrowcolor=ACCENT_LIME)
        style.map('TCombobox', fieldbackground=[('readonly', INPUT_BG)])

        self.industry_combo = ttk.Combobox(
            inner,
            textvariable=self.industry_var,
            values=industries,
            state="readonly",
            font=("Helvetica Neue", 11),
            height=8
        )
        self.industry_combo.pack(fill=tk.X, pady=(0, 20))

        # === ENTRY POINT SECTION ===
        tk.Label(
            inner,
            text="SELECT SERVICE ENTRY POINT *",
            font=("Helvetica Neue", 12, "bold"),
            fg=ACCENT_LIME,
            bg=PRIMARY_BG
        ).pack(anchor=tk.W, pady=(10, 5))

        tk.Label(
            inner,
            text="Choose how to engage this prospect:",
            font=("Helvetica Neue", 10),
            fg=TEXT_GRAY,
            bg=PRIMARY_BG
        ).pack(anchor=tk.W, pady=(0, 12))

        self.entry_var = tk.StringVar(value="revenue-leak-audit")

        # Click handler for cards
        def apply_card_style(card, top, info, labels, is_selected):
            """Apply styling to a card based on selection state."""
            bg = ACCENT_LIME if is_selected else CARD_BG
            fg_title = PRIMARY_BG if is_selected else TEXT_WHITE
            fg_sub = PRIMARY_BG if is_selected else ACCENT_LIME
            fg_bullet = PRIMARY_BG if is_selected else TEXT_GRAY
            
            card.configure(bg=bg)
            top.configure(bg=bg)
            info.configure(bg=bg)
            for lbl in labels:
                if hasattr(lbl, 'configure'):
                    # Determine if this is title, sub, or bullet by checking current fg
                    current_fg = lbl.cget('fg')
                    if current_fg in (TEXT_WHITE, PRIMARY_BG):
                        lbl.configure(bg=bg, fg=fg_title)
                    elif current_fg in (ACCENT_LIME,):
                        lbl.configure(bg=bg, fg=fg_sub)
                    else:
                        lbl.configure(bg=bg, fg=fg_bullet)
            # Update radio button
            for child in top.winfo_children():
                if isinstance(child, tk.Radiobutton):
                    child.configure(bg=bg, selectcolor=TEXT_WHITE if is_selected else ACCENT_LIME)

        def select_sprint():
            self.entry_var.set("founding-client-audit")
            apply_card_style(sprint_card, sprint_top, sprint_info, sprint_labels, True)
            apply_card_style(audit_card, audit_top, audit_info, audit_labels, False)

        def select_audit():
            self.entry_var.set("revenue-leak-audit")
            apply_card_style(audit_card, audit_top, audit_info, audit_labels, True)
            apply_card_style(sprint_card, sprint_top, sprint_info, sprint_labels, False)

        # === FOUNDING CLIENT AUDIT CARD (starts unselected) ===
        sprint_card = tk.Frame(inner, bg=CARD_BG, padx=18, pady=18, cursor="hand2",
                               highlightbackground=ACCENT_LIME, highlightthickness=2)
        sprint_card.pack(fill=tk.X, pady=6)
        sprint_card.bind("<Button-1>", lambda e: select_sprint())

        sprint_top = tk.Frame(sprint_card, bg=CARD_BG)
        sprint_top.pack(fill=tk.X)
        sprint_top.bind("<Button-1>", lambda e: select_sprint())

        # Bigger radio button using ttk with custom style
        radio_style = ttk.Style()
        radio_style.configure("Big.TRadiobutton", background=CARD_BG, foreground=TEXT_WHITE)
        
        sprint_radio = tk.Radiobutton(
            sprint_top,
            text="",
            variable=self.entry_var,
            value="founding-client-audit",
            bg=CARD_BG,
            selectcolor=ACCENT_LIME,
            activebackground=CARD_BG,
            highlightthickness=0,
            indicatoron=1,
            width=3,
            height=1,
            font=("Helvetica Neue", 14)
        )
        sprint_radio.pack(side=tk.LEFT, padx=(0, 12))
        sprint_radio.bind("<Button-1>", lambda e: select_sprint())

        sprint_info = tk.Frame(sprint_top, bg=CARD_BG)
        sprint_info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sprint_info.bind("<Button-1>", lambda e: select_sprint())

        sprint_labels = []

        l1 = tk.Label(sprint_info, text="FOUNDING CLIENT AUDIT",
                 font=("Helvetica Neue", 13, "bold"),
                 fg=TEXT_WHITE, bg=CARD_BG)
        l1.pack(anchor=tk.W)
        l1.bind("<Button-1>", lambda e: select_sprint())
        sprint_labels.append(l1)

        l2 = tk.Label(sprint_info, text="€2,500  ·  2 weeks  ·  Founding rate — case study required",
                 font=("Helvetica Neue", 10),
                 fg=ACCENT_LIME, bg=CARD_BG)
        l2.pack(anchor=tk.W, pady=(2, 0))
        l2.bind("<Button-1>", lambda e: select_sprint())
        sprint_labels.append(l2)

        # Bullet points
        for item in ["Full Revenue Leak Audit at founding rate",
                     "Client approves a written case study + testimonial",
                     "3 places — then the programme closes"]:
            lbl = tk.Label(sprint_card, text=f"  ✓  {item}",
                     font=("Helvetica Neue", 10),
                     fg=TEXT_GRAY, bg=CARD_BG)
            lbl.pack(anchor=tk.W, pady=(6, 0))
            lbl.bind("<Button-1>", lambda e: select_sprint())
            sprint_labels.append(lbl)

        # === REVENUE LEAK AUDIT CARD (starts selected as default) ===
        audit_card = tk.Frame(inner, bg=ACCENT_LIME, padx=18, pady=18, cursor="hand2",
                              highlightbackground=ACCENT_LIME, highlightthickness=2)
        audit_card.pack(fill=tk.X, pady=6)
        audit_card.bind("<Button-1>", lambda e: select_audit())

        audit_top = tk.Frame(audit_card, bg=ACCENT_LIME)
        audit_top.pack(fill=tk.X)
        audit_top.bind("<Button-1>", lambda e: select_audit())

        audit_radio = tk.Radiobutton(
            audit_top,
            text="",
            variable=self.entry_var,
            value="revenue-leak-audit",
            bg=ACCENT_LIME,
            selectcolor=TEXT_WHITE,
            activebackground=ACCENT_LIME,
            highlightthickness=0,
            indicatoron=1,
            width=3,
            height=1,
            font=("Helvetica Neue", 14)
        )
        audit_radio.pack(side=tk.LEFT, padx=(0, 12))
        audit_radio.bind("<Button-1>", lambda e: select_audit())

        audit_info = tk.Frame(audit_top, bg=ACCENT_LIME)
        audit_info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        audit_info.bind("<Button-1>", lambda e: select_audit())

        audit_labels = []

        l3 = tk.Label(audit_info, text="REVENUE LEAK AUDIT",
                 font=("Helvetica Neue", 13, "bold"),
                 fg=PRIMARY_BG, bg=ACCENT_LIME)
        l3.pack(anchor=tk.W)
        l3.bind("<Button-1>", lambda e: select_audit())
        audit_labels.append(l3)

        l4 = tk.Label(audit_info, text="€7,500  ·  Full diagnosis  ·  2–3 automations + 90-day roadmap",
                 font=("Helvetica Neue", 10),
                 fg=PRIMARY_BG, bg=ACCENT_LIME)
        l4.pack(anchor=tk.W, pady=(2, 0))
        l4.bind("<Button-1>", lambda e: select_audit())
        audit_labels.append(l4)

        for item in ["Full process map: every leak identified",
                     "CRM audit + 2–3 automations configured",
                     "90-day action plan with milestones",
                     "30-day check-in call"]:
            lbl = tk.Label(audit_card, text=f"  ✓  {item}",
                     font=("Helvetica Neue", 10),
                     fg=PRIMARY_BG, bg=ACCENT_LIME)
            lbl.pack(anchor=tk.W, pady=(6, 0))
            lbl.bind("<Button-1>", lambda e: select_audit())
            audit_labels.append(lbl)

        # Default selection: Revenue Leak Audit (pre-selected)
        # Already styled above with gold bg

        # === RUN BUTTON ===
        self.run_btn = tk.Button(
            inner,
            text="RUN AUDIT",
            font=("Helvetica Neue", 14, "bold"),
            fg=PRIMARY_BG,
            bg=ACCENT_LIME,
            activebackground=TEXT_WHITE,
            activeforeground=PRIMARY_BG,
            bd=0,
            padx=40,
            pady=14,
            cursor="hand2",
            command=self.run_audit
        )
        self.run_btn.pack(pady=25)

        # === PROGRESS ===
        self.progress_frame = tk.Frame(inner, bg=PRIMARY_BG)
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Helvetica Neue", 10),
            fg=TEXT_GRAY,
            bg=PRIMARY_BG
        )
        self.progress_label.pack(anchor=tk.W)

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=600
        )
        self.progress_bar.pack(fill=tk.X, pady=8)

        # === RESULT ===
        self.result_frame = tk.Frame(inner, bg=PRIMARY_BG)

        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Helvetica Neue", 11),
            fg=TEXT_WHITE,
            bg=PRIMARY_BG,
            wraplength=580,
            justify=tk.LEFT
        )
        self.result_label.pack(anchor=tk.W, pady=(0, 12))

        self.btn_row = tk.Frame(self.result_frame, bg=PRIMARY_BG)
        self.btn_row.pack(anchor=tk.W)

        self.open_btn = tk.Button(
            self.btn_row,
            text="Open Report",
            font=("Helvetica Neue", 11),
            fg=PRIMARY_BG,
            bg=SUCCESS_GREEN,
            activebackground=TEXT_WHITE,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.open_report
        )
        self.open_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.folder_btn = tk.Button(
            self.btn_row,
            text="Open Folder",
            font=("Helvetica Neue", 11),
            fg=TEXT_WHITE,
            bg=CARD_BG,
            activebackground=INPUT_BG,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.open_folder
        )
        self.folder_btn.pack(side=tk.LEFT)

    def _label(self, parent, text):
        tk.Label(parent, text=text,
                 font=("Helvetica Neue", 11),
                 fg=TEXT_WHITE, bg=PRIMARY_BG).pack(anchor=tk.W, pady=(10, 4))

    def _input(self, parent, placeholder):
        entry = tk.Entry(
            parent,
            font=("Helvetica Neue", 12),
            fg=TEXT_GRAY,
            bg=INPUT_BG,
            insertbackground=TEXT_WHITE,
            bd=0,
            highlightthickness=1,
            highlightcolor=ACCENT_LIME,
            highlightbackground="#3a3a3a"
        )
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=TEXT_WHITE)

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg=TEXT_GRAY)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry

    def run_audit(self):
        url = self.url_entry.get().strip()
        placeholder = "https://example.com"

        if not url or url == placeholder:
            messagebox.showerror("Error", "Please enter a website URL.")
            return

        if not url.startswith("http"):
            url = "https://" + url

        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError
        except:
            messagebox.showerror("Error", "Please enter a valid URL (e.g., https://example.com)")
            return

        revenue = self.revenue_entry.get().strip()
        revenue_placeholder = "e.g. 250000"
        revenue_val = None
        if revenue and revenue != revenue_placeholder:
            try:
                revenue_val = int(revenue.replace(",", "").replace("€", "").replace(" ", ""))
            except ValueError:
                messagebox.showerror("Error", "Revenue must be a number (e.g., 250000)")
                return

        # Map display text to command key
        industry_display = self.industry_var.get()
        industry_map = {
            "Auto-detect": "auto",
            "Wedding Services": "wedding_services",
            "Professional Services": "professional_services",
            "E-commerce": "ecommerce",
            "SaaS / Tech": "saas",
            "Health & Wellness": "health_wellness",
            "Hospitality": "hospitality",
            "Retail": "retail",
            "General Business": "general",
        }
        industry = industry_map.get(industry_display, "auto")
        entry_point = self.entry_var.get()

        # Show progress - clear any previous result state first
        self.run_btn.config(state=tk.DISABLED, text="RUNNING AUDIT...")
        self.result_frame.pack_forget()
        # Destroy old PDF button if it exists from previous run
        if hasattr(self, 'pdf_btn') and self.pdf_btn.winfo_exists():
            self.pdf_btn.destroy()
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))
        self.progress_bar.start()
        self.progress_label.config(text=f"Auditing {urlparse(url).netloc}...")
        self.root.update()

        # Build command
        cmd = [
            sys.executable,
            str(self.script_dir / "scripts" / "audit.py"),
            "--url", url,
            "--output", "html",
            "--output-dir", str(self.script_dir.parent.parent.parent / "prospect-audits"),
            "--entry-point", entry_point
        ]

        if revenue_val:
            cmd.extend(["--revenue", str(revenue_val)])

        if industry != "auto":
            cmd.extend(["--industry", industry])

        # Run audit
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            self.progress_bar.stop()
            self.progress_frame.pack_forget()
            self.run_btn.config(state=tk.NORMAL, text="RUN AUDIT")

            if result.returncode != 0:
                messagebox.showerror("Audit Failed", result.stderr or "Unknown error occurred.")
                return

            # Parse output for report paths
            self.report_path = None
            self.pdf_path = None

            for line in result.stdout.split("\n"):
                if "Report complete:" in line:
                    paths = line.split("Report complete:")[1].strip()
                    path_parts = paths.split("|")
                    self.report_path = path_parts[0].strip()
                    if len(path_parts) > 1:
                        self.pdf_path = path_parts[1].strip()
                    break
                elif "HTML report saved:" in line:
                    self.report_path = line.split("HTML report saved:")[1].strip()
                elif "PDF report saved:" in line:
                    self.pdf_path = line.split("PDF report saved:")[1].strip()

            # Show result
            self.result_frame.pack(fill=tk.X, pady=(10, 0))

            if self.report_path and Path(self.report_path).exists():
                msg = f"Audit complete for {urlparse(url).netloc}\n"
                msg += f"HTML: {Path(self.report_path).name}"
                if self.pdf_path and Path(self.pdf_path).exists():
                    msg += f"\nPDF: {Path(self.pdf_path).name}"
                else:
                    msg += "\nPDF: Use browser Print -> Save as PDF"

                self.result_label.config(text=msg, fg=SUCCESS_GREEN)

        # Add PDF button if available
                if self.pdf_path and Path(self.pdf_path).exists():
                    self.pdf_btn = tk.Button(
                        self.btn_row,
                        text="Open PDF",
                        font=("Helvetica Neue", 11),
                        fg=PRIMARY_BG,
                        bg=ACCENT_LIME,
                        activebackground=TEXT_WHITE,
                        bd=0,
                        padx=20,
                        pady=10,
                        cursor="hand2",
                        command=self.open_pdf
                    )
                    self.pdf_btn.pack(side=tk.LEFT, padx=(0, 10))
                
                # New Audit button — clears form for next run
                self.new_audit_btn = tk.Button(
                    self.btn_row,
                    text="New Audit →",
                    font=("Helvetica Neue", 11),
                    fg=PRIMARY_BG,
                    bg=TEXT_WHITE,
                    activebackground=ACCENT_LIME,
                    bd=0,
                    padx=20,
                    pady=10,
                    cursor="hand2",
                    command=self.reset_for_new_audit
                )
                self.new_audit_btn.pack(side=tk.LEFT)

                webbrowser.open(f"file:///{self.report_path}")
            else:
                self.result_label.config(
                    text="Audit complete. Check the prospect-audits/ folder.",
                    fg=TEXT_GRAY
                )

        except subprocess.TimeoutExpired:
            self.progress_bar.stop()
            self.progress_frame.pack_forget()
            self.run_btn.config(state=tk.NORMAL, text="RUN AUDIT")
            messagebox.showerror("Timeout", "Audit took too long. The website may be slow or unreachable.")
        except Exception as e:
            self.progress_bar.stop()
            self.progress_frame.pack_forget()
            self.run_btn.config(state=tk.NORMAL, text="RUN AUDIT")
            messagebox.showerror("Error", str(e))

    def open_report(self):
        if self.report_path and Path(self.report_path).exists():
            webbrowser.open(f"file:///{self.report_path}")

    def open_pdf(self):
        if self.pdf_path and Path(self.pdf_path).exists():
            webbrowser.open(f"file:///{self.pdf_path}")

    def reset_for_new_audit(self):
        """Clear form and prepare for next audit."""
        # Clear URL
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "https://example.com")
        self.url_entry.config(fg=TEXT_GRAY)
        
        # Clear revenue
        self.revenue_entry.delete(0, tk.END)
        self.revenue_entry.insert(0, "e.g. 250000")
        self.revenue_entry.config(fg=TEXT_GRAY)
        
        # Hide result frame
        self.result_frame.pack_forget()
        
        # Destroy PDF button if it exists
        if hasattr(self, 'pdf_btn') and self.pdf_btn.winfo_exists():
            self.pdf_btn.destroy()
        if hasattr(self, 'new_audit_btn') and self.new_audit_btn.winfo_exists():
            self.new_audit_btn.destroy()
        
        # Focus URL field
        self.url_entry.focus_set()

    def open_folder(self):
        folder = self.script_dir.parent.parent.parent / "prospect-audits"
        if folder.exists():
            os.startfile(str(folder))


def main():
    root = tk.Tk()

    # Style for progressbar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TProgressbar",
                    thickness=8,
                    background=ACCENT_LIME,
                    troughcolor=INPUT_BG,
                    borderwidth=0)
    style.configure("Vertical.TScrollbar",
                    background=CARD_BG,
                    troughcolor=PRIMARY_BG,
                    borderwidth=0)

    app = RevenueRitualGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
