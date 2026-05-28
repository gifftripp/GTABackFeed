import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from src.suppressor import AudioSuppressor

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AudioSuppressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("GTA BackFeed - Audio Suppressor")
        self.geometry("800x520")
        self.resizable(False, False)
        
        self.input_path = ""
        self.output_path = ""
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(self, text="🎤 GTA BackFeed - Audio Suppressor", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Input file
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(self.input_frame, text="Input Audio File:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        self.input_btn = ctk.CTkButton(self.input_frame, text="Browse", command=self.select_input, width=140)
        self.input_btn.pack(side="left", padx=20, pady=5)
        self.input_label = ctk.CTkLabel(self.input_frame, text="No file selected", text_color="gray")
        self.input_label.pack(side="left", padx=10)
        
        # Output
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(self.output_frame, text="Output File (auto if empty):", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        self.output_btn = ctk.CTkButton(self.output_frame, text="Browse", command=self.select_output, width=140)
        self.output_btn.pack(side="left", padx=20, pady=5)
        self.output_label = ctk.CTkLabel(self.output_frame, text="clean_output.wav", text_color="gray")
        self.output_label.pack(side="left", padx=10)
        
        # Strength
        self.strength_frame = ctk.CTkFrame(self)
        self.strength_frame.pack(fill="x", padx=40, pady=15)
        
        ctk.CTkLabel(self.strength_frame, text="Noise Reduction Strength (0.3 = light, 0.9 = strong)", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        self.strength_slider = ctk.CTkSlider(self.strength_frame, from_=0.3, to=0.95, number_of_steps=13)
        self.strength_slider.set(0.7)
        self.strength_slider.pack(fill="x", padx=20, pady=5)
        
        self.strength_value = ctk.CTkLabel(self.strength_frame, text="Medium (0.7)")
        self.strength_value.pack()
        
        # Bind slider update
        self.strength_slider.configure(command=self.update_strength_label)
        
        # Process Button
        self.process_btn = ctk.CTkButton(self, text="🚀 Process Audio", font=ctk.CTkFont(size=18, weight="bold"), height=50, command=self.start_processing)
        self.process_btn.pack(pady=30, padx=40, fill="x")
        
        # Progress
        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(fill="x", padx=40, pady=10)
        self.progress.set(0)
        
        # Status
        self.status = ctk.CTkLabel(self, text="Ready - Select a file to begin", text_color="lightgreen", font=ctk.CTkFont(size=14))
        self.status.pack(pady=10)
        
    def update_strength_label(self, value):
        self.strength_value.configure(text=f"{float(value):.2f}")
        
    def select_input(self):
        self.input_path = filedialog.askopenfilename(
            title="Select noisy audio file",
            filetypes=[("Audio files", "*.wav *.mp3 *.m4a *.ogg *.flac")]
        )
        if self.input_path:
            self.input_label.configure(text=os.path.basename(self.input_path), text_color="white")
            
    def select_output(self):
        self.output_path = filedialog.asksaveasfilename(
            title="Save clean audio as",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if self.output_path:
            self.output_label.configure(text=os.path.basename(self.output_path), text_color="white")
    
    def start_processing(self):
        if not self.input_path:
            self.status.configure(text="❌ Please select an input file first!", text_color="red")
            return
            
        self.process_btn.configure(state="disabled")
        self.status.configure(text="⏳ Processing noise suppression...", text_color="orange")
        self.progress.set(0.1)
        
        # Run in thread to keep GUI responsive
        thread = threading.Thread(target=self.process_audio, daemon=True)
        thread.start()
        
    def process_audio(self):
        try:
            suppressor = AudioSuppressor()
            strength = self.strength_slider.get()
            
            if not self.output_path:
                base_name = os.path.splitext(os.path.basename(self.input_path))[0]
                self.output_path = os.path.join(os.path.dirname(self.input_path), f"{base_name}_clean.wav")
            
            self.progress.set(0.5)
            suppressor.reduce_noise(self.input_path, self.output_path, reduction_strength=strength)
            
            self.progress.set(1.0)
            # Fixed f-string
            clean_name = os.path.basename(self.output_path)
            self.status.configure(text=f"✅ Success! Clean file saved:\n{clean_name}", text_color="lightgreen")
            
        except Exception as e:
            self.status.configure(text=f"❌ Error: {str(e)}", text_color="red")
        finally:
            self.process_btn.configure(state="normal")
            # Reset output for next run
            self.output_path = ""

if __name__ == "__main__":
    app = AudioSuppressorApp()
    app.mainloop()
