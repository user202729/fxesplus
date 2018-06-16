@echo off
@if not "%init%"=="done" (
	set InclU8=C:\Program Files\U8Dev\Inc
	set  LibU8=C:\Program Files\U8Dev\Lib
	set    DCL=C:\Program Files\U8Dev\Dcl
	set path=%path%;C:\Program Files\U8Dev\Bin

	set init=done
)

