# C2 server
## Description
During an investigation, your security team found a web folder that allowed directory browsing on an attacker’s C2 server. In that folder, a backup file of the web content was discovered and downloaded. Review the contents of the zip file and determine how to take control of the attacker’s server. 

## Author


## Solve
hashcat -m 1410 -a 0 c5f64fba0f52ae8ec298c3d2549bb4da1e636dc5c07c01476820f56f032f5f52:borscht /opt/wordlists/rockyou.txt -r /opt/rules/append_ds.rule

The flag for the challenge is "ivan2020!".
