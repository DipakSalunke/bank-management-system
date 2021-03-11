# bank-management-system   
### python3, flask-restful, SQLAlchemy, flask_jwt_extended, pytest   
   
![bms](bank-management-system.svg)   
   
## How to run
requirements:   
python3 in cmd   
install pipenv   
```pip install pipenv```      
cd to bank-management-system folder   

### for run
install the last successful environment for run   
```pipenv install --ignore-pipfile```      
run registration service   
```python src\registration\app.py```   
run account service   
```python src\account\app.py```   
run loan service   
```python src\loan\app.py```   

### for dev
install the last successful environment for developement   
```pipenv install --dev```     
for testing   
```coverage run -m pytest <test_files_path>```   
```coverage run -m pytest src/registration/tests/user_tests.py```  
```coverage run -m pytest src/account/tests/account_tests.py```   
```coverage run -m pytest src/loan/tests/loan_tests.py``` 

check test coverage   
```coverage report -m```   

registration service endpoints(port: 5001):
```
/register/customer [POST]
/register/user [POST]
/user/ispresent [POST]
/user/<int:user_id> [GET, DELETE]
/login [POST, GET]
/refresh [POST]
/logout [POST]
```  
   
account service endpoints(port: 5002):
```
/account [GET, PUT]
/account/ispresent [POST]
```
loan service endpoints(port: 5003):
```
/loan [GET, POST]
```


