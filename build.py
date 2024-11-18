import os
import subprocess
import sys

UE_PATH = r""
PROJECT_PATH = r""
BUILD_PATH = r""
BATCH_SCRIPTS = [ 
]
CONFIGURATION = "Shipping"
PLATFORMS = ["Win64", "Linux", "LinuxArm64", "Android"]
MAC_IP = "your_mac_ip" 
MAC_USERNAME = "your_mac_username"
REMOTE_SCRIPT_PATH = "~/mac_build.sh"

def run_command(command):
    """Run a command synchronously and check for errors."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        sys.exit(1)

def build_project(platform):
    """Build the project for the specified platform."""
    print(f"Building for platform: {platform}")
    uat_path = os.path.join(UE_PATH, "Engine", "Build", "BatchFiles", "RunUAT.bat")
    build_command = f'"{uat_path}" BuildCookRun -project="{PROJECT_PATH}" -noP4 -platform={platform} -clientconfig={CONFIGURATION} -serverconfig={CONFIGURATION} -cook -allmaps -build -stage -package -archive -archivedirectory="{BUILD_PATH}\\{platform}"'
    run_command(build_command)

def execute_batch_scripts():
    """Execute the list of batch scripts synchronously."""
    for script in BATCH_SCRIPTS:
        print(f"Executing script: {script}")
        run_command(script)

def execute_remote_build(mac_ip, mac_username, remote_script_path):
    """
    Executes a build script on a remote Mac using SSH.
    """
    ssh_command = f'ssh {mac_username}@{mac_ip} "bash {remote_script_path}"'
    print(f"Executing remote build script on {mac_ip}...")
    try:
        subprocess.run(ssh_command, check=True, shell=True)
        print(f"Successfully triggered build script on {mac_ip}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute remote build script: {e}")
        sys.exit(1)

def fetch_files_from_mac(mac_ip, mac_username, mac_file_path, windows_dest_path):
    """
    Fetch files from Mac to Windows using SCP.
    """
    scp_command = f'scp {mac_username}@{mac_ip}:{mac_file_path} "{windows_dest_path}"'
    print(f"Fetching files from {mac_ip} to {windows_dest_path}...")
    try:
        subprocess.run(scp_command, check=True, shell=True)
        print(f"Files successfully fetched to {windows_dest_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch files: {e}")
        sys.exit(1)

def main():
    for platform in PLATFORMS:
        build_project(platform)

    #execute_remote_build(MAC_IP, MAC_USERNAME, REMOTE_SCRIPT_PATH)

    print("All builds and scripts completed successfully!")
    execute_batch_scripts()

    print("All builds and scripts completed successfully!")

if __name__ == "__main__":
    main()
