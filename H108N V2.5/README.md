# ZTE ZXHN H108N V2.5
Very popular ADSL router provided by Vodafone, Forthnet and Wind 

## Decrypting config.bin
[ZTE Config Utility](https://github.com/mkst/zte-config-utility) can be used to decrypt the user configuration exported from the web interface. It needs and it's easy to find these by looking at the strings of the `cspd` binary. We can then decrypt the file like that:
```sh
python zte-config-utility/examples/auto.py --key-prefix 'GrWM2H&LTvz&f^' --iv-prefix '67b02a85c61c' --serial YOUR_SN_HERE config.bin config.xml
```
The config file will include the root password

## Decrypting /etc/db_default_*_cfg.xml
These are the default configurations and there are two of them, one for when the router is in DSL mode and one for when it is on WAN mode (getting internet through the ethernet port). Root passwords only work in DSL mode.
<br>The `decrypt_default.py` script can be used to decrypt these files to find the default root passwords

## Passwords
For the Vodafone version the credentials are:
```
root
A2?w{(h:^82RgyV5
```
For the Forthnet version the credentials are:
```
forthnet
F0rth@c$n3t#
```
<br>If using it on WAN mode, the valid credentials are `admin`/`admin` and `user`/`user`
