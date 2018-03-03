# -*- coding:utf-8 -*-

from datetime import datetime
from schematics.models import Model
from schematics.types import StringType, EmailType, BooleanType, IntType, ListType, ModelType, DateTimeType
from .my_types import One2One

#type for user
class UserType(Model):
    _name = 'user_type'
    id = IntType(required=False)
    type_name = StringType(required=True)
    create_time = DateTimeType(required=True, default=datetime.now())

#class for adding user in db
class UserAddModel(Model):
    _name = 'users_add'
    id = IntType(required=False)
    age = IntType(default=None, required=False)
    create_time = DateTimeType(required=True, default=datetime.now())
    phone = StringType(default=None, required=False)
    address = StringType(default=None, required=False)
    sex = IntType(default=None, required=False)

#user and his abilities
class UserModel(Model):
    _name = 'users'
    id = IntType(required=False)
    first_name = StringType(required=True)
    last_name = StringType(required=False, default='')
    type = ModelType(UserType, required=True)
    descr = StringType(required=False, default='')
    user_photo = StringType(required=False, default='')
    user_photos = StringType(required=False, default='')
    email = EmailType(required=True)
    nickname = StringType(required=True)
    password = StringType(required=True)
    create_time = DateTimeType(required=True, default=datetime.now())
    user_add = One2One(UserAddModel)

#interaction with 2 users
class UserRelation(Model):
    _name = 'user_relation'
    id = IntType(required=False)
    user1 = IntType(required=True)
    user2 = IntType(required=True)
    block = IntType(required=True, default=0)
    sender_id = IntType(required=False)
    create_time = DateTimeType(required=True, default=datetime.now())

#class for group and her abilities
class GroupUserModel(Model):
    id = IntType(required=False)
    group = ModelType(UserModel, required=True)
    user = ModelType(UserModel, required=True)
    create_time = DateTimeType(required=True, default=datetime.now())

#class for post and its abilities
class PostModel(Model):
    id = IntType(required=False)
    title = StringType(required=True)
    photos = StringType(required=False, default='')
    text = StringType(required=False, default=None)
    likes = IntType(required=True, default=0)
    user = ModelType(UserModel, required=True)
    create_time = DateTimeType(required=True, default=datetime.now())

#class for comment and its abilities
class CommentsModel(Model):
    id = IntType(required=False)
    text = StringType(required=False, default=None)
    likes = IntType(required=True, default=0)
    user = ModelType(UserModel, required=True)
    create_time = DateTimeType(required=True, default=datetime.now())

#class for comment under post and its abilities(idefentication number,to what post does it belong)
class PostCommentModel(Model):
    id = IntType(required=False)
    post = ModelType(PostModel, required=True)
    comment = ModelType(CommentsModel, required=True)
    create_time = DateTimeType(required=True, default=datetime.now())

#class for Message and its abilities
class MessageModel(Model):
    id = IntType(required=False)
    user_from = ModelType(UserModel, required=True)
    user_to = ModelType(UserModel, required=True)
    is_read = BooleanType(required=True, default=False)
    create_time = DateTimeType(required=True, default=datetime.now())


if __name__ == '__main__':
    typep = UserType()
    # typep.id = 1
    # typep.name = 'test'

    typep.import_data({'id':1,'name':'test'})
    print(typep.id)

    # user = UserModel()
    # user.id = 1
    # user.first_name = 'test'
    # user.last_name = 'test'
    # user.type = typep
    # user.descr = 'test'
    # user.user_photo = 'test'
    # user.user_photos = ['test']
    # user.email = 'testtest.test'
    # user.nickname = 'test'
    # user.password = 'test'
