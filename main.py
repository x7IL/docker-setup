import os

def get_image_names():
    image_names = []
    print("Enter image names (enter a blank line to finish):")
    while True:
        name = input().strip().lower()
        if not name:
            break
        image_names.append(name)
    return image_names

def create_directories_and_files(image_names):
    # Création du dossier docker et de ses sous-dossiers et fichiers
    if not os.path.exists('docker'):
        os.mkdir('docker')
    for name in image_names:
        os.makedirs(f'docker/{name}', exist_ok=True)
        with open(f'docker/{name}/Dockerfile', 'w') as f:
            pass

    # Création du dossier config et de ses sous-dossiers et fichiers
    if not os.path.exists('config'):
        os.mkdir('config')
    for name in image_names:
        os.makedirs(f'config/{name}', exist_ok=True)
        with open(f'config/{name}/.env', 'w') as f, open(f'config/{name}/.env.example', 'w') as f_example:
            pass

    # Création du dossier scripts et de ses fichiers
    if not os.path.exists('scripts'):
        os.mkdir('scripts')
    with open('scripts/build.sh', 'w') as f_build, open('scripts/run.sh', 'w') as f_run:
        f_build.write("#!/bin/bash\n# Add your build commands here\n")
        f_run.write("#!/bin/bash\n# Add your run commands here\n")

def main():
    image_names = get_image_names()
    create_directories_and_files(image_names)
    print("Directories and files have been successfully created.")

if __name__ == "__main__":
    main()
