Prerequisites:
	-Docker version 20 or later
Steps for running the prototype:
	- Command to build the prototype - (docker build -t 'container_name' .)  . Any container name can be used as long as it remains consistent with running the prototype.
	- Command for running the prototype - (docker run -it --mount type=bind,source="$(pwd)",target=/host -e "filename='filename'" -e "timeout='timeout'") capstone2. The recommended values for 'timeout' are 1,2 and 10 seconds for the easy, medium and hard problems respectively. The list of available filenames can be found at the end of the readme.
	- The output of the prototype is printed on the command line while the docker container is running. The last line of output is the values for parameters a,b,c,e,f,r,x which produced the lowest cost.
Common errors:
	- Unable to build docker because docker daemon denies permission. Solution sudo chmod 666 /var/run/docker.sock
	- The timeout environment variable must only contain numbers, i.e no white spaces, letters or symbols
	- The notation 'variable' is used to indicate a part of the command where the client must supply their choice of input. When doing so the ' ' symbol musn't be used.
Available problems:
	- test-30-10681.wcard, test-30-14971.wcard, test-30-26011.wcard, test-30-29086.wcard, test-30-29218.wcard, test-100-7902.wcard, test-100-10119.wcard, test-100-11503.wcard, test-100-14082.wcard, test-100-30439.wcard, test-500-14838.wcard, test-500-15790.wcard, test-500-24992.wcard, test-500-25645.wcard, test-500-26676.wcard
