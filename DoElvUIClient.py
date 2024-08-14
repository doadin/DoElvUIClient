import json
import requests
import urllib.request
from zipfile import ZipFile
import tkinter as tk
from tkinter import ttk
import os
import shutil
import tempfile
import winreg
import webbrowser
import markdown
from bs4 import BeautifulSoup
LocalElvUIVersion = None
remoteElvUIVersion = None
remoteElvUIURL = None
LocalElvUIClassicVersion = None
LocalElvUIWrathVersion = None
LocalDoElvUIClientVersion = None

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
ClassicRotatingFound = True

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
    access_key = winreg.OpenKey(access_registry, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Burning Crusade Classic")
    WoWClassicRotatingDir = winreg.QueryValueEx(access_key, 'InstallLocation')[0]
except:
    ClassicRotatingFound = False
    pass

#result = subprocess.run(['git', 'rev-list', '--tags', '--max-count=1'], stdout=subprocess.PIPE)
#gitVersion = result.stdout.decode('utf-8')
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

response = requests.get("https://api.github.com/repos/tukui-org/ElvUI/tags?per_page=1")
responce_json = response.text.replace("[","").replace("]","")

data_dict = json.loads(responce_json)

try:
    if data_dict["name"]:
        remoteElvUIVersion = data_dict["name"]
    if data_dict["zipball_url"]:
        remoteElvUIURL = data_dict["zipball_url"]
    if data_dict["commit"]["sha"]:
        remoteElvUISHA = data_dict["commit"]["sha"]
    label = ttk.Label(text="Latest ElvUI Vesion: " + remoteElvUIVersion)
    label.pack()
except:
    pass

responsetukuiOrg = requests.get("https://api.tukui.org/v1/addon/elvui")
responce_jsontukuiOrg = responsetukuiOrg.text#.replace("[","").replace("]","")
#print(responce_jsontukuiOrg)
data_dicttukuiOrg = json.loads(responce_jsontukuiOrg)
#print(data_dicttukuiOrg)

try:
    if data_dicttukuiOrg["url"]:
        remoteElvUIURL = data_dicttukuiOrg["url"]
        #print(remoteElvUIURL)
except:
    pass

print(remoteElvUIURL)

tempdir = tempfile.gettempdir()
#print(tempdir)

def install_elvui_classic():
    # https://www.tukui.org/downloads/elvui-13.21.zip

    local_filename, headers = opener.retrieve(remoteElvUIURL, tempdir + "\\" + remoteElvUIVersion + ".zip")
    print(local_filename, headers)
    #urllib.request.urlretrieve("https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip", remoteElvUIVersion + ".zip")
    with ZipFile(tempdir + "\\" + remoteElvUIVersion + ".zip", 'r') as zObject:
        zObject.extractall(path = tempdir + "\\" + "DoElvUIUpdater")
    #os.rename("E:\\test\\AddOns\\ElvUI-main","E:\\test\\AddOns\\ElvUI")
    #distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns")
    try:
        #shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWClassicDir + '\\_classic_era_\\Interface\\AddOns', dirs_exist_ok = True)
        shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\", WoWClassicDir + '\\_classic_era_\\Interface\\AddOns', dirs_exist_ok = True)
        for widget in window.winfo_children():
            widget.destroy()
    
        greeting = ttk.Label(text="Welcome to the Do ElvUI Updater")
        greeting.pack()
    
        label = ttk.Label(text="Classic Era Install Complete!")
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
        classicinstallerror = ttk.Label(text="Classic Era Install Faiiled! Please report this!")
        classicinstallerror.pack()
        if svtheme:
            sv_ttk.set_theme(lightdarktheme)
        window.mainloop()

def install_elvui_classic_rotating():
    # https://www.tukui.org/downloads/elvui-13.21.zip

    local_filename, headers = opener.retrieve(remoteElvUIURL, tempdir + "\\" + remoteElvUIVersion + ".zip")
    print(local_filename, headers)
    #urllib.request.urlretrieve("https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip", remoteElvUIVersion + ".zip")
    with ZipFile(tempdir + "\\" + remoteElvUIVersion + ".zip", 'r') as zObject:
        zObject.extractall(path = tempdir + "\\" + "DoElvUIUpdater")
    #os.rename("E:\\test\\AddOns\\ElvUI-main","E:\\test\\AddOns\\ElvUI")
    #distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns")
    try:
        #shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWClassicRotatingDir + '\\_classic_\\Interface\\AddOns', dirs_exist_ok = True)
        shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\", WoWClassicRotatingDir + '\\_classic_\\Interface\\AddOns', dirs_exist_ok = True)
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
    except Exception as inst:
        print(inst)
        for widget in window.winfo_children():
            widget.destroy()
        wrathinstallerror = ttk.Label(text="Classic Install Faiiled! Please report this!")
        wrathinstallerror.pack()
        if svtheme:
            sv_ttk.set_theme(lightdarktheme)
        window.mainloop()

def install_elvui_retail():
    # https://www.tukui.org/downloads/elvui-13.21.zip

    local_filename, headers = opener.retrieve(remoteElvUIURL, tempdir + "\\" + remoteElvUIVersion + ".zip")
    print(local_filename, headers)
    #urllib.request.urlretrieve("https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip", remoteElvUIVersion + ".zip")
    with ZipFile(tempdir + "\\" + remoteElvUIVersion + ".zip", 'r') as zObject:
        zObject.extractall(path = tempdir + "\\" + "DoElvUIUpdater")
    #os.rename("E:\\test\\AddOns\\ElvUI-main","E:\\test\\AddOns\\ElvUI")
    #distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns")
    try:
        #shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], WoWDir + '\\_retail_\\Interface\\AddOns', dirs_exist_ok = True)
        shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\", WoWDir + '\\_retail_\\Interface\\AddOns', dirs_exist_ok = True)
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
        ElvUILocation = WoWDir + '\\_retail_\\Interface\\AddOns\\ElvUI\\ElvUI_Mainline.toc'
        ElvUIToC = open(ElvUILocation, 'r')
        for line in ElvUIToC:
            if line.find("Version") != -1:
               ElvUIToCVersionLine = line
        ElvUIToC.close()
        if ElvUIToCVersionLine:
            ElvUIToCVersionNumber = ElvUIToCVersionLine.partition(":")[2]
            LocalElvUIVersion = ElvUIToCVersionNumber.strip()
        
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
        ElvUIClassicLocation = WoWClassicDir + '\\_classic_era_\\Interface\\AddOns\\ElvUI\\ElvUI_Vanilla.toc'
        ElvUIClassicToC = open(ElvUIClassicLocation, 'r')
        for line in ElvUIClassicToC:
            if line.find("Version") != -1:
               ElvUIClassicToCVersionLine = line
        ElvUIClassicToC.close()
        if ElvUIClassicToCVersionLine:
            ElvUIClassicToCVersionLine = ElvUIClassicToCVersionLine.partition(":")[2]
            LocalElvUIClassicVersion = ElvUIClassicToCVersionLine.strip()
        
        ElvUIClassicVersionlabel = ttk.Label(text="Installed Classic Era ElvUI Vesion: " + LocalElvUIClassicVersion)
    except:
        pass
    
    try: 
        ElvUIClassicVersionlabel
    except NameError:
        ElvUIClassicVersionlabel = ttk.Label(text="Installed Classic Era ElvUI Vesion: None")
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

#Classic Rotating
if ClassicRotatingFound:
    try:
        try:
            WoWClassicRotatingDir
        except NameError:
            pass
        #ElvUIToC = open('C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns\\ElvUI\\ElvUI_Mainline.toc', 'r')
        ElvUIClassicRotatingDirLocation = WoWClassicRotatingDir + '\\_classic_\\Interface\\AddOns\\ElvUI\\ElvUI_Cata.toc'
        ElvUIRotatingToC = open(ElvUIClassicRotatingDirLocation, 'r')
        for line in ElvUIRotatingToC:
            if line.find("Version") != -1:
               ElvUIRotatingToCVersionLine = line
        ElvUIRotatingToC.close()
        if ElvUIRotatingToCVersionLine:
            ElvUIRotatingToCVersionLine = ElvUIRotatingToCVersionLine.partition(":")[2]
            LocalElvUIRotatingVersion = ElvUIRotatingToCVersionLine.strip()
        
        ElvUIRotatingVersionlabel = ttk.Label(text="Installed Classic ElvUI Vesion: " + LocalElvUIRotatingVersion)
    except:
        pass
    try: 
        ElvUIRotatingVersionlabel
    except NameError:
        ElvUIRotatingVersionlabel = ttk.Label(text="Installed Classic ElvUI Vesion: None")
        ElvUIRotatingVersionlabel.pack()
        ElvUIRotatingInstall = ttk.Button(
            text="Install ElvUI To Classic",
            width=25,
            command=lambda : install_elvui_classic_rotating(),
        )
        ElvUIRotatingInstall.pack(after = ElvUIRotatingVersionlabel)
    try:
        ElvUIRotatingVersionlabel.pack()
    except:
        pass


def run_update():
    # https://www.tukui.org/downloads/elvui-13.21.zip

    try:
      local_filename, headers = opener.retrieve(remoteElvUIURL, tempdir + "\\" + remoteElvUIVersion + ".zip")
      print(headers)
      #urllib.request.urlretrieve("https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip", remoteElvUIVersion + ".zip")
    except Exception as e:
        print(e)
        pass
    with ZipFile(tempdir + "\\" + remoteElvUIVersion + ".zip", 'r') as zObject:
        zObject.extractall(path = tempdir + "\\" + "DoElvUIUpdater")
    #os.rename("E:\\test\\AddOns\\ElvUI-main","E:\\test\\AddOns\\ElvUI")
    #distutils.dir_util.copy_tree(tempdir + "\\" + "DoElvUIUpdater" + "\\" + "tukui-org-ElvUI-" + remoteElvUISHA[0:7], "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns")
    try:
        if (LocalElvUIVersion and remoteElvUIVersion) and (LocalElvUIVersion != remoteElvUIVersion):
            shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" , WoWDir + '\\_retail_\\Interface\\AddOns', dirs_exist_ok = True)
    except:
        pass
    try:
      if (LocalElvUIClassicVersion and remoteElvUIVersion) and (LocalElvUIClassicVersion != remoteElvUIVersion):
          shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" , WoWClassicDir + '\\_classic_era_\\Interface\\AddOns', dirs_exist_ok = True)
    except:
        pass
    try:
      if (LocalElvUIWrathVersion and remoteElvUIVersion) and (LocalElvUIWrathVersion != remoteElvUIVersion):
          shutil.copytree(tempdir + "\\" + "DoElvUIUpdater" + "\\" , WoWClassicRotatingDir + '\\_classic_\\Interface\\AddOns', dirs_exist_ok = True)
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

def open_DoElvUIUpdater_url():
    webbrowser.open("https://github.com/doadin/DoElvUIClient/releases", new=0, autoraise=True)

response = requests.get("https://api.github.com/repos/doadin/DoElvUIClient/tags?per_page=1")
responce_json = response.text.replace("[","").replace("]","")

data_dict = json.loads(responce_json)

try:
    if data_dict["name"]:
        RemoteDoElvUIClientVersion = data_dict["name"]
    if (LocalDoElvUIClientVersion and RemoteDoElvUIClientVersion) and (LocalDoElvUIClientVersion != RemoteDoElvUIClientVersion):
        label = ttk.Label(text="There is an Update for DoElvUIUpdater!", font=15, foreground="red")
        label.pack()
        button = ttk.Button(
            text="Open Browser To Release Page",
            width=30,
            command=open_DoElvUIUpdater_url,
        )
        button.pack()
except:
    pass

# LocalElvUIClassicVersion
# LocalElvUIWrathVersion
if ((LocalElvUIVersion and remoteElvUIVersion) and (LocalElvUIVersion != remoteElvUIVersion) and remoteElvUIURL) or ((LocalElvUIClassicVersion and remoteElvUIVersion) and (LocalElvUIClassicVersion != remoteElvUIVersion) and remoteElvUIURL) or ((LocalElvUIWrathVersion and remoteElvUIVersion) and (LocalElvUIWrathVersion != remoteElvUIVersion) and remoteElvUIURL):
    changelogbox = tk.Text(window,width=45, height= 20,wrap="word")
    #changelogresponse = requests.get("https://api.github.com/repos/tukui-org/ElvUI/tags?per_page=1")
    #changelogresponsetext = response.text.replace("[","").replace("]","")

    try:
        #s = requests.get("https://api.tukui.org/v1/changelog/elvui")
        s = requests.get("https://raw.githubusercontent.com/tukui-org/ElvUI/" + remoteElvUIVersion + "/CHANGELOG.md")
        text = s.text
        if s.status_code == 200:
            extensions = ['extra', 'smarty']
            html = markdown.markdown(text, extensions=extensions, output_format='html5')
            soup = BeautifulSoup(html, features='html.parser')
            #if lightdarktheme == "dark":
            #    html = '<h2 style="background-color:black" font-size: 10px>' + '<li style="color:white">' + html
            #html_text = HTMLScrolledText(window, html=html,width=65, height= 20)
            #html_text.pack(fill="both", expand=True)
            changelogbox.insert('1.0',soup.get_text())
            #html_text.fit_height()
            #soup = BeautifulSoup(html, "html.parser")
            #for data in soup(['style', 'script']):
            #    data.decompose()
            #changelogbox.insert('1.0',s.text)
            changelogbox.pack(expand= 1)
        else:
            raise Exception('404 Changelog Unavailable')
    except:
        text = "Changelog Unavailable"
        changelogbox.insert('1.0',text)
        changelogbox.pack(expand= 1)
    #soup = BeautifulSoup(s.content, "html.parser")
    #soupdiv = soup.find("div", id='changelog')
    #for data in soupdiv(['style', 'script']):
    #    # Remove tags
    #    data.decompose()
    #print(soup.find("div", id='changelog'))
    #print(' '.join(soup.stripped_strings))
    #changelogbox.insert('1.0',' '.join(soupdiv.stripped_strings))
    

    #changelogbox.pack(expand= 1)

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
