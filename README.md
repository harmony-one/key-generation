# key-generation
To generate private key and address pairs for harmony tokens, 
first download keygen_linux or keygen_mac executable from bin directory, and then run the following command in Terminal.
```bash
(on Linux)
chmod +x keygen_linux 
./keygen_linux  
(on MacOS)
chmod +x keygen_mac 
./keygen_mac
 ```


You can also run key generation by the following instructions:
##### Install python and python libraries
```bash
git clone https://github.com/harmony-one/key-generation
cd key-generation 
chmod +x install.sh
./install
```

##### Generate private key and public address 
```bash
python3 client.py
```
### Keep your private key safe
The program will first ask for your password which is used to encrypt the private key. The encrypted private key is stored in key.json file, so don't lose key.json file and don't forget your password.

The program also creates seed phrase (12 ordered words) which can be used to recover your private key. 

This means you can recover the private key from either seed phrase or key.json with your password. The best practice is to write down the seed phrase (12 words) 
in a paper and store it securely, and save the key.json file in some offline storage (e.g. usb or computer that not connecting to network)

