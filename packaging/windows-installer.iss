#define AppVersion "5.6.0-zh.1"
#ifndef PayloadDir
  #define PayloadDir "..\.build\upstream\full\app"
#endif
#ifndef ArtifactDir
  #define ArtifactDir "..\.build\artifacts"
#endif

[Setup]
AppId={{A1E39E27-D4EF-40CB-B8B8-1D4B9EF22742}
AppName=Ultimate Vocal Remover - 简体中文
AppVersion={#AppVersion}
AppVerName=Ultimate Vocal Remover 简体中文版 {#AppVersion}
AppPublisher=ConfigCrate
AppPublisherURL=https://configcrate.com/
AppSupportURL=https://github.com/configcrate/ultimatevocalremovergui/issues
AppUpdatesURL=https://github.com/configcrate/ultimatevocalremovergui/releases
VersionInfoVersion=5.6.0.1
VersionInfoDescription=Ultimate Vocal Remover 简体中文安装程序
DefaultDirName={localappdata}\Programs\Ultimate Vocal Remover CN
DefaultGroupName=Ultimate Vocal Remover 简体中文版
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputDir={#ArtifactDir}
OutputBaseFilename=UVR_v5.6.0_zh-CN_setup
SetupIconFile={#PayloadDir}\gui_data\img\GUI-Icon.ico
UninstallDisplayIcon={app}\gui_data\img\GUI-Icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no
SetupLogging=yes

[Languages]
Name: "chinesesimp"; MessagesFile: "ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加选项："; Flags: unchecked

[Files]
Source: "{#PayloadDir}\*"; DestDir: "{app}"; Excludes: "unins000.exe,unins000.dat,data.pkl"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\LICENSE"; DestDir: "{app}"; DestName: "LICENSE.txt"; Flags: ignoreversion
Source: "..\NOTICE.md"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\ensemble_temps"
Name: "{app}\temp_sample_clips"
Name: "{app}\tmp"

[Icons]
Name: "{group}\Ultimate Vocal Remover 简体中文版"; Filename: "{app}\UVR_Launcher.exe"; WorkingDir: "{app}"; IconFilename: "{app}\gui_data\img\GUI-Icon.ico"
Name: "{autodesktop}\Ultimate Vocal Remover 简体中文版"; Filename: "{app}\UVR_Launcher.exe"; WorkingDir: "{app}"; IconFilename: "{app}\gui_data\img\GUI-Icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\UVR_Launcher.exe"; Description: "启动 Ultimate Vocal Remover 简体中文版"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\data.pkl"
Type: filesandordirs; Name: "{app}\ensemble_temps"
Type: filesandordirs; Name: "{app}\temp_sample_clips"
Type: filesandordirs; Name: "{app}\tmp"
