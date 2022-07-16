# Prerequisites
1. A computer powerful enogh for running Apollo+LGSVL. 
(Or two computers: one for Apollo, one for LGSVL)
2. antlr4
3. rtamt
4. python3

## Install antlr4 for LawBreaker
Make sure installation of version antlr-4.8(the latest version is not supported):
[Install By Package](https://www.antlr.org/download/antlr-4.8-complete.jar)


## Install RTAMT for LawBreaker
Please refer to [the github page](https://github.com/nickovic/rtamt) for installation of RTAMT.

# Step by step

## Run Apollo with LGSVL
Please refer to [the detailed documentation](https://www.svlsimulator.com/docs/system-under-test/apollo-master-instructions/) for co-simulation of Apollo with LGSVL.
Set the LGSVL to API-Only mode.

## Setup our bridge.
1. Download and go to the root. Note that the source code should be downloaded and set up on the computer running Apollo.
	```bash
	git clone https://github.com/lawbreaker2021/LawBreaker-SourceCode.git
	cd LawBreaker-SourceCode
	```
2. Install Python API support for LGSVL.
	```bash
	cd LawBreaker-SourceCode/bridge/PythonAPImaster
	pip3 install --user -e .  
	##If "pip3 install --user -e ." fail, try the following command:
	python3 -m pip install -r requirements.txt --user .
	```

3. Connect our bridge to the LGSVL and Apollo:
	Go the bridge in the folder:/LawBreaker-SourceCode/bridge
	```bash
	cd /root_of_LawBreaker-SourceCode/bridge
	```
	Find file: [bridge.py](https://github.com/lawbreaker2021/LawBreaker-SourceCode/blob/main/bridge/bridge.py).
	There is class `Server` in [bridge.py](https://github.com/lawbreaker2021/LawBreaker-SourceCode/blob/main/bridge/bridge.py). 

	Modify the `SIMULATOR_HOST` and `SIMULATOR_PORT` of `Server` to your IP and port of LGSVL.
	Modify the `BRIDGE_HOST` and `BRIDGE_PORT` of `Server` to your IP and port of Apollo.
	
4. Test the parser:
	If the support for parser is properly installed, we can test it by running:
	```bash
	cd /root_of_LawBreaker-SourceCode
	python3 monitor.py
	```
	If there is no errors and warnings, the parser is correct.


## Run our bridge.
Open a terminal on the computer running Apollo.
```bash
cd /root_of_LawBreaker-SourceCode/bridge
python3 bridge.py
```
Keep it Running.


## Run the Fuzzing Algorithm.
Open another terminal on the computer running Apollo.
```bash
cd /root_of_LawBreaker-SourceCode
python3 Law_Breaking_Fuzzing.py
```
If the brige is set properly, you will see the LGSVL and Apollo running. The results will be put into a folder: The_Results.

