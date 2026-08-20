# wifi-deauther
**> Fully automatic wifi deauther (killer) coded in Python**

Built to understand 802.11 management frame injection and how deauthentication
attacks work at the protocol level. Intended for testing on networks you own
or have explicit permission to test.

**HOW TO INSTALL**

``` bash
git clone https://github.com/ZKAW/wifi-deauther && cd wifi-deauther && chmod +x INSTALL && sudo ./INSTALL
```

**HOW TO USE**

* Execute the program with:
``` bash
sudo python3 w-killer.py 
```
or (if you added the script to path):
``` bash
sudo w-killer
```
* Select your wireless interface
* Select the AP to deauth

That's it !

**IMPORTANT NOTES**

- This script is designed for **Linux** based operating systems. Using this script in another operating system may cause errors.
- The use of two wireless cards is **highly recommended** to avoid errors and complications.
- Your wireless card must have **monitor mode** available and enabled.
