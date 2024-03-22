import os

def get_project_name():
    print("=== Project Name Input ===")
    # Ask the user for the project name; this will be used to create a directory under 'output'.
    project_name = input("Please enter the project name: ").strip().replace(' ', '_').lower()
    return project_name

def get_image_names():
    image_names = []
    print("\n==== Docker Image Name Input ====")
    print("Please enter the names of the Docker images you'd like to create.")
    print("Enter one name per line. When you are finished, enter a blank line.")
    index = 1
    while True:
        name = input(f"Image name #{index}: ").strip().lower()
        if not name:
            break
        image_names.append(name)
        index += 1
    return image_names

def create_project_structure(project_name, image_names):
    # Create the output directory if it doesn't exist
    output_path = os.path.join('output_folders', project_name)
    docker_path = os.path.join(output_path, 'docker')
    config_path = os.path.join(output_path, 'config')
    scripts_path = os.path.join(output_path, 'scripts')

    os.makedirs(docker_path, exist_ok=True)
    for name in image_names:
        os.makedirs(os.path.join(docker_path, name), exist_ok=True)
        with open(os.path.join(docker_path, name, 'Dockerfile'), 'w') as f:
            pass

    os.makedirs(config_path, exist_ok=True)
    for name in image_names:
        image_config_path = os.path.join(config_path, name)
        os.makedirs(image_config_path, exist_ok=True)
        with open(os.path.join(image_config_path, '.env'), 'w') as f, \
             open(os.path.join(image_config_path, '.env.example'), 'w') as f_example:
            pass

    os.makedirs(scripts_path, exist_ok=True)
    with open(os.path.join(scripts_path, 'build.sh'), 'w') as f_build, \
         open(os.path.join(scripts_path, 'run.sh'), 'w') as f_run:
        f_build.write("#!/bin/bash\n# Add your build commands here\n")
        f_run.write("#!/bin/bash\n# Add your run commands here\n")

def main():
    print("=== Docker Project Setup Script ===")
    project_name = get_project_name()
    image_names = get_image_names()
    create_project_structure(project_name, image_names)
    print(f"\nSetup complete! Your Docker project '{project_name}' has been successfully created inside the 'output' directory.")

if __name__ == "__main__":
    main()
