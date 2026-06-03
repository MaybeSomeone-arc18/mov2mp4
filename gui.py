import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path

# Import our backend logic
from utils import check_ffmpeg_installed, find_mov_files
from converter import VideoConverter
from logger import setup_logger

class Mov2Mp4App:
    def __init__(self, root):
        self.root = root
        self.root.title("MOV2MP4 Converter")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # Set up a logger for the GUI run
        log_dir = Path.cwd() / "logs"
        self.logger = setup_logger(log_dir, verbose=False)
        
        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.delete_original = tk.BooleanVar(value=False)
        self.overwrite = tk.BooleanVar(value=False)
        
        self.setup_ui()
        self.check_prerequisites()

    def check_prerequisites(self):
        if not check_ffmpeg_installed():
            messagebox.showerror(
                "FFmpeg Missing", 
                "FFmpeg is not installed or not in the system PATH.\n\nPlease install FFmpeg to use this application."
            )
            self.convert_btn.config(state=tk.DISABLED)

    def setup_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Batch Convert MOV to MP4", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input Folder
        ttk.Label(main_frame, text="Input Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_folder, width=40).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input).grid(row=1, column=2, pady=5)
        
        # Output Folder
        ttk.Label(main_frame, text="Output Folder (Optional):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_folder, width=40).grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=2, column=2, pady=5)
        
        # Options Frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=tk.EW, pady=20)
        
        ttk.Checkbutton(options_frame, text="Delete original .mov files after conversion", variable=self.delete_original).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Overwrite existing .mp4 files", variable=self.overwrite).pack(anchor=tk.W, pady=2)
        
        # Convert Button
        self.convert_btn = ttk.Button(main_frame, text="Start Conversion", command=self.start_conversion)
        self.convert_btn.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Progress and Status
        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Helvetica", 10, "italic"))
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)

    def browse_input(self):
        folder = filedialog.askdirectory(title="Select Folder containing .mov files")
        if folder:
            self.input_folder.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder (Optional)")
        if folder:
            self.output_folder.set(folder)

    def start_conversion(self):
        if not self.input_folder.get():
            messagebox.showwarning("Input Required", "Please select an input folder.")
            return
            
        in_path = Path(self.input_folder.get())
        if not in_path.exists() or not in_path.is_dir():
            messagebox.showerror("Invalid Path", "The selected input folder does not exist.")
            return

        out_path = Path(self.output_folder.get()) if self.output_folder.get() else None
        
        self.convert_btn.config(state=tk.DISABLED)
        self.status_var.set("Scanning for .mov files...")
        
        # Run conversion in a separate thread so GUI doesn't freeze
        threading.Thread(target=self.run_conversion_thread, args=(in_path, out_path), daemon=True).start()

    def run_conversion_thread(self, in_path, out_path):
        try:
            mov_files = find_mov_files(in_path)
            
            if not mov_files:
                self.root.after(0, self.conversion_finished, "No .mov files found in the selected folder.", "info")
                return
                
            self.root.after(0, lambda: self.status_var.set(f"Converting {len(mov_files)} files. Please wait..."))
            
            converter = VideoConverter(
                delete_original=self.delete_original.get(),
                output_dir=out_path,
                overwrite=self.overwrite.get()
            )
            
            result = converter.run(mov_files, in_path)
            
            msg = (
                f"Conversion Complete!\n\n"
                f"Total Found: {result.total_found}\n"
                f"Converted: {result.converted}\n"
                f"Skipped: {result.skipped}\n"
                f"Failed: {result.failed}"
            )
            self.root.after(0, self.conversion_finished, msg, "success")
            
        except Exception as e:
            self.logger.exception("Error during conversion thread")
            self.root.after(0, self.conversion_finished, f"An error occurred:\n{str(e)}", "error")

    def conversion_finished(self, message, msg_type):
        self.status_var.set("Ready.")
        self.convert_btn.config(state=tk.NORMAL)
        
        if msg_type == "error":
            messagebox.showerror("Error", message)
        elif msg_type == "info":
            messagebox.showinfo("Information", message)
        else:
            messagebox.showinfo("Success", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = Mov2Mp4App(root)
    root.mainloop()
