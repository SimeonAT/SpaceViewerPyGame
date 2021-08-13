# Bash Script that converts all files in a folder from .mp3 to .wav using ffmpeg
# RESOURCES USED:
# - https://opensource.com/article/19/6/how-write-loop-bash 
# 	-> Taught how to write a bash shell for loop
# - https://askubuntu.com/questions/919788/convert-mp3-file-to-wav-using-the-command-line 
# 	-> Taught me how to use ffmpeg, gave me the idea of using a bash script to do 
#	   the conversion on many files at once, and introduced me to the "basename" command
# - https://linuxhint.com/remove_characters_string_bash/
# 	-> Taught me how to use "sed" command to remove characters from a string 
# - https://stackoverflow.com/questions/7194192/basename-with-spaces-in-a-bash-script
#   -> Taught me how to use "basename" command when there are spaces in the string
# - https://stackoverflow.com/questions/18929149/print-double-quotes-in-shell-programming
#   -> Taught me how to type literal quotes onto a string in the bash script
# - https://unix.stackexchange.com/questions/131766
#   /why-does-my-shell-script-choke-on-whitespace-or-other-special-characters
#   -> Made me realize that working with spaces with filenames is difficult to do in bash
# - https://askubuntu.com/questions/385528/how-to-increment-a-variable-in-bash
#   -> Learned how to increment variables in bash

for file in {1..26}; do
		echo $file;
		echo $(basename -s .mp3 $file).wav;
		mpg123 -w $(basename -s .mp3 $file).wav $file.mp3;
done;
