DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="${DIR}/../aws_lambda/pgp_encrypt"
cd $BASE_DIR
rm -rf package-lock.json node_modules
npm install openpgp@2.3.5
rm -rf pgp_encrypt.zip
zip -r9 pgp_encrypt.zip index.js node_modules package-lock.json
mv pgp_encrypt.zip $DIR
cd ${DIR}
aws --profile default --region us-west-2 lambda update-function-code --function-name pgp_encrypt --zip-file fileb://${DIR}/pgp_encrypt.zip