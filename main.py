import xxtea
import zlib
import os
import traveDir
import sys
import random
import zipfile
from io import BytesIO

try:
    from shutil import get_terminal_size as get_terminal_size
except:
    try:
        from backports.shutil_get_terminal_size import get_terminal_size as get_terminal_size
    except:
        pass
try:
    import click

except:
    class click:

        @staticmethod
        def secho(message=None, **kwargs):
            print(message)

        @staticmethod
        def style(**kwargs):
            raise Exception("unsupported style")

banner = """
 ooo        ooooo                      .oooo.              
 `88.       .888'                     d8P'`Y8b             
  888b     d'888   .oooo.    .oooo.o 888    888 ooo. .oo.  
  8 Y88. .P  888  `P  )88b  d88(  "8 888    888 `888P"Y88b 
  8  `888'   888   .oP"888  `"Y88b.  888    888  888   888 
  8    Y     888  d8(  888  o.  )88b `88b  d88'  888   888 
  o8o        o888o `Y888""8o 8""888P'  `Y8bd8P'  o888o o888o 
                     Running Start                           
\n"""


def show_banner():
    colors = ['bright_red', 'bright_green', 'bright_blue', 'cyan', 'magenta']
    try:
        click.style('color test', fg='bright_red')
    except:
        colors = ['red', 'green', 'blue', 'cyan', 'magenta']
    try:
        columns = get_terminal_size().columns
        if columns >= len(banner.splitlines()[1]):
            for line in banner.splitlines():
                if line:
                    fill = int((columns - len(line)) / 2)
                    line = line[0] * fill + line
                    line += line[-1] * fill
                click.secho(line, fg=random.choice(colors))
    except:
        pass


class ColorPrinter:
    @staticmethod
    def print_red_text(content, end="\n"):
        print("\033[1;31m %s \033[0m" % content, end=end),

    @staticmethod
    def print_green_text(content, end="\n"):
        print("\033[1;32m %s \033[0m" % content, end=end),

    @staticmethod
    def print_blue_text(content, end="\n"):
        print("\033[1;34m %s \033[0m" % content, end=end),

    @staticmethod
    def print_cyan_text(content, end="\n"):
        print("\033[1;36m %s \033[0m" % content, end=end),

    @staticmethod
    def print_white_text(content, end="\n"):
        print("\033[1;37m %s \033[0m" % content, end=end),


def read_jsc_file(path):
    f = open(path, "rb")
    data = f.read()
    f.close()
    return data


def save_file(fileDir, outData):
    rootPath = os.path.split(fileDir)[0]
    try:
        os.makedirs(rootPath)
    except OSError:
        if not os.path.exists(rootPath):
            raise Exception("Error: create directory %s failed." % rootPath)
    if fileDir.endswith("c"):
        file = fileDir[:-1]
    with open(file, "w", encoding="utf-8") as fd:
        fd.write(outData)
    fd.close()


def decrypt(filePath, key):
    data = read_jsc_file(path=filePath)
    dec_data = xxtea.decrypt(data=data, key=key, padding=False)
    if dec_data[:2] == b"PK":
        fio = BytesIO(dec_data)
        fzip = zipfile.ZipFile(file=fio)
        dec_data = fzip.read(fzip.namelist()[0]).decode("utf-8")
    elif dec_data[:2] == b"\x1f\x8b":
        dec_data = bytes(zlib.decompress(dec_data, 16 + zlib.MAX_WBITS)).decode("utf-8")
    else:
        dec_data = bytes(dec_data).decode("utf-8")
    return dec_data


def batch_decrypt(srcDir, xxtea_key):
    if not os.path.exists(srcDir):
        ColorPrinter.print_white_text("Error:FileNotFound")
        exit(1)
    rootDir = os.path.split(srcDir)[0]
    outDir = rootDir
    if outDir[-2:-1] != "\\":
        outDir += "\\"
    outDir += "out\\"
    traveDir.deep_iterate_dir(srcDir)
    files_list = traveDir.getfileslist()
    for file_path in files_list:
        ColorPrinter.print_green_text("Decrypting flie:{0}".format(file_path))
        decData = decrypt(filePath=file_path, key=xxtea_key)
        outFile = outDir + file_path[len(rootDir + os.path.split(srcDir)[1]) + 1:]
        save_file(fileDir=outFile, outData=decData)
        print("        Save flie:{0}".format(outFile))


def main():
    ColorPrint = ColorPrinter()
    # print(sys.argv)
    if len(sys.argv) != 4:
        print("\nThis is decrypt for Coco2d-js .jsc.")
        ColorPrint.print_white_text("Usage : ")
        print("        python {0} [-d] [xxteaKey] [jscDir]".format(sys.argv[0]))
        ColorPrint.print_white_text("Example : ")
        print(r"        python {0} -d 6362d9fe-c3ad-47 C:\DecJsc-master\src".format(sys.argv[0]))
        ColorPrint.print_white_text("Tips : ")
        print("        -d or -decrypt [decrypt]")
        print("        If you have any questions, please contact [ MasonShi@88.com ]\n")
        exit(1)
    instruct = sys.argv[1]
    xxtea_key = sys.argv[2]
    srcDir = sys.argv[3]
    if instruct[1:2] == "d":
        show_banner()

        batch_decrypt(srcDir=srcDir, xxtea_key=xxtea_key)

        ColorPrint.print_white_text("Running exit...\n")


if __name__ == "__main__":
     main()
