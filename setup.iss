[Setup]
AppName=PyWiseClicker
AppVersion=1.0.0
DefaultDirName={pf}\PyWiseClicker
DisableDirPage=no
DirExistsWarning=auto
OutputDir=installer
OutputBaseFilename=PyWiseClicker_Setup
Compression=lzma2
PrivilegesRequired=admin

[Files]
Source: "dist\PyWiseClicker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\PyWiseClicker.ini"; DestDir: "{app}"; Flags: onlyifdoesntexist
Source: "VC_redist.x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
; 桌面快捷方式（使用程序自身图标）
Name: "{userdesktop}\PyWiseClicker"; Filename: "{app}\PyWiseClicker.exe"; IconFilename: "{app}\PyWiseClicker.exe"

; 开始菜单快捷方式（使用程序自身图标）
Name: "{group}\PyWiseClicker"; Filename: "{app}\PyWiseClicker.exe"; IconFilename: "{app}\PyWiseClicker.exe"

[Run]
Filename: "{tmp}\VC_redist.x64.exe"; Parameters: "/install /quiet /norestart"; StatusMsg: "安装运行库..."