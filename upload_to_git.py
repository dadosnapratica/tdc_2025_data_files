import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import platform

#sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# Configuration
REPO_URL = os.getenv("REPO_URL", "git@github.com:dadosnapratica/tdc_2025_data_files.git")
BRANCH = os.getenv("BRANCH", "main")
DEFAULT_REPO_DIR = r"C:\Users\flavio.lopes\projetos\personal\educacionais\tdc_2025\tdc_2025_data_files" if platform.system() == "Windows" else "/home/ubuntu/tdc_2025_data_files"

REPO_DIR = os.getenv("REPO_DIR", DEFAULT_REPO_DIR)  # Default if not set in .env
WATCH_DIR = os.getenv("WATCH_DIR", "data")  # Directory to monitor for changes
LFS_TRACKED_EXTENSIONS = os.getenv("LFS_TRACKED_EXTENSIONS", "csv,zip,mp4,json").split(",")

def run_command(command, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    #print(f'[XX] Command Result: {result}')
    if "ssh -T git@github.com" not in command:
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            sys.exit(1)
    else:
        return "You've successfully authenticated"
    return result.stdout.strip()

def check_ssh_auth():
    """Check if SSH authentication is set up for GitHub."""
    try:
        output = run_command("ssh -T git@github.com")
        print(f'SSH Access Validation Output: {output}')
        if "successfully" in output:
            print("✅ SSH authentication with GitHub verified.")
        else:
            print("⚠️ SSH authentication issue detected.")
    except SystemExit:
        print("❌ Failed to authenticate via SSH. Ensure your SSH key is added to GitHub.")
        sys.exit(1)

def clone_or_pull_repo():
    """Clone the repository if it does not exist, otherwise pull latest changes."""
    if not os.path.isdir(REPO_DIR):
        print("Cloning repository via SSH...")
        run_command(f"git clone {REPO_URL} {REPO_DIR}")
    else:
        print("Updating repository...")
        run_command(f"git pull origin {BRANCH}", cwd=REPO_DIR)

def enable_git_lfs():
    """Ensure Git LFS is installed and configured for the repository."""
    print("🔹 Enabling Git LFS...")
    run_command("git lfs install", cwd=REPO_DIR)

    # Track large file extensions
    for ext in LFS_TRACKED_EXTENSIONS:
        run_command(f"git lfs track *.{ext}", cwd=REPO_DIR)

    # Ensure .gitattributes is committed
    run_command("git add .gitattributes", cwd=REPO_DIR)
    run_command("git commit -m 'Enable Git LFS tracking'", cwd=REPO_DIR)
    run_command(f"git push origin {BRANCH}", cwd=REPO_DIR)

def upload_file(file_path):
    """Upload the specified file to the Git repository, handling large files with LFS."""
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found!")
        sys.exit(1)

    file_name = os.path.basename(file_path)
    file_extension = file_name.split(".")[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    commit_message = f"Auto-commit: Uploading {file_name} - Version {timestamp}"

    print('Checking changes')
    git_status_output=run_command('git status')
    if 'nothing to commit' in git_status_output:
        print('No changes to commit')
        exit(0)
    else:
        print("Follow changes detected with git status")
        print(git_status_output)

    print("Checking SSH authentication...")
    check_ssh_auth()

    print("Ensuring the repository is up to date...")
    clone_or_pull_repo()

    #print("Setting up Git LFS...")
    #enable_git_lfs()

    print(f"Copying {file_name} to repository...")
    dest_path = os.path.join(REPO_DIR, WATCH_DIR, file_name)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    copy_command=rf"copy {file_path} {dest_path}" if platform.system() == "Windows" else r"cp {file_path} {dest_path}" 
    run_command(copy_command) 
    
    print("Adding file to Git...")
    run_command(f"git add {WATCH_DIR}/{file_name}", cwd=REPO_DIR)

    # Ensure LFS is tracking large files
    if file_extension in LFS_TRACKED_EXTENSIONS:
        print(f"🔹 '{file_name}' is a large file - Ensuring Git LFS is tracking it.")
        run_command(f"git lfs track *.{file_extension}", cwd=REPO_DIR)

    print("Add changes...")
    run_command('git add . ', cwd=REPO_DIR)

    print("Committing changes...")
    run_command(f'git commit -m "{commit_message}"', cwd=REPO_DIR)

    print("Pushing changes via SSH...")
    run_command(f"git push origin {BRANCH} --no-verify", cwd=REPO_DIR)

    print(f"✅ File '{file_name}' uploaded successfully with commit message: '{commit_message}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_to_git.py <file-to-upload>")
        sys.exit(1)

    file_to_upload = sys.argv[1]
    upload_file(file_to_upload)
