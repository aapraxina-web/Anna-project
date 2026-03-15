set projectPath to "/Users/user/Documents/GitHub/Anna-project"
set pythonCandidates to {"/opt/homebrew/bin/python3", "/usr/local/bin/python3", "/usr/bin/python3"}
set pythonBin to ""

repeat with candidate in pythonCandidates
	set candidatePath to contents of candidate
	set probeCommand to "if [ -x " & (quoted form of candidatePath) & " ]; then echo yes; fi"
	set probeResult to (do shell script probeCommand)
	if probeResult is "yes" then
		set pythonBin to candidatePath
		exit repeat
	end if
end repeat

if pythonBin is "" then
	display dialog "Python 3 не найден. Установите Python 3 и попробуйте снова." buttons {"OK"} default button "OK" with icon stop
	return
end if

set launchCommand to "cd " & quoted form of projectPath & " && export PYTHONPYCACHEPREFIX=${TMPDIR:-/tmp}/anna_pycache && nohup " & quoted form of pythonBin & " tic_tac_toe.py >/tmp/tic_tac_toe.log 2>&1 &"

try
	do shell script launchCommand
on error errMsg
	display dialog "Не удалось запустить игру:" & return & errMsg buttons {"OK"} default button "OK" with icon stop
	return
end try
