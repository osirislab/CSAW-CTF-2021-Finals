# Malicious Solaris Download

## Overview

Attached is a malicious firmware updater package (`blackthorn_fw_updater.msi`) for some of legacy Solaris equipment. The package contains an ELF file that sends and modifies IEC104 traffic.

From the network traffic observed in `iec104.pcap`, it looks like it's just polling the controller for certain fields periodically, but the firmware does have the ability to change values at some point.

Can you figure out what IOA it tries to change, and what value it sets it to?

*Note: flag format: `IOA=Value`, e.g. `101=0xaabbccdd`*

## Solution

Opening MSI File (Linux):

```bash
$ msiextract blackthorn_fw_updater.msi 
Program Files/Blackthorn Firmware Updater/installer.exe

$ mv Program\ Files/Blackthorn\ Firmware\ Updater/installer.exe .

$ file installer.exe 
installer.exe: PE32+ executable (GUI) x86-64 (stripped to external PDB), for MS Windows 
```

We can then extract ELF file via binwalk:

```bash
$ binwalk -e installer.exe
$ mv _installer.exe.extracted/bt_monitor_fake_stripped .
```

or manually via dd:

```bash
$ dd if=installer.exe bs=10105822 skip=1 | gzip -cd > bt_monitor_fake_stripped
```

If we load up `bt_monitor_fake_stripped` in IDA/Ghidra/etc., it becomes clear pretty quickly that this binary is more challenging to look at than usual for a couple of reasons:

* It is statically linked, so it doesn't have any imports.
* It targets an older, more esoteric platform, so syscalls, etc. look different.
* Because it is self-contained, the compiler gets to have fun optimizing.

However, a few things should stick out as being odd/different after a little bit of digging. One in particular is the use of the irregular-looking `call far ptr 7:0`; this is an Intel call gate, and is used by Solaris to trigger syscalls (it's possible to find information about this online, or one might just guess that that's what it does since it's an oddity).

Knowing that, we can try to figure out what syscalls it might be using. To know that, we'd need more-or-less a copy of Solaris' `<sys/syscall.h>` (there is an equivalent under Linux, so making the logical leap from one to the other isn't crazy). If we Google for "Solaris syscall.h", the first result points us to [Radare's Solaris syscall header][syscall.h]; this isn't *exactly* right for Solaris 2.5.1, but all the relevant syscall numbers are correct.

Now that we know what triggers syscalls, we can figure out a bit more about what the binary does. We know that it talks over the network (via IEC104), and we have an example of the traffic (in the PCAP), so we should be able to figure out how the binary accomplishes this. A number of the different constants we see in the PCAP will show up in the binary, specifically in the functions that actually construct the packets.

We can figure out that the main loop tries to read data from the controller periodically, sleeping in between (although that is complicated by it needing to respond to external messages, both to receive spontaneous information transmission and keep-alive pings). There is one path that is only taken if a flag has been set, that sends a `C_BO_NA_1` message to change a bitfield on the controller. It takes the value of the bitstring in IOA 403, `and`s it with `0xffff00ff`, and `or`s it with `0x4200`. We can get the value of IOA 403 from the PCAP (it only ever has one value), and generate the answer from there.

In the artifacts directory, there is also the unstripped version of the binary (`bt_monitor_fake`) that could be used to help answer participants' questions if need be, recognizing that they might take a variety of approaches to figuring this out.

Solution Notes from verification during CTF play testing:
* The `C_BO_NA_1` message is not in the network traffic (Wireshark filter: `104asdu.typeid == 51`).  From the challenge author - "The idea is that one can make the analogue from looking at the PCAP data to main code path to understand how the binary is doing network communication, then extend that to figuring out what the part of the code that isn't called does."
* When calculating the solution, endianness is important.  In Wireshark, the value of IOA 403 (`104asdu.ioa == 403`) is `0x201fd473` in network byte order aka Big Endian.  For the calculation, the value needs to be in Little Endian (`0x73d41f20`) with the result then moved back to Big Endian to match the solution.

```
      0x73d41f20 AND 0xffff0ff OR 0x4200 = 0x73d44220 -> 0x2042d473
```

[syscall.h]: https://github.com/radare/radare/blob/master/doc/xtra/solaris-sys-syscall.h