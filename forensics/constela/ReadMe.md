# Constela
## Description
The year is 7331, and BadCorp rules the galaxy with it's omnipresent satelites. But recently a resistance movement led by a band of hackers calling themselves the OSIRIS has hacked into BadCorp systems, they have taken over the satelites and it is believed they are trying to send a message across the galaxy... </br>
Can humanity _see_ their message?

## Solution
The data has been exfiltrated using DNS. We extract out all the suspicious looking packets and find that the data is base64 encoded.

Taking the data and joining every pair of suspicious website and decoding it, we get some GPS coordinates.

Plotting the latitude and altitude gives us a QR code when scanned gives us the flag.

The final solver script that does everything is `solve.py`.
