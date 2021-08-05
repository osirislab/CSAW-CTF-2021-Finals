# Collision course

A database administrator wrote a script to create unique IDs from the original numeric IDs contained within a database. While doing so, they decided to use the original IDs to encrypt his password, since they were sure the original IDs couldn't be recovered. Prove them wrong and recover their password.

Tip - my_aes.py is a library they used for encrypting and decrypting password.bin. It can be used as a standalone script to decrypt the .bin file if the password is obtained

### Files provided:
encrypt_database.py

encrypted_database.csv

my_aes.py

password.bin

## Testing speed of standard laptop
```
lime:csaw_crypto sean$ python3 test_md5_speed.py
[*] Running hash test of 1,000,000 iterations
[*] Runtime of 1.56850807 seconds
[*] Estimated speed of 637 Kmd5/s
```
## Calculating numbers with current configuration
```
lime:csaw_crypto sean$ python3 calculate_numbers.py --id 500 --salt $((36**3)) --hash-length 4 --md5-speed 500
[*] Total hash space: 23,328,000
[*] Estimated single entry hash space crack time: 0.78 m
[*] Estimated all entry hash space crack time: 6.48 h
[*] Single-entry collisions: 355.96
[*] ID collision possibility (for known salt): 0.76294 %
[*] How many salt/id combos match 1 records: 355.95703125
[*] How many salt/id combos match 2 records: 2.7157366275787354
[*] How many salt/id combos match 3 records: 0.02071942617476452
[*] How many salt/id combos match 4 records: 0.00015807667674838655
[*] Time to crack all IDs with known salt: 0.01 m
```

## Running actual hash collision

```
lime:csaw_crypto sean$ python3 test_md5_collisions.py
[*] Testing collisions of valid combos for aaaa
    -Salt set: abcdefghijklmnopqrstuvwxyz1234567890
    -Salt len: 3
    -Hash len: 4
    -Num ids: 500
[*] Got 349 instances for aaaa
[*] Took 47.622256983 seconds
```
