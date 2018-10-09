# Becoming a (tiny) Certificate Authority
It’s kind of ridiculous how easy it is to generate the files needed to become a certificate authority. It only takes two commands. First, we generate our private key:

```bash
  # openssl genrsa -des3 -out myCA.key 2048
```

You will be prompted for a pass phrase, which I recommend not skipping and keeping safe. The pass phrase will prevent anyone who gets your private key from generating a root certificate of their own. Output should look like this:

```
  Generating RSA private key, 2048 bit long modulus
  .................................................................+++
  .....................................+++
  e is 65537 (0x10001)
  Enter pass phrase for myCA.key:
  Verifying - Enter pass phrase for myCA.key:
```

Then we generate a root certificate:

```bash
  # openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem
```

You will prompted for the pass phrase of your private key (that you just choose) and a bunch of questions. The answers to those questions aren’t that important. They show up when looking at the certificate, which you will almost never do. I suggest making the Common Name something that you’ll recognize as your root certificate in a list of other certificates. That’s really the only thing that matters.
 
```
  Enter pass phrase for myCA.key:
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  -----
  Country Name (2 letter code) [AU]:NL
  State or Province Name (full name) [Some-State]:Flevoland
  Locality Name (eg, city) []:Almere
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:localhost
  Organizational Unit Name (eg, section) []:
  Common Name (e.g. server FQDN or YOUR name) []:localhost
  Email Address []:noreply@localhost
```

You should now have two files: myCA.key (your private key) and myCA.pem (your root certificate).

Congratulations, you’re now a CA. Sort of.

# Installing Your Root Certificate
We need to add the root certificate to any laptops, desktops, tablets, and phones that will be accessing your HTTPS sites. This can be a bit of a pain, but the good news is that we only have to do it once. Once our root certificate is on each device, it will be good until it expires.

# Creating CA-Signed Certificates for Your Dev Sites

Now that we’re a CA on all our devices, we can sign certificates for any new dev sites that need HTTPS. First, we create a private key:

```bash
  # openssl genrsa -out dev.localhost.key 2048
```

Then we create a CSR:

```bash
  # openssl req -new -key dev.localhost.key -out dev.localhost.csr
```

You’ll get all the same questions as you did above and, again, your answers don’t matter. In fact, they matter even less because you won’t be looking at this certificate in a list next to others.

```
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  -----
  Country Name (2 letter code) [AU]:NL
  State or Province Name (full name) [Some-State]:Flevoland
  Locality Name (eg, city) []:Almere
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:localhost
  Organizational Unit Name (eg, section) []:
  Common Name (e.g. server FQDN or YOUR name) []:localhost
  Email Address []:noreply@localhost
  
  Please enter the following 'extra' attributes
  to be sent with your certificate request
  A challenge password []:
  An optional company name []:
```

Next we’ll create the certificate using our CSR, the CA private key, the CA certificate, and a config file, but first we need to create that config file.

The config file is needed to define the Subject Alternative Name (SAN) extension we discussed in my last article. I created a new file named dev.localhost.ext and added the following contents:

```
  authorityKeyIdentifier=keyid,issuer
  basicConstraints=CA:FALSE
  keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
  subjectAltName = @alt_names

  [alt_names]
  DNS.1 = localhost
  DNS.2 = 127.0.0.1
```

We’re using a different config file for the SAN than in my last article because we’ll be running the openssl x509 command instead of the openssl req command. From what I understand, the x509 command is needed to do the signing with the root certificate and private key. Again, I found this example config file on Stack Overflow and it seems to work.

Now we run the command to create the certificate:

```bash
  # openssl x509 -req -in dev.localhost.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out dev.localhost.crt -days 1825 -sha256 -extfile dev.localhost.ext
```

You should be prompted for your CA private key pass phrase.

I now have three files: dev.localhost.key (the private key), dev.localhost.csr (the certificate signing request), and dev.localhost.crt (the signed certificate).

I can now configure my web server with the private key and the certificate. If you’re running a Linux server, you can use the instructions in our Hosting WordPress Yourself series. If you’re using MAMP, you can select the certificate and key files using the UI:

For any other dev sites, we can just repeat this last part of creating a certificate. No need to install any new certificates on any of my devices. Much better.
