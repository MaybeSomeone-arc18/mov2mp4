import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox
import threading
from pathlib import Path
import os
import sys
import math
import re

import runtime
runtime.setup_environment()

from utils import check_ffmpeg_installed, find_mov_files
from converter import VideoConverter, ConversionResult
from logger import setup_logger

THEME = {
    "bg": "#111214",
    "surface": "#181A1F",
    "surface_secondary": "#202329",
    "border": "#30343B",
    "text_primary": "#F5F7FA",
    "text_secondary": "#A7ADB7",
    "text_muted": "#6F7682",
    "accent": "#6C8CFF",
    "accent_hover": "#7D9AFF",
    "success": "#43C98B",
    "warning": "#F2B84B",
    "error": "#FF6B6B"
}

def format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

class TkinterDnD_CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class Mov2Mp4App(TkinterDnD_CTk):
    def __init__(self):
        super().__init__()
        
        # Base window config
        self.title("MOV2MP4")
        self.geometry("900x650")
        self.configure(fg_color=THEME["bg"])
        
        log_dir = Path.cwd() / "logs"
        self.logger = setup_logger(log_dir, verbose=False)
        
        # Windows native taskbar grouping and window icon
        if sys.platform.startswith("win"):
            try:
                import ctypes
                myappid = "mov2mp4.desktop.app.1.0"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception:
                pass
            icon_ico = Path(__file__).parent / "assets" / "icon.ico"
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                icon_ico = Path(sys._MEIPASS) / "assets" / "icon.ico"

            if icon_ico.exists():
                try:
                    self.iconbitmap(str(icon_ico))
                except Exception as e:
                    self.logger.warning(f"Could not set window icon: {e}")

        # State
        self.file_queue = []  # List of dicts: {"path": Path, "size": int, "status": str}
        self.output_folder = None # None means save next to original
        self.delete_original = ctk.BooleanVar(value=False)
        self.overwrite = ctk.BooleanVar(value=False)
        self.is_converting = False
        self.converter = None
        
        self.setup_ui()
        self.check_prerequisites()
        self.setup_bindings()
        
        # Force window to the front on macOS
        self.lift()
        self.attributes('-topmost', True)
        self.after(50, lambda: self.attributes('-topmost', False))

    def check_prerequisites(self):
        if not check_ffmpeg_installed():
            messagebox.showerror(
                "FFmpeg Missing", 
                "FFmpeg is not installed or not in the system PATH.\n\nPlease install FFmpeg to use this application."
            )
            self.start_btn.configure(state="disabled")

    def setup_bindings(self):
        self.bind('<Return>', lambda event: self.start_conversion() if not self.is_converting else None)
        self.bind('<Escape>', lambda event: self.quit())
        self.bind('<Command-q>', lambda event: self.quit())
        self.bind('<Control-q>', lambda event: self.quit())
        self.bind('<Command-o>', lambda event: self.browse_files())

    def setup_ui(self):
        # Fonts
        self.font_h1 = ctk.CTkFont(family="SF Pro Display", size=28, weight="bold")
        self.font_h2 = ctk.CTkFont(family="SF Pro Text", size=16, weight="bold")
        self.font_body = ctk.CTkFont(family="SF Pro Text", size=14)
        self.font_secondary = ctk.CTkFont(family="SF Pro Text", size=13)
        self.font_btn = ctk.CTkFont(family="SF Pro Text", size=15, weight="bold")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=30)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1) # Queue expands
        
        self.build_header()
        self.build_drag_drop()
        self.build_queue()
        self.build_settings()
        self.build_action()

    def build_header(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title = ctk.CTkLabel(header_frame, text="MOV2MP4", font=self.font_h1, text_color=THEME["text_primary"])
        title.grid(row=0, column=0, sticky="w")
        
        subtitle = ctk.CTkLabel(header_frame, text="Batch Video Converter", font=self.font_secondary, text_color=THEME["text_muted"])
        subtitle.grid(row=1, column=0, sticky="w")

    def build_drag_drop(self):
        self.drop_frame = ctk.CTkFrame(self.main_container, fg_color=THEME["surface"], border_color=THEME["border"], border_width=1, corner_radius=10, height=120)
        self.drop_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.drop_frame.grid_columnconfigure(0, weight=1)
        self.drop_frame.grid_propagate(False)
        
        drop_label = ctk.CTkLabel(self.drop_frame, text="Drop MOV files or folders here", font=self.font_body, text_color=THEME["text_secondary"])
        drop_label.grid(row=0, column=0, pady=(25, 5))
        
        btn_frame = ctk.CTkFrame(self.drop_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, pady=(0, 20))
        
        browse_file_btn = ctk.CTkButton(btn_frame, text="Browse Files", font=self.font_btn, fg_color=THEME["surface_secondary"], hover_color=THEME["border"], text_color=THEME["text_primary"], border_width=1, border_color=THEME["border"], command=self.browse_files, width=120)
        browse_file_btn.grid(row=0, column=0, padx=5)
        
        browse_folder_btn = ctk.CTkButton(btn_frame, text="Browse Folder", font=self.font_btn, fg_color=THEME["surface_secondary"], hover_color=THEME["border"], text_color=THEME["text_primary"], border_width=1, border_color=THEME["border"], command=self.browse_folder, width=120)
        browse_folder_btn.grid(row=0, column=1, padx=5)
        
        # DND
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)

    def build_queue(self):
        queue_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        queue_container.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        queue_container.grid_columnconfigure(0, weight=1)
        queue_container.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkFrame(queue_container, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)
        
        self.queue_title = ctk.CTkLabel(header, text="Files to convert", font=self.font_h2, text_color=THEME["text_primary"])
        self.queue_title.grid(row=0, column=0, sticky="w")
        
        self.clear_btn = ctk.CTkButton(header, text="Clear All", font=self.font_secondary, fg_color="transparent", text_color=THEME["text_secondary"], hover_color=THEME["surface_secondary"], command=self.clear_queue, width=60, height=24)
        self.clear_btn.grid(row=0, column=1, sticky="e")
        
        self.queue_scroll = ctk.CTkScrollableFrame(queue_container, fg_color=THEME["surface"], border_color=THEME["border"], border_width=1, corner_radius=10)
        self.queue_scroll.grid(row=1, column=0, sticky="nsew")
        self.queue_scroll.grid_columnconfigure(0, weight=1)
        
        self.queue_items_frames = {}

    def build_settings(self):
        settings_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        settings_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        settings_frame.grid_columnconfigure(0, weight=1)
        
        # Output
        out_frame = ctk.CTkFrame(settings_frame, fg_color=THEME["surface"], border_color=THEME["border"], border_width=1, corner_radius=10)
        out_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        out_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(out_frame, text="Output:", font=self.font_body, text_color=THEME["text_secondary"]).grid(row=0, column=0, padx=15, pady=15)
        self.out_path_lbl = ctk.CTkLabel(out_frame, text="Save next to originals", font=self.font_body, text_color=THEME["text_primary"])
        self.out_path_lbl.grid(row=0, column=1, sticky="w")
        
        ctk.CTkButton(out_frame, text="Change", font=self.font_secondary, fg_color=THEME["surface_secondary"], hover_color=THEME["border"], text_color=THEME["text_primary"], command=self.change_output_folder, width=70).grid(row=0, column=2, padx=(0, 5))
        ctk.CTkButton(out_frame, text="Reset", font=self.font_secondary, fg_color=THEME["surface_secondary"], hover_color=THEME["border"], text_color=THEME["text_primary"], command=self.reset_output_folder, width=60).grid(row=0, column=3, padx=(0, 15))
        
        # Advanced (Collapsible)
        self.adv_btn = ctk.CTkButton(settings_frame, text="Advanced Options ▾", font=self.font_secondary, fg_color="transparent", text_color=THEME["text_secondary"], hover_color=THEME["surface_secondary"], anchor="w", command=self.toggle_advanced, width=150)
        self.adv_btn.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        self.adv_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        # Do not grid it initially
        
        ctk.CTkCheckBox(self.adv_frame, text="Delete original .mov files", variable=self.delete_original, font=self.font_body, text_color=THEME["text_secondary"], checkbox_height=20, checkbox_width=20, border_color=THEME["border"], hover_color=THEME["accent_hover"], fg_color=THEME["accent"]).grid(row=0, column=0, sticky="w", padx=(10, 20), pady=10)
        ctk.CTkCheckBox(self.adv_frame, text="Overwrite existing .mp4 files", variable=self.overwrite, font=self.font_body, text_color=THEME["text_secondary"], checkbox_height=20, checkbox_width=20, border_color=THEME["border"], hover_color=THEME["accent_hover"], fg_color=THEME["accent"]).grid(row=0, column=1, sticky="w", pady=10)

    def toggle_advanced(self):
        if self.adv_frame.winfo_ismapped():
            self.adv_frame.grid_remove()
            self.adv_btn.configure(text="Advanced Options ▾")
        else:
            self.adv_frame.grid(row=2, column=0, sticky="ew")
            self.adv_btn.configure(text="Advanced Options ▴")

    def build_action(self):
        action_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        action_frame.grid(row=4, column=0, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)
        
        # Status / Progress (left side)
        self.status_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        self.status_container.grid(row=0, column=0, sticky="w")
        
        self.status_lbl = ctk.CTkLabel(self.status_container, text="Ready", font=self.font_body, text_color=THEME["text_muted"])
        self.status_lbl.grid(row=0, column=0, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(self.status_container, mode="determinate", width=350, fg_color=THEME["surface_secondary"], progress_color=THEME["accent"])
        self.progress_bar.grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.progress_bar.set(0)
        self.progress_bar.grid_remove() # hide initially
        
        # CTA buttons
        btns = ctk.CTkFrame(action_frame, fg_color="transparent")
        btns.grid(row=0, column=1, sticky="e")
        
        self.cancel_btn = ctk.CTkButton(btns, text="Cancel", font=self.font_btn, fg_color="transparent", text_color=THEME["text_primary"], hover_color=THEME["surface_secondary"], border_width=1, border_color=THEME["border"], command=self.cancel_conversion, width=100, height=40)
        self.cancel_btn.grid(row=0, column=0, padx=(0, 10))
        self.cancel_btn.grid_remove()
        
        self.start_btn = ctk.CTkButton(btns, text="Select files to begin", font=self.font_btn, fg_color=THEME["accent"], hover_color=THEME["accent_hover"], text_color="#FFFFFF", command=self.start_conversion, height=40, state="disabled")
        self.start_btn.grid(row=0, column=1)

    # UI Logic & File Handling
    def handle_drop(self, event):
        if self.is_converting: return
        paths = self.parse_drop_data(event.data)
        self.process_paths(paths)
        
    def parse_drop_data(self, data):
        paths = []
        if '{' in data:
            matches = re.findall(r'\{([^}]+)\}', data)
            paths.extend(matches)
            data = re.sub(r'\{[^}]+\}', '', data).strip()
        if data:
            paths.extend(data.split())
        return [Path(p) for p in paths]

    def browse_files(self):
        if self.is_converting: return
        files = filedialog.askopenfilenames(title="Select MOV files", filetypes=[("MOV files", "*.mov"), ("All files", "*.*")])
        if files:
            self.process_paths([Path(f) for f in files])
            
    def browse_folder(self):
        if self.is_converting: return
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.process_paths([Path(folder)])
            
    def change_output_folder(self):
        if self.is_converting: return
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = Path(folder)
            self.out_path_lbl.configure(text=str(self.output_folder))
            
    def reset_output_folder(self):
        if self.is_converting: return
        self.output_folder = None
        self.out_path_lbl.configure(text="Save next to originals")

    def process_paths(self, paths):
        added = 0
        for p in paths:
            if not p.exists(): continue
            if p.is_dir():
                movs = find_mov_files(p)
                for m in movs:
                    if self.add_file_to_queue(m):
                        added += 1
            elif p.is_file() and p.suffix.lower() == ".mov":
                if self.add_file_to_queue(p):
                    added += 1
        
        self.update_queue_ui()
        
    def add_file_to_queue(self, path):
        # Check for duplicates
        if any(f["path"] == path for f in self.file_queue):
            return False
            
        try:
            size = path.stat().st_size
        except Exception:
            size = 0
            
        self.file_queue.append({
            "path": path,
            "size": size,
            "status": "Ready"
        })
        return True

    def clear_queue(self):
        if self.is_converting: return
        self.file_queue.clear()
        self.update_queue_ui()
        
    def remove_item(self, path):
        if self.is_converting: return
        self.file_queue = [f for f in self.file_queue if f["path"] != path]
        self.update_queue_ui()

    def update_queue_ui(self):
        # Clear existing
        for widget in self.queue_items_frames.values():
            widget.destroy()
        self.queue_items_frames.clear()
        
        q_len = len(self.file_queue)
        total_size = sum(f["size"] for f in self.file_queue)
        
        if q_len > 0:
            self.queue_title.configure(text=f"Files to convert  —  {q_len} files ({format_size(total_size)})")
            self.start_btn.configure(text=f"Convert {q_len} File{'s' if q_len > 1 else ''}", state="normal")
            if not self.is_converting:
                self.status_lbl.configure(text="Ready", text_color=THEME["text_muted"])
        else:
            self.queue_title.configure(text="Files to convert")
            self.start_btn.configure(text="Select files to begin", state="disabled")
            if not self.is_converting:
                self.status_lbl.configure(text="Ready", text_color=THEME["text_muted"])
            
        for i, item in enumerate(self.file_queue):
            frame = ctk.CTkFrame(self.queue_scroll, fg_color="transparent")
            frame.grid(row=i, column=0, sticky="ew", pady=4)
            frame.grid_columnconfigure(1, weight=1)
            
            icon = ctk.CTkLabel(frame, text="🎬", font=self.font_body)
            icon.grid(row=0, column=0, padx=(5, 10))
            
            name = ctk.CTkLabel(frame, text=item["path"].name, font=self.font_body, text_color=THEME["text_primary"])
            name.grid(row=0, column=1, sticky="w")
            
            size_lbl = ctk.CTkLabel(frame, text=format_size(item["size"]), font=self.font_secondary, text_color=THEME["text_secondary"])
            size_lbl.grid(row=0, column=2, padx=15)
            
            status_color = THEME["text_secondary"]
            if item["status"] == "Converting...": status_color = THEME["accent"]
            elif item["status"] == "Completed": status_color = THEME["success"]
            elif item["status"] in ["Failed", "Skipped", "Cancelled"]: status_color = THEME["error"]
            
            status_lbl = ctk.CTkLabel(frame, text=item["status"], font=self.font_secondary, text_color=status_color, width=80, anchor="e")
            status_lbl.grid(row=0, column=3, padx=(0, 15))
            
            if not self.is_converting:
                rm_btn = ctk.CTkButton(frame, text="✕", font=self.font_secondary, width=28, height=28, fg_color="transparent", hover_color=THEME["surface_secondary"], text_color=THEME["text_muted"], command=lambda p=item["path"]: self.remove_item(p))
                rm_btn.grid(row=0, column=4, padx=(0, 5))
            
            self.queue_items_frames[item["path"]] = frame

    # Conversion flow
    def start_conversion(self):
        if not self.file_queue or self.is_converting: return
        
        # Don't convert completed files again
        pending_files = [f for f in self.file_queue if f["status"] not in ["Completed"]]
        if not pending_files:
            return
        
        self.is_converting = True
        self.start_btn.configure(text="Converting...", state="disabled")
        self.cancel_btn.grid()
        self.clear_btn.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.set(0)
        self.status_lbl.configure(text="Preparing conversion...", text_color=THEME["text_primary"])
        
        for item in pending_files:
            item["status"] = "Queued"
                
        self.update_queue_ui()
        
        paths = [f["path"] for f in pending_files]
        
        # Calculate base_dir as common path if possible, else just first file's parent
        try:
            parents = [str(p.parent) for p in paths]
            base_dir_str = os.path.commonpath(parents)
            base_dir = Path(base_dir_str)
        except ValueError:
            base_dir = paths[0].parent

        self.converter = VideoConverter(
            delete_original=self.delete_original.get(),
            output_dir=self.output_folder,
            overwrite=self.overwrite.get()
        )
        self.converter.cancel_event = threading.Event()
        
        threading.Thread(target=self.run_conversion_thread, args=(paths, base_dir), daemon=True).start()

    def cancel_conversion(self):
        if self.converter and self.converter.cancel_event:
            self.status_lbl.configure(text="Cancelling...", text_color=THEME["warning"])
            self.converter.cancel_event.set()
            self.cancel_btn.configure(state="disabled")

    def run_conversion_thread(self, paths, base_dir):
        try:
            result = self.converter.run(
                paths, 
                base_dir, 
                progress_callback=self.on_progress,
                file_status_callback=self.on_file_status
            )
            self.after(0, self.on_finished, result)
        except Exception as e:
            self.logger.exception("Thread error")
            self.after(0, self.on_error, str(e))
            
    def on_progress(self, result: ConversionResult):
        self.after(0, self.update_progress_ui, result)
        
    def update_progress_ui(self, result: ConversionResult):
        completed = result.converted + result.skipped + result.failed + result.cancelled
        total = result.total_found
        if total > 0:
            self.progress_bar.set(completed / total)
            self.status_lbl.configure(text=f"Converting {completed} of {total}...")
            
    def on_file_status(self, file_path, status):
        self.after(0, self.update_file_status_ui, file_path, status)
        
    def update_file_status_ui(self, file_path, status_str):
        ui_status = status_str.capitalize()
        if ui_status == "Converting":
            ui_status = "Converting..."
            
        for item in self.file_queue:
            if item["path"] == file_path:
                item["status"] = ui_status
                break
                
        if file_path in self.queue_items_frames:
            frame = self.queue_items_frames[file_path]
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("width") == 80:
                    widget.configure(text=ui_status)
                    if ui_status == "Converting...": widget.configure(text_color=THEME["accent"])
                    elif ui_status == "Completed": widget.configure(text_color=THEME["success"])
                    elif ui_status in ["Failed", "Skipped", "Cancelled"]: widget.configure(text_color=THEME["error"])
                    break
                    
    def on_finished(self, result: ConversionResult):
        self.is_converting = False
        self.cancel_btn.grid_remove()
        self.cancel_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        
        self.update_queue_ui()
        
        if result.cancelled > 0:
            self.status_lbl.configure(text="⚠ Conversion Cancelled", text_color=THEME["warning"])
            self.start_btn.configure(text="Convert Remaining", state="normal")
            self.progress_bar.grid_remove()
        elif result.failed > 0:
            self.status_lbl.configure(text=f"⚠ Conversion Finished ({result.failed} failed)", text_color=THEME["warning"])
            self.start_btn.configure(text="Retry Failed", state="normal")
            self.progress_bar.grid_remove()
        else:
            self.status_lbl.configure(text=f"✓ Conversion Complete ({result.converted} converted)", text_color=THEME["success"])
            self.start_btn.configure(text="Convert More", state="disabled")
            self.progress_bar.set(1)

    def on_error(self, err_msg):
        self.is_converting = False
        self.cancel_btn.grid_remove()
        self.clear_btn.configure(state="normal")
        self.status_lbl.configure(text="⚠ Internal Error", text_color=THEME["error"])
        messagebox.showerror("Error", f"Something went wrong:\n\n{err_msg}")
        self.update_queue_ui()
        self.progress_bar.grid_remove()

if __name__ == "__main__":
    app = Mov2Mp4App()
    app.mainloop()
