; This file is part of OpenSesame.

; OpenSesame is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.

; OpenSesame is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.

; You should have received a copy of the GNU General Public License
; along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.

; USAGE
; -----
; This script assumes that the binary is located as an extracted folder in
; 	C:\Users\dev\Documents\gît\OpenSesame\dist\opensesame_[version]
;
; The extension FileAssociation.nsh must be installed. This can be
; done by downloading the script from the link below and copying it
; to a file named FileAssociation.nsh in the Include folder of NSIS.
; - <http://nsis.sourceforge.net/File_Association>

; For each new release, adjust the PRODUCT_VERSION as follows:
; 	X.X.X-pyX.X-win32-X

SetCompressor /SOLID /FINAL lzma

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "OpenSesame"
!define PRODUCT_VERSION "3.2.2-py3.6-win64-1"
!define EXEC_SUBFOLDER "Scripts\"
!define PRODUCT_PUBLISHER "Sebastiaan Mathot"
!define PRODUCT_WEB_SITE "http://osdoc.cogsci.nl"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "FileAssociation.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "C:\Users\dev\Documents\git\OpenSesame\opensesame_resources\opensesame.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\python.exe ${EXEC_SUBFOLDER}opensesame"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "opensesame_${PRODUCT_VERSION}.exe"
InstallDir "$PROGRAMFILES\OpenSesame"
ShowInstDetails hide
ShowUnInstDetails hide

Section "OpenSesame" SEC01
  SetShellVarContext all
  IfFileExists "$INSTDIR" 0 true
  MessageBox MB_YESNO "Another version of OpenSesame is already installed in $INSTDIR, and will be removed. Do you want to continue?" /SD IDYES IDYES true IDNO false
  false:
    Abort
  true:
    RMDir /r "$INSTDIR"
    SetOutPath "$INSTDIR"
    SetOverwrite try
    File /r "C:\Users\dev\Documents\git\OpenSesame\dist\opensesame_${PRODUCT_VERSION}\*.*"
    ${registerExtension} "$INSTDIR\python.exe ${EXEC_SUBFOLDER}opensesame" ".osexp" "OpenSesame experiment"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateDirectory "$SMPROGRAMS\OpenSesame"
  CreateShortCut "$SMPROGRAMS\OpenSesame\OpenSesame.lnk" "$INSTDIR\pythonw.exe" "${EXEC_SUBFOLDER}opensesame" "$INSTDIR\Lib\site-packages\share\opensesame_resources\opensesame.ico"
  CreateShortCut "$SMPROGRAMS\OpenSesame\OpenSesame (runtime).lnk" "$INSTDIR\pythonw.exe" "${EXEC_SUBFOLDER}opensesamerun" "$INSTDIR\Lib\site-packages\share\opensesame_resources\opensesamerun.ico"
  CreateShortCut "$SMPROGRAMS\OpenSesame\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\OpenSesame\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer." /SD IDOK
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" /SD IDYES IDYES +2
  Abort
FunctionEnd

Section Uninstall
  SetShellVarContext all
  Delete "$SMPROGRAMS\OpenSesame\OpenSesame.lnk"
  Delete "$SMPROGRAMS\OpenSesame\OpenSesame (runtime).lnk"
  Delete "$SMPROGRAMS\OpenSesame\Website.lnk"
  Delete "$SMPROGRAMS\OpenSesame\Uninstall.lnk"
  RMDir "$SMPROGRAMS\OpenSesame"
  RMDir /r "$INSTDIR"
  ${unregisterExtension} ".osexp" "OpenSesame experiment"
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd
