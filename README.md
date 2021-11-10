## Usage
Database stores login, password and token issued to user during the authentication




## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requests.

```bash
pip3 install datetime flask_sqlalchemy flask flask.helpers flask.json jwt
```
## Example
  user1 = User('Arman', 'passowrd', '')
  user2 = User('Sanzhar', 'password', '')
  user3 = User('Eldos', 'password', '')
  db.session.add(user1)
  db.session.add(user2)
  db.session.add(user3)
  db.session.commit()
  
 After creating user you can log in to localhost/login route 
which will assign token value to token atribute of the user in User table which will expire a#Assignment3
