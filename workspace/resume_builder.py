import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
import threading

# Create a single global root which will be used for all windows.
main_root = tk.Tk()
main_root.withdraw()  # Hide the main window; we'll use Toplevels.

# ------------------------------
# Global Variables
# ------------------------------
resume_generated = False
output_format = None      # "HTML", "Word", or "PDF"
selected_template = None  # Only used if building from scratch with HTML
base_resume_file = None   # Holds the file path of the current resume
TEMPLATE_DIR = "templates"

def get_templates():
    """Return a list of .html files in the TEMPLATE_DIR."""
    if os.path.exists(TEMPLATE_DIR):
        return [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.html')]
    else:
        return []

# Retrieve available templates.
templates = get_templates()
if not templates:
    templates = ["No templates found"]
current_index = 0

# ------------------------------
# Stage 1: Output Format Selection
# ------------------------------
def open_output_format_gui():
    win = tk.Toplevel(main_root)
    win.title("Eric - Resume Assistant")
    header = tk.Label(win,
                      text="Hello, I'm Eric, your Resume Assistant!\nPlease choose your desired output format:",
                      font=("Helvetica", 20, "bold"), pady=20)
    header.pack()
    global output_format
    output_format_var = tk.StringVar(value="HTML")
    options = [("HTML (Recommended)", "HTML"),
               ("docx File", "Word"),  # changed label to 'docx File'
               ("PDF", "PDF")]
    for text, mode in options:
        tk.Radiobutton(win, text=text, variable=output_format_var, value=mode,
                       font=("Helvetica", 14)).pack(anchor="w", padx=20)
    def submit_format():
        global output_format
        output_format = output_format_var.get()
        win.destroy()
        if output_format == "HTML":
            open_template_selection_gui()
        else:
            open_user_info_gui()
    submit_btn = tk.Button(win, text="Submit Format", font=("Helvetica", 14, "bold"),
                           command=submit_format, padx=10, pady=5)
    submit_btn.pack(pady=20)
    
# ------------------------------
# Stage 2: Template Selection (HTML Only)
# ------------------------------
def open_template_selection_gui():
    global selected_template, current_index
    current_index = 0  # reset index
    win = tk.Toplevel(main_root)
    win.title("Eric - Choose Your Template")
    header = tk.Label(win,
                     text="HTML is our recommended format!\nPlease choose a template for your resume.",
                     font=("Helvetica", 20, "bold"), pady=20)
    header.pack()
    frame = tk.Frame(win)
    frame.pack(pady=20)
    def update_label():
        lbl.config(text=templates[current_index])
    def next_template():
        global current_index
        current_index = (current_index + 1) % len(templates)
        update_label()
    def prev_template():
        global current_index
        current_index = (current_index - 1) % len(templates)
        update_label()
    btn_prev = tk.Button(frame, text="<< Previous", font=("Helvetica", 12), command=prev_template)
    btn_prev.grid(row=0, column=0, padx=10)
    lbl = tk.Label(frame, text="", font=("Helvetica", 16))
    lbl.grid(row=0, column=1, padx=10)
    btn_next = tk.Button(frame, text="Next >>", font=("Helvetica", 12), command=next_template)
    btn_next.grid(row=0, column=2, padx=10)
    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)
    def preview_template():
        if templates and templates[0] != "No templates found":
            filepath = os.path.join(TEMPLATE_DIR, templates[current_index])
            webbrowser.open_new_tab(filepath)
        else:
            messagebox.showinfo("Info", "No templates available to preview.")
    def select_template():
        global selected_template
        if templates and templates[0] != "No templates found":
            selected_template = templates[current_index]
            webbrowser.open_new_tab(os.path.join(TEMPLATE_DIR, selected_template))
            win.destroy()
            open_user_info_gui()
        else:
            messagebox.showinfo("Info", "No templates available.")
    btn_preview = tk.Button(button_frame, text="Preview Template", font=("Helvetica", 12), command=preview_template)
    btn_preview.grid(row=0, column=0, padx=10)
    btn_select = tk.Button(button_frame, text="Select Template", font=("Helvetica", 12, "bold"),
                           command=select_template)
    btn_select.grid(row=0, column=1, padx=10)
    update_label()
    
# ------------------------------
# Stage 3: User Information Input
# ------------------------------
def open_user_info_gui():
    win = tk.Toplevel(main_root)
    win.title("Eric - Enter Your Information")
    header = tk.Label(win,
                      text="Please enter your details below:",
                      font=("Helvetica", 16, "bold"), pady=10)
    header.grid(row=0, column=0, columnspan=2)
    tk.Label(win, text="Full Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_name = tk.Entry(win, width=50)
    entry_name.grid(row=1, column=1, pady=5)
    tk.Label(win, text="Email:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_email = tk.Entry(win, width=50)
    entry_email.grid(row=2, column=1, pady=5)
    tk.Label(win, text="Phone:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_phone = tk.Entry(win, width=50)
    entry_phone.grid(row=3, column=1, pady=5)
    tk.Label(win, text="Address:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_address = tk.Entry(win, width=50)
    entry_address.grid(row=4, column=1, pady=5)
    tk.Label(win, text="Professional Summary:").grid(row=5, column=0, sticky="ne", padx=5, pady=5)
    text_summary = tk.Text(win, width=38, height=5)
    text_summary.grid(row=5, column=1, pady=5)
    tk.Label(win, text="Skills (optional):").grid(row=6, column=0, sticky="e", padx=5, pady=5)
    entry_skills = tk.Entry(win, width=50)
    entry_skills.grid(row=6, column=1, pady=5)
    tk.Label(win, text="Languages (optional):").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    entry_languages = tk.Entry(win, width=50)
    entry_languages.grid(row=7, column=1, pady=5)
    def submit_info():
        info = {
            "Full Name": entry_name.get(),
            "Email": entry_email.get(),
            "Phone": entry_phone.get(),
            "Address": entry_address.get(),
            "Professional Summary": text_summary.get("1.0", tk.END).strip(),
            "Skills": entry_skills.get(),
            "Languages": entry_languages.get()
        }
        with open("user_info.txt", "w") as f:
            for key, value in info.items():
                f.write(f"{key}: {value}\n")
        win.destroy()
        # Create a "Generating Resume" window.
        gen_win = tk.Toplevel(main_root)
        gen_win.title("Generating Resume")
        tk.Label(gen_win, text="Generating resume, please wait...", 
                 font=("Helvetica", 16, "bold"), padx=20, pady=20).pack()
        # Start resume generation in a background thread and pass gen_win as the UI widget.
        threading.Thread(
            target=generate_resume,
            args=(info, selected_template, lambda: finish_generation(gen_win), gen_win),
            daemon=True
        ).start()
    submit_btn = tk.Button(win, text="Submit", font=("Helvetica", 12, "bold"),
                           command=submit_info, padx=10, pady=5)
    submit_btn.grid(row=8, column=1, pady=15)
    
# ------------------------------
# Stage 4: Resume Generation via AI (Background Thread)
# ------------------------------
def generate_resume(user_info, template_filename, callback, ui_widget):
    """
    Construct an AI prompt using the user info and (if HTML) the chosen template.
    Instruct the AI to return ONLY the resume content (without markdown formatting,
    code fences, or extra commentary). When finished, schedule the callback using ui_widget.
    """
    global resume_generated, base_resume_file
    try:
        with open("user_info.txt", "r") as f:
            info_content = f.read()
    except Exception as e:
        print("Error reading user info:", e)
        return
    if output_format == "HTML":
        template_path = os.path.join(TEMPLATE_DIR, template_filename)
        try:
            with open(template_path, "r") as f:
                template_content = f.read()
        except Exception as e:
            print("Error reading template:", e)
            return
        prompt = f"""Using the following HTML resume template:

{template_content}

And the following user information:
{info_content}

Generate a complete resume in HTML format.
Respond with ONLY the HTML content without any markdown formatting, code fences, or extra commentary.
"""
        output_file = "generated_resume.html"
    elif output_format == "Word":
        prompt = f"""Using the following user information:
{info_content}

Generate a professionally worded resume in Microsoft Word format.
Respond with ONLY the resume content without any markdown formatting, code fences, or extra commentary.
"""
        output_file = "generated_resume.docx"
    elif output_format == "PDF":
        prompt = f"""Using the following user information:
{info_content}

Generate a professionally worded resume in plain text format suitable for conversion to PDF.
Respond with ONLY the resume content without any markdown formatting, code fences, or extra commentary.
"""
        # We will generate a proper PDF later using FPDF.
    else:
        prompt = f"""Using the following user information:
{info_content}

Generate a complete resume in HTML format.
Respond with ONLY the HTML content without any markdown formatting, code fences, or extra commentary.
"""
        output_file = "generated_resume.html"
    try:
        from openai import OpenAI
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        resume_content = completion.choices[0].message.content
    except Exception as e:
        print("Error calling AI API:", e)
        resume_content = "<html><body><h1>Error generating resume</h1></body></html>"
    
    if output_format == "PDF":
        try:
            from fpdf import FPDF
        except ImportError:
            print("Please install fpdf library to generate PDF files.")
            return
        pdf_file = "generated_resume.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in resume_content.split('\n'):
            pdf.multi_cell(0, 10, txt=line)
        pdf.output(pdf_file)
        output_file = pdf_file
    else:
        with open(output_file, "w") as f:
            f.write(resume_content)
    
    webbrowser.open_new_tab(output_file)
    print(f"Resume saved to {output_file}")
    base_resume_file = output_file
    resume_generated = True
    ui_widget.after(0, callback)

def finish_generation(gen_win):
    gen_win.destroy()
    open_feedback_loop()

# ------------------------------
# Stage 5: Feedback Loop
# ------------------------------
def open_feedback_loop():
    fb_win = tk.Toplevel(main_root)
    fb_win.title("Eric - Resume Feedback")
    label = tk.Label(fb_win,
                     text="Enter feedback to modify your resume (leave blank if you're happy):",
                     font=("Helvetica", 14), pady=10)
    label.pack(pady=10)
    feedback_text = tk.Text(fb_win, width=60, height=10)
    feedback_text.pack(pady=10)
    status_label = tk.Label(fb_win, text="", font=("Helvetica", 12))
    status_label.pack(pady=5)
    button_frame = tk.Frame(fb_win)
    button_frame.pack(pady=10)
    def finish_update():
        popup = tk.Toplevel(fb_win)
        popup.title("Update Complete")
        tk.Label(popup, text="Your resume has been updated!", font=("Helvetica", 16, "bold"), padx=20, pady=20).pack()
        popup.attributes('-topmost', True)
        popup.after(3000, lambda: popup.destroy())
        feedback_text.delete("1.0", tk.END)
        submit_btn.config(state="normal")
        content_btn.config(state="normal")
        status_label.config(text="")
    def submit_feedback():
        fb = feedback_text.get("1.0", tk.END).strip()
        if fb:
            submit_btn.config(state="disabled")
            content_btn.config(state="disabled")
            status_label.config(text="Updating resume, please wait...")
            threading.Thread(target=lambda: update_resume_with_feedback(fb, finish_update), daemon=True).start()
        else:
            messagebox.showinfo("All Set", "Your resume looks great! Good luck!")
            fb_win.destroy()
    submit_btn = tk.Button(button_frame, text="Submit Changes", font=("Helvetica", 12, "bold"),
                           command=submit_feedback, padx=10, pady=5)
    submit_btn.pack(side="left", padx=10)
    content_btn = tk.Button(button_frame, text="I'm Content", font=("Helvetica", 12, "bold"),
                            command=lambda: (messagebox.showinfo("All Set", "Your resume looks great! Good luck!"),
                                             fb_win.destroy()))
    content_btn.pack(side="right", padx=10)
    
# ------------------------------
# Update Resume with Feedback
# ------------------------------
def update_resume_with_feedback(feedback, callback):
    global base_resume_file
    file_name = base_resume_file
    try:
        with open(file_name, "r") as f:
            current_resume = f.read()
    except Exception as e:
        print("Error reading resume:", e)
        current_resume = ""
    prompt = f"""Using the current resume as a base:

{current_resume}

Incorporate the following feedback to enhance the resume professionally:
{feedback}

Generate a professionally worded and enhanced resume.
Respond with ONLY the updated resume content without any markdown formatting, code fences, or extra commentary.
"""
    try:
        from openai import OpenAI
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        updated_resume = completion.choices[0].message.content
    except Exception as e:
        print("Error during feedback update:", e)
        updated_resume = current_resume
    with open(file_name, "w") as f:
        f.write(updated_resume)
    webbrowser.open_new_tab(file_name)
    print(f"Updated resume saved to {file_name}")
    main_root.after(0, lambda: callback())

# ------------------------------
# Start the Application Flow
# ------------------------------
if __name__ == "__main__":
    open_output_format_gui()
    main_root.mainloop()
