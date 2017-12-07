# -*- coding:utf-8 -*-
# __author__ = 'seawalker'

import wx


class QuestionListCtrl(wx.ListCtrl):
    def __init__(self, parent, subDatas, size, id=-1, pos=(0, 0), style=wx.LC_SMALL_ICON):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style)
        self.SetColumnWidth(0, 500)
        self.subDatas = subDatas
        self.InitUI()
        pass

    def InitUI(self):
        self.ShowListDatas(self.subDatas)
        pass

    def ShowListDatas(self, datas):
        self.subDatas = datas
        for index in range(len(self.subDatas)):
            subject = self.subDatas[index]
            content = subject.get('simques', '')
            self.InsertItem(index, content, 0)

    def refreshDataShow(self, newDatas):
        self.datas = newDatas
        self.DeleteAllItems()
        self.ShowListDatas(self.datas)
        self.Refresh()