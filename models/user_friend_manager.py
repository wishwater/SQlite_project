# -*- coding:utf-8 -*-


from models.models import UserRelation

from models.base_manager import SNBaseManager

class UserRelationManager(SNBaseManager):


    def __init__(self):
        self.object = UserRelation()

    def addFriend(self,user,friend):
        if not (isinstance(user, int) and isinstance(friend, int)):
            return
        if self.getFriend(user, friend):
            return

        if self.object.block == 2:
            self.object.user1 = user
            self.object.user2 = friend
            self.object.block = 0
            return self.save()


        self.object.user1 = user
        self.object.user2 = friend
        self.object.block = 2

        return self.saveFriends()

    def saveFriends(self):
        sql = self.insert_sql.format(self.object._name, self._sqlValues(self.insert_sql_values))
        return self.executeSQL(sql)
        return('ok')

    def delFriend(self, user1, friend1):
        friend = int(friend1)
        user = int(user1)
        if not (isinstance(user, int) and isinstance(friend, int)):
            return

        print('del1')

        return self.delete().And([('user1','=',user),('user2','=',friend)])\
            .Or([('user1','=',friend),('user2','=',user)]).run()

    def getFriends(self, user):
        if not isinstance(user, int):
            return

        all = True

        self.select().And([('user1','=',user)]).Or([('user2','=',user)]).run(all)

    def getFriend(self, user, friend):
        if not (isinstance(user, int) and isinstance(friend, int)):
            return

        self.select().And([('user1', '=', user), ('user2', '=', friend)]) \
            .Or([('user1', '=', friend), ('user2', '=', user)]).run()

    def isFriend(self, user, friend):
        if not (isinstance(user, int) and isinstance(friend, int)):
            return

        self.select().And([('user1', '=', user), ('user2', '=', friend)]) \
            .Or([('user1', '=', friend), ('user2', '=', user)]).run()

        if self.object.id:
            return True
        return False

    def blockFriend(self,user1, friend1):
        friend = int(friend1)
        user = int(user1)
        if not (isinstance(user, int) and isinstance(friend, int)):
            return
        print(user,friend)
        print('hello,misciu')
        self.getFriend(user,friend)
        if self.object.block == 0:
            self.object.block = 1
        else:
            self.object.block = 0
        self.save()
