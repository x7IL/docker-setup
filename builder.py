import os
def generate_bash_script(project_name, network_name, image_names):
    bash_script = f"""#!/bin/bash

# Current script directory
SCRIPT_DIR=$(dirname $(readlink -f $0))

# Network configuration
NETWORK_NAME="{network_name}"
if [ ! -z "$NETWORK_NAME" ]; then
    docker network inspect $NETWORK_NAME >/dev/null 2>&1 || docker network create $NETWORK_NAME
fi
"""

    for image_name in image_names:
        upper_image_name = image_name.upper().replace('-', '_')
        bash_script += f"""
# Image names for {image_name}
{upper_image_name}_NAME="local/{project_name}/{image_name}"

# Image tagging configuration
TAG=$(git log -1 --pretty=%h)
{upper_image_name}_LATEST="${{{upper_image_name}_NAME}}:latest"
{upper_image_name}_TAGGED="${{{upper_image_name}_NAME}}:$TAG"

# Removing old {image_name} image
docker image rm \\
  "${{{upper_image_name}_LATEST}}" \\
  "${{{upper_image_name}_TAGGED}}" 2> /dev/null

# Build {image_name}
docker build \\
  -t "${{{upper_image_name}_LATEST}}" \\
  -t "${{{upper_image_name}_TAGGED}}" \\
  "$SCRIPT_DIR/../../docker/{image_name}/{image_name}"
"""
    return bash_script

# run.sh

# builder.py

def generate_run_script(project_name, network_name, image_names, scripts_path):
    run_script_contents = f"""#!/bin/bash

# Current script directory
SCRIPT_DIR=$(dirname $(readlink -f $0))

# Network configuration
NETWORK_NAME="{network_name}"
"""

    # Collect port mappings directly during run script generation
    port_mappings = {}
    print("\n==== Port Mapping Input ====")
    for image_name in image_names:
        port_mapping = input(f"Enter port mapping for {image_name} (e.g., '80:80') or press enter if none: ").strip()
        port_mappings[image_name] = port_mapping

    # Append container run commands for each image with conditional port mappings
    for image_name in image_names:
        container_name = f"{image_name}.{project_name}.local"
        image_full_name = f"local/{project_name}/{image_name}"
        env_file_path = f"../../config/{image_name}/.env"
        port_mapping = port_mappings[image_name]

        # Stopping and removing existing containers
        run_script_contents += f"""
# Stopping any running {image_name} containers
docker stop "{container_name}" 2> /dev/null;
docker rm "{container_name}" 2> /dev/null;

# Running {image_name} container
docker run -d \\
  --name "{container_name}" \\
  --network $NETWORK_NAME \\
  --env-file "{env_file_path}" \\
"""
        if port_mapping:
            run_script_contents += f'  -p {port_mapping} \\\n'
        
        run_script_contents += f'  -t "{image_full_name}:latest"\n'

    # Write the script contents to the file
    run_script_path = os.path.join(scripts_path, 'run.sh')
    with open(run_script_path, 'w') as file:
        file.write(run_script_contents)

    os.chmod(run_script_path, 0o755)
    return run_script_contents
