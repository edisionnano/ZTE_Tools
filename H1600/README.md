# H1600
The latest DSL router provided by Cosmote Telekom

## Decrypting the Firmware Updates
Firmware update (OTA) packages can be found [here](https://github.com/k-marios/Gr_ISP_Router_Firmware/tree/main/Cosmote/ZTE/H1600). You can use the `decrypt_ota.py` script to decrypt them and then use `binwalk -Me` to unpack them. Annex A is for PSTN and Annex B is for ISDN.

## Decrypting the default configuration
`/etc/db_default_auto_cfg.xml` is the default configuration, just like every modern ZTE router. You can use [ZTE Config Utility](github.com/mkst/zte-config-utility) to decrypt it like that:
```sh
python zte-config-utility/examples/decode.py --model "H1600" db_default_auto_cfg.xml out.xml
```

## Getting root access
1. Downgrade your device by uploading the earliest OTA from [here](https://github.com/k-marios/Gr_ISP_Router_Firmware/tree/main/Cosmote/ZTE/H1600). Annex A is for PSTN and Annex B is for ISDN.
2. After the downgrade is confirmed, you will have the option to download a configuration backup, do that.
3. Decrypt the config file using [ZTE Config Utility](github.com/mkst/zte-config-utility) and the following command
```sh
python examples/auto.py config.bin config.xml'
```
4. Find `<Tbl name="DevAuthInfo" RowCount="7">` and enable the first user (`Admin`)
5. Save and re-encrypt using
```sh
python ./examples/encode.py config.xml config_new.bin --key 'ZTEH1600Key02670001' --iv 'ZTEH1600Iv02670001' --signature "ZTE H1600"
```
6. Restore the modified config
7. You can login as `Admin`/`Admin`
8. You can now flash the latest version, you will lose the ability to export a config file but retain root access