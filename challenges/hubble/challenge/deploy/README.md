# Deployment
- Make sure `ASLR` is turned on `echo 2 > /proc/sys/kernel/randomize_va_space`, otherwise `PIE` might not apply as intended
- Note(s) for Docker
    * Build for `Debian Bookworm`
    * Copy `files/flag.txt` to `/flag.txt` and `chmod 440`
    * Copy challenge file `files/main` to, e.g., `/home/ctf/main` and `chmod 550`
    * Use stuff like `xinetd` etc. to run challenge file