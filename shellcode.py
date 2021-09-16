import sys, time, os, colorama, ctypes, datetime, platform
from colorama import Fore, Back, Style
from datetime import date
from time import gmtime, strftime
from subprocess import Popen, PIPE

today = date.today()
d2 = today.strftime("%B %d, %Y")

if platform.system()=='Linux':
    os.system('clear')
    sys.stdout.write("\x1b]2;Binary File Shellcoder\x07")
else:
    os.system('cls')
    ctypes.windll.kernel32.SetConsoleTitleW(f'Binary File Shellcoder | {d2}')

print(f"""{Style.BRIGHT + Fore.RED}
 ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗███████╗ ██████╗ ██████╗  ██████╗███████╗   ██╗ ██████╗ 
 ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝   ██║██╔═══██╗
 ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║     █████╗     ██║██║   ██║
 ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝     ██║██║   ██║
 ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██║     ╚██████╔╝██║  ██║╚██████╗███████╗██╗██║╚██████╔╝
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝╚═╝ ╚═════╝ 
                                                                                                             
{Fore.WHITE}═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
{Style.BRIGHT + Fore.YELLOW}  
                                 Binary File to Shellcode Converter by Eagle Eye
                             Make Sure You already installed MinGW/objdump libraries
                                https://dragonforce.io | Telegram: dragonforceio

{Fore.WHITE}═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
""")

def helpdesk():
    print(Style.BRIGHT+Fore.BLUE+'Usage (example) : python shellcode.py -f binary.exe -o shellcode.txt')

def position(arr,types):
    if(types=="-f" or types=="-o" or types=="-h"):
        return arr.index(types) + 1
    else:
        return 0

def dumpBinary(target,o):
    try:
        if(os.path.isfile(target)):
            try:
                if platform.system()=='Linux':
                    dumpFile = target + "_dump"
                    p = Popen(['objdump -d '+target],stdout=PIPE,shell=True)
                    (out, err) = p.communicate()
                    f = open(dumpFile,"w")
                    print(Style.BRIGHT+Fore.YELLOW+"Disassembling binary file...")
                    f.write(out.decode('utf-8'))
                else:
                    dumpFile = target + "_dump.txt"
                    p = Popen(['objdump','-d',target],stdout=PIPE,shell=True)
                    (out, err) = p.communicate()   
                    f = open(dumpFile,"w")
                    print(Style.BRIGHT+Fore.YELLOW+"Disassembling binary file...")
                    f.write(out.decode('utf-8').replace("\n",""))
            except:
                print(Style.BRIGHT+Fore.RED+"File cannot be read!")
                try:
                    sys.exit(0)
                except:
                    os._exit(0)
            f.close()
            if(os.path.isfile(dumpFile)):
                print(Style.BRIGHT+Fore.BLUE+"Output dumped in {} ".format(dumpFile))
                ConvertShellCode(dumpFile,o)
                return True
            else:
                return False
        else:
            print(Style.BRIGHT+Fore.RED+"File may not found! please check your target file path")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
    except:
        print(Style.BRIGHT+Fore.RED+"File may not found or cannot be read! please check your target file path")

def ConvertShellCode(fname,output):
    filtered = []
    dump = open(fname, 'r')
    lines = dump.readlines()
    s = open(output,'w')
    print(Style.BRIGHT+Fore.YELLOW+"Converting dumped output into hexcode...")
    
    s.write("---- BEGIN OF SHELLCODE -----\n")
    for line in lines:
        xsm = line.replace("\n","")
        if 'file format' in xsm or 'Disassembly' in xsm or '...' in xsm or ('<' in xsm and '>' in xsm):
            filtered.append(xsm)
        else:
            if(xsm!=""):
                sh = xsm.split(":\t")
                shell = sh[1].split("\t")
                repShell = shell[0].replace(" ","x")
                shellcode = repShell.split("x")
                for i in range(0,len(shellcode)):
                    if(shellcode[i]!="" and shellcode[i]!=" " and shellcode[i]!="\n"):
                        s.write("\\x"+shellcode[i])

    s.write("\n---- END OF SHELLCODE -----")
                
    print("\n")
    if(os.path.isfile(output)):
        j = open(output,"r")
        print(Style.BRIGHT+Fore.GREEN+j.read())
        print("\n")
        print(Style.BRIGHT+Fore.BLUE+"Hex Shellcode successfully created in '{}'".format(output))
    dump.close()
    s.close()

def argvLength(arr):
    if(len(arr)<2):
        return False
    elif(len(arr)>5):
        return False
    else:
        return True

if(argvLength(sys.argv)==False):
    helpdesk()
    os._exit(0)
else:
    try:
        target = position(sys.argv,"-f")
        output = position(sys.argv,"-o")
        if(dumpBinary(sys.argv[target],sys.argv[output])==True):
            print(Style.BRIGHT+Fore.GREEN+"Hexdump & Shellcode process done!"+Style.BRIGHT+Fore.WHITE+" ")
        else:
            print(Style.BRIGHT+Fore.RED+"Failed to convert! check your arguments and filepath"+Style.BRIGHT+Fore.WHITE+" ")
    except:
        helpdesk()
