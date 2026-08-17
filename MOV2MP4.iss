[Setup]
AppName=MOV2MP4
AppVersion=1.0
AppPublisher=MOV2MP4
DefaultDirName={autopf}\MOV2MP4
DefaultGroupName=MOV2MP4
OutputDir=dist
OutputBaseFilename=MOV2MP4-Setup
SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\MOV2MP4.exe
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=commandline

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\MOV2MP4\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MOV2MP4"; Filename: "{app}\MOV2MP4.exe"; IconFilename: "{app}\MOV2MP4.exe"
Name: "{autodesktop}\MOV2MP4"; Filename: "{app}\MOV2MP4.exe"; IconFilename: "{app}\MOV2MP4.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MOV2MP4.exe"; Description: "Launch MOV2MP4"; Flags: nowait postinstall skipifsilent
