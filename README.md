# makeuros

`makeuros` is a CLI tool that lets you customize your Arch Linux system identity, allowing you to choose your own OS name, hostname, logo, etc.

## Required Dependencies:

You need to have Python installed (latest version recommended, but works on older versions.), thats all.

## Installation

You can install this package via `yay` (Via: yay -S makeuros) or build it manually:

```bash
git clone https://github.com/OfficialSpaceship/makeuros.git
cd makeuros
makepkg -si
```

However, if there is an Authentication error please run the next command:
```
git config --global --unset credential.helper
```

## Usage

Since `makeuros` modifies system configuration files (`/etc/os-release`, `/etc/hostname`), it must be ran with `sudo`:

```bash
# Set OS Name and Hostname
sudo makeuros --name "Sx Server OS" --id "shadowos" --pretty-name "ShadowOS GNU/Linux" --hostname "shadow-box"

# Reset changes to backups
sudo makeuros --reset
```

## Build Time

Since makeuros is not big and does not use any dependencies apart from python, it will build in seconds.
