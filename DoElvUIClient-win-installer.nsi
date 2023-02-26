# Script version; displayed when running the installer
!define DoElvUIClient_INSTALLER_VERSION "2.0"

# Deluge program information
!define PROGRAM_NAME "DoElvUIClient"
# Detect version from file
!searchparse /file VERSION.tmp `build_version = "` PROGRAM_VERSION `"`
!ifndef PROGRAM_VERSION
   !error "Program Version Undefined"
!endif
!define PROGRAM_WEB_SITE "https://github.com/doadin/DoElvUIClient"
!define LICENSE_FILEPATH "..\..\LICENSE"

!include FileFunc.nsh

!ifndef arch
!define INSTALLER_FILENAME "DoElvUIClient-${PROGRAM_VERSION}-win64-setup.exe"
!endif
!If "${arch}" == "x64"
!define INSTALLER_FILENAME "DoElvUIClient-${PROGRAM_VERSION}-win64-setup.exe"
!EndIf
!If "${arch}" == "x86"
!define INSTALLER_FILENAME "DoElvUIClient-${PROGRAM_VERSION}-win32-setup.exe"
!EndIf

# Set default compressor
SetCompressor /FINAL /SOLID lzma
SetCompressorDictSize 64

# --- Interface settings ---
# Modern User Interface 2
!include MUI2.nsh
# Installer
!define MUI_ICON "..\..\deluge\ui\data\pixmaps\deluge.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_HEADERIMAGE_BITMAP "installer-top.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "installer-side.bmp"
!define MUI_COMPONENTSPAGE_SMALLDESC
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_ABORTWARNING
# Start Menu Folder Page Configuration
!define MUI_STARTMENUPAGE_DEFAULTFOLDER ${PROGRAM_NAME}
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCR"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\DoElvUIClient"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
# Uninstaller
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_HEADERIMAGE_UNBITMAP "installer-top.bmp"
!define MUI_WELCOMEFINISHPAGE_UNBITMAP "installer-side.bmp"
!define MUI_UNFINISHPAGE_NOAUTOCLOSE

!define MUI_FINISHPAGE_SHOWREADME ""
!define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Create Desktop Shortcut"
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION finishpageaction

# --- Start of Modern User Interface ---
Var StartMenuFolder
# Welcome, License & Components pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE ${LICENSE_FILEPATH}
!insertmacro MUI_PAGE_COMPONENTS
# Let the user select the installation directory
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
# Run installation
!insertmacro MUI_PAGE_INSTFILES
# Display 'finished' page
!insertmacro MUI_PAGE_FINISH
# Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES
# Language files
!insertmacro MUI_LANGUAGE "English"


# --- Functions ---

# Check for running DoElvUIClient instance.
Function .onInit
    System::Call 'kernel32::OpenMutex(i 0x100000, b 0, t "DoElvUIClient") i .R0'
    IntCmp $R0 0 notRunning
        System::Call 'kernel32::CloseHandle(i $R0)'
        MessageBox MB_OK|MB_ICONEXCLAMATION "DoElvUIClient is running. Please close it first" /SD IDOK
        Abort
    notRunning:
FunctionEnd

Function un.onUninstSuccess
    HideWindow
    MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer." /SD IDOK
FunctionEnd

Function un.onInit
    MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Do you want to completely remove $(^Name)?" /SD IDYES IDYES +2
    Abort
FunctionEnd

Function finishpageaction
    CreateShortCut "$DESKTOP\DoElvUIClient.lnk" "$INSTDIR\DoElvUIClient.exe"
FunctionEnd

# --- Installation sections ---
!define PROGRAM_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PROGRAM_NAME}"
!define PROGRAM_UNINST_ROOT_KEY "HKLM"
!define PROGRAM_UNINST_FILENAME "$INSTDIR\DoElvUIClient-uninst.exe"

BrandingText "${PROGRAM_NAME} Windows Installer v${DoElvUIClient_INSTALLER_VERSION}"
Name "${PROGRAM_NAME} ${PROGRAM_VERSION}"
OutFile "${INSTALLER_FILENAME}"

!ifndef arch
InstallDir "$PROGRAMFILES64\DoElvUIClient"
!endif
!If "${arch}" == "x64"
InstallDir "$PROGRAMFILES64\DoElvUIClient"
!endIf
!If "${arch}" == "x86"
InstallDir "$PROGRAMFILES32\DoElvUIClient"
!endIf

ShowInstDetails show
ShowUnInstDetails show

# Install main application
Section "DoElvUIClient Bittorrent Client" Section1
    SectionIn RO
    !include "install_files.nsh"

    SetOverwrite ifnewer
    SetOutPath "$INSTDIR"
    File ${LICENSE_FILEPATH}
    WriteIniStr "$INSTDIR\homepage.url" "InternetShortcut" "URL" "${PROGRAM_WEB_SITE}"

    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
        SetShellVarContext all
        CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
        CreateShortCut "$SMPROGRAMS\$StartMenuFolder\DoElvUIClient.lnk" "$INSTDIR\DoElvUIClient.exe"
        CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Website.lnk" "$INSTDIR\homepage.url"
        CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall DoElvUIClient.lnk" ${PROGRAM_UNINST_FILENAME}
    !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

LangString DESC_Section1 ${LANG_ENGLISH} "Install DoElvUIClient."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${Section1} $(DESC_Section1)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

# Create uninstaller.
Section -Uninstaller
    WriteUninstaller ${PROGRAM_UNINST_FILENAME}
    WriteRegStr ${PROGRAM_UNINST_ROOT_KEY} "${PROGRAM_UNINST_KEY}" "DisplayName" "$(^Name)"
    WriteRegStr ${PROGRAM_UNINST_ROOT_KEY} "${PROGRAM_UNINST_KEY}" "DisplayVersion" ${PROGRAM_VERSION}
    WriteRegStr ${PROGRAM_UNINST_ROOT_KEY} "${PROGRAM_UNINST_KEY}" "UninstallString" ${PROGRAM_UNINST_FILENAME}
SectionEnd

# --- Uninstallation section ---
Section Uninstall
    # Delete DoElvUIClient files.
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\homepage.url"
    Delete ${PROGRAM_UNINST_FILENAME}
    !include "uninstall_files.nsh"

    # Delete Start Menu items.
    !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
        SetShellVarContext all
        Delete "$SMPROGRAMS\$StartMenuFolder\DoElvUIClient.lnk"
        Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall DoElvUIClient.lnk"
        Delete "$SMPROGRAMS\$StartMenuFolder\DoElvUIClient Website.lnk"
        RmDir "$SMPROGRAMS\$StartMenuFolder"
        DeleteRegKey /ifempty HKCR "Software\DoElvUIClient"

    Delete "$DESKTOP\DoElvUIClient.lnk"

    # Delete registry keys.
    DeleteRegKey ${PROGRAM_UNINST_ROOT_KEY} "${PROGRAM_UNINST_KEY}"
    DoElvUIClient_skip_delete:
    # This key is only used by DoElvUIClient, so we should always delete it
    DeleteRegKey HKCR "DoElvUIClient"
SectionEnd

# Add version info to installer properties.
VIProductVersion "${DoElvUIClient_INSTALLER_VERSION}.0.0"
VIAddVersionKey ProductName ${PROGRAM_NAME}
VIAddVersionKey Comments "DoElvUIClient"
VIAddVersionKey CompanyName "Doadin"
VIAddVersionKey LegalCopyright "Doadin"
VIAddVersionKey FileDescription "${PROGRAM_NAME} Application Installer"
VIAddVersionKey FileVersion "${DoElvUIClient_INSTALLER_VERSION}.0.0"
VIAddVersionKey ProductVersion "${PROGRAM_VERSION}.0"
VIAddVersionKey OriginalFilename ${INSTALLER_FILENAME}
