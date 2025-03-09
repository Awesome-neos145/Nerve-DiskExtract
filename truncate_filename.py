import os

def rename_files(directory):
    for filename in os.listdir(directory):
        if 'þ' in filename:
            new_filename = filename.replace('þ', '')
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

if __name__ == "__main__":
    directory = '.'  # Change this to the directory you want to process
    rename_files(directory)