set launchCommand to "/bin/zsh -lc " & quoted form of "cd /Users/user/Documents/GitHub/Anna-project && ./launch_tic_tac_toe.command"

try
	do shell script (launchCommand)
on error errMsg
	display dialog "Не удалось запустить игру:" & return & errMsg buttons {"OK"} default button "OK" with icon stop
	return
end try
