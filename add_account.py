from prostgresssql.total import DataBase
from werkzeug.security import generate_password_hash

class AddAccounts:
    @staticmethod
    def encrypting_password(password):
        """
        Hashes the given password using PBKDF2 + SHA256.
        :param password: Plaintext password string
        :return: Hashed password string
        """
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    @staticmethod
    def add(email,firstname,lastname,username,password):
        new_password = AddAccounts.encrypting_password(password)
        DataBase.insert('users','firstname,lastname,username,email,password,roleid',f'({firstname},{lastname},{username},{email},{new_password},{1})')