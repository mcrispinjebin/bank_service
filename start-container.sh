# Set env vars
db_user='root'
db_pwd='Global!23'
db_name='bank_service'

# Host vars
db_host='db_host_ip'
db_host_ip='192.168.18.209'

source_dir=$PWD
destination_dir='/src'

if [ "$1" = restart ]
then
  docker restart bank-system
  exit
fi


docker stop bank-system
docker rm -f bank-system

echo "Starting Container.."
echo "bank-system"
docker run -d -w /src/ --env DB_URL=$db_host --env DB_NAME=$db_name --env DB_USER=$db_user --env DB_PASS=$db_pwd --add-host=$db_host:$db_host_ip -v "$source_dir":$destination_dir --name bank-system -p 8000:4982 bank-service-img:latest
