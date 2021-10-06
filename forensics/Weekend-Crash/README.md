# Weekend Crash
## Production note
The zip file for this challenge is hosted on Google Drive and avilable at this link: https://drive.google.com/file/d/16qvSOXVgPJVWiVKB1leNxJ18joKgLhyP/view?usp=sharing

## Description
It’s Friday evening and you have been working nonstop for the past few days on your assignment due at midnight. Alas, fate is not on your side as your computer crashed! Luckily, with your forensics knowledge, you were able to take a snapshot of your memory. But now, your frazzled brain can’t remember what was the state of your assignment. Can you recover the information needed to make sure that you submit it in time?

## Solution
This is a Volatility 3 challenge make sure you are running up to date Volatility 3 from the `develop` branch

1. List processes
`~/Tools/volatility3/vol.py -f ./weekend_crash.bin windows.pslist.PsList`

```
6016	5292	firefox.exe	0x940cd7d480c0	16	-	1	True	2021-09-25 00:12:30.000000 	N/A	Disabled
5536	5292	firefox.exe	0x940cd4be5080	18	-	1	True	2021-09-25 00:12:33.000000 	N/A	Disabled
4192	5292	firefox.exe	0x940cdc0e3300	14	-	1	True	2021-09-25 00:13:11.000000 	N/A	Disabled
```
Firefox is running 

2. Firefox stores its history and bookmarks in a file called `places.sqlite`
`~/Tools/volatility3/vol.py -f ./weekend_crash.bin windows.filescan.FileScan | grep places`
```
0x940cdc0252d0.0\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite	216
0x940cdc025780	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite-wal	216
0x940cdc026bd0	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite-wal	216
0x940cdc0273a0	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite	216
0x940cdc5df890	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite-shm	216
0x940cdc5e0510	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite-wal	216
0x940cdc5e1af0	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite	216
0x940cdc5e1e10	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite	216
0x940cdc5e22c0	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\places.sqlite-wal	216
```

3. Dumping the `places.sqlite` file
`~/Tools/volatility3/vol.py -f ./weekend_crash.bin windows.dumpfiles.DumpFiles --virtaddr 0x940cdc0252d0`

```
DataSectionObject	0x940cdc0252d0	places.sqlite	Error dumping file
SharedCacheMap	0x940cdc0252d0	places.sqlite	file.0x940cdc0252d0.0x940cdc068460.SharedCacheMap.places.sqlite.vacb
```
For some reason it fails to dump the entire file and it is not a valid sqlite file (I think it is a bug in vol3...)

We can run strings on it to get some partial data.
`strings file.0x940cdc0252d0.0x940cdc269b50.DataSectionObject.places.sqlite.dat`

We can see some mozilla domains and this other domain `http://congon4tor.com:7777`

4. Visiting the domain from a browser shows the message `No flag sorry` 

5. Look for cookie files
`~/Tools/volatility3/vol.py -f ./weekend_crash.bin windows.filescan.FileScan | grep cookies`

```
0x940cdb88e220.0\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\cookies.sqlite	216
0x940cdc5aae60	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\cookies.sqlite	216
0x940cdc5abc70	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\cookies.sqlite-wal	216
0x940cdc5ac2b0	\Users\congon4tor\AppData\Roaming\Mozilla\Firefox\Profiles\lylfp465.default-release\cookies.sqlite-shm	216
```

6. Dump the cookie file
`~/Tools/volatility3/vol.py -f ./weekend_crash.bin windows.dumpfiles.DumpFiles --virtaddr 0x940cdb88e220`

```
DataSectionObject	0x940cdb88e220	cookies.sqlite	file.0x940cdb88e220.0x940cdc261310.DataSectionObject.cookies.sqlite.dat
SharedCacheMap	0x940cdb88e220	cookies.sqlite	file.0x940cdb88e220.0x940cdb5c9d80.SharedCacheMap.cookies.sqlite.vacb
```

This one did not error out and we can open it with a sqlite database browser

```
id,originAttributes,name,value,host,path,expiry,lastAccessed,creationTime,isSecure,isHttpOnly,inBrowserElement,sameSite,rawSameSite,schemeMap
1,,magic,6670ee0a08c2818f76256954c72ad077,congon4tor.com,/,1632508520,1632506927713000,1632422139087000,0,0,0,0,0,1
```

7. Adding a cookie with name `magic`, value `6670ee0a08c2818f76256954c72ad077` and `congon4tor.com` as the path and revisiting `http://congon4tor.com:7777` shows:
`rot13(synt{sbkrf_qbag_yvxr_pbbxvrf})`

We decode using rot13 and obtain the flag `flag{foxes_dont_like_cookies}`

