from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config

from resources.follow import FollowResource
from resources.memo import MemoListResource, MemoResource, fMemoListResource
from resources.user import UserLoginResource, UserRegisterResource

app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)
# JWT 매니저 초기화
jwt=JWTManager(app)

# # 로그아웃된 토큰으로 요청하는 경우 실행되지 않도록 처리하는 코드
# @jwt.token_in_blocklist_loader
# def check_if_token_is_revoked(jwt_header, jwt_payload) :
#     jti = jwt_payload['jti']
#     return jti in jwt_blocklist

api = Api(app)

# 경로와 리소스를 연결한다.
api.add_resource(UserRegisterResource, '/user/register')        # 회원가입
api.add_resource(UserLoginResource, '/user/login')              # 로그인
api.add_resource(MemoListResource,'/memo')                      # 메모작성, 리스트보기
api.add_resource(MemoResource,'/memo/<int:memo_id>')            # 메모수정, 삭제
api.add_resource(fMemoListResource,'/fMemo')                      # 친구메모 불러오기
api.add_resource(FollowResource,'/follow/<int:followeeId>')     # 친구맺기, 끊기
if __name__ == '__main__' :
    app.run()