Name "FaceitFinderInstaller-v1"
OutFile "FaceitFinderInstaller-v1.exe"
InstallDir $PROGRAMFILES64\FaceitFinder

# Default sections
Section
    # ouput path
    SetOutPath $INSTDIR
    # Files inlcuded to the ouput path
    FILE /r C:\Users\Henri\Desktop\FF\dist
    FILE /r C:\Users\Henri\Desktop\FF\build
    FILE /r C:\Users\Henri\Desktop\FF\images

    
    # Create uninstaller.exe
    WriteUninstaller $INSTDIR\unistaller.exe
    # Create a shortcut
    CreateShortCut "$DESKTOP\FaceitFinder.lnk" "$INSTDIR\dist\FaceitFinder.exe"
SectionEnd

# Uninstall section
Section "Uninstall"
    # Files to be deleted
    RMDir /r $INSTDIR\dist
    RMDir /r $INSTDIR\build
    RMDir /r $INSTDIR\images
    Delete $INSTDIR\unistaller.exe
    Delete $DESKTOP\FaceitFinder.lnk
    
    # Remove directory
    RMDir $INSTDIR
SectionEnd