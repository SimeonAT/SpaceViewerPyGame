# Bash Script that converts all files in a folder from .mp3 to .wav using ffmpeg
# RESOURCES USED:
# - https://opensource.com/article/19/6/how-write-loop-bash 
# 	-> Taught how to write a bash shell for loop
# - https://askubuntu.com/questions/919788/convert-mp3-file-to-wav-using-the-command-line 
# 	-> Taught me how to use ffmpeg, along with giving me the idea of using a bash script to do 
	   the conversion on many files at once
# - https://linuxhint.com/remove_characters_string_bash/
# 	-> Taught me how to use "sed" command to remove characters from a string 

for file in *.mp3;
do echo $file;
   echo $file | sed "s/.mp3//";
   echo " ";
done;
