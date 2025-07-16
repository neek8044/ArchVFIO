# ArchVFIO
**Automated VFIO setup for arch based distros.**

---

## The code is shit. This project will get a complete re-write in C++. Star/Watch the repo to stay tuned or whatever idk

**WARNING:** Reverting changes is not yet implemented. You will have to revert the changes yourself:

- reattaching the gpu to the host machine
- deleting the custom grub config and going back to the backup that was created automatically (`/etc/default/grub.archvfiobackup`)
- rebuilding the linux.img with mkinitcpio.
