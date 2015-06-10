; -- Example1.iss --
; Demonstrates copying 3 files and creating an icon.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=Kaira
AppVersion=0.9
DefaultDirName={pf}\Kaira-extractor
DefaultGroupName=Kaira
UninstallDisplayIcon={app}\Kaira.exe
Compression=lzma2
SolidCompression=yes
OutputDir=userdocs:Inno Setup Examples Output

[Files]
Source: "*"; DestDir: "{app}"
Source: "/platforms/*"; DestDir: "{app}\platforms"
Source: "../../names/*"; DestDir: "{app}\names"
Source: "../../mongodb/*"; DestDir: "{app}\mongodb"
Source: "../../mongodb/bin/*"; DestDir: "{app}\mongodb\bin"
Source: "../../mongodb/data/db/*"; DestDir: "{app}\mongodb\data\db"
Source: "../../mongodb/data/db/journal/*"; DestDir: "{app}\mongodb\data\db\journal"
;Source: "/translations/*"; DestDir: "{app}\platforms"
;Source: "MyProg.chm"; DestDir: "{app}"
;Source: "OHJEKIRJA.pdf"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Kaira"; Filename: "{app}\Kaira.exe"
;Name: "{group}\Käyttöohje"; Filename: "{app}\OHJEKIRJA.pdf"
