# Emergency Alert System (EAS) Specific Area Message Encoding (SAME) Encoder

[Here's a quick background on how EAS SAME headers work.](https://www.youtube.com/watch?v=Z5o1sfXXf9E)

Since the mid-90's, a a device has sat in the headend room of every TV / FM / AM station that listens for EAS SAME signals on neighboring stations and, if the specified information matches the predefined filters for location and type of emergency, rebroadcasts the emergency message on its local station.

Because I couldn't find an app that didn't require ten thousand dependencies, I wrote a Python script that generates these tones!  Tested and is correctly interpreted by my SAGE
EAS ENDEC.

[YouTube demo!](https://www.youtube.com/watch?v=OVxHkMDX2F8)

# Important Note

Please please please please PLEASE use this responsibly.  You will get in a lot of trouble if you send these over the airwaves.  But if you just bought an old ENDEC on eBay and want to put it through its paces, this is the script for you!  

Also if you create a fork of this repo, please credit the [original project](https://github.com/nicksmadscience/eas-same-encoder/) :)
