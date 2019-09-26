# @File  : tuiTest.py
# @Author: LiuXingsheng
# @Date  : 2019/5/28
# @Desc  :

# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class MyFrame3
###########################################################################

class MyFrame3(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"推送工具", pos=wx.DefaultPosition, size=wx.Size(538, 487),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"头参数"), wx.HORIZONTAL)

        self.m_staticText_phoneModel = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"phoneModel",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_phoneModel.Wrap(-1)
        sbSizer3.Add(self.m_staticText_phoneModel, 0, wx.ALL, 5)

        self.m_textCtrl_phoneModel = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        sbSizer3.Add(self.m_textCtrl_phoneModel, 0, wx.ALL, 5)

        self.m_staticText_phoneSysver = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"phoneSysver",
                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_phoneSysver.Wrap(-1)
        sbSizer3.Add(self.m_staticText_phoneSysver, 0, wx.ALL, 5)

        self.m_textCtrl_phoneSysver = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer3.Add(self.m_textCtrl_phoneSysver, 0, wx.ALL, 5)

        bSizer19.Add(sbSizer3, 1, 0, 5)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"请求体"), wx.HORIZONTAL)

        gSizer5 = wx.GridSizer(0, 2, 0, 0)

        self.m_staticText_machineId = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"machineId",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_machineId.Wrap(-1)
        gSizer5.Add(self.m_staticText_machineId, 0, wx.ALL, 5)

        self.m_textCtrl_machineId = wx.TextCtrl(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        gSizer5.Add(self.m_textCtrl_machineId, 0, wx.ALL, 5)

        self.m_staticText_accountId = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"accountId",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_accountId.Wrap(-1)
        gSizer5.Add(self.m_staticText_accountId, 0, wx.ALL, 5)

        self.m_textCtrl_accountId = wx.TextCtrl(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        gSizer5.Add(self.m_textCtrl_accountId, 0, wx.ALL, 5)

        self.m_staticText_secretContent = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"secretContent",
                                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_secretContent.Wrap(-1)
        gSizer5.Add(self.m_staticText_secretContent, 0, wx.ALL, 5)

        self.m_textCtrl_secretContent = wx.TextCtrl(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer5.Add(self.m_textCtrl_secretContent, 0, wx.ALL, 5)

        self.m_staticText_SecretType = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"SecretType",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_SecretType.Wrap(-1)
        gSizer5.Add(self.m_staticText_SecretType, 0, wx.ALL, 5)

        m_comboBox_typeChoices = [u"1文本", u"2表情", u"3爱的约定", u"4语音"]
        self.m_comboBox_type = wx.ComboBox(sbSizer4.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize,
                                           m_comboBox_typeChoices, wx.CB_READONLY)
        self.m_comboBox_type.SetSelection(0)
        gSizer5.Add(self.m_comboBox_type, 0, wx.ALL, 5)

        sbSizer4.Add(gSizer5, 1, wx.EXPAND, 5)

        bSizer19.Add(sbSizer4, 1, wx.EXPAND, 5)

        sbSizer5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"其他设置"), wx.HORIZONTAL)

        self.m_staticText41 = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"循环次数", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText41.Wrap(-1)
        sbSizer5.Add(self.m_staticText41, 0, wx.ALL, 5)

        self.m_textCtrl_times = wx.TextCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_textCtrl_times.SetToolTipString(u"请输入整数")

        sbSizer5.Add(self.m_textCtrl_times, 0, wx.ALL, 5)

        self.m_staticText_clock = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"时间间隔", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.m_staticText_clock.Wrap(-1)
        sbSizer5.Add(self.m_staticText_clock, 0, wx.ALL, 5)

        self.m_textCtrl_clock = wx.TextCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_textCtrl_clock.SetToolTipString(u"请输入整数")

        sbSizer5.Add(self.m_textCtrl_clock, 0, wx.ALL, 5)

        bSizer19.Add(sbSizer5, 1, wx.EXPAND, 5)

        bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_send = wx.Button(self, wx.ID_ANY, u"发送请求", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.btn_send, 0, wx.EXPAND, 5)

        self.m_textCtrl_log = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                          wx.TE_MULTILINE)
        bSizer20.Add(self.m_textCtrl_log, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.SHAPED, 5)

        bSizer19.Add(bSizer20, 1, wx.ALL | wx.EXPAND | wx.SHAPED, 5)

        self.SetSizer(bSizer19)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btn_send.Bind(wx.EVT_BUTTON, self.onclick)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def onclick(self, event):
        event.Skip()


