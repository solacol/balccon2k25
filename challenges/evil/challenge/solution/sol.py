#!/usr/bin/env python3

import string
import struct
import sys
import binascii
import subprocess
import re
import json
import base64



decodeJS = '''
// https://github.com/satoshinm/pill_duck/blob/master/js/web/web.js
// https://github.com/satoshinm/pill_duck/blob/master/js/hid.js

'use strict';

const REPORT_ID_KEYBOARD = 1;
const REPORT_ID_MOUSE = 2;



function decode(buf) {
    const result = {};
    const report_id = buf.readUInt8(0);
    result.report_id = report_id;

    if (report_id === REPORT_ID_MOUSE) {
        result.buttons = buf.readUInt8(1);
        result.x = buf.readUInt8(1);
        result.y = buf.readUInt8(2);
        result.wheel = buf.readUInt8(3);
    } else if (report_id === REPORT_ID_KEYBOARD) {
        result.modifiers = buf.readUInt8(1);
        result.reserved = buf.readUInt8(2);
        result.keys_down = [];
        for (let i = 0; i < 6; ++i) {
          result.keys_down.push(buf.readUInt8(3 + i));
        }
        result.leds = buf.readUInt8(8);
    } else {
    }

    return result;
}



function encode(result) {
    const buf = Buffer.alloc(16);

    if (result.report_id == REPORT_ID_MOUSE) {
        buf.writeUInt8(REPORT_ID_MOUSE, 0);
        buf.writeUInt8(result.buttons, 1);
        buf.writeUInt8(result.x, 2);
        buf.writeUInt8(result.y, 3);
        buf.writeUInt8(result.wheel, 4);
    } else if (result.report_id == REPORT_ID_KEYBOARD) {
        buf.writeUInt8(REPORT_ID_KEYBOARD, 0);
        buf.writeUInt8(result.modifiers, 1);
        buf.writeUInt8(result.reserved, 2);
        for (let i = 0; i < 6; ++i) {
          buf.writeUInt8(result.keys_down[i], 3 + i);
        }
        buf.writeUInt8(result.leds, 8);
    }

    return buf;
}



function splitReports(bufs) {
    const array = [];
    let i = 0;
    do {
        const buf = bufs.slice(i, (i + 1) * 16);
        array.push(buf);
        i += 16;
    } while (i < bufs.length);

    return array;
}



function decodeAll(buf) {
    const array = splitReports(buf);
    const result = [];
    array.forEach((buf) => {
        result.push(decode(buf));
    });

    return result;
}



let input = process.argv[2];;

if ((input.length % 2) != 0) input = input.substr(0, input.length - 1)
const binary_input = new Buffer(input, 'hex');

const output = decodeAll(binary_input);
const json_output = JSON.stringify(output);
console.log(json_output);
'''

DEBUG = False

#
# Decrypt
#
# https://code.activestate.com/recipes/496737-python-xtea-encryption/
def xteaDecrypt(block, key, n):
    v0,v1 = struct.unpack('<2I',block)
    k = key
    delta = 0x9e3779b9
    mask = 0xffffffff
    sum = (delta * n) & mask
    for round in range(n):
        v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
        sum = (sum - delta) & mask
        v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
    return struct.pack('II',v0,v1)

#
# Decode keys
#
def decodeKeys(data):
    KEY_PRESSED = json.loads(data)

    MAPPING = { c : l for c, l in zip(range(0x04, 0x28), string.ascii_lowercase + "1234567890") }
    MAPPING.update({ c : l for c, l in zip((0x28, 0x2c, 0x2d, 0x2e), "\n -=") })

    # Mapping for shift
    SHIFT_MAPPING = { a : b for a, b in zip("1234567890-= ", "!@#$%^&*()_+ ") }
    SHIFT_MAPPING.update({ a: b for a, b in zip(string.ascii_lowercase, string.ascii_uppercase) })

    result = ''
    for mod, key in KEY_PRESSED:
        if mod == 0:
            result += MAPPING[key]
        elif mod == 2: # shift
            result += SHIFT_MAPPING[MAPPING[key]]
    return(result)

#
# Decode binary
#
def decodeBinary(data):
    node = subprocess.Popen(['which', 'nodejs'], stdout=subprocess.PIPE)
    node = node.stdout.read()
    node = node.decode('utf-8').rstrip()
    if re.search("/nodejs$", node):
        data = subprocess.Popen([node, '--no-deprecation', 'decode.js', data], stdout=subprocess.PIPE)
        data = data.stdout.read()
        return(data)
    else:
        print("No nodejs installed?")
        exit(-1)

#
# Transform data
#
def transformData(data):
    jq = subprocess.Popen(['which', 'jq'], stdout=subprocess.PIPE)
    jq = jq.stdout.read()
    jq = jq.decode('utf-8').rstrip()
    echo = subprocess.Popen(['which', 'echo'], stdout=subprocess.PIPE)
    echo = echo.stdout.read()
    echo = echo.decode('utf-8').rstrip()
    if re.search("/jq$", jq):
        if re.search("/echo$", echo):
            dataecho = '\'' + data.decode('utf-8').rstrip()
            datajq = '''[.[] | [.modifiers, .keys_down[0]]] - [[0,0], [null,null]]'''
            #echodata = data.decode('utf-8').rstrip()
            data = subprocess.Popen([echo, data], stdout=subprocess.PIPE)
            data =  subprocess.Popen([jq, '-c', datajq], stdin=data.stdout, stdout=subprocess.PIPE)
            data = data.stdout.read()
            return(data)
        else:
            print("No echo installed?")
            exit(-1)
    else:
        print("No jq installed?")
        exit(-1)

#
# Main
#
#
# Use ghidra etc. to analyze ...
# ... from the pictures we can assume it is a cortex little endian
#
def main():
    REPORT_ID_END = 255
    TEA_KEY = [ 0xd34db33f, 0x5014c010, 0x83560621, 0x68378324 ]

    print("Step 0 - Creating decode.js")
    try:
        with open('decode.js', 'w', encoding='utf-8') as f:
            f.write(decodeJS)
    except:
        print("Fucked up writing decode.js")
        exit(-1)

    print("Step 1 - Get user data")
    try:
        with open(sys.argv[1], 'rb') as f:
            # Read user.data ---> base is 0x08000000 ---> user data starts at 0x08002000
            data = f.read()[0x2000:]
    except:
        print("No input file")
        exit(-1)

    # Next to other from FUN_08000230 we know its some kind of TEA family (here: 64bit block cipher in CBC mode) ...
    # ... cause of the magic hash 0x9e3779b9 (is pseudo obfuscated, see FUN_08000150 and FUN_08000188)
    # Second arg of FUN_08000230 seems to be key to be found at DAT_08001c7c
    print("Step 2 - Decrypt user data to binary")
    try:
        last = bytes(8)
        pt = b''
        rounds = 64
        for i in range(0, len(data), 8):
            current = xteaDecrypt(data[i:i+8], TEA_KEY, rounds)
            pt += bytes(a ^ b for a, b in zip(current, last))
            last = data[i:i+8]
            # Check REPORT_ID_END reached
            if i % 16 == 8 and pt[-16] == REPORT_ID_END:
                break
    except:
        print("Something went wrong during decryption")

    try:
        # Decode binary to json
        userDataBin = binascii.hexlify(pt).decode('utf-8')
        if DEBUG:
            print(userDataBin)

        print("Step 3 - Decode binary")
        userDataKeys = decodeBinary(userDataBin)
        if DEBUG:
            print(userDataKeys)

        print("Step 4 - Transform data")
        userDataTransformed = transformData(userDataKeys)
        if DEBUG:
            print(userDataTransformed)
    except:
        print("Something went wrong during decoding or transformation")

    try:
        # Extract modifiers and keys_down values from json from above and transform them in their equivalent characters
        print("Step 5 - Get flag")
        userDataFlag = decodeKeys(userDataTransformed.decode('utf-8').rstrip())
        flag = re.search("echo (.*)", userDataFlag)
        print(base64.b64decode(flag.group(1)).decode('utf-8'))
    except:
        print("Something went wrong during flag extraction")

#
# Start
#
if __name__ == '__main__':
    main()
