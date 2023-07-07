# FileHunter Integration Steps

## Part 1: Initial
1. ~~From CLI (or future AI function) choose directory or current~~
2. ~~Get path to specified directory~~
3. ~~Navigate to specified directory and create a directory path~~

## Step 2: Begin AI Setup
1. After create a directory path from the specified directory, set up the initial AI settings
    1. Create and provide the AI with a system message instructing them of the following behaviors
        - ~~System will first be provided with a repository directory structure to be reviewing and understand of how it is setup~~
        - System will be reviewing project overview description provided by the user
        - System will be review code files based on the user instructions. Ex: User provides you with a file name, you will review all the contents in that file

## Step 3: Design Logic Implimentation
1. Potential Design Implimentation
	- Maybe this can be one of those automatic function things
	- The check function will check lenght of the file, if the is larger, break it up into multiple parts
	- Based on the size of the function, you will build the user to instruct the ai to wait until you send all the messages in total length