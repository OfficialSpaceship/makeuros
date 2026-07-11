# makeuros

`makeuros` is a tool to customize your OS branding, set up docker containers easily, and much more!

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

Since makeuros ***modifies settings system wide***, it needs to be ran with sudo. 

Examples:

```
sudo makeuros --pretty-name "SX Server OS"
sudo makeuros --pretty-name SxServerOS
sudo makeuros --reset
sudo makeuros --id ~/logo.txt
```

## How to create a logo

If you wanna create your own custom logo please create a file in your home directory with ``nano ~/logo.txt``, then paste your ASCII logo in there.
After that run ``sudo makeuros --id ~/logo.txt``.

## Build Time
Since makeuros is not big and does not use any dependencies apart from python, it will build in seconds.

## Useful command

There is a builtin command with ``--install`` which will install any package you want, completely by itself. It is there to help YOU the user out, so you do not need to search manually if pacman or yay or ETC has it, it automatically searches and installs it.

Usage Example:

```
sudo makeuros --install spxc-core
```

## Setting up docker containers

With the latest release, you can now setup your own docker environments easily, and manage easily.

## Usage:

```
makeuros --setup-gitea
```

It will ask you if it should auto-start, path, ETC.
