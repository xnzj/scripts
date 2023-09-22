; 获取剪贴板中的文本内容
$clipboardText = ClipGet()

; 检查剪贴板内容是否包含文件路径
If StringInStr($clipboardText, "C:\") > 0 Then
    ; 剪贴板中包含文件路径
    ;~ MsgBox(0, "文件路径", $clipboardText)
	;~ 把剪贴板中的文件路径赋值给变量
	$filePath = $clipboardText
	;~ 把文件路径中的反斜杠替换为正斜杠
	$filePath = StringReplace($filePath, "\", "/")
	;~ 把文件路径放入剪贴板
	ClipPut($filePath)
	;~ 在命令行打印文件路径
	ConsoleWrite("文件路径: " & $filePath & @CRLF)
Else
    ; 剪贴板中不包含文件路径
    MsgBox(0, "无文件路径", "剪贴板中没有文件路径。")
EndIf
