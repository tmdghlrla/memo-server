from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask import request
from mysql.connector import Error

from mysql_connection import get_connection

class FollowResource(Resource) :
    @jwt_required()
    def post(self, followeeId) :
        followerId = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''insert into follow
                    (followerId, followeeId)
                    values
                    (%s, %s);'''
            
            record = (followerId, followeeId)

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500
        
        return {"result" : "success"}, 200
    
    @jwt_required()
    def delete(self, followeeId) :
        followerId = get_jwt_identity()
        try :
            connection = get_connection()
            query = '''delete from follow
                        where followerId = %s and 
                        followeeId = %s;'''
            
            record = (followerId, followeeId)

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()
        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500
        
        return {"resutl" : "success"}, 200