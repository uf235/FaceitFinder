Name "FaceitFinderInstaller-v1"
OutFile "FaceitFinderInstaller-v1.exe"
InstallDir $PROGRAMFILES\FaceitFinder

# Default sections
Section
    # ouput path
    SetOutPath $INSTDIR
    # Files inlcuded to the ouput path
    File C:\Users\Henri\Desktop\faceit_app\dist\FaceitFinder.exe
    File C:\Users\Henri\Desktop\faceit_app\Faceit_Icon.ico
    # Create uninstaller.exe
    WriteUninstaller $INSTDIR\unistaller.exe
    # Create a shortcut
    CreateShortCut "$DESKTOP\FaceitFinder.lnk" "$INSTDIR\FaceitFinder.exe"
SectionEnd

# Uninstall section
Section "Uninstall"
    # Files to be deleted
    Delete $INSTDIR\FaceitFinder.exe
    Delete $INSTDIR\unistaller.exe
    Delete $INSTDIR\Faceit_Icon.ico
    # Remove directory
    RMDir $INSTDIR
SectionEnd