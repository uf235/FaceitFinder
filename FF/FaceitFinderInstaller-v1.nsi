Name "FaceitFinderInstaller-v1.0"
OutFile "FaceitFinderInstaller-v1.0.exe"
InstallDir $PROGRAMFILES64\FaceitFinder

RequestExecutionLevel admin

# Default sections
Section
    # ouput path
    SetOutPath $INSTDIR
    # Files inlcuded to the ouput path
    #FILE C:\Users\Henri\Desktop\FaceitFinder\FF\dist\FaceitFinder.exe
    #FILE C:\Users\Henri\Desktop\FaceitFinder\FF\dist\Faceit_Icon.ico
    FILE /r C:\Users\Henri\Desktop\FaceitFinder\FF\dist
    FILE /r C:\Users\Henri\Desktop\FaceitFinder\FF\build
    
    # Create uninstaller.exe
    WriteUninstaller $INSTDIR\unistaller.exe
    # Create a shortcut
    CreateShortCut "$DESKTOP\FaceitFinder.lnk" "$INSTDIR\dist\FaceitFinder.exe"
SectionEnd

# Uninstall section
Section "Uninstall"
    # Files to be deleted
    Delete $INSTDIR\FaceitFinder.exe
    Delete $INSTDIR\Faceit_Icon.ico
    Delete $INSTDIR\Friends.txt
    Delete $INSTDIR\logger.log
    Delete $INSTDIR\unistaller.exe
    Delete $DESKTOP\FaceitFinder.lnk
    
    # Remove directory
    RMDir $INSTDIR
SectionEnd