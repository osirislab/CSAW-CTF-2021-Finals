
https://drive.google.com/file/d/1hFN2uWoTsAOF53B2WMawJssD7JCI4Q3B/view?usp=sharing

## Evidence Files:
    disk-image-1.vmdk
SHA256: A7B4642B426AD163BD7374DCAD41454637E1332FC7DE95F4B32154EFBE42CA02
disk-image-2.vmdk
SHA256: B354A04CC5880DFB903B51BD208B76CE0C7BC52F4F0CCDE4654111BF0E83EEF4
disk-image-3.vmdk
SHA256: FB679101C2A1BAECEA707B28CE57785C9868378674D7B2D5D8FB6A0050571F5D
wd17-ee06c78a.vmem
SHA256: 6AD380E5B83B7C230630B68D5C2C8519EDF90A2B07330EE5DF4F7FDBA958DF16
wd17-ee06c78a.vmss
SHA256: 0285D7E9DC74D730496845044898EE5184C51ADFDF23424FC330FD22E4296E4C

## Disks Make a RAID 5 storage pool on windows 10:
Using the memory dump you can find the drive recovery key

Mount the vmware drives to a windows 10 pro/enterprise system that is fully updated and you will get a prompt to unlock a storage device with the indeifition of AF42D
Use strings on the memory image:

strings -a -td wd17-ee06c78a.vmem > strings.txt
strings -a -td -el wd17-ee06c78a.vmem >> strings.txt
grep AF42D615 strings.txt -C 10 |grep "Recovery Key:" -A 1 |grep - |cut -c14-72

## Answer Data
The output gives us the recovery key
    457083-367026-031449-323785-173822-071071-510774-671924
Using the recovered key you can unlock the drive and see 4 files on the system

cat1.jpg
cat2.jpg
cat3.jpg
cat4.jpg

