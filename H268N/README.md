# ZTE ZXHN H268N / Speedport Entry 2i
The the ZTE H268N is a DSL router provided by Cosmote Telekom (ΟΤΕ) as Speedport Entry 2i and WIND Greece as H268N.

## Decrypting the Firmware
Speedport OTA firmware images can be found [here](https://github.com/k-marios/Gr_ISP_Router_Firmware/tree/main/Cosmote/ZTE/Speedport_Entry_2i) and can be decrypted using the `decrypt_ota.py` script and then `binwalk -Me` to extract the rootfs.

## Deriving the config key
Each unit has a unique key used to encrypt the configuration backup exported from the router's web interface. The key is the first half of the md5sum of the `paramtag`. `paramtag` is a file on the nvram of ZTE routers that holds its unique values like the WiFi password, thankfully all of these values can be found on the label (and the hardware version on the web interface) so we can use the `derive_key_speedport.py` and `derive_key_wind.py` script to derive the key depending on your version, just don't forget to edit the placeholder values.

## Decrypting and manipulating the config
Once you get your key you can decrypt the config using [ZTE Config Utility](https://github.com/mkst/zte-config-utility) like that
```
python ./zte-config-utility/examples/decode.py 789682268EG8JG4Q01759_1970-01-01_config.bin config.xml --key 4cee9f56c18bc0f9
```
After you get the plaintext `config.xml` you can manipulate it to enable the root account, telnet and SSH.
<br>For the WIND version the root username is `WindSuper268N` and the password is `W!n0$Up3&PaSs68N`, the account is enabled so you can just login without any manipulation.
<br>The Speedport version has the root account disabled so you must find
```xml
<Tbl name="DevAuthInfo" RowCount="6">
<Row No="0">
<DM name="ViewName" val="IGD.AU1"/>
<DM name="Enable" val="0"/>
<DM name="AppID" val="1"/>
<DM name="User" val="Admin"/>
<DM name="Pass" val="Admin"/>
<DM name="Level" val="1"/>
<DM name="Extra" val=""/>
<DM name="ExtraInt" val="0"/>
</Row>
```
and flip the enable value
<br>To repackage the config use
```
python ./zte-config-utility/examples/encode.py config.xml config.bin --key 4cee9f56c18bc0f9 --signature "Speedport Entry 2i"
```
(with your own key) to encrypt it and then use the `fix.py` script to add the required `DDDDUUUU` header before restoring it on the web interface.