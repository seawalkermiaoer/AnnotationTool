#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configparser

import wx
import os

from copy import deepcopy

from getBaiduZhidao import getQuestion
from question_list_ctrl import QuestionListCtrl


class TagFrame(wx.Frame):
    def __init__(self, *args, **kw):
        # 读取上一次进度
        self.cf = configparser.ConfigParser()
        if os.path.exists('status.ini'):
            self.cf.read('status.ini')
        self.input_path = str(self.cf.get('default', 'last_path')).replace('\\', '/', -1)
        self.size = int(self.cf.get('default', 'size'))
        self.done_index = int(self.cf.get('default', 'done_index'))
        print(self.done_index, self.size, self.input_path)

        self.candidate_ques = []
        self.done_ques = []

        # ensure the parent's __init__ is called
        super(TagFrame, self).__init__(*args, **kw)
        self.Center()
        # create a panel in the frame
        self.panel = wx.Panel(self)

        self.s1_tips = wx.StaticText(self.panel, 0, u"文件路径:", style=wx.TE_LEFT)
        self.s1_filename = wx.TextCtrl(self.panel, style=wx.TE_LEFT)
        self.s1_filename.SetEditable(False)
        self.s1_open = wx.Button(self.panel, label=u'打开')
        # 绑定打开文件对话框事件
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.s1_open)

        self.s2_tips = wx.StaticText(self.panel, 0, u"用户问题:", style=wx.TE_LEFT)
        self.s2_question = wx.TextCtrl(self.panel, style=wx.TE_LEFT)
        self.s2_question.SetEditable(False)

        self.s3_candidate_ques = QuestionListCtrl(self.panel, [], size=(500, 600))
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnCanClick, self.s3_candidate_ques)
        self.s3_tips = wx.StaticText(self.panel, 0, u"--->", style=wx.TE_LEFT)
        self.s3_sim_ques = QuestionListCtrl(self.panel, [], size=(500, 600))
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnSimClick, self.s3_sim_ques)

        self.s4_tips = wx.StaticText(self.panel, 0, u"当前进度:", style=wx.TE_LEFT)
        self.s4_progress = wx.StaticText(self.panel, 0, u"1/1000", style=wx.TE_LEFT)
        self.s4_next = wx.Button(self.panel, label=u'下一个问题')
        self.Bind(wx.EVT_BUTTON, self.OnNext, self.s4_next)

        # self.makeMenuBar()
        self.makeWorkspace()
        self.CreateStatusBar()
        self.SetStatusText("邂智科技")

        # 上一次标注是否完成，如果未完成，则自动初始化
        print(self.size, self.done_index)
        if self.input_path and os.path.exists(self.input_path) and self.size > 0 and self.done_index < self.size:
            # 初始化
            print('自动填充内容...')
            # 填充文件路径
            self.s1_filename.SetLabelText(self.input_path)
            # 填充进度内容
            self.s4_progress.SetLabelText('%d/%d' % (self.done_index, self.size))
            with open(self.input_path, 'r', encoding='utf-8') as fi:
                self.todo_questions = [i.strip('\n') for i in fi.readlines()]
            self.todo_index = self.done_index - 1
            if self.todo_index < 0:
                self.todo_index = 0
            # 填充问题区
            self.s2_question.SetLabelText(self.todo_questions[self.todo_index])
            self.do_search(self.s2_question.GetLabelText())

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
        dlg = wx.FileDialog(self, u"选择待标注文件", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            print(dlg.GetPath())  # 文件路径
            self.s1_filename.SetLabelText(dlg.GetPath())
        dlg.Destroy()
        # 检测

    def OnNext(self, event):
        # TODO 保存当前标注结果
        self.done_index += 1
        self.todo_index += 1
        if self.done_index + 1 > self.size:
            # 清空控件信息
            wx.MessageDialog(self, "恭喜你", caption="Message box",style=wx.OK, pos=wx.DefaultPosition).ShowModal()
            self.clear()
        else:
            self.do_search(self.todo_questions[self.todo_index])
            self.s4_progress.SetLabelText('%d/%d' % (self.done_index, self.size))

    def OnCanClick(self, event):
        """
        候选相似问题被双击
        :param event:
        :return:
        """
        text = event.GetText()
        id = event.GetIndex()
        print(id, text)
        if text:
            self.done_ques[id]['simques'] = text
            self.candidate_ques[id]['simques'] = ""
            self.f5_dlist()

    def OnSimClick(self, event):
        """
        已经标注了的相似问题被双击
        :param event:
        :return:
        """
        text = event.GetText()
        id = event.GetIndex()
        print(id, text)
        if text:
            self.candidate_ques[id]['simques'] = text
            self.done_ques[id]['simques'] = ""
            self.f5_dlist()

    def do_search(self, question):
        self.done_ques = []
        rsp = getQuestion(question=question)
        if rsp['issuccess'] and len(rsp['data']) > 0:
            self.candidate_ques = rsp['data']
            for i in rsp['data']:
                tmp = deepcopy(i)
                tmp['simques'] = ""
                self.done_ques.append(tmp)
            self.f5_dlist()

    def clear(self):
        """
        清空数据 和 标注状态
        :return:
        """
        self.candidate_ques = []
        self.done_ques = []
        self.size = 0
        self.done_index = 0
        self.todo_index = 0
        self.s1_filename.SetLabelText("")
        self.s2_question.SetLabelText("")
        self.f5_dlist()
        self.s4_progress.SetLabelText("0/0")

    def f5_dlist(self):
        self.s3_candidate_ques.refreshDataShow(self.candidate_ques)
        self.s3_sim_ques.refreshDataShow(self.done_ques)


if __name__ == '__main__':
    app = wx.App()
    frm = TagFrame(None, title='相似问句标注工具', size=(1200, 900))
    frm.Show()
    app.MainLoop()
