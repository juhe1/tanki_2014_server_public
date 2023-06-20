Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "bat\launch_cs_1x.bat" & Chr(34), 0
Set WshShell = Nothing