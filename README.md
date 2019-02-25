# key-generation
To generate private key and address pairs for harmony tokens, 
first download keygen_linux or keygen_mac executable from bin directory, and then run the following command in the terminal.
```bash
(on Linux)
chmod +x keygen_linux 
./keygen_linux  
(on MacOS)
chmod +x keygen_mac 
./keygen_mac
 ```


You can also generate the key.json by the following instructions:
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
### What's next
Keep your key.json safe by saving it offline 

