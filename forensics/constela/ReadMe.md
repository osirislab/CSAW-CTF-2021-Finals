# Constela
## Description
Stuff will come here

## Solution
The data has been exfiltrated using DNS. We extract out all the suspicious looking packets and find that the data is base64 encoded.

Taking the data and joining every pair of suspicious website and decoding it, we get some GPS coordinates.

Plotting the latitude and altitude gives us a QR code when scanned gives us the flag.

The final solver script that does everything is `solve.py`.
