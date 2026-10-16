#!/bin/bash

#
# With the challtitle and file name -> lmgtfu -> andOTP
#

ECHO=$(which echo)
GREP=$(which grep)
APT=$(which apt)
PYTHON=$(which python)
PIP=$(which pip)
A2J=$(which andotp2john)
JOHN=$(which john)
TAR=$(which tar)
SED=$(which sed)
XXD=$(which xxd)

CHALL_FILE="./json.aes"
JTR_FILE="./crackme"
WORDLIST_ZIP="/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz"
WORDLIST="./rockyou.txt"
PASSWORD=""
FLAG=""
#ARR_PACKAGES=(zlib1g-dev libjpeg-dev libpng-dev python3-pycryptodome python3-pyotp python3-pyqrcode python3-pillow python3-docopt john python3-venv)
ARR_PACKAGES=(zlib1g-dev libjpeg-dev libpng-dev python3-pycryptodome john python3-venv seclists)

${ECHO} "[*] Note: Script is Debian based, make sure to install needed packages"
${ECHO} "[*] More important note: Script is noob like, hence errors are almost not handled ... unexpected behavior might occur"

${ECHO} "[*] Checking installed packages ..."
for package in ${ARR_PACKAGES[@]}
do
    if [[ ! $(${APT} -qq list ${package} 2>/dev/null | ${GREP} -c "installed") == 1 ]]; then
        ${ECHO} "[-] Package ${package} NOT installed"
        exit 1
    else
        continue
    fi
done

${ECHO} "[*] Converting to john format ..."
${A2J} ${CHALL_FILE} > ${JTR_FILE}

${ECHO} "[*] Prep cracking ..."
${TAR} xvf ${WORDLIST_ZIP} > ${WORDLIST}

${ECHO} "[*] Start cracking ..."
${JOHN} --wordlist=${WORDLIST} ${JTR_FILE}
PASSWORD=$( ${JOHN} --show ${JTR_FILE} | ${GREP} -o ':.*' | ${SED} -e 's/://')

if [[ ! -z ${PASSWORD} ]]; then
    ${ECHO} "[*] Checking python venv ..."
    if [ ! -e balcconVenv ]; then
        ${PYTHON} -m venv balcconVenv
    fi

    ${ECHO} "[*] Activating python venv ..."
    . ./balcconVenv/bin/activate

    PIP=$(which pip)
    if [[ $(${ECHO} ${PIP} | ${GREP} -c "balcconVenv") == 1 ]]; then
        ${ECHO} "[*] Installing andotp-decrypt ..."
        ${PIP} install andotp-decrypt 2>/dev/null

        if [[ ! $(${PIP} list | ${GREP} -c "andotp-decrypt") == 1 ]]; then
            ${ECHO} "[-] Something went wrong during andotp-decrypt install"
        else
            ${ECHO} "[*] Decrypting andOTP backup file ..."
            AOTPDEC=$(which andotp_decrypt)
            FLAG=$(${ECHO} ${PASSWORD} | ${AOTPDEC} -o ${CHALL_FILE} | ${SED} -r 's/^.*\[\"(.*)\".*$/\1/' | ${XXD} -p -r)

            if [[ ! -z ${FLAG} ]]; then
                ${ECHO} "[*] Flag: ${FLAG}"
            else
                ${ECHO} "[-] No flag for you today :("
            fi
        fi
    else
        ${ECHO} "[-] Seems we are not in our venv"
    fi

    deactivate
else
    ${ECHO} "[-] Password not cracked"
fi








