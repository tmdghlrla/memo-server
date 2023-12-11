from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector import Error

from mysql_connection import get_connection
class MemoListResource(Resource) :
    @jwt_required()
    def post(self) :
        data = request.get_json()
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''insert into memo
                    (userId, title, date, content)
                    values
                    (%s, %s, %s, %s);'''

            record = (user_id, data['title'], data['date'], data['content'])

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
    def get(self) :
        user_id = get_jwt_identity()

        # 쿼리스트링(쿼리 파라미터)를 통해서 데이터를 받아온다.

        offset = request.args.get('offset')      # args는 딕셔너리
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            query = '''select id, title, date, content
                    from memo
                    where userId = %s
                    order by date asc
                    limit '''+ str(offset) +''', '''+ str(limit) + ''';'''
            
            record = (user_id, )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            
            i = 0
            for row in result_list :
                result_list[i]['date'] = row['date'].isoformat()
                i= i+1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500
        
        
        return {"result" : "success", "items" : result_list, "count" : len(result_list)}, 200

class MemoResource(Resource) :
    @jwt_required() 
    def delete(self, memo_id) :
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query ='''delete from memo
                    where id= %s and userId = %s;'''
            
            record = (memo_id, user_id)

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
    def put(self, memo_id) :
        data = request.get_json()
        user_id = get_jwt_identity()        

        try :
            connection = get_connection()
            query = '''update memo
                    set title = %s,
                      content = %s, 
                      date = %s
                    where id = %s and userId=%s;'''
            
            record = (data['title'], data['content'], data['date'], memo_id, user_id)

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
    
class fMemoListResource(Resource) :
    @jwt_required()
    def get(self) :
        followerId = get_jwt_identity()
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            query = '''select m.id as memoId, m.userId, m.title,
                        m.date, m.content, m.createdAt,
                         m.updatedAt, u.nickname
                        from follow as f
                        join memo as m
                        on f.followeeId = m.userId
                        join user as u
                        on u.id = m.userId
                        where f.followerId = %s
                        order by m.date
                        limit ''' + offset +''', ''' + limit + ''';'''
            
            record = (followerId,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            print()
            print(result_list)
            print()

            i = 0
            for row in result_list :
                result_list[i]['date'] = row['date'].isoformat()
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['updatedAt'] = row['updatedAt'].isoformat()

                i = i+1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500
        
        return {"result" : "success", 
                "items" : result_list, 
                "count" : len(result_list)}, 200
