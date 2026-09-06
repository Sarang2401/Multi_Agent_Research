' ============================================================
'  START HERE.vbs
'  Double-click this file to launch the Social Media Script Generator.
'  This opens a visible window and runs the app automatically.
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
           vbCritical, "Social Media Script Generator"
    WScript.Quit 1
End If

' Open cmd.exe with run.bat — /k keeps the window open after the script finishes
' The 1 as second parameter means: show the window (not hidden)
shell.Run "cmd.exe /k """ & batFile & """", 1, False
