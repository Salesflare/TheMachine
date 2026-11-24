; What the app itself put in this person's part of the registry and their folders goes with it. An update keeps it all, also one by hand.
!macro NSIS_HOOK_PREUNINSTALL
  ${If} ${FileExists} "$INSTDIR\the-machine-desktop.exe"
    nsExec::Exec '"$INSTDIR\the-machine-desktop.exe" --quit'
    Pop $0
  ${EndIf}
!macroend

!macro NSIS_HOOK_POSTUNINSTALL
  ${If} $UpdateMode <> 1
  ${AndIf} $EXEDIR != $INSTDIR ; in its own folder, and not from a copy: the installer runs it, before it puts a newer one there
    DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "The Machine"
    DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run" "The Machine"
    DeleteRegKey HKCU "Software\Classes\AppUserModelId\computer.themachine.desktop"
    DeleteRegKey HKCU "Software\Classes\computer.themachine.app"
    DeleteRegKey HKCU "${MANUPRODUCTKEY}"
    DeleteRegKey /ifempty HKCU "${MANUKEY}"
    SetShellVarContext current
    RMDir /r "$APPDATA\computer.themachine.desktop"
    RMDir /r "$LOCALAPPDATA\computer.themachine.desktop"
  ${EndIf}
!macroend
