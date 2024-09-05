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
    "Verifying IOMMU groups": f"{cwd}/iommu.sh",
    "Isolating the GPU": "vfio_conf",
    "Running mkinitcpio": "sudo mkinitcpio -g /boot/linux-archvfio.img"
}


doCPUloop = True

while doCPUloop:
    cpu = input("Select the CPU brand of this machine: [1] Intel [2] AMD : ")
    if cpu == "1" or cpu.lower() == "amd":
        cpu = "amd"
        doCPUloop = False
    elif cpu == "2" or cpu.lower() == "intel":
        cpu = "intel"
        doCPUloop = False
    else:
        print("Selection invalid. Choose either Intel or AMD using '1' or '2', or by typing out the name of the brand.")


def new_process(command, msg, show_stdout=False):
    sp = s.Popen(
        command,
        shell=True,
        stdout=s.DEVNULL if show_stdout is False else s.STDOUT
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


def vfio_conf():
    vfio_file = '/etc/modprobe.d/vfio.conf'

    id1 = input("Type the ID of your GPU from the output window above: ")
    id2 = input("Type the ID of your GPU AUDIO device from the output window above: ")

    lines_to_add = [
        "softdep amdgpu pre: vfio-pci",
        "softdep snd_hda_intel pre: vfio-pci",
        f"options vfio-pci ids={id1},{id2}"
    ]

    if not os.path.exists(vfio_file):
        with open(vfio_file, 'w') as file:
            for line in lines_to_add:
                file.write(line + '\n')
    else:
        with open(vfio_file, 'r') as file:
            current_lines = file.readlines()

        with open(vfio_file, 'a') as file:
            for line in lines_to_add:
                if line not in current_lines:
                    file.write(line + '\n')


for i in commands:
    if commands[f"{i}"] == "grub_iommu":
        print(i, end="")
        grub_iommu()
        print("...OK")
    elif commands[f"{i}"] == "vfio_conf":
        print(i, end="")
        vfio_conf()
        print("...OK")
    elif commands[f"{i}"].endswith("/iommu.sh"):
        new_process(commands[f"{i}"], i, True)
    else:
        new_process(commands[f"{i}"], i)

print("\nREBOOT TO APPLY CHANGES.")

sys.exit(0)
