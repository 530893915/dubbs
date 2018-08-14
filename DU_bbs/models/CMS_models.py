#coding:utf8

from exts import db
import datetime
from werkzeug.security import generate_password_hash,check_password_hash




# CMS组(权限)表
class CMSPermission(object):
    ADMINISTRATOR = 255
    OPERATOR = 1
    PERMISSION_MAP = {
        ADMINISTRATOR: ('超级管理员权限','拥有最高的权限'),
        OPERATOR: ('普通管理员权限','可以操作前台用户/帖子等')
    }

# CMS 用户-角色 关系表
cms_user_role = db.Table('cms_user_role',
    db.Column('role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True))

# CMS组(角色)表
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.String(100),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    permissions = db.Column(db.Integer,default=CMSPermission.OPERATOR,nullable=False)


# CMS用户表模型
class CMSUser(db.Model):
    __tablename__ = 'cms_user'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.datetime.now)
    is_active = db.Column(db.Boolean,default=True)
    last_login_time = db.Column(db.DateTime,nullable=True)
    roles = db.relationship('CMSRole',secondary=cms_user_role,backref='users')

    # 密码加密
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)

    # 验证加密的密码和原生密码是否一致
    def check_password(self,rawpwd):
        return check_password_hash(self.password,rawpwd)

    # 判断是否为超级管理员
    @property
    def is_superadmin(self):
        return self.has_permission(CMSPermission.ADMINISTRATOR)

    # 判断当前用户有没有某一个权限
    def has_permission(self,permission):
        if not self.roles:
            return False
        all_permissions = 0
        for role in self.roles:
            all_permissions = all_permissions | role.permissions
        return all_permissions & permission == permission

    # 返回所有权限和对应的内容
    @property
    def permissions(self):
        if not self.roles:
            return None

        all_permissions = 0
        for role in self.roles:
            all_permissions |= role.permissions

        permission_dicts = []  # 是个数组，里面放的字典
        for permission,permission_info in CMSPermission.PERMISSION_MAP.items():
            if permission & all_permissions == permission:
                permission_dicts.append({permission:permission_info})

        return permission_dicts