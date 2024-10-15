import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

file_types = {
    "Images": ['.jpeg', '.jpg', '.png', '.gif', '.bmp'],
    "Documents": ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx'],
    "Videos": ['.mp4', '.mov', '.avi', '.mkv'],
    "Musics": ['.mp3', '.wav', '.aac'],
    "Archives": ['.zip', '.tar', '.rar', '.gz'],
    "Scripts": ['.py', '.js', '.html', '.css']
}

def create_folder(destination_directory):
    for folder_name in file_types.keys():
        folder_path = os.path.join(destination_directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

def organize_files(source_directory):
    while True:
        files_moved = False
        file_list = os.listdir(source_directory)

        if not file_list:
            break

        for file_name in file_list:
            file_path = os.path.join(source_directory, file_name)

            if os.path.isdir(file_path):
                continue

            file_extension = os.path.splitext(file_name)[1].lower()

            moved = False
            for folder_name, extensions in file_types.items():
                if file_extension in map(str.lower, extensions):
                    destination = os.path.join(source_directory, folder_name, file_name)
                    shutil.move(file_path, destination)
                    moved = True
                    files_moved = True
                    break

            if not moved:
                other_folder = os.path.join(source_directory, "Others")
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                shutil.move(file_path, os.path.join(other_folder, file_name))
                files_moved = True

        if not files_moved:
            break

def organize():
    directory = path_entry.get()

    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Please provide a valid directory path.")
        return

    create_folder(directory)
    organize_files(directory)
    messagebox.showinfo("Success", "Files have been organized successfully!")

def browse_directory():
    folder_selected = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, folder_selected)

root = tk.Tk()
root.title("File Organizer")

label = tk.Label(root, text="Enter the folder path or select one:")
label.pack(pady=10)

path_entry = tk.Entry(root, width=50)
path_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.pack(pady=5)

organize_button = tk.Button(root, text="Organize Files", command=organize)
organize_button.pack(pady=20)

root.mainloop()
