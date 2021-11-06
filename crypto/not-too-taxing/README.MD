# Not Too Taxing

## Overview

We intercepted some email communications between a tax consultant and his client that contained some important tax documents. We were able to successfully extract two of the documents, but we can't figure out the password to the file to get the data. Attached are the two extracted files, Tax_Ret_Form_Blank.pdf and Tax_Ret_Form_Nov_2021.zip, and a transcript of the emails we found, SPBlock_Email.pdf.

Can you figure out the password so we can get this guy's info?


## Summary of Idea

The idea of the challenge is to take an advantage of a known vulnerability in the way windows used to encrypt zip files in the past. The broken algorithm is called ZipCrypto which today, is also known as "legacy windows encryption".The conditions for the attack to succeed is to know at least 12 bytes of plaintext (at least 8 of the bytes should be contiguous, also as long as the known plaintext is, the fastest the attack). The theme of the challenge is that a client insists to send his tax return form encrypted using that algorithm, to the CPA, even tho the CPA tells him that's not a safe algorithm anymore, and it's easily broken. This part of the challenge (break the ZipCrypto algoritm) is done but there will be another "challenge" that covers this one. PCAP file should be provided contains all the email chain between the client to the CPA.

The theme of the challenge involves email communications between a CPA and his client in preparation for a meeting to complete the client's taxes. The client is worried about sending his information in plaintext over email and insists on sending the information encrypted. The CPA is not necessarily tech savvy and won't install unapproved software on his company system because he doesn't want to upset his boss. The client really needs to get his taxes done, so he compromises and encrypts the file in a way that would allow any Windows 10 machine to prompt for a password for decryption without any additional software. This just so happens to be using the backwards compatible, legacy Windows  encryption method "ZipCrypto".

Note: The goal was to capture a PCAP with all the communications traffic to have the challengers extract the information and files themselves. The newer QUIC protocol made this a more difficult than expected, but the idea should be pursued in future rounds once more is known about decrypting the protocol.

## Solution

password for zip : 5up3r_53cr37_p455w0rd_5up3r_53cr37_p455w0rd (not part of the challenge)

https://blog.devolutions.net/2020/08/why-you-should-never-use-zipcrypto

use the command:
7z l -slt Tax_Ret_Form_Nov_2021.zip | grep Method

now we know it used the ZipCrypto algorithm.

solver to obtain the zip keys: 

bkcrack -C Tax_Ret_Form_Nov_2021.zip -c Tax_Ret_Form_Nov_2021.pdf -P Tax_Ret_Form_Blank.zip -p Tax_Ret_Form_Blank.pdf 

use the keys to make a new zip archive with known password "cracked":

bkcrack -C Tax_Ret_Form_Nov_2021.zip -k b2c4a24e f036ff3a 998f6727 -U Tax_Ret_Form_Nov_2021_cracked.zip cracked

then you got the zip archive and you can extract it using the password "cracked" that we set above:

unzip -P cracked Tax_Ret_Form_Nov_2021_cracked.zip

in the decrypted pdf, flag is in phone number field at the second page

flag{y0u_5h0uld_n3v3r_u53_z1pcryp70}
