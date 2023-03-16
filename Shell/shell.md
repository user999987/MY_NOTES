Exit code in shell \
Every Linux or Unix command executed by the shell script or user has an exit status. Exit status is an integer number. 0 exit status means the command was successful without any errors. A non-zero (1-255 values) exit status means command was a failure.
0. ` >> /dev/null 2>&1` \
```shell
# >> output redirection
# used to redirect the program output and append the output at the end of the file

# /dev/null 
# /dev/null is a special file, accepts and discards all input; produces no output (always returns an end-of-file indication on a read).

# 2>&1
# Merges output from stream 2 with stream 1
# Whenever you execute a program, the operating system always opens 3 files, standard input, standard output and standard error as we know whenever a file is opened, the operating system (from kernel) returns a non-negative integer called file descriptor. The file descriptor for these files are 0,1,2 respectively.
# & after > means whatever follows is a file descriptor, not a file name.
```
1. `;` \
Shell command separator
2. `&` \
Background job
3. `&&` \
chain commands together, such that the next command is run if and only if the preceding command exited without errors
4. `||` \
execute the statement which follows only if the preceding statement failed (returned a non-zero exit code).
5. `!` \
Pipeline logical NOT
```shell
# if ! [ 1 -lt 2 ]; then echo 'ok'; else echo 'no'; fi
ok
```
6. `$` \
```shell
# a=10
# echo $a
10
```
7. 