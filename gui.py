import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path

# Import our backend logic
from utils import check_ffmpeg_installed, find_mov_files
from converter import VideoConverter
from logger import setup_logger

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Mov2Mp4App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("MOV2MP4 Converter")
        self.geometry("650x550")
        self.resizable(False, False)
        
        # Set up a logger for the GUI run
        log_dir = Path.cwd() / "logs"
        self.logger = setup_logger(log_dir, verbose=False)
        
        # Variables
        self.input_folder = ctk.StringVar()
        self.output_folder = ctk.StringVar()
        self.delete_original = ctk.BooleanVar(value=False)
        self.overwrite = ctk.BooleanVar(value=False)
        
        self.setup_ui()
        self.check_prerequisites()
        self.setup_bindings()
        
        # Force window to the front on macOS
        self.lift()
        self.attributes('-topmost', True)
        self.after(50, lambda: self.attributes('-topmost', False))

    def setup_bindings(self):
        # Keyboard shortcuts
        self.bind('<Return>', lambda event: self.start_conversion())
        self.bind('<Escape>', lambda event: self.quit())
        self.bind('<Command-q>', lambda event: self.quit())
        self.bind('<Control-q>', lambda event: self.quit())

    def check_prerequisites(self):
        if not check_ffmpeg_installed():
            messagebox.showerror(
                "FFmpeg Missing", 
                "FFmpeg is not installed or not in the system PATH.\n\nPlease install FFmpeg to use this application."
            )
            self.convert_btn.configure(state="disabled")

    def setup_ui(self):
        # Main Frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Batch Convert MOV to MP4", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Paths Card
        paths_frame = ctk.CTkFrame(main_frame)
        paths_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        paths_frame.grid_columnconfigure(1, weight=1)
        
        # Input Folder
        input_label = ctk.CTkLabel(paths_frame, text="Input Folder:", font=ctk.CTkFont(weight="bold"))
        input_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.input_entry = ctk.CTkEntry(paths_frame, textvariable=self.input_folder, placeholder_text="Select folder with .mov files...")
        self.input_entry.grid(row=0, column=1, padx=(0, 15), pady=(15, 5), sticky="ew")
        
        input_btn = ctk.CTkButton(paths_frame, text="Browse", width=80, command=self.browse_input)
        input_btn.grid(row=0, column=2, padx=(0, 15), pady=(15, 5))
        
        # Output Folder
        output_label = ctk.CTkLabel(paths_frame, text="Output Folder:", font=ctk.CTkFont(weight="bold"))
        output_label.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")
        
        self.output_entry = ctk.CTkEntry(paths_frame, textvariable=self.output_folder, placeholder_text="(Optional) Save to specific folder...")
        self.output_entry.grid(row=1, column=1, padx=(0, 15), pady=(5, 15), sticky="ew")
        
        output_btn = ctk.CTkButton(paths_frame, text="Browse", width=80, command=self.browse_output)
        output_btn.grid(row=1, column=2, padx=(0, 15), pady=(5, 15))
        
        # Options Card
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        options_frame.grid_columnconfigure(0, weight=1)
        
        options_label = ctk.CTkLabel(options_frame, text="Conversion Options", font=ctk.CTkFont(weight="bold"))
        options_label.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")
        
        del_chk = ctk.CTkCheckBox(options_frame, text="Delete original .mov files after conversion", variable=self.delete_original)
        del_chk.grid(row=1, column=0, padx=15, pady=(5, 5), sticky="w")
        
        ovr_chk = ctk.CTkCheckBox(options_frame, text="Overwrite existing .mp4 files", variable=self.overwrite)
        ovr_chk.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="w")
        
        # Convert Button
        self.convert_btn = ctk.CTkButton(main_frame, text="Start Conversion", font=ctk.CTkFont(size=16, weight="bold"), height=40, command=self.start_conversion)
        self.convert_btn.grid(row=3, column=0, pady=(10, 15))
        
        # Progress Bar (Hidden initially)
        self.progress_bar = ctk.CTkProgressBar(main_frame, mode="determinate")
        self.progress_bar.set(0)
        
        # Status Label
        self.status_var = ctk.StringVar(value="Ready.")
        self.status_label = ctk.CTkLabel(main_frame, textvariable=self.status_var, font=ctk.CTkFont(slant="italic"), text_color="gray")
        self.status_label.grid(row=5, column=0, pady=(0, 10))

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
        
        self.convert_btn.configure(state="disabled")
        self.status_var.set("Scanning for .mov files...")
        self.progress_bar.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Run conversion in a separate thread so GUI doesn't freeze
        threading.Thread(target=self.run_conversion_thread, args=(in_path, out_path), daemon=True).start()

    def update_progress(self, current_result):
        # Calculate completion percentage
        completed = current_result.converted + current_result.skipped + current_result.failed
        total = current_result.total_found
        
        if total > 0:
            progress = completed / total
            self.progress_bar.set(progress)
            self.status_var.set(f"Converting... ({completed}/{total})")

    def run_conversion_thread(self, in_path, out_path):
        try:
            mov_files = find_mov_files(in_path)
            
            if not mov_files:
                self.after(0, self.conversion_finished, "No .mov files found in the selected folder.", "info")
                return
                
            self.after(0, lambda: self.status_var.set(f"Found {len(mov_files)} files. Starting conversion..."))
            
            converter = VideoConverter(
                delete_original=self.delete_original.get(),
                output_dir=out_path,
                overwrite=self.overwrite.get()
            )
            
            # Helper to wrap the callback so it executes on the main thread safely
            def progress_cb(res):
                self.after(0, self.update_progress, res)
                
            result = converter.run(mov_files, in_path, progress_callback=progress_cb)
            
            msg = (
                f"Conversion Complete!\n\n"
                f"Total Found: {result.total_found}\n"
                f"Converted: {result.converted}\n"
                f"Skipped: {result.skipped}\n"
                f"Failed: {result.failed}"
            )
            self.after(0, self.conversion_finished, msg, "success")
            
        except Exception as e:
            self.logger.exception("Error during conversion thread")
            self.after(0, self.conversion_finished, f"An error occurred:\n{str(e)}", "error")

    def conversion_finished(self, message, msg_type):
        self.status_var.set("Ready.")
        self.convert_btn.configure(state="normal")
        self.progress_bar.grid_remove()  # Hide progress bar when done
        
        if msg_type == "error":
            messagebox.showerror("Error", message)
            self.status_label.configure(text_color="red")
        elif msg_type == "info":
            messagebox.showinfo("Information", message)
            self.status_label.configure(text_color="gray")
        else:
            messagebox.showinfo("Success", message)
            self.status_label.configure(text_color="green")

if __name__ == "__main__":
    app = Mov2Mp4App()
    app.mainloop()
