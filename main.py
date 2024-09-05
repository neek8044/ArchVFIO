import subprocess as s
import time
import sys
import os
import platform

cwd = os.getcwd()

dots = [".  ", ".. ", "..."]

commands = {
    "Installing software": "sudo pacman -S libvirt virt-manager ovmf qemu",
    "Starting libvirtd": "sudo systemctl start libvirtd.service",
    "Starting virtlogd": "sudo systemctl start virtlogd.socket",
    "Enabling libvirtd": "sudo systemctl enable libvirtd.service",
    "Enabling virtlogd": "sudo systemctl enable virtlogd.socket",
    "Creating a GRUB backup file": "sudo cp /etc/default/grub /etc/default/grub.archvfiobackup",
    "Tweaking the GRUB config": "grub_iommu",
    "Verifying IOMMU groups": f"{cwd}/iommu.sh"
}


if "intel" in platform.processor().lower():
    cpu = "intel"
elif "amd" in platform.processor().lower():
    cpu = "amd"
else:
    print("ERROR: Unsupported CPU brand. Only Intel and AMD work with this script.")
    sys.exit(1)


def new_process(command, msg):
    sp = s.Popen(
        command,
        shell=True,
        stdout=s.DEVNULL
    )

    while sp.poll() is None:
        for i in dots:
            print(msg + i, end="\r")
            time.sleep(0.5)

    print(msg + "...OK")


def grub_iommu():
    with open("/etc/default/grub", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith("GRUB_CMDLINE_LINUX_DEFAULT"):
            if f"{cpu}_iommu=on" not in line:
                line = line.strip().replace("\"", f" {cpu}_iommu=on\"")
                lines[i] = line + "\n"

    with open("/etc/default/grub", "w") as file:
        file.writelines(lines)


for i in commands:
    if commands[f"{i}"] == "grub_iommu":
        print(i, end="")
        grub_iommu()
        print("...OK")
    else:
        new_process(commands[f"{i}"], i)

sys.exit(0)
