import os
import errno
import urllib.request

commandList = ["newproject", "cls", "clear",
               "exit", "listprojects", "addproject"]

fileCreated = False


def getLibFile(libPath):
    filePath = os.path.join(libPath, "p5.js")
    url = "https://www.github.com/processing/p5.js/releases/download/v1.4.0/p5.js"
    u = urllib.request.urlopen(url)
    file = open(filePath, 'wb')
    meta = u.info()
    file_size = int(meta.get_all("Content-Length")[0])
    print("\n\t[ DOWNLOAD INFO ]:\tDownloading: %s, Bytes: %s" %
          ("p5.js", file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        file.write(buffer)
        status = r"%10d [%3.2f%%]" % (
            file_size_dl, file_size_dl * 100 / file_size)
        status = status + chr(8)*(len(status)+1)
        print(f"\t\tCompleted %: {status}", end="\r")


def makeHtmlFile(path, libs):
    with open(path + "/index.html", "w") as f:
        htmlTitle = input("\t[ PROMPT ] Enter your html page title: ")
        if(htmlTitle == ""):
            print(
                "\n\t[ ERROR ]: Please set a valid title for the html page, Empty title is not allowed")
            return None
        print("\t[ LOG ] Setting default language for html page: en")
        if libs == False:
            f.write(
                f'<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<title>{htmlTitle}</title>\n\t</head>\n\t<body>\n\t\t<script src="sketch.js"></script>\n\n\t\t<script src="https://cdn.jsdelivr.net/npm/p5@1.4.0/lib/p5.js"></script>\n\t</body>\n</html>')
        elif libs == True:
            libPath = os.path.join(path, "libs")
            os.mkdir(libPath)
            f.write(
                f'<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<title>{htmlTitle}</title>\n\t</head>\n\t<body>\n\t\t<script src="index.js"></script>\n\n\t\t<script src="./libs/p5.js"></script>\n\t</body>\n</html>')
            getLibFile(libPath)
    f.close()


def makeSketchFile(path):
    with open(path + "/sketch.js", "w") as f:
        f.write(
            "function setup() {\n\tcreateCanvas(400, 400);\n}\n\nfunction draw() {\n\tbackground(220);\n}")
    f.close()


def createProject(path, libs):
    try:
        os.mkdir(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            print(
                "[ Error ]: Cannot create project as the specified directory/folder already exists.")
            return None
        elif exc.errno == errno.EACCES:
            print(
                "[ Error ]: Permission denied, You cannot create a project in that directory, if you however want to make it there then try running `sudo   {python program name}` for linux or for windows try running the cmd or you terminal has administrator.")
            return None
        elif exc.errno == errno.ENOENT:
            print(
                "[ Error ]: Cannot create project as the specified (directory/folder)'s parent directory does not exist.")
            return None
    makeHtmlFile(path, libs)
    makeSketchFile(path)
    global fileCreated
    with open("projectList.txt", "a") as f:
        fileCreated = True
        f.write(f"{path}\n")
    f.close()


def parse(comList):
    command = comList[0]
    command = command.lower()
    comList.pop(0)
    args = comList[0]
    comList.pop(0)
    if(command in commandList):
        if(command == "newproject"):
            if(len(args) < 1):
                print(
                    f"[ ERROR ]: Not enough arguments for `{command}` command.")
                return None
            elif(len(args) > 2):
                print(
                    f"[ ERROR ]: Too many arguments for `{command}` command.\n")
                return None
            if(len(args) == 1):
                installLibsInput = input(
                    "\t[ PROMPT ] Do you want to install the p5.js file or use the cdn (Choose 1 to install, 2 to use cdn)? ")
                if(installLibsInput == "1"):
                    createProject(args[0], True)
                elif(installLibsInput == "2"):
                    createProject(args[0], False)
                else:
                    print(
                        f'\t[ ERROR ]: `{installLibsInput}` Not understood choose only 1 or 2.')
                    return None
            elif((len(args) == 2)):
                if(args[1] == "-libs"):
                    createProject(args[0], True)
                elif(args[1] != "-libs"):
                    print(f"[ ERROR ]: Unkown argument `{args[1]}`")
        elif(command == "listprojects"):
            if(fileCreated == False):
                try:
                    f = open("projectList.txt", "x")
                except OSError as exc:
                    if exc.errno == errno.EEXIST:
                        pass
            with open("projectList.txt", "r") as f:
                projects = f.readlines()
                if(projects == ""):
                    print(
                        "\n\t[ PROJECTS ]:\tNo projects currently available, add a project \n\t\t\tfrom existing folder or create a project with boilerplate code.")
                    return None
                else:
                    print("\n\tAvailable Project List (Path):")
                    print(f"\t\t{projects}")
            f.close()
        elif(command == "addproject"):
            indexHtmlFiles = []
            jsFiles = []
            for root, dirs, files in os.walk(args[0]):
                for file in files:
                    if file.endswith('.js'):
                        jsFiles.append(file)
                    if file == "index.html":
                        indexHtmlFiles.append(file)
            if(len(indexHtmlFiles) > 1):
                print(
                    "\n\t[ ERROR ]: Multiple `index.html` files. Please only include one `index.html`.")
                return None
            elif(len(jsFiles) < 1):
                print(
                    "\n\t[ ERROR ]: No js files were found. This does not look like a project directory.")
                return None
            try:
                f = open("projectList.txt", "x")
                f.close()
            except OSError as exc:
                if exc.errno == errno.EEXIST:
                    pass
            with open("projectList.txt", "a") as a:
                a.write(args[0])
        elif(command == "clear" or "cls"):
            if(len(args) == 0):
                os.system('clear')
            else:
                print(
                    f"[ ERROR ]: Too many arguments for `{command}` command.\n")
                return None
    elif(command not in commandList):
        print(
            f"`{command}` Not understood only use valid commands, Type help to print all commands.")


def getArgs(text):
    splitted = text.split()
    if(len(splitted) == 0):
        print("[ ERROR ]: No argument provided, Quitting the program.\n")
        exit()
    command = splitted[0]
    if(command == "exit"):
        if(len(splitted[1]) > 0):
            print("[ ERROR ]: Too many arguments for `exit` command.\n")
        else:
            exit()
    splitted.pop(0)
    return [command, splitted]


while True:
    parse(getArgs(input("\n@> ")))
