#!/usr/bin/sh

# key generation for server1
openssl req -x509 -days 365 -nodes -newkey rsa:4096 -keyout "./server/server1/keys/server1-priv-key" -out "./server/server1/keys/server1-pub-key" -outform der
openssl rsa -in "./server/server1/keys/server1-priv-key" -out "./server/server1/keys/server1-priv-key" -outform der

# key generation for server2
openssl req -x509 -days 365 -nodes -newkey rsa:4096 -keyout "./server/server2/keys/server2-priv-key" -out "./server/server2/keys/server2-pub-key" -outform der
openssl rsa -in "./server/server2/keys/server2-priv-key" -out "./server/server2/keys/server2-priv-key" -outform der

# key generation for server3
openssl req -x509 -days 365 -nodes -newkey rsa:4096 -keyout "./server/server3/keys/server3-priv-key" -out "./server/server3/keys/server3-pub-key" -outform der
openssl rsa -in "./server/server3/keys/server3-priv-key" -out "./server/server3/keys/server3-priv-key" -outform der

# key generation for client1
openssl req -x509 -days 365 -nodes -newkey rsa:4096 -keyout "./client/client1/keys/client1-priv-key" -out "./client/client1/keys/client1-pub-key" -outform der
openssl rsa -in "./client/client1/keys/client1-priv-key" -out "./client/client1/keys/client1-priv-key" -outform der

# key generation for client2
openssl req -x509 -days 365 -nodes -newkey rsa:4096 -keyout "./client/client2/keys/client2-priv-key" -out "./client/client2/keys/client2-pub-key" -outform der
openssl rsa -in "./client/client2/keys/client2-priv-key" -out "./client/client2/keys/client2-priv-key" -outform der

# key generation for client3
openssl req -x509 -days 365 -nodes -newkey rsa:4096 -keyout "./client/client3/keys/client3-priv-key" -out "./client/client3/keys/client3-pub-key" -outform der
openssl rsa -in "./client/client3/keys/client3-priv-key" -out "./client/client3/keys/client3-priv-key" -outform der

# key exchanges
cp ./server/server1/keys/server1-pub-key ./server/server2/keys/server1-pub-key
cp ./server/server1/keys/server1-pub-key ./server/server3/keys/server1-pub-key
cp ./server/server1/keys/server1-pub-key ./client/client1/keys/server1-pub-key
cp ./server/server1/keys/server1-pub-key ./client/client2/keys/server1-pub-key
cp ./server/server1/keys/server1-pub-key ./client/client3/keys/server1-pub-key

cp ./server/server2/keys/server2-pub-key ./server/server1/keys/server2-pub-key
cp ./server/server2/keys/server2-pub-key ./server/server3/keys/server2-pub-key
cp ./server/server2/keys/server2-pub-key ./client/client1/keys/server2-pub-key
cp ./server/server2/keys/server2-pub-key ./client/client2/keys/server2-pub-key
cp ./server/server2/keys/server2-pub-key ./client/client3/keys/server2-pub-key

cp ./server/server3/keys/server3-pub-key ./server/server1/keys/server3-pub-key
cp ./server/server3/keys/server3-pub-key ./server/server2/keys/server3-pub-key
cp ./server/server3/keys/server3-pub-key ./client/client1/keys/server3-pub-key
cp ./server/server3/keys/server3-pub-key ./client/client2/keys/server3-pub-key
cp ./server/server3/keys/server3-pub-key ./client/client3/keys/server3-pub-key

cp ./client/client1/keys/client1-pub-key ./server/server1/keys/client1-pub-key
cp ./client/client1/keys/client1-pub-key ./server/server2/keys/client1-pub-key
cp ./client/client1/keys/client1-pub-key ./server/server3/keys/client1-pub-key
cp ./client/client1/keys/client1-pub-key ./client/client2/keys/client1-pub-key
cp ./client/client1/keys/client1-pub-key ./client/client3/keys/client1-pub-key

cp ./client/client2/keys/client2-pub-key ./server/server1/keys/client2-pub-key
cp ./client/client2/keys/client2-pub-key ./server/server2/keys/client2-pub-key
cp ./client/client2/keys/client2-pub-key ./server/server3/keys/client2-pub-key
cp ./client/client2/keys/client2-pub-key ./client/client1/keys/client2-pub-key
cp ./client/client2/keys/client2-pub-key ./client/client3/keys/client2-pub-key

cp ./client/client3/keys/client3-pub-key ./server/server1/keys/client3-pub-key
cp ./client/client3/keys/client3-pub-key ./server/server2/keys/client3-pub-key
cp ./client/client3/keys/client3-pub-key ./server/server3/keys/client3-pub-key
cp ./client/client3/keys/client3-pub-key ./client/client1/keys/client3-pub-key
cp ./client/client3/keys/client3-pub-key ./client/client2/keys/client3-pub-key