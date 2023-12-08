from email_validator import validate_email, EmailNotValidError
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from mysql.connector import Error

from mysql_connection import get_connection
from utils import check_password, hash_password


class UserRegisterResource(Resource) :
    def post(self) :
        data = request.get_json()

        try :
            validate_email(data['email'])
        except EmailNotValidError as e :
            print(e)
            return {"Error" : str(e)}, 400

        if len(data['password']) < 4 and len(data['password']) > 14 :
            return {"Error" : "비밀번호 길이가 올바르지 않습니다."}, 400
        
        password = hash_password(data['password'])

        try :
            connection = get_connection()        

            query = '''insert into user
                    (email, password, nickname)
                    values
                    (%s, %s, %s);'''
            record = (data['email'], password, data['nickname'])

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            user_id = cursor.lastrowid

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"Error" : str(e)}, 500
        
        # user 테이블의 id로 JWT 토큰을 만들어야 한다.
        access_token = create_access_token(user_id)
        
        return {"result" : "success", "accessToken" : access_token}, 200

class UserLoginResource(Resource) :
    def post(self) :
        data = request.get_json()

        try :
            connection = get_connection()

            query = '''select *
                    from user
                    where email = %s;'''
            
            record = (data['email'],)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500
        
        if len(result_list) == 0 :
            return {"Error" : "회원가입된 정보가 없습니다."}, 400
        
        # 비밀번호가 맞는지 체크
        check = check_password(data['password'], result_list[0]['password'])
        if check == False :
            return {"error" : "비밀번호가 맞지 않습니다."}, 406
        
        # 암호화 토큰생성
        access_token = create_access_token(result_list[0]['id'])

        return {"result" : "success", "accessToken" : access_token}, 200