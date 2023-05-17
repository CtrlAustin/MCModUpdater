from bs4 import BeautifulSoup
from os.path import exists
import os
import requests

# links are formatted like this:
# modname-modorigin

#modname = "iris"
#curseforgeURL = "https://www.curseforge.com/minecraft/mc-mods/" + modname + "/files"

#modorigin = "modrinth"

fileDirectory = os.path.dirname(os.path.abspath(__file__))

latest = False
seperator = '~'
modpath = fileDirectory + '/mods/'


def clr():
    # _ = call('clear' if os.name == 'posix' else 'cls')
    # os.system('cls')
    print('')
    print('###################################')
    print('# Minecraft mod downloader v0.1.1 #')
    print('###################################')
    print('')


def init():
    if exists('mods.txt'):
        print('mods.txt found!')
    else:
        print('mods.txt not found!\nadd mods to the file and reload this script.')
        mods = open('mods.txt', 'x')
        mods.close()

    if os.path.exists(fileDirectory + '/mods'):
        print('mod folder found!')
        print('skipping setup...')
    else:
        print('creating mods folder...')
        os.mkdir(fileDirectory + "/mods")

    main()

def main():
    clr()
    print(modpath + '\n')
    action = input('Download a specific version: 1 \nDownload latest mods (not recommended): 2 \nAbout: 3 \nQuit: 4 \n')
    if action == '1':
        clr()
        version = input("Enter a version number (x.x.x) \n")
        findspecific(version)

    elif action == '2':
        clr()
        print('Downloading latest mods')
        findlatest()

    elif action == '3':
        clr()
        print('TODO: add curseforge support, \n add mods folder management \n add multiple mod profiles \n')
        input('press enter to continue \n')
        main()

    elif action == '4':
        pass
    else:
        input('Command not found: this action is not supported or is not yet implemented \npress enter to continue...')
        main()
    pass


def findlatest():
    hasdownload = False
    modcount = 0
    latestver = "1.19.2"
    with open('mods.txt') as f:
        for mod in f.read().splitlines():
            modcount = modcount + 1
            modname, modorigin = mod.split(seperator)
            if modcount < 1:
                input("No mods found! add mods to the mods.txt file like this 'modname~modorigin' \nPress enter to continue")
            else:
                modrinthURL = "https://modrinth.com/mod/" + modname + "/versions"
                page = requests.get(modrinthURL)
                soup = BeautifulSoup(page.content, "html.parser")
                wrapper = soup.find_all("div", class_="version-button")
                for element in wrapper:
                    supports = element.find("div", class_="version__supports")
                    item = supports.find_all("span")
                    for content in item:
                        if not exists(modpath + modname + "-" + latestver + ".jar"):
                            if content.text.count(".") > 1:
                                if content.text == latestver:
                                    versionNum = content.text
                                    downloadlink = element.find("a", href=True)
                                    # hasdownload = True
                                    print("downloading " + modname + " v" + latestver + " from " + modorigin + "\n" + downloadlink['href'])
                                    download(downloadlink['href'], modname, versionNum)
    print('downloaded ' + str(modcount) + " mods")
    f.close()
    main()

def findspecific(version):
    hasdownload = False
    modcount = 0
    ver = version
    with open('mods.txt') as f:
        for mod in f.read().splitlines():
            modcount = modcount + 1
            modname, modorigin = mod.split(seperator)
            if modcount < 1:
                input("No mods found! add mods to the mods.txt file like this 'modname~modorigin' \nPress enter to continue")
            else:
                modrinthURL = "https://modrinth.com/mod/" + modname + "/versions"
                page = requests.get(modrinthURL)
                soup = BeautifulSoup(page.content, "html.parser")
                wrapper = soup.find_all("div", class_="version-button")
                for element in wrapper:
                    supports = element.find("div", class_="version__supports")
                    item = supports.find_all("span")
                    for content in item:
                        if not exists(modpath + modname + "-" + ver + ".jar"):
                            if content.text.count(".") > 1:
                                if content.text == ver:
                                    versionNum = content.text
                                    downloadlink = element.find("a", href=True)
                                    print("downloading " + modname + " v" + ver + " from " + modorigin + "\n" + downloadlink['href'])
                                    download(downloadlink['href'], modname, versionNum)
    print('downloaded ' + str(modcount) + " mods")
    f.close()
    main()


def download(download, modname, version):
    print("Downloading...")
    r = requests.get(download)
    filename = modpath + modname + "-" + version + ".jar"
    with open(filename, 'wb') as f:
        f.write(r.content)
    print("Download Complete!")


init()


# hasdownload = False
# modcount = 0
# requestver = version
# with open('mods.txt') as f:
#     for mod in f.read().splitlines():
#         modcount = modcount + 1
#         modname, modorigin = mod.split(seperator)
#         if modcount < 1:
#             input(
#                 "No mods found! add mods to the mods.txt file like this (modname~modorigin) \nPress enter to continue")
#         else:  # modorigin == "modrith":
#             modrinthURL = "https://modrinth.com/mod/" + modname + "/versions"
#             page = requests.get(modrinthURL)
#             soup = BeautifulSoup(page.content, "html.parser")
#             wrapper = soup.find_all("div", class_="version-button")
#             for element in wrapper:
#                 supports = element.find("div", class_="version__supports")
#                 item = supports.find_all("span")
#                 for content in item:
#                     if not hasdownload:
#                         if content.text.count(".") > 1:
#                             if content.text == requestver:
#                                 versionNum = content.text
#                                 downloadlink = element.find("a", href=True)
#                                 hasdownload = True
#                                 print("downloading " + modname + " v" + versionNum + " from " + modorigin + "\n" +
#                                       downloadlink['href'])
#                                 download(downloadlink['href'], modname)





# def findlatest():
#     modcount = 1
#     if modcount <= 0:
#         input("No mods found! add mods to the mods.txt file like this (modname~modorigin) \nPress enter to continue")
#     else:
#         with open('mods.txt') as f:
#             for mod in f.read().splitlines():
#                 modcount = modcount + 1
#                 modname, modorigin = mod.split(seperator)
#                 if modorigin == "modrinth":
#                     modrinthURL = "https://modrinth.com/mod/" + modname + "/versions"
#                     page = requests.get(modrinthURL)
#                     soup = BeautifulSoup(page.content, "html.parser")
#                     # get the parent container of the a tag containing the link to the download
#                     wrapper = soup.find_all("div", class_="version-button")
#
#                     print("downloading " + modname + " from " + modorigin + "\n" + modrinthURL)
#
#                     for element in wrapper:
#                         if not latest:
#                             latest = True
#                             download = element.find("a", href=True)
#                             title = element.find("span", class_="version__title")
#                             supports = element.find("div", class_="version__supports")
#                             item = supports.find_all("span")
#                             for content in item:
#                                 # print(content.text)
#                                 if content.text.count(".") > 1:
#                                     versionNum = content.text
#                                     print(versionNum)
#
#                             # version =
#                             # print(download['href'])
#                             # print(title.text.strip())
#                             download(download, modname)
#
#                 elif modorigin == "curseforge":
#                     # curseforgeURL = "https://www.curseforge.com/minecraft/mc-mods/" + modname + "/files"
#                     curseforgeURL = "https://www.curseforge.com/minecraft/mc-mods/jei/files"
#                     print("downloading " + modname + " from " + modorigin + "\n" + curseforgeURL)
#                     page = requests.get(curseforgeURL)
#
#                     soup = BeautifulSoup(page.content, "html.parser")
#
#                     # get the parent container of the a tag containing the link to the download
#                     wrapper = soup.find_all("tr")
#                     latest = False
#                     for element in wrapper:
#                         print("item")
#                         if not latest:
#                             latest = True
#                             itemcount = 0
#                             for item in wrapper:
#                                 if itemcount < 2:
#                                     itemcount= itemcount + 1
#                                 else:
#                                     download = element.find("a", href=True) + "/file"
#                                     title = element.find("div", class_="mr-2")
#                                     print(download['href'])
#                                     print(title.text.strip())
#                                     download(download, modname)
#
#                 else:
#                     input(modname + " has invalid mod source " + modorigin + ", check mods.txt \npress enter to continue...")
#     main()
