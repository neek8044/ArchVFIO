# ArchVFIO
**Automated VFIO setup for arch based distros.**

WARNING: Reverting changes is not yet implemented. You will have to revert the changes yourself:

- reattaching the gpu to the host machine
- deleting the custom grub config and going back to the backup that was created automatically ( grub.archvfiobackup )
- rebuild the linux.img with mkinitcpio).
