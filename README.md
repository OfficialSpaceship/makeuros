# makeuros

`makeuros` is a CLI tool that lets you customize your Arch Linux system identity, allowing you to choose your own OS name, hostname, logo, etc.

## Installation

You can install this package via `yay` (once pushed to the AUR) or build it manually:

```bash
git clone https://github.com/shadow/makeuros.git
cd makeuros
makepkg -si
```

## Usage

Since `makeuros` modifies system configuration files (`/etc/os-release`, `/etc/hostname`), it must be ran with `sudo`:

```bash
# Set OS Name and Hostname
sudo makeuros --name "ShadowOS" --id "shadowos" --pretty-name "ShadowOS GNU/Linux" --hostname "shadow-box"

# Reset changes to backups
sudo makeuros --reset
```
