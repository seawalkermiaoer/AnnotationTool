#!/usr/bin/python
# -*- coding: UTF-8 -*-
import wx

from question_list_ctrl import QuestionListCtrl


class TagFrame(wx.Frame):
    """
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(TagFrame, self).__init__(*args, **kw)
        self.Center()
        # create a panel in the frame
        self.panel = wx.Panel(self)

        self.s1_tips = wx.StaticText(self.panel, 0, u"文件路径:", style=wx.TE_LEFT)
        self.s1_filename = wx.TextCtrl(self.panel, style=wx.TE_LEFT)
        self.s1_open = wx.Button(self.panel, label=u'打开')

        self.s2_tips = wx.StaticText(self.panel, 0, u"用户问题:", style=wx.TE_LEFT)
        self.s2_question = wx.TextCtrl(self.panel, style=wx.TE_LEFT)

        courseNames = [u'大学物理', u'计算机技术', u'微积分', u'电力电子']
        courseDatas = []
        for index in range(len(courseNames)):
            obj = {}
            obj['name'] = courseNames[index]
            obj['intro'] = courseNames[index] + u'的简介......'
            courseDatas.append(obj)

        self.s3_candidate_ques = QuestionListCtrl(self.panel, courseDatas, size=(500, 600))
        self.s3_tips = wx.StaticText(self.panel, 0, u"-->", style=wx.TE_LEFT)
        self.s3_sim_ques = QuestionListCtrl(self.panel, courseDatas, size=(500, 600))

        self.s4_tips = wx.StaticText(self.panel, 0, u"当前进度:", style=wx.TE_LEFT)
        self.s4_progress = wx.StaticText(self.panel, 0, u"1/1000", style=wx.TE_LEFT)
        self.s4_next = wx.Button(self.panel, label=u'下一个问题')

        self.makeMenuBar()
        self.makeWorkspace()
        self.CreateStatusBar()
        self.SetStatusText("邂智科技")

    def makeWorkspace(self):
        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(self.s1_tips, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, border=5)
        s1.Add(self.s1_filename, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        s1.Add(self.s1_open, proportion=1, flag=wx.ALL, border=5)

        s2 = wx.BoxSizer(wx.HORIZONTAL)
        s2.Add(self.s2_tips, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, border=5)
        s2.Add(self.s2_question, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        s3 = wx.BoxSizer(wx.HORIZONTAL)
        s3.Add(self.s3_candidate_ques, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER, border=5)
        s3.Add(self.s3_tips, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER, border=5)
        s3.Add(self.s3_sim_ques, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER, border=5)

        s4 = wx.BoxSizer(wx.HORIZONTAL)
        s4.Add(self.s4_tips, proportion=2, flag=wx.ALL, border=5)
        s4.Add(self.s4_progress, proportion=2, flag=wx.ALL, border=5)
        s4.Add(self.s4_next, proportion=2, flag=wx.ALL, border=5)

        # wx.VERTICAL 横向分割
        total = wx.BoxSizer(wx.VERTICAL)
        total.Add(s1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        total.Add(s2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        total.Add(s3, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        total.Add(s4, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.panel.SetSizer(total)

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        openItem = fileMenu.Append(-1, "&打开\tCtrl-H", "打开待标注文件")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT,  "&退出")
        openMenu = wx.Menu()
        aboutItem = openMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&文件")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnOpen(self, event):
        pass


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = TagFrame(None, title='相似问句标注工具', size=(1200, 900))
    frm.Show()
    app.MainLoop()
