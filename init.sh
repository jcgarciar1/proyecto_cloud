export DB_HOST='34.121.176.97'
export DB_DB='files'
export DB_USER='cloud'
export DB_PORT='5432'
export DB_PW='cs(z3bT)<H{<9)bE'
export SECRET="GT1]t8h?'dSHVJSM"
export JWTSECRET="GT1]t8h?'dSHVJSM"
export CLOUD_SQL='cloud-project-382023'

sudo apt update
sudo apt install git -y
sudo apt install python3-pip -y
sudo pip install gunicorn
git clone https://github.com/jcgarciar1/proyecto_cloud.git
cd proyecto_cloud/API
git checkout entrega-4
pip install --upgrade pip
pip install -r requirements.txt
gunicorn -b  0.0.0.0:8000 app:app --workers=1
