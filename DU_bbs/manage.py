#coding:utf8

from exts import db
from DU_bbs import app
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from models import CMS_models,common_models,front_models
from sqlalchemy.orm.collections import InstrumentedList



CMSUser = CMS_models.CMSUser
CMSRole = CMS_models.CMSRole
CMSPermission = CMS_models.CMSPermission

FrontUser = front_models.FrontUser
BoardModel = common_models.BoardModel
PostModel = common_models.PostModel

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)


# 添加CMS用户
@manager.option('-e','--email',dest='email')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-r','--role_name',dest='role')
def create_cms_user(email,username,password,role):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        print('邮箱已经存在！')
        return
    roleModel = CMSRole.query.filter_by(name=role).first()
    if not roleModel:
        print('角色不存在！')
        return
    user = CMSUser(username=username,password=password,email=email)
    roleModel.users.append(user)
    db.session.commit()
    print('恭喜！cms用户添加成功！')


# 添加CMS角色
@manager.option('-n','--name',dest='name')
@manager.option('-d','--desc',dest='desc')
@manager.option('-p','--permissions',dest='permissions')
def create_role(name,desc,permissions):
    role = CMSRole(name=name,desc=desc,permissions=permissions)
    db.session.add(role)
    db.session.commit()
    print('角色添加成功！')

@manager.command
def test_board():
    board = BoardModel.query.first()
    # list类型没有filter方法
    # Query.filter
    print(type(board.posts))



if __name__ == '__main__':
    manager.run()