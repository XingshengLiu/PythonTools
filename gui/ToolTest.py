# @File  : ToolTest.py
# @Author: LiuXingsheng
# @Date  : 2019/5/27
# @Desc  :
import wx
import wx.xrc


class MyApp(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent,id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(492, 388),
                          style=wx.TAB_TRAVERSAL)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText_heaer = wx.StaticText(self, wx.ID_ANY, u"头参数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_heaer.Wrap(-1)
        bSizer1.Add(self.m_staticText_heaer, 0, wx.ALL, 5)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"phoneModel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer2.Add(self.m_staticText1, 0, 0, 5)

        self.m_textCtrl_phoneModel = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl_phoneModel, 0, wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"phoneSysver", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer2.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_textCtrl_phoneServer = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                  0)
        bSizer2.Add(self.m_textCtrl_phoneServer, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 1, wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"请求体参数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        bSizer1.Add(self.m_staticText7, 0, wx.ALL, 5)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"machineId", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        gSizer1.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.m_textCtrl_machineId = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_textCtrl_machineId, 0, wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"accountId", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        gSizer1.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.m_textCtrl_accountId = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_textCtrl_accountId, 0, wx.ALL, 5)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"secretContent", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        gSizer1.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.m_textCtrl_secretContent = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                    0)
        gSizer1.Add(self.m_textCtrl_secretContent, 0, wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"SecretType", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        gSizer1.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.m_textCtrl_secretType = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_textCtrl_secretType, 0, wx.ALL, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_send = wx.Button(self, wx.ID_ANY, u"发送请求", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_button_send, 0, wx.ALL, 5)

        bSizer1.Add(bSizer4, 1, wx.ALIGN_CENTER, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        self.m_button_send.Bind(wx.EVT_BUTTON, self.onclick)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def onclick(self, event):
        content = self.m_textCtrl_secretType.GetLineText(1)
        print('内容是：',content)


class MyTest(wx.App):
    def OnInit(self):
        frame = MyApp()
        frame.Show()
        return True


if __name__ == '__main__':
    mytest = MyTest()
    mytest.MainLoop()




