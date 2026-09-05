# ZTE ZXHN H268Q V8 Wi-Fi 6
Tools for the retail (ODP, 256MiB) and ONE Net (128 MiB) versions of the router, tested on the Vodafone variant.

## Decrypting the firmware
The `decrypt_ota.py` python script from the `Scripts` folder can be used to extract and decrypt the jffs2 rootfs partition from the OTA firmware image. You can find retail images [here](https://github.com/k-marios/Gr_ISP_Router_Firmware/tree/main/Vodafone/Retail/ZTE/H268Q) and ONE Net images [here](https://github.com/k-marios/Gr_ISP_Router_Firmware/tree/main/Vodafone/OneNet/ZTE/H268Q_WiFi6).

## Default Config
The `decrypt_default.py` script can decrypt the default xml configuration found in `/etc/`. From the configs we found that the password for the `root` account is `v7@d4F36&$hT4DAa:[0^` on the ONE Net firmware and `Vod@f0nE_24-R00t` on the retail firmware.