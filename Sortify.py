import os
import shutil
import threading
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

FILE_TYPES = {
    "Images": ['.jpeg', '.jpg', '.png', '.gif', '.bmp'],
    "Documents": ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx'],
    "Videos": ['.mp4', '.mov', '.avi', '.mkv'],
    "Music": ['.mp3', '.wav', '.aac'],
    "Archives": ['.zip', '.tar', '.rar', '.gz'],
    "Scripts": ['.py', '.js', '.html', '.css']
}

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("700x450")
        self.root.resizable(False, False)
        self.create_widgets()

    def set_background(self, image_path):
        try:
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((700, 450), Image.ANTIALIAS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tb.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Failed to load background image: {e}")

    def create_widgets(self):
        main_frame = tb.Frame(self.root, padding=20, bootstyle="dark")
        main_frame.pack(fill=tb.BOTH, expand=True)

        label = tb.Label(main_frame, text="Select the folder to organize:", font=("Helvetica", 14, "bold"), bootstyle="inverse-primary")
        label.pack(pady=(0, 10))

        entry_frame = tb.Frame(main_frame, bootstyle="dark")
        entry_frame.pack(fill=tb.X, pady=(0, 10))

        self.path_var = tb.StringVar()
        self.path_entry = tb.Entry(entry_frame, textvariable=self.path_var, width=50, bootstyle="dark")
        self.path_entry.pack(side=tb.LEFT, fill=tb.X, expand=True, padx=(0, 5))

        browse_button = tb.Button(entry_frame, text="Browse", command=self.browse_directory, bootstyle="info-outline")
        browse_button.pack(side=tb.LEFT)

        organize_button = tb.Button(main_frame, text="Organize Files", command=self.start_organizing, bootstyle="success-outline")
        organize_button.pack(pady=10)

        self.progress = tb.Progressbar(main_frame, bootstyle="success-striped", length=500, mode='determinate')
        self.progress.pack(pady=10)
        self.progress['value'] = 0

        self.status_label = tb.Label(main_frame, text="", font=("Helvetica", 10), bootstyle="inverse-dark")
        self.status_label.pack(pady=(10, 0))

        footer_frame = tb.Frame(self.root, padding=10, bootstyle="dark")
        footer_frame.pack(side=tb.BOTTOM, fill=tb.X)

        credit_label = tb.Label(
            footer_frame,
            text="Made by William Mauricio",
            font=("Helvetica", 10, "italic"),
            bootstyle="secondary"
        )
        credit_label.pack()

    def browse_directory(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_var.set(folder_selected)

    def start_organizing(self):
        directory = self.path_var.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Please provide a valid directory path.")
            return

        self.toggle_widgets(state='disabled')
        self.status_label.config(text="Organizing files...")

        thread = threading.Thread(target=self.organize_files, args=(directory,))
        thread.start()

    def organize_files(self, directory):
        try:
            self.create_folders(directory)
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            total_files = len(files)
            self.progress['maximum'] = total_files
            moved_files = 0

            for file_name in files:
                file_path = os.path.join(directory, file_name)
                file_extension = os.path.splitext(file_name)[1].lower()
                moved = False

                for folder, extensions in FILE_TYPES.items():
                    if file_extension in [ext.lower() for ext in extensions]:
                        destination = os.path.join(directory, folder, file_name)
                        self.move_file(file_path, destination)
                        moved = True
                        break

                if not moved:
                    other_folder = os.path.join(directory, "Others")
                    destination = os.path.join(other_folder, file_name)
                    self.move_file(file_path, destination)

                moved_files += 1
                self.update_progress(moved_files)

            self.status_label.config(text="Files have been organized successfully!")
            messagebox.showinfo("Success", "Files have been organized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_label.config(text="An error occurred.")
        finally:
            self.toggle_widgets(state='normal')
            self.progress['value'] = 0

    def create_folders(self, destination_directory):
        for folder_name in FILE_TYPES.keys():
            folder_path = os.path.join(destination_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)
        os.makedirs(os.path.join(destination_directory, "Others"), exist_ok=True)

    def move_file(self, src, dest):
        try:
            if os.path.exists(dest):
                base, extension = os.path.splitext(dest)
                counter = 1
                new_dest = f"{base}({counter}){extension}"
                while os.path.exists(new_dest):
                    counter += 1
                    new_dest = f"{base}({counter}){extension}"
                dest = new_dest
            shutil.move(src, dest)
        except Exception as e:
            error_message = f"Failed to move {src} to {dest}: {e}"
            print(error_message)
            self.log_error(error_message)

    def log_error(self, message):
        with open("error_log.txt", "a") as log_file:
            log_file.write(message + "\n")

    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()

    def toggle_widgets(self, state):
        for child in self.root.winfo_children():
            if isinstance(child, tb.Frame):
                for grandchild in child.winfo_children():
                    try:
                        grandchild.configure(state=state)
                    except:
                        pass

def main():
    root = tb.Window(themename="superhero") 
    app = FileOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
