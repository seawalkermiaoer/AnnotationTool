# -*- coding:utf-8 -*-
# __author__ = 'seawalker'

import wx


class QuestionListCtrl(wx.ListCtrl):
    def __init__(self, parent, subDatas, size, id=-1, pos=(0, 0)):
        wx.ListCtrl.__init__(self, parent, id, pos, size,
                             style=wx.LC_SMALL_ICON)
        self.SetColumnWidth(0, 550)
        self.subDatas = subDatas
        self.InitUI()
        pass


    def InitUI(self):
        self.ShowListDatas(self.subDatas)
        pass

    def ShowListDatas(self, datas):
        self.subDatas = datas
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.SetFont(font)

        for index in range(len(self.subDatas)):
            subject = self.subDatas[index]
            content = subject.get('simques', '')
            self.InsertItem(index, content)


    def refreshDataShow(self, newDatas):
        self.datas = newDatas
        self.DeleteAllItems()
        self.ShowListDatas(self.datas)
        self.Refresh()
