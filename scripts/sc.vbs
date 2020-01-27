Set oWS = WScript.CreateObject("WScript.Shell")
str_desktop = CreateObject("WScript.Shell").SpecialFolders("Desktop")
str_username = CreateObject("WScript.Network").UserName
str_dist = "C:/Users/" + str_username + "/source/dstctl/dist/dstctl/"
str_ex = str_dist + "dstctl.exe"

sLinkFile = str_desktop + "/DST Server Control.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = str_dist + "dstctl.exe"
'  oLink.Arguments = ""
'  oLink.Description = "MyProgram"   
'  oLink.HotKey = "ALT+CTRL+F"
oLink.IconLocation = str_dist + "dstctl.ico"
'  oLink.WindowStyle = "1"   
oLink.WorkingDirectory = str_dist
oLink.Save

