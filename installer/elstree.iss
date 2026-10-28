#define MyAppName "elstree"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Ezu"
#define MyAppExeName "elstree.exe"

[Setup]

AppId={{8d82f419-0389-4c7e-b6ac-50004e06ff6c}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={localappdata}\Programs\elstree
DisableDirPage=no
DefaultGroupName=elstree

PrivilegesRequired=lowest

OutputDir=.
OutputBaseFilename=elstree-Setup-{#MyAppVersion}

SetupIconFile=
WizardStyle=modern

Uninstallable=yes

ChangesEnvironment=yes




[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: ..\dist\elstree.exe; DestDir: "{app}"

[Icons]
Name: "{group}\elstree"; Filename: "{app}\elstree.exe"
Name: "{group}\Uninstall elstree"; Filename: "{uninstallexe}"

[Messages]
WelcomeLabel1=Welcome to elstree Setup
WelcomeLabel2=This wizard will install elstree on your computer.%n%nClick Next to continue.


[Tasks]
Name: "addtopath"; Description: "Add elstree to PATH"; GroupDescription: "Additional options:"

[Code]

function NeedsAddPath(Param: string): Boolean;
var
    OrigPath: string;
begin
    if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath) then
    begin
        Result := True;
        Exit;
    end;

    Result := Pos(';' + Uppercase(Param) + ';', ';' + Uppercase(OrigPath) + ';') = 0;

end;

function RemovePathEntry(CurrentPath, Entry: String): String;
var
    Remaining, Part: String;
    P: Integer;
begin
    Remaining := CurrentPath;
    Result := '';

    while Remaining <> '' do
    begin
        P := Pos(';', Remaining);

        if P > 0 then
        begin
            Part := Copy(Remaining, 1, P - 1);
            Delete(Remaining, 1, P);
        end
        else
        begin
            Part := Remaining;
            Remaining := '';
        end;

        if (CompareText(Part, Entry) <> 0) and (Part <> '') then
        begin
            if Result <> '' then
                Result := Result + ';';

            Result := Result + Part;
        end;
    end;
end;

procedure AddPathEntry(Entry: String);
var
    CurrentPath: String;
begin
    if not RegQueryStringValue(
        HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath
    ) then
        CurrentPath := '';

    if NeedsAddPath(Entry) then
    begin
        if CurrentPath <> '' then
            CurrentPath := CurrentPath + ';';

        CurrentPath := CurrentPath + Entry;

        RegWriteStringValue(
            HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath
        );
    end;
end;

procedure DeletePathEntry(Entry: String);
var
    CurrentPath: String;
begin
    if RegQueryStringValue(
        HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath
    ) then
    begin
        CurrentPath := RemovePathEntry(CurrentPath, Entry);

        RegWriteStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath);

    end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
    Entry: String;
begin
    if CurStep = ssPostInstall then
    begin
        if WizardIsTaskSelected('addtopath') then
        begin

            Entry := ExpandConstant('{app}');

            if NeedsAddPath(Entry) then
            begin
                AddPathEntry(Entry);

                RegWriteStringValue(
                    HKEY_CURRENT_USER,
                    'Software\elstree',
                    'PathEntryAdded',
                    Entry
                );
            end;
        end;
    end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
    Entry: String;
begin
    if CurUninstallStep = usUninstall then
    begin
        if RegQueryStringValue(
            HKEY_CURRENT_USER,
            'Software\elstree',
            'PathEntryAdded',
            Entry
        ) then
        begin
            DeletePathEntry(Entry);

            RegDeleteValue(
                HKEY_CURRENT_USER,
                'Software\elstree',
                'PathEntryAdded'
            );

            RegDeleteKeyIfEmpty(
                HKEY_CURRENT_USER,
                'Software\elstree'
            );
        end;
    end;
end;