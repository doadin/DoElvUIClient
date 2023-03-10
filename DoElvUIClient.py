#import subprocess
import json
import requests
import urllib.request
from zipfile import ZipFile
#import zipfile
import tkinter as tk
import os
import distutils.dir_util
import shutil
import tempfile
from bs4 import BeautifulSoup
import winreg
LocalElvUIVersion = None
remoteElvUIVersion = None
remoteElvUIURL = None
LocalElvUIClassicVersion = None
LocalElvUIWrathVersion = None

window = tk.Tk()
title = window.title("DoElvUIUpdater")
greeting = tk.Label(text="Welcome to the Do ElvUI Updater")
greeting.pack()

access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
#InstallLocation key in
#Uninstall\World of Warcraft + \_retail_\= Retail
#Uninstall\World of Warcraft Classic Era + \_classic_era_\ = Classic Install Location
#Uninstall\Wrath of the Lich King Classic + \_classic_\ = Wrath

try:
    access_key = winreg.OpenKey(access_registry, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\World of Warcraft")
    WoWDir = winreg.QueryValueEx(access_key, 'InstallLocation')[0]
except:
    pass
try:
    access_key = winreg.OpenKey(access_registry, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\World of Warcraft Classic Era")
    WoWClassicDir = winreg.QueryValueEx(access_key, 'InstallLocation')[0]
except:
    pass
try:
    access_key = winreg.OpenKey(access_registry, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Wrath of the Lich King Classic")
    WoWWrathDir = winreg.QueryValueEx(access_key, 'InstallLocation')[0]
except:
    pass

#result = subprocess.run(['git', 'rev-list', '--tags', '--max-count=1'], stdout=subprocess.PIPE)
#gitVersion = result.stdout.decode('utf-8')

response = requests.get("https://api.github.com/repos/tukui-org/ElvUI/tags?per_page=1")
responce_json = response.text.replace("[","").replace("]","")

data_dict = json.loads(responce_json)

if data_dict["name"]:
    remoteElvUIVersion = data_dict["name"]
if data_dict["zipball_url"]:
    remoteElvUIURL = data_dict["zipball_url"]
if data_dict["commit"]["sha"]:
    remoteElvUISHA = data_dict["commit"]["sha"]

label = tk.Label(text="Latest ElvUI Vesion: " + remoteElvUIVersion)
label.pack()

tempdir = tempfile.gettempdir()
#print(tempdir)

def install_elvui_classic():
    # https://www.tukui.org/downloads/elvui-13.21.zip

    urllib.request.urlretrieve(remoteElvUIURL, tempdir + "\\" + remoteElvUIVersion + ".zip")
    #urllib.request.urlretrieve("https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip", remoteElvUIVersion + ".zip")
    with ZipFile(tempdir + "\\" + remoteElvUIVersion + ".zip", 'r') as zObject:
        zObject.extractall(path = tempdir + "\\" + "DoElvUIUpdater")
    #os.rename("E:\\test\\AddOns\\ElvUI-main","E:\\test\\AddOns\\ElvUI")
    #distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns")
    try:
        distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWClassicDir + '\\_classic_era_\\Interface\\AddOns')
        window.destroy()
    
        greeting = tk.Label(text="Welcome to the Do ElvUI Updater")
        greeting.pack()
    
        label = tk.Label(text="Classic Install Complete!")
        label.pack()
        window.mainloop()
        shutil.rmtree(tempdir + "\\" + "DoElvUIUpdater")
        os.remove(tempdir + "\\" + remoteElvUIVersion + ".zip")
        #shutil.copytree("E:\\test\\AddOns\\tukui-org-ElvUI-" + remoteElvUISHA[0:7], "E:\\test", copy_function = shutil.copy)
    except:
        window.destroy()
        classicinstallerror = tk.Label(text="Classic Install Faiiled! Please report this!")
        classicinstallerror.pack()
        window.mainloop()


def install_elvui_wrath():
    # https://www.tukui.org/downloads/elvui-13.21.zip

    urllib.request.urlretrieve(remoteElvUIURL, tempdir + "\\" + remoteElvUIVersion + ".zip")
    #urllib.request.urlretrieve("https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip", remoteElvUIVersion + ".zip")
    with ZipFile(tempdir + "\\" + remoteElvUIVersion + ".zip", 'r') as zObject:
        zObject.extractall(path = tempdir + "\\" + "DoElvUIUpdater")
    #os.rename("E:\\test\\AddOns\\ElvUI-main","E:\\test\\AddOns\\ElvUI")
    #distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns")
    try:
        distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWWrathDir + '\\_classic_\\Interface\\AddOns')
        window.destroy()
    
        greeting = tk.Label(text="Welcome to the Do ElvUI Updater")
        greeting.pack()
    
        label = tk.Label(text="Wrath Install Complete!")
        label.pack()
        window.mainloop()
        shutil.rmtree(tempdir + "\\" + "DoElvUIUpdater")
        os.remove(tempdir + "\\" + remoteElvUIVersion + ".zip")
        #shutil.copytree("E:\\test\\AddOns\\tukui-org-ElvUI-" + remoteElvUISHA[0:7], "E:\\test", copy_function = shutil.copy)
    except:
        window.destroy()
        wrathinstallerror = tk.Label(text="Wrath Install Faiiled! Please report this!")
        wrathinstallerror.pack()
        window.mainloop()

def install_elvui_retail():
    # https://www.tukui.org/downloads/elvui-13.21.zip

    urllib.request.urlretrieve(remoteElvUIURL, tempdir + "\\" + remoteElvUIVersion + ".zip")
    #urllib.request.urlretrieve("https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip", remoteElvUIVersion + ".zip")
    with ZipFile(tempdir + "\\" + remoteElvUIVersion + ".zip", 'r') as zObject:
        zObject.extractall(path = tempdir + "\\" + "DoElvUIUpdater")
    #os.rename("E:\\test\\AddOns\\ElvUI-main","E:\\test\\AddOns\\ElvUI")
    #distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns")
    try:
        distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWDir + '\\_retail_\\Interface\\AddOns')
        window.destroy()
    
        greeting = tk.Label(text="Welcome to the Do ElvUI Updater")
        greeting.pack()
    
        label = tk.Label(text="Retail Install Complete!")
        label.pack()
        window.mainloop()
        shutil.rmtree(tempdir + "\\" + "DoElvUIUpdater")
        os.remove(tempdir + "\\" + remoteElvUIVersion + ".zip")
        #shutil.copytree("E:\\test\\AddOns\\tukui-org-ElvUI-" + remoteElvUISHA[0:7], "E:\\test", copy_function = shutil.copy)
    except:
        window.destroy()
        retailinstallerror = tk.Label(text="Retail Install Faiiled! Please report this!")
        retailinstallerror.pack()
        window.mainloop()

try:
    try:
        WoWDir
    except NameError:
        label = None
    #ElvUIToC = open('C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns\\ElvUI\\ElvUI_Mainline.toc', 'r')
    ElvUILocation = WoWDir + '\_retail_\Interface\AddOns\ElvUI\ElvUI_Mainline.toc'
    ElvUIToC = open(ElvUILocation, 'r')
    for line in ElvUIToC:
        if line.find("Version") != -1:
           ElvUIToCVersionLine = line
    ElvUIToC.close()
    if ElvUIToCVersionLine:
        ElvUIToCVersionNumber = ElvUIToCVersionLine.partition(":")[2]
        LocalElvUIVersion = "v" + ElvUIToCVersionNumber.strip()
    
    label = tk.Label(text="Installed Retail ElvUI Vesion: " + LocalElvUIVersion)
except:
    pass
try: 
    label
except NameError:
    label = tk.Label(text="Installed Retail ElvUI Vesion: None")
    ElvUIRetailInstall = tk.Button(
        text="Install ElvUI To Retail",
        width=25,
        height=1,
        bg="green",
        fg="white",
        command=lambda : install_elvui_retail(),
    )
    ElvUIRetailInstall.pack()
try:
    label.pack()
except:
    pass

try:
    try:
        WoWClassicDir
    except NameError:
        ElvUIClassicVersionlabel = None
    #ElvUIToC = open('C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns\\ElvUI\\ElvUI_Mainline.toc', 'r')
    ElvUIClassicLocation = WoWClassicDir + '\_classic_era_\Interface\AddOns\ElvUI\ElvUI_Classic.toc'
    ElvUIClassicToC = open(ElvUIClassicLocation, 'r')
    for line in ElvUIClassicToC:
        if line.find("Version") != -1:
           ElvUIClassicToCVersionLine = line
    ElvUIClassicToC.close()
    if ElvUIClassicToCVersionLine:
        ElvUIClassicToCVersionLine = ElvUIClassicToCVersionLine.partition(":")[2]
        LocalElvUIClassicVersion = "v" + ElvUIClassicToCVersionLine.strip()
    
    ElvUIClassicVersionlabel = tk.Label(text="Installed Classic ElvUI Vesion: " + LocalElvUIClassicVersion)
except:
    pass

try: 
    ElvUIClassicVersionlabel
except NameError:
    ElvUIClassicVersionlabel = tk.Label(text="Installed Classic ElvUI Vesion: None")
    ElvUIClassicInstall = tk.Button(
        text="Install ElvUI To Classic",
        width=25,
        height=1,
        bg="green",
        fg="white",
        command=lambda : install_elvui_classic(),
    )
    ElvUIClassicInstall.pack()
try:
    ElvUIClassicVersionlabel.pack()
except:
    pass

try:
    try:
        WoWWrathDir
    except NameError:
        ElvUIWrathVersionlabel = None
    #ElvUIToC = open('C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns\\ElvUI\\ElvUI_Mainline.toc', 'r')
    ElvUIWrathLocation = WoWWrathDir + '\_classic_\Interface\AddOns\ElvUI\ElvUI_Classic.toc'
    ElvUIWrathToC = open(ElvUIWrathLocation, 'r')
    for line in ElvUIWrathToC:
        if line.find("Version") != -1:
           ElvUIWrathToCVersionLine = line
    ElvUIWrathToC.close()
    if ElvUIWrathToCVersionLine:
        ElvUIWrathToCVersionLine = ElvUIWrathToCVersionLine.partition(":")[2]
        LocalElvUIWrathVersion = "v" + ElvUIWrathToCVersionLine.strip()
    
    ElvUIWrathVersionlabel = tk.Label(text="Installed Wrath ElvUI Vesion: " + LocalElvUIWrathVersion)
except:
    pass
try: 
    ElvUIWrathVersionlabel
except NameError:
    ElvUIWrathVersionlabel = tk.Label(text="Installed Wrath ElvUI Vesion: None")
    ElvUIWrathInstall = tk.Button(
        text="Install ElvUI To Wrath",
        width=25,
        height=1,
        bg="green",
        fg="white",
        command=lambda : install_elvui_wrath(),
    )
    ElvUIWrathInstall.pack()
try:
    ElvUIWrathVersionlabel.pack()
except:
    pass


def run_update():
    # https://www.tukui.org/downloads/elvui-13.21.zip

    urllib.request.urlretrieve(remoteElvUIURL, tempdir + "\\" + remoteElvUIVersion + ".zip")
    #urllib.request.urlretrieve("https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip", remoteElvUIVersion + ".zip")
    with ZipFile(tempdir + "\\" + remoteElvUIVersion + ".zip", 'r') as zObject:
        zObject.extractall(path = tempdir + "\\" + "DoElvUIUpdater")
    #os.rename("E:\\test\\AddOns\\ElvUI-main","E:\\test\\AddOns\\ElvUI")
    #distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns")
    try:
        if (LocalElvUIVersion and remoteElvUIVersion) and (LocalElvUIVersion != remoteElvUIVersion):
            distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWDir + '\\_retail_\\Interface\\AddOns')
    except:
        pass
    try:
      if (LocalElvUIClassicVersion and remoteElvUIVersion) and (LocalElvUIClassicVersion != remoteElvUIVersion):
          distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWClassicDir + '\\_classic_era_\\Interface\\AddOns')
    except:
        pass
    try:
      if (LocalElvUIWrathVersion and remoteElvUIVersion) and (LocalElvUIWrathVersion != remoteElvUIVersion):
          distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWWrathDir + '\\_classic_\\Interface\\AddOns')
    except:
        pass
    shutil.rmtree(tempdir + "\\" + "DoElvUIUpdater")
    os.remove(tempdir + "\\" + remoteElvUIVersion + ".zip")
    #shutil.copytree("E:\\test\\AddOns\\tukui-org-ElvUI-" + remoteElvUISHA[0:7], "E:\\test", copy_function = shutil.copy)

    window.destroy()

    greeting = tk.Label(text="Welcome to the Do ElvUI Updater")
    greeting.pack()

    label = tk.Label(text="Update Complete!")
    label.pack()
    window.mainloop()

# LocalElvUIClassicVersion
# LocalElvUIWrathVersion
if (LocalElvUIVersion and remoteElvUIVersion) and (LocalElvUIVersion != remoteElvUIVersion) and remoteElvUIURL or (LocalElvUIClassicVersion and remoteElvUIVersion) and (LocalElvUIClassicVersion != remoteElvUIVersion) and remoteElvUIURL or (LocalElvUIWrathVersion and remoteElvUIVersion) and (LocalElvUIWrathVersion != remoteElvUIVersion) and remoteElvUIURL:
    changelogbox = tk.Text(window,width=45, height= 20,wrap="word")
    #changelogresponse = requests.get("https://api.github.com/repos/tukui-org/ElvUI/tags?per_page=1")
    #changelogresponsetext = response.text.replace("[","").replace("]","")

    s = requests.get("https://www.tukui.org/download.php?ui=elvui&changelog")
    soup = BeautifulSoup(s.content, "html.parser")
    soupdiv = soup.find("div", id='changelog')
    for data in soupdiv(['style', 'script']):
        # Remove tags
        data.decompose()
    #print(soup.find("div", id='changelog'))
    #print(' '.join(soup.stripped_strings))
    #changelogbox.insert('1.0',' '.join(soupdiv.stripped_strings))
    changelogbox.insert('1.0',soupdiv.text)

    changelogbox.pack(expand= 1)

    button = tk.Button(
        text="Update",
        width=25,
        height=5,
        bg="red",
        fg="white",
        command=run_update,
    )
    button.pack()
else:
    label = tk.Label(text="You Are Up to Date!")
    label.pack()

window.mainloop()
