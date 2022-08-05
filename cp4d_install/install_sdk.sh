#!/bin/sh

# modify HOME_DIR / SRC_DIR variables to fit your environment
HOME_DIR="/home/wsuser/work/"
SRC_DIR="/project_data/data_asset/"

TEMP_DIR="${HOME_DIR}temp/"

arrDIR=("ibm-cloud-sdk-core"
        "wmla-python-sdk-master"
        "wmla-python-client-master")

arrFILE=("ibm-cloud-sdk-core.zip" 
        "wmla-python-sdk-master.zip"
        "wmla-python-client-master.zip")

echo -e "[1] Check file exists and unzip to temporary directory"

# check TEMP_DIR
if [ ! -d "$TEMP_DIR" ]
then
    mkdir "$TEMP_DIR"
else
    rm -rf "$TEMP_DIR"
    mkdir "$TEMP_DIR"
fi

# check file exists
for i in ${!arrFILE[@]};
do
    FILE="${SRC_DIR}${arrFILE[$i]}"
    FILE_NAME="${arrFILE[$i]}"

    if test -f "$FILE"; 
    then
        unzip "$FILE" -d $TEMP_DIR > unzip.log
        sleep 0.2
        echo -e "\t - ${arrFILE[$i]} ... OK."
    else
        echo -e "\n\n[Error] \n \tCheck the File: ${arrFILE[$i]}"
        exit 1
    fi
done


echo -e "\n[2] install ibm-cloud-sdk-core"
FILE_NAME="${arrFILE[0]}"
WORK_DIR="${TEMP_DIR}${arrDIR[0]}"

cd "$WORK_DIR"
echo -e "\t 2-1. change to directory: $WORK_DIR ... OK."

cd "$WORK_DIR"
pip install ./PyJWT-2.4.0-py3-none-any.whl > "PyJWT.log"
echo -e "\t 2-2. install dependency (PyJWT 2.4.0) ... OK."

tar -zxf ibm-cloud-sdk-core-3.15.3.tar.gz
echo -e "\t 2-3. untar ibm-cloud-sdk-core-3.15.3.tar.gz ... OK."

cd ibm-cloud-sdk-core-3.15.3
pip install . > "ibm-cloud-sdk-core-3.15.3.log"
echo -e "\t 2-4. install ibm-cloud-sdk-core-3.15.3 ... OK."


echo -e "\n[3] install wmla-python-sdk"
FILE_NAME="${arrFILE[1]}"
WORK_DIR="${TEMP_DIR}${arrDIR[1]}"

cd "$WORK_DIR"
echo -e "\t 3-1. change to directory: $WORK_DIR ... OK."

pip install . > "${FILE_NAME}.log"
cd "$HOME_DIR"
echo -e "\t 3-2. install library: $FILE_NAME ... OK."


echo -e "\n[4] install wmla-python-client"
FILE_NAME="${arrFILE[2]}"
WORK_DIR="${TEMP_DIR}${arrDIR[2]}"

cd "$WORK_DIR"
echo -e "\t 4-1. change to directory: $WORK_DIR ... OK."

pip install . > "${FILE_NAME}.log" 
cd "$HOME_DIR"
echo -e "\t 4-2. install library: $FILE_NAME ... OK."


cd "$HOME_DIR"
echo -e "\n\n [DONE] installation is completed"

