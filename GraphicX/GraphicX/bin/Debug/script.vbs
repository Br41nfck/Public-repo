Const x_min = 1
Const x_max = 10
Const x_step = 1

On Error Resume Next
Dim fw: Set fw = CreateObject("Scripting.FileSystemObject").OpenTextFile("output.txt",2,true)

Dim x, y
For x = x_min To x_max Step x_step
	y = x+1
	If Err.Number <> 0 Then
		Err.Clear
		fw.Close
		Set fw = Nothing
		WScript.Quit 1
	End If
	fw.WriteLine CStr(x) & " " & CStr(y)
Next

fw.Close
Set fw = Nothing
