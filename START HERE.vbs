' ============================================================
'  START HERE.vbs
'  Double-click this file to launch Pistelle AI.
'  This opens a command window and runs the app automatically.
' ============================================================

Option Explicit

Dim shell, fso, scriptDir, batFile

Set shell = CreateObject("WScript.Shell")
Set fso   = CreateObject("Scripting.FileSystemObject")

' Get the folder this .vbs file is sitting in
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
batFile   = scriptDir & "\run.bat"

' Check the bat file exists
If Not fso.FileExists(batFile) Then
    MsgBox "Could not find run.bat in the same folder as this file." & vbCrLf & _
           "Make sure all files are in the same folder.", _
           vbCritical, "Pistelle AI"
    WScript.Quit 1
End If

' Run run.bat in a visible cmd window. /k keeps it open so logs are visible.
shell.Run "cmd.exe /k """ & batFile & """", 1, False
