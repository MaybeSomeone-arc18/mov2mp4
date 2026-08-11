[Setup]
AppName=MOV2MP4
AppVersion=1.0
DefaultDirName={autopf}\MOV2MP4
DefaultGroupName=MOV2MP4
OutputDir=dist
OutputBaseFilename=MOV2MP4-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\MOV2MP4\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MOV2MP4"; Filename: "{app}\MOV2MP4.exe"
Name: "{autodesktop}\MOV2MP4"; Filename: "{app}\MOV2MP4.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MOV2MP4.exe"; Description: "Launch MOV2MP4"; Flags: nowait postinstall skipifsilent
