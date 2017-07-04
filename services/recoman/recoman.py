# -*- coding: utf-8 -*-



#-----------------------------------------------------------------------------------
#class
class Recoman(object):
    def __init__(self, _postObj):
        self.postObj = _postObj

    def getData(self):
        return [self.postObj, self.postObj, self.postObj, self.postObj]
