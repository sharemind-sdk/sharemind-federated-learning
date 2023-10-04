#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR

# read variables from path.env
source ${ROOT_DIR}/path.env

# create necessary directories
ssh ${PARTY1_PATH} "cd ${PROJECT_DIR}; mkdir -p keys programs logs audit profiles tdbhdf5"
ssh ${PARTY2_PATH} "cd ${PROJECT_DIR}; mkdir -p keys programs logs audit profiles tdbhdf5"
ssh ${PARTY3_PATH} "cd ${PROJECT_DIR}; mkdir -p keys programs logs audit profiles tdbhdf5"

# key exchanges
scp ./server/server1/keys/server1-pub-key ${PARTY1_PATH}:${PROJECT_DIR}/keys/server1-pub-key
scp ./server/server1/keys/server1-priv-key ${PARTY1_PATH}:${PROJECT_DIR}/keys/server1-priv-key
scp ./server/server1/keys/server1-pub-key ${PARTY2_PATH}:${PROJECT_DIR}/keys/server1-pub-key
scp ./server/server1/keys/server1-pub-key ${PARTY3_PATH}:/${PROJECT_DIR}/keys/server1-pub-key

scp ./server/server2/keys/server2-pub-key ${PARTY2_PATH}:${PROJECT_DIR}/keys/server2-pub-key
scp ./server/server2/keys/server2-priv-key ${PARTY2_PATH}:${PROJECT_DIR}/keys/server2-priv-key
scp ./server/server2/keys/server2-pub-key ${PARTY1_PATH}:${PROJECT_DIR}/keys/server2-pub-key
scp ./server/server2/keys/server2-pub-key ${PARTY3_PATH}:/${PROJECT_DIR}/keys/server2-pub-key

scp ./server/server3/keys/server3-pub-key ${PARTY3_PATH}:${PROJECT_DIR}/keys/server3-pub-key
scp ./server/server3/keys/server3-priv-key ${PARTY3_PATH}:${PROJECT_DIR}/keys/server3-priv-key
scp ./server/server3/keys/server3-pub-key ${PARTY1_PATH}:${PROJECT_DIR}/keys/server3-pub-key
scp ./server/server3/keys/server3-pub-key ${PARTY2_PATH}:${PROJECT_DIR}/keys/server3-pub-key

scp ./client/client1/keys/client1-pub-key ${PARTY1_PATH}:${PROJECT_DIR}/keys/client1-pub-key
scp ./client/client1/keys/client1-pub-key ${PARTY2_PATH}:${PROJECT_DIR}/keys/client1-pub-key
scp ./client/client1/keys/client1-pub-key ${PARTY3_PATH}:/${PROJECT_DIR}/keys/client1-pub-key

scp ./client/client2/keys/client2-pub-key ${PARTY1_PATH}:${PROJECT_DIR}/keys/client2-pub-key
scp ./client/client2/keys/client2-pub-key ${PARTY2_PATH}:${PROJECT_DIR}/keys/client2-pub-key
scp ./client/client2/keys/client2-pub-key ${PARTY3_PATH}:/${PROJECT_DIR}/keys/client2-pub-key

scp ./client/client3/keys/client3-pub-key ${PARTY1_PATH}:${PROJECT_DIR}/keys/client3-pub-key
scp ./client/client3/keys/client3-pub-key ${PARTY2_PATH}:${PROJECT_DIR}/keys/client3-pub-key
scp ./client/client3/keys/client3-pub-key ${PARTY3_PATH}:/${PROJECT_DIR}/keys/client3-pub-key

# copy license-dev.p7b
echo ""
echo "Copy license-dev.p7b"
scp ${ROOT_DIR}/server/server1/license-dev.p7b ${PARTY1_PATH}:/${PROJECT_DIR}/license-dev.p7b
scp ${ROOT_DIR}/server/server2/license-dev.p7b ${PARTY2_PATH}:/${PROJECT_DIR}/license-dev.p7b
scp ${ROOT_DIR}/server/server3/license-dev.p7b ${PARTY3_PATH}:/${PROJECT_DIR}/license-dev.p7b

# copy import-script.sb
echo ""
echo "Copy import-script.sb"
scp ${ROOT_DIR}/server/server1/programs/import-script.sb ${PARTY1_PATH}:/${PROJECT_DIR}/programs/import-script.sb
scp ${ROOT_DIR}/server/server1/programs/import-script.sb ${PARTY2_PATH}:/${PROJECT_DIR}/programs/import-script.sb
scp ${ROOT_DIR}/server/server1/programs/import-script.sb ${PARTY3_PATH}:/${PROJECT_DIR}/programs/import-script.sb

# copy run.sh
echo ""
echo "Copy run.sh"
scp ${ROOT_DIR}/server/server1/run.sh ${PARTY1_PATH}:/${PROJECT_DIR}/run.sh
scp ${ROOT_DIR}/server/server2/run.sh ${PARTY2_PATH}:/${PROJECT_DIR}/run.sh
scp ${ROOT_DIR}/server/server3/run.sh ${PARTY3_PATH}:/${PROJECT_DIR}/run.sh

# copy configuration files
echo ""
echo "Copy configuration files"
scp ${ROOT_DIR}/server/server1/access-control.conf ${PARTY1_PATH}:/${PROJECT_DIR}/access-control.conf
scp ${ROOT_DIR}/server/server2/access-control.conf ${PARTY2_PATH}:/${PROJECT_DIR}/access-control.conf
scp ${ROOT_DIR}/server/server3/access-control.conf ${PARTY3_PATH}:/${PROJECT_DIR}/access-control.conf
scp ${ROOT_DIR}/server/server1/shared3p.cfg ${PARTY1_PATH}:/${PROJECT_DIR}/shared3p.cfg
scp ${ROOT_DIR}/server/server2/shared3p.cfg ${PARTY2_PATH}:/${PROJECT_DIR}/shared3p.cfg
scp ${ROOT_DIR}/server/server3/shared3p.cfg ${PARTY3_PATH}:/${PROJECT_DIR}/shared3p.cfg
scp ${ROOT_DIR}/server/server1/server1.cfg ${PARTY1_PATH}:/${PROJECT_DIR}/server1.cfg
scp ${ROOT_DIR}/server/server2/server2.cfg ${PARTY2_PATH}:/${PROJECT_DIR}/server2.cfg
scp ${ROOT_DIR}/server/server3/server3.cfg ${PARTY3_PATH}:/${PROJECT_DIR}/server3.cfg
scp ${ROOT_DIR}/server/server1/server1-tabledb.cfg ${PARTY1_PATH}:/${PROJECT_DIR}/server1-tabledb.cfg
scp ${ROOT_DIR}/server/server2/server2-tabledb.cfg ${PARTY2_PATH}:/${PROJECT_DIR}/server2-tabledb.cfg
scp ${ROOT_DIR}/server/server3/server3-tabledb.cfg ${PARTY3_PATH}:/${PROJECT_DIR}/server3-tabledb.cfg
scp ${ROOT_DIR}/server/server1/server1-tabledb_hdf5-DS1.cfg ${PARTY1_PATH}:/${PROJECT_DIR}/server1-tabledb_hdf5-DS1.cfg
scp ${ROOT_DIR}/server/server2/server2-tabledb_hdf5-DS1.cfg ${PARTY2_PATH}:/${PROJECT_DIR}/server2-tabledb_hdf5-DS1.cfg
scp ${ROOT_DIR}/server/server3/server3-tabledb_hdf5-DS1.cfg ${PARTY3_PATH}:/${PROJECT_DIR}/server3-tabledb_hdf5-DS1.cfg