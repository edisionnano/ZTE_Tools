# ZTE Tools
Tools for ZTE routers provided by Greek ISPs

## Available Routers
➣ [H268Q V8 WiFi 6](H268Q%20V8) - Firmware and Default configuration decryption for the ZTE ZXHN H268Q V8 Wi-Fi 6

➣ [H268Q V7 WiFi 5](H268Q%20V7) - Firmware and Default configuration decryption for the ZTE ZXHN H268Q V7 Wi-Fi 5

➣ [F8648P](https://github.com/edisionnano/F8648P) - The main router of DEI Fiber, also provided by Telekom Greece for 3 Gbps connections. Includes tools to decrypt the user config, find the admin password and get shell access among other things

➣ [H108N V2.5](H108N%20V2.5) - Very popular ADSL router provided by Vodafone, Forthnet and Wind 

➣ [H268N / Speedport Entry 2i](H268N) - ADSL Router mostly provided by Cosmote as Speedport Entry 2i and also by WIND as ZXHN H268N

➣ [H208N](H208N) - Old ADSL router initially provided by Cyta and then Vodafone, for the CyTA version use `--key 'Renjx%2$CjM'` to decrypt the user config with ZCU

➣ [H1600](H1600) - The latest DSL router provided by Cosmote Telekom

➣ [H288A](H288A) - DSL router provided by NOVA

➣ [H267A](H267A) - DSL router provided by Vodafone for retail and One Net customers. Use `--model "ZXHN H267A V1.0 VDFSOHO"` in ZCU for One Net and `ZXHN H267A V1.0` for retail.

## General Info and Tips
 - To get full privileges when enabling Telnet and SSH, in their respective blocks change fields level to 1 and `ProcType` to 0, if they exist.

- To get the signature needed to re-encrypt the user configuration file just run `hexedit` on the encrypted config and you will find a string at the top that describes the router's model, for example `ZXHN H267A V1.0`. If the file starts with `DDDDUUUU` you will also need to use the `--include-header` flag when re-encrypting with zte config utility.
