# -*- coding:utf-8 -*-


class BaseForm():
    fields = []

    def __init__(self,model = None):
        self.model = model

