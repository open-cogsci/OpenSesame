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
; This script assumes that the binary is located in
; 	C:\Users\Dévélõpe®\Documents\gît\opensesame-ising\dist
;
; The extension FileAssociation.nsh must be installed. This can be
; done by downloading the script from the link below and copying it
; to a file named FileAssociation.nsh in the Include folder of NSIS.
; - <http://nsis.sourceforge.net/File_Association>

; For each new release, adjust the PRODUCT_VERSION as follows:
; 	version-win32-package#

; After compilation, rename the .exe file to (e.g.)
; 	opensesame_{PRODUCT_VERSION}.exe

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "OpenSesame"
!define PRODUCT_VERSION "3.0.2-py2.7-win32-1"
!define PRODUCT_PUBLISHER "Sebastiaan Mathot"
!define PRODUCT_WEB_SITE "http://osdoc.cogsci.nl"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "FileAssociation.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "C:\Users\Dévélõpe®\Documents\gît\opensesame-ising\resources\opensesame.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "opensesame.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "opensesame_X-win32-X.exe"
InstallDir "$PROGRAMFILES\OpenSesame"
ShowInstDetails hide
ShowUnInstDetails hide

Section "OpenSesame" SEC01
  SetOutPath "$INSTDIR"
  RMDir /r "$INSTDIR\extensions"
  RMDir /r "$INSTDIR\plugins"
  RMDir /r "$INSTDIR\libopensesame"
  RMDir /r "$INSTDIR\libqtopensesame"
  RMDir /r "$INSTDIR\resources"
  RMDir /r "$INSTDIR\openexp"
  RMDir /r "$INSTDIR\expyriment"
  RMDir /r "$INSTDIR\psychopy"
  RMDir /r "$INSTDIR\bidi"
  RMDir /r "$INSTDIR\dateutil"
  RMDir /r "$INSTDIR\help"
  RMDir /r "$INSTDIR\IPython"
  RMDir /r "$INSTDIR\markdown"
  RMDir /r "$INSTDIR\matplotlib"
  RMDir /r "$INSTDIR\numpy"
  RMDir /r "$INSTDIR\openexp"
  RMDir /r "$INSTDIR\OpenGL"
  RMDir /r "$INSTDIR\parallel"
  RMDir /r "$INSTDIR\PIL"
  RMDir /r "$INSTDIR\pyflakes"
  RMDir /r "$INSTDIR\pygame"
  RMDir /r "$INSTDIR\PyQt4"
  RMDir /r "$INSTDIR\PyQt4_plugins"
  RMDir /r "$INSTDIR\pytz"
  RMDir /r "$INSTDIR\QProgEdit"
  RMDir /r "$INSTDIR\scipy"
  RMDir /r "$INSTDIR\serial"
  RMDir /r "$INSTDIR\sounds"
  RMDir /r "$INSTDIR\tcl"
  RMDir /r "$INSTDIR\wx"
  RMDir /r "$INSTDIR\yaml"
  RMDir /r "$INSTDIR\zmq"
  SetOverwrite try
  File /r "C:\Users\Dévélõpe®\Documents\gît\opensesame-ising\dist\*.*"
  ${registerExtension} "$INSTDIR\opensesame.exe" ".osexp" "OpenSesame experiment"
  ${registerExtension} "$INSTDIR\opensesame.exe" ".opensesame" "OpenSesame script"
  ${registerExtension} "$INSTDIR\opensesame.exe" ".gz" "OpenSesame experiment archive"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateDirectory "$SMPROGRAMS\OpenSesame"
  CreateShortCut "$SMPROGRAMS\OpenSesame\OpenSesame.lnk" "$INSTDIR\opensesame.exe" "" "$INSTDIR\resources\opensesame.ico"
  CreateShortCut "$SMPROGRAMS\OpenSesame\OpenSesame (runtime).lnk" "$INSTDIR\opensesamerun.exe" "" "$INSTDIR\resources\opensesamerun.ico"
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
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$SMPROGRAMS\OpenSesame\OpenSesame.lnk"
  Delete "$SMPROGRAMS\OpenSesame\OpenSesame (runtime).lnk"
  Delete "$SMPROGRAMS\OpenSesame\Website.lnk"
  Delete "$SMPROGRAMS\OpenSesame\Uninstall.lnk"
  RMDir "$SMPROGRAMS\OpenSesame"
  RMDir /r "$INSTDIR"
  ${unregisterExtension} ".osexp" "OpenSesame experiment"
  ${unregisterExtension} ".opensesame" "OpenSesame script"
  ${unregisterExtension} ".opensesame.tar.gz" "OpenSesame experiment"
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd
