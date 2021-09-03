# -*- coding: utf-8 -*-
# @Time    : 2021-03-31 22:03
# @Author  : Mas0n
# @FileName: main.py
# @Software: PyCharm
# @Blog    ：https://blog.shi1011.cn

import xxtea
import zlib
import os
from traveDir import depthIteratePath
from loguru import logger
import sys
import random
import zipfile
from io import BytesIO
import json

def setExtFile(rootPath, type):
    filePath = os.path.join(rootPath, "JSC-DECRYPTION")
    with open(filePath, "w") as f:
        f.write(json.dump({
            "Tools": "jsc-Decrytion",
            "Verify": "True",
            "Type": type
        }))


def getExtFile(rootPath, type):
    filePath = os.path.join(rootPath, "JSC-DECRYPTION")
    with open(filePath, "r", encoding="utf-8") as f:
        try:
            rePackType = json.loads(f.read())
        except json.JSONDecodeError:
            logger.error("jsonDecodeError")
            exit(-1)

    if rePackType["Tools"] != "jsc-Decrytion" or rePackType["Verify"] != "True":
        logger.error("read JSC-DECRYPTION Error")
        exit(-1)

    return rePackType["Type"]


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


def readJscFile(path):
    f = open(path, "rb")
    data = f.read()
    f.close()
    return data


def saveFile(fileDir, outData):
    """
    保存解密文件

    :param fileDir: 文件目录
    :param outData: 保存数据
    :return: None
    """
    rootPath = os.path.split(fileDir)[0]
    try:
        os.makedirs(rootPath)
    except OSError:
        if not os.path.exists(rootPath):
            raise Exception("Error: create directory %s failed." % rootPath)
    if fileDir.endswith("c"):
        file = fileDir[:-1]

    if isinstance(outData, str):  # 判断数据类型 以防utf8转码失败的文件无法保存
        with open(file, "w", encoding="utf-8") as fd:
            fd.write(outData)
    else:
        with open(file, "wb") as fd:
            fd.write(outData)
    fd.close()


def decrypt(filePath, key):
    """
    核心为XXtea 附zip/gzip压缩

    :param filePath: 文件目录
    :param key: xxteaKey
    :return: None
    """
    if key == "NONE":
        key = "\x00" * 16
    elif len(key) < 16:
        key += "".join("\0" * (16 - len(key)))  # key填充
    data = readJscFile(path=filePath)
    dec_data = xxtea.decrypt(data=data, key=key, padding=False)
    if dec_data[:2] == b"PK":
        decType = "zip"
        fio = BytesIO(dec_data)
        fzip = zipfile.ZipFile(file=fio)
        dec_data = fzip.read(fzip.namelist()[0]).decode("utf-8")
    elif dec_data[:2] == b"\x1f\x8b":
        decType = "gzip"
        dec_data = bytes(zlib.decompress(dec_data, 16 + zlib.MAX_WBITS)).decode("utf-8")
    else:
        decType = "unknown"
        try:
            dec_data = bytes(dec_data).decode("utf-8")
        except UnicodeDecodeError:
            ColorPrinter.print_blue_text("    This file looks like have some unknown byte, try save as unknown files")

    return decType, dec_data


def batchDecrypt(srcDir, xxteaKey):
    """
    块解密

    :param srcDir: 文件夹目录
    :param xxteaKey: xxteaKey
    :return: None
    """
    if not os.path.exists(srcDir):
        ColorPrinter.print_white_text("Error:FileNotFound")
        exit(1)
    rootDir = os.path.split(srcDir)[0]
    outDir = rootDir
    outDir = os.path.join(rootDir, "out")
    if os.path.isfile(srcDir):
        filesPathArr = [srcDir]
    elif os.path.isdir(srcDir):
        filesPathArr = depthIteratePath([".jsc"]).getDepthDir(srcDir)
    else:
        logger.error("UnknownError -> setPathExt")
        exit(-1)

    for filePath in filesPathArr:
        ColorPrinter.print_green_text("Decrypting flie:{0}".format(filePath))
        decType, decData = decrypt(filePath=filePath, key=xxteaKey)
        outFile = outDir + filePath[len(rootDir + os.path.split(srcDir)[1]) + 1:]
        saveFile(fileDir=outFile, outData=decData)
        print("        Save flie:{0}".format(outFile))


def encrypt():
    # TODO: no process
    pass


def batchEncrypt():
    # TODO: no process
    pass


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
        print("        If the TEA is 16 bytes of \\x00, please fill in NONE")
        print("        If you have any questions, please contact [ MasonShi@88.com ]\n")
        exit(1)
    instruct = sys.argv[1]
    xxtea_key = sys.argv[2]
    srcDir = sys.argv[3]
    if instruct[1:2] == "d":
        show_banner()
        batchDecrypt(srcDir=srcDir, xxteaKey=xxtea_key)
        ColorPrint.print_white_text("    Running exit...\n")


if __name__ == "__main__":
     main()
