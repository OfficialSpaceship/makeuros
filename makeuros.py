#!/usr/bin/env python3
import os
import sys
import argparse
import shutil

OS_RELEASE_PATH = "/etc/os-release"
HOSTNAME_PATH = "/etc/hostname"
ISSUE_PATH = "/etc/issue"

def check_root():
    if os.geteuid() != 0:
        print("Error: This script must be run as root (sudo).", file=sys.stderr)
        sys.exit(1)

def parse_os_release():
    if not os.path.exists(OS_RELEASE_PATH):
        return {}
    data = {}
    with open(OS_RELEASE_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                # Strip quotes if present
                val = val.strip('"\'')
                data[key] = val
    return data

def write_os_release(data):
    # Backup first
    backup_path = OS_RELEASE_PATH + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy2(OS_RELEASE_PATH, backup_path)
        print(f"Backed up {OS_RELEASE_PATH} to {backup_path}")

    with open(OS_RELEASE_PATH, "w") as f:
        for k, v in data.items():
            # If value contains spaces, wrap it in double quotes
            if " " in v or not v.isalnum():
                f.write(f'{k}="{v}"\n')
            else:
                f.write(f'{k}={v}\n')

def update_fetch_configs(logo_path):
    # Determine the real user (since script runs as root/sudo)
    username = os.environ.get("SUDO_USER")
    if not username:
        try:
            import subprocess
            username = subprocess.check_output("logname", text=True).strip()
        except Exception:
            username = os.getlogin()

    if not username or username == "root":
        # Fallback to check directories in /home
        if os.path.exists("/home"):
            dirs = [d for d in os.listdir("/home") if os.path.isdir(os.path.join("/home", d)) and d != "lost+found"]
            if dirs:
                username = dirs[0]

    if not username or username == "root":
        return

    user_home = os.path.expanduser(f"~{username}")

    # Fastfetch config update
    fastfetch_dir = os.path.join(user_home, ".config/fastfetch")
    fastfetch_conf_path = os.path.join(fastfetch_dir, "config.jsonc")
    
    # If the fastfetch config dir exists but not the config, we generate it or write one
    if os.path.exists(fastfetch_dir) and not os.path.exists(fastfetch_conf_path):
        os.system(f"su - {username} -c 'fastfetch --gen-config'")

    if os.path.exists(fastfetch_conf_path):
        try:
            with open(fastfetch_conf_path, "r") as f:
                content = f.read()

            # We need to insert or update the "logo" field in the JSON structure
            import re
            if '"logo"' in content:
                # Replace existing logo block source and type
                content = re.sub(
                    r'("logo"\s*:\s*\{[^}]*"source"\s*:\s*")[^"]*(")',
                    r'\g<1>' + logo_path + r'\g<2>',
                    content
                )
                if '"type"' in content:
                    content = re.sub(
                        r'("logo"\s*:\s*\{[^}]*"type"\s*:\s*")[^"]*(")',
                        r'\g<1>file\g<2>',
                        content
                    )
                else:
                    content = re.sub(
                        r'("logo"\s*:\s*\{)',
                        r'\g<1>\n    "type": "file",',
                        content
                    )
            else:
                # Insert a logo block before the modules or at the start
                replacement = '{\n  "logo": {\n    "source": "' + logo_path + '",\n    "type": "file"\n  },'
                content = content.replace('{', replacement, 1)

            with open(fastfetch_conf_path, "w") as f:
                f.write(content)
            print(f"Updated fastfetch config at {fastfetch_conf_path} to use custom logo.")
        except Exception as e:
            print(f"Failed to update fastfetch config: {e}")

    # Neofetch config update
    neofetch_conf_path = os.path.join(user_home, ".config/neofetch/config.conf")
    if os.path.exists(neofetch_conf_path):
        try:
            with open(neofetch_conf_path, "r") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                if line.strip().startswith("image_source="):
                    lines[i] = f'image_source="{logo_path}"\n'
                elif line.strip().startswith("image_backend="):
                    lines[i] = f'image_backend="ascii"\n'

            with open(neofetch_conf_path, "w") as f:
                f.writelines(lines)
            print(f"Updated neofetch config at {neofetch_conf_path} to use custom logo.")
        except Exception as e:
            print(f"Failed to update neofetch config: {e}")

def set_hostname(new_hostname):
    check_root()
    # Backup first
    backup_path = HOSTNAME_PATH + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy2(HOSTNAME_PATH, backup_path)
        print(f"Backed up {HOSTNAME_PATH} to {backup_path}")

    with open(HOSTNAME_PATH, "w") as f:
        f.write(new_hostname.strip() + "\n")
    
    # Try to set hostname in current session as well
    os.system(f"hostnamectl set-hostname {new_hostname}")
    print(f"Hostname updated to: {new_hostname}")

def install_package(pkg):
    print(f"Resolving the best installation path for: {pkg}...")
    import shutil
    import subprocess

    # 1. Custom overrides for tricky applications
    if pkg.lower() == "ollama":
        print("Detected 'ollama'. Checking installation options...")
        # Check if yay is available to install from AUR (preferred on Arch for updates)
        if shutil.which("yay"):
            print("Installing ollama via 'yay' (AUR)...")
            res = os.system("yay -S --noconfirm ollama")
            if res == 0:
                print("ollama installed successfully via yay!")
                return
        # Fallback to official install script
        if shutil.which("curl"):
            print("Installing ollama via official curl installer script...")
            res = os.system("curl -fsSL https://ollama.com/install.sh | sh")
            if res == 0:
                print("ollama installed successfully via curl script!")
                return

    # 2. Check if package exists in official Arch repositories (pacman)
    if shutil.which("pacman"):
        check_pacman = subprocess.run(["pacman", "-Sp", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if check_pacman.returncode == 0:
            print(f"Package '{pkg}' found in official repositories. Installing via pacman...")
            # pacman needs root/sudo privileges
            res = os.system(f"sudo pacman -S --noconfirm {pkg}")
            if res == 0:
                print(f"Successfully installed {pkg} via pacman!")
                return

    # 3. Check if package can be installed via AUR (yay)
    if shutil.which("yay"):
        print(f"Checking if '{pkg}' is available in the AUR...")
        check_aur = subprocess.run(["yay", "-Sp", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if check_aur.returncode == 0:
            print(f"Package '{pkg}' found in AUR. Installing via yay...")
            res = os.system(f"yay -S --noconfirm {pkg}")
            if res == 0:
                print(f"Successfully installed {pkg} via yay!")
                return

    # 4. Global generic installer scripts check (rustup, bun, deno, etc.)
    common_scripts = {
        "rustup": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        "bun": "curl -fsSL https://bun.sh/install | sh",
        "deno": "curl -fsSL https://deno.land/install.sh | sh",
        "nvm": "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash",
        "pipx": "python3 -m pip install --user pipx && python3 -m pipx ensurepath"
    }

    if pkg.lower() in common_scripts:
        script = common_scripts[pkg.lower()]
        print(f"Found developer install script for '{pkg}'. Running installer...")
        res = os.system(script)
        if res == 0:
            print(f"Successfully installed {pkg}!")
            return

    print(f"Error: Could not find a suitable installation method for '{pkg}'. Try installing it manually.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="makeuros: Customize your Arch Linux system identity")
    parser.add_argument("--name", help="Set the OS Name (e.g. MySuperOS)")
    parser.add_argument("--id", help="Set the OS ID (lowercase, e.g. mysuperos)")
    parser.add_argument("--pretty-name", help="Set the Pretty Name (e.g. MySuperOS GNU/Linux)")
    parser.add_argument("--hostname", help="Set the system hostname")
    parser.add_argument("--logo", help="Set the OS logo icon name (e.g. archlinux, ubuntu, or custom)")
    parser.add_argument("--home-url", help="Set the Home Page URL")
    parser.add_argument("--reset", action="store_true", help="Restore /etc/os-release and /etc/hostname from backups")
    parser.add_argument("--install", help="Install a package automatically using the best tool (pacman, yay, curl script, etc.)")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.install:
        install_package(args.install)
        sys.exit(0)

    check_root()

    if args.reset:
        restored = False
        for path in [OS_RELEASE_PATH, HOSTNAME_PATH]:
            bak = path + ".bak"
            if os.path.exists(bak):
                shutil.copy2(bak, path)
                print(f"Restored {path} from {bak}")
                restored = True
        if not restored:
            print("No backups found to restore.")
        sys.exit(0)

    data = parse_os_release()

    modified = False

    if args.name:
        data["NAME"] = args.name
        modified = True
    if args.id:
        # Check if the input to --id is a filepath
        if os.path.exists(os.path.expanduser(args.id)):
            logo_path = os.path.abspath(os.path.expanduser(args.id))
            data["ID"] = "custom_os"
            data["LOGO"] = logo_path
            # Also update fetch configs if they exist
            update_fetch_configs(logo_path)
        else:
            data["ID"] = args.id
        modified = True
    if args.pretty_name:
        data["PRETTY_NAME"] = args.pretty_name
        modified = True
    if args.logo:
        if os.path.exists(os.path.expanduser(args.logo)):
            logo_path = os.path.abspath(os.path.expanduser(args.logo))
            data["LOGO"] = logo_path
            update_fetch_configs(logo_path)
        else:
            data["LOGO"] = args.logo
        modified = True
    if args.home_url:
        data["HOME_URL"] = args.home_url
        modified = True

    if modified:
        write_os_release(data)
        print("Updated /etc/os-release successfully!")
        # Also update /etc/issue for local login screens if appropriate
        if "PRETTY_NAME" in data:
            with open(ISSUE_PATH, "w") as f:
                f.write(f"{data['PRETTY_NAME']} (\\l)\n\n")

    if args.hostname:
        set_hostname(args.hostname)

if __name__ == "__main__":
    main()
