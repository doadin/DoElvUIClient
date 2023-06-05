#import subprocess
import json
import requests
import urllib.request
from zipfile import ZipFile
#import zipfile
import tkinter as tk
from tkinter import ttk
import os
import shutil
import tempfile
#from bs4 import BeautifulSoup
import winreg
LocalElvUIVersion = None
remoteElvUIVersion = None
remoteElvUIURL = None
LocalElvUIClassicVersion = None
LocalElvUIWrathVersion = None

try:
    import darkdetect
    if darkdetect.isDark():
        lightdarktheme = "dark"
    if darkdetect.isLight():
        lightdarktheme = "light"    
except ImportError:
    lightdarktheme = "light"

try:
    import sv_ttk
    svtheme = True
except ImportError:
    svtheme = False
#sv_ttk.set_theme(lightdarktheme)

window = tk.Tk()
title = window.title("DoElvUIUpdater")
greeting = ttk.Label(text="Welcome to the Do ElvUI Updater")
greeting.pack()

access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
#InstallLocation key in
#Uninstall\World of Warcraft + \_retail_\= Retail
#Uninstall\World of Warcraft Classic Era + \_classic_era_\ = Classic Install Location
#Uninstall\Wrath of the Lich King Classic + \_classic_\ = Wrath
RetailFound = True
ClassicFound = True
WrathFound = True

try:
    access_key = winreg.OpenKey(access_registry, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\World of Warcraft")
    WoWDir = winreg.QueryValueEx(access_key, 'InstallLocation')[0]
except:
    RetailFound = False
    pass
try:
    access_key = winreg.OpenKey(access_registry, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\World of Warcraft Classic Era")
    WoWClassicDir = winreg.QueryValueEx(access_key, 'InstallLocation')[0]
except:
    ClassicFound = False
    pass
try:
    access_key = winreg.OpenKey(access_registry, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Wrath of the Lich King Classic")
    WoWWrathDir = winreg.QueryValueEx(access_key, 'InstallLocation')[0]
except:
    WrathFound = False
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

label = ttk.Label(text="Latest ElvUI Vesion: " + remoteElvUIVersion)
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
        shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWClassicDir + '\\_classic_era_\\Interface\\AddOns', dirs_exist_ok = True)
        for widget in window.winfo_children():
            widget.destroy()
    
        greeting = ttk.Label(text="Welcome to the Do ElvUI Updater")
        greeting.pack()
    
        label = ttk.Label(text="Classic Install Complete!")
        label.pack()
        title = window.title("DoElvUIUpdater")
        if svtheme:
            sv_ttk.set_theme(lightdarktheme)
        window.mainloop()
        shutil.rmtree(tempdir + "\\" + "DoElvUIUpdater")
        os.remove(tempdir + "\\" + remoteElvUIVersion + ".zip")
        #shutil.copytree("E:\\test\\AddOns\\tukui-org-ElvUI-" + remoteElvUISHA[0:7], "E:\\test", copy_function = shutil.copy)
    except:
        for widget in window.winfo_children():
            widget.destroy()
        classicinstallerror = ttk.Label(text="Classic Install Faiiled! Please report this!")
        classicinstallerror.pack()
        if svtheme:
            sv_ttk.set_theme(lightdarktheme)
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
        shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWWrathDir + '\\_classic_\\Interface\\AddOns', dirs_exist_ok = True)
        for widget in window.winfo_children():
            widget.destroy()
    
        greeting = ttk.Label(text="Welcome to the Do ElvUI Updater")
        greeting.pack()
    
        label = ttk.Label(text="Wrath Install Complete!")
        label.pack()
        title = window.title("DoElvUIUpdater")
        if svtheme:
            sv_ttk.set_theme(lightdarktheme)
        window.mainloop()
        shutil.rmtree(tempdir + "\\" + "DoElvUIUpdater")
        os.remove(tempdir + "\\" + remoteElvUIVersion + ".zip")
        #shutil.copytree("E:\\test\\AddOns\\tukui-org-ElvUI-" + remoteElvUISHA[0:7], "E:\\test", copy_function = shutil.copy)
    except:
        for widget in window.winfo_children():
            widget.destroy()
        wrathinstallerror = ttk.Label(text="Wrath Install Faiiled! Please report this!")
        wrathinstallerror.pack()
        if svtheme:
            sv_ttk.set_theme(lightdarktheme)
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
        shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWDir + '\\_retail_\\Interface\\AddOns', dirs_exist_ok = True)
        for widget in window.winfo_children():
            widget.destroy()
    
        greeting = ttk.Label(text="Welcome to the Do ElvUI Updater")
        greeting.pack()
    
        label = ttk.Label(text="Retail Install Complete!")
        label.pack()
        title = window.title("DoElvUIUpdater")
        if svtheme:
            sv_ttk.set_theme(lightdarktheme)
        window.mainloop()
        shutil.rmtree(tempdir + "\\" + "DoElvUIUpdater")
        os.remove(tempdir + "\\" + remoteElvUIVersion + ".zip")
        #shutil.copytree("E:\\test\\AddOns\\tukui-org-ElvUI-" + remoteElvUISHA[0:7], "E:\\test", copy_function = shutil.copy)
    except:
        for widget in window.winfo_children():
            widget.destroy()
        retailinstallerror = ttk.Label(text="Retail Install Faiiled! Please report this!")
        retailinstallerror.pack()
        if svtheme:
            sv_ttk.set_theme(lightdarktheme)
        window.mainloop()

#Retail
if RetailFound:
    try:
        try:
            WoWDir
        except NameError:
            pass
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
        
        ElvUIRetailVersionlabel = ttk.Label(text="Installed Retail ElvUI Vesion: " + LocalElvUIVersion)
    except Exception as e:
        print(e)
        pass
    try: 
        ElvUIRetailVersionlabel
    except NameError:
        ElvUIRetailVersionlabel = ttk.Label(text="Installed Retail ElvUI Vesion: None")
        ElvUIRetailVersionlabel.pack()
        ElvUIRetailInstall = ttk.Button(
            text="Install ElvUI To Retail",
            width=25,
            command=lambda : install_elvui_retail(),
        )
        ElvUIRetailInstall.pack(after = ElvUIRetailVersionlabel)
    try:
        ElvUIRetailVersionlabel.pack()
    except:
        pass

#Classic
if ClassicFound:
    try:
        try:
            WoWClassicDir
        except NameError:
            pass
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
        
        ElvUIClassicVersionlabel = ttk.Label(text="Installed Classic ElvUI Vesion: " + LocalElvUIClassicVersion)
    except:
        pass
    
    try: 
        ElvUIClassicVersionlabel
    except NameError:
        ElvUIClassicVersionlabel = ttk.Label(text="Installed Classic ElvUI Vesion: None")
        ElvUIClassicVersionlabel.pack()
        ElvUIClassicInstall = ttk.Button(
            text="Install ElvUI To Classic",
            width=25,
            command=lambda : install_elvui_classic(),
        )
        ElvUIClassicInstall.pack(after = ElvUIClassicVersionlabel)
    try:
        ElvUIClassicVersionlabel.pack()
    except:
        pass

#Wrath
if WrathFound:
    try:
        try:
            WoWWrathDir
        except NameError:
            pass
        #ElvUIToC = open('C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns\\ElvUI\\ElvUI_Mainline.toc', 'r')
        ElvUIWrathLocation = WoWWrathDir + '\_classic_\Interface\AddOns\ElvUI\ElvUI_Wrath.toc'
        ElvUIWrathToC = open(ElvUIWrathLocation, 'r')
        for line in ElvUIWrathToC:
            if line.find("Version") != -1:
               ElvUIWrathToCVersionLine = line
        ElvUIWrathToC.close()
        if ElvUIWrathToCVersionLine:
            ElvUIWrathToCVersionLine = ElvUIWrathToCVersionLine.partition(":")[2]
            LocalElvUIWrathVersion = "v" + ElvUIWrathToCVersionLine.strip()
        
        ElvUIWrathVersionlabel = ttk.Label(text="Installed Wrath ElvUI Vesion: " + LocalElvUIWrathVersion)
    except:
        pass
    try: 
        ElvUIWrathVersionlabel
    except NameError:
        ElvUIWrathVersionlabel = ttk.Label(text="Installed Wrath ElvUI Vesion: None")
        ElvUIWrathVersionlabel.pack()
        ElvUIWrathInstall = ttk.Button(
            text="Install ElvUI To Wrath",
            width=25,
            command=lambda : install_elvui_wrath(),
        )
        ElvUIWrathInstall.pack(after = ElvUIWrathVersionlabel)
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
            shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWDir + '\\_retail_\\Interface\\AddOns', dirs_exist_ok = True)
    except:
        pass
    try:
      if (LocalElvUIClassicVersion and remoteElvUIVersion) and (LocalElvUIClassicVersion != remoteElvUIVersion):
          shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWClassicDir + '\\_classic_era_\\Interface\\AddOns', dirs_exist_ok = True)
    except:
        pass
    try:
      if (LocalElvUIWrathVersion and remoteElvUIVersion) and (LocalElvUIWrathVersion != remoteElvUIVersion):
          shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWWrathDir + '\\_classic_\\Interface\\AddOns', dirs_exist_ok = True)
    except:
        pass
    shutil.rmtree(tempdir + "\\" + "DoElvUIUpdater")
    os.remove(tempdir + "\\" + remoteElvUIVersion + ".zip")
    #shutil.copytree("E:\\test\\AddOns\\tukui-org-ElvUI-" + remoteElvUISHA[0:7], "E:\\test", copy_function = shutil.copy)

    for widget in window.winfo_children():
            widget.destroy()

    greeting = ttk.Label(text="Welcome to the Do ElvUI Updater")
    greeting.pack()

    label = ttk.Label(text="Update Complete!")
    label.pack()
    if svtheme:
        sv_ttk.set_theme(lightdarktheme)
    window.mainloop()

# LocalElvUIClassicVersion
# LocalElvUIWrathVersion
if (LocalElvUIVersion and remoteElvUIVersion) and (LocalElvUIVersion != remoteElvUIVersion) and remoteElvUIURL or (LocalElvUIClassicVersion and remoteElvUIVersion) and (LocalElvUIClassicVersion != remoteElvUIVersion) and remoteElvUIURL or (LocalElvUIWrathVersion and remoteElvUIVersion) and (LocalElvUIWrathVersion != remoteElvUIVersion) and remoteElvUIURL:
    changelogbox = tk.Text(window,width=45, height= 20,wrap="word")
    #changelogresponse = requests.get("https://api.github.com/repos/tukui-org/ElvUI/tags?per_page=1")
    #changelogresponsetext = response.text.replace("[","").replace("]","")

    try:
        s = requests.get("https://api.tukui.org/v1/changelog/elvui")
        changelogbox.insert('1.0',s.text)
    except:
        text = "Changelog Unavailable"
        changelogbox.insert('1.0',text)
    #soup = BeautifulSoup(s.content, "html.parser")
    #soupdiv = soup.find("div", id='changelog')
    #for data in soupdiv(['style', 'script']):
    #    # Remove tags
    #    data.decompose()
    #print(soup.find("div", id='changelog'))
    #print(' '.join(soup.stripped_strings))
    #changelogbox.insert('1.0',' '.join(soupdiv.stripped_strings))
    

    changelogbox.pack(expand= 1)

    button = ttk.Button(
        text="Update",
        width=25,
        command=run_update,
    )
    button.pack()
else:
    label = ttk.Label(text="You Are Up to Date!")
    label.pack()

if svtheme:
    sv_ttk.set_theme(lightdarktheme)
window.mainloop()
