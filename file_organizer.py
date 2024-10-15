import os
import shutil

source_directory = ''  # path to where you want to sort your files

file_types = {
    "Images": ['.jpeg', '.jpg', '.png', '.gif', '.bmp'],
    "Documents": ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx'],
    "Videos": ['.mp4', '.mov', '.avi', '.mkv'],
    "Musics": ['.mp3', '.wav', '.aac'],
    "Archives": ['.zip', '.tar', '.rar', '.gz'],
    "Scripts": ['.py', '.js', '.html', '.css']
}

# Create new folder for the file types if they don't exist
def create_folder(destination_directory):
    for folder_name in file_types.keys():
        folder_path = os.path.join(destination_directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

# Organize files by moving them into the appropriate folders
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
                    print(f'Moved: {file_name} -> {folder_name}')
                    moved = True
                    files_moved = True
                    break

            if not moved:
                other_folder = os.path.join(source_directory, "Others")
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                shutil.move(file_path, os.path.join(other_folder, file_name))
                print(f'Moved: {file_name} -> Others')
                files_moved = True

        # If no files were moved, break the loop (prevents infinite looping)
        if not files_moved:
            break

if __name__ == '__main__':
    create_folder(source_directory)
    organize_files(source_directory)
    print("File organization complete!")
