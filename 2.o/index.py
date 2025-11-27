import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class ATSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ATS Resume Enhancer")
        self.geometry("900x550")

        header = ctk.CTkLabel(self, text="ATS Resume Enhancer", font=("Arial Bold", 24))
        header.pack(pady=10)

        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Left frame: Resume upload
        left_frame = ctk.CTkFrame(main_frame, border_color="#007f5f", border_width=1)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(left_frame, text="Upload Resume", font=("Arial Bold", 16)).pack(pady=(15, 5))
        ctk.CTkLabel(left_frame, text="PDF only (Max 5MB)", font=("Arial", 12)).pack(pady=(0, 10))
        self.resume_path = ctk.StringVar()
        ctk.CTkEntry(left_frame, textvariable=self.resume_path, width=300).pack(pady=10)
        ctk.CTkButton(left_frame, text="Select PDF", command=self.select_file).pack(pady=10)

        # Right frame: Job description
        right_frame = ctk.CTkFrame(main_frame, border_color="#007f5f", border_width=1)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(right_frame, text="Job Description", font=("Arial Bold", 16)).pack(pady=(15, 5))
        self.jd_text = ctk.CTkTextbox(right_frame, height=300, width=350)
        self.jd_text.pack(padx=10, pady=10, fill="both", expand=True)

        # Button to show ResultPage
        ctk.CTkButton(self, text="Show ATS Score", height=40, command=self.open_result_page).pack(pady=15)
        ctk.CTkLabel(self, text="Score is read directly from score.txt", font=("Arial", 12)).pack(pady=(0, 10))

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select Resume PDF", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            if not file_path.lower().endswith(".pdf"):
                messagebox.showerror("Invalid File", "Please select a PDF file.")
            else:
                self.resume_path.set(file_path)

    def open_result_page(self):
        score_file = os.path.join(os.getcwd(), "score.txt")
        if not os.path.exists(score_file):
            messagebox.showerror("File Not Found", "score.txt not found in current directory.")
            return
        ResultPage(self, score_file)


class ResultPage(ctk.CTkToplevel):
    def __init__(self, parent, score_file):
        super().__init__(parent)
        self.title("ATS Score Result")
        self.geometry("800x500")

        # Read the score directly from score.txt
        try:
            with open(score_file, "r", encoding="utf-8") as sf:
                overall_match = float(sf.read().strip())
        except:
            overall_match = 0.0

        # ===== Score Bar =====
        ctk.CTkLabel(self, text="ATS Match Score", font=("Arial Bold", 18)).pack(pady=10)
        self.progressbar = ctk.CTkProgressBar(self, width=500)
        self.progressbar.pack(pady=10)
        self.progressbar.set(overall_match / 100)

        ctk.CTkLabel(self, text=f"{overall_match}%", font=("Arial", 16)).pack()

        # ===== PDF Output Area =====
        output_frame = ctk.CTkFrame(self, border_color="#007f5f", border_width=1)
        output_frame.pack(padx=20, pady=20, fill="both", expand=True)
        ctk.CTkLabel(output_frame, text="PDF Output / Analysis", font=("Arial Bold", 14)).pack(pady=10)
        self.output_text = ctk.CTkTextbox(output_frame)
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_text.insert("1.0", f"Your resume matches {overall_match}% with the job description.\n\n"
                                       "Suggestions:\n- Highlight relevant experience.\n- Add missing skills.")


if __name__ == "__main__":
    app = ATSApp()
    app.mainloop()
