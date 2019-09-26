# @File  : guistaticbox.py
# @Author: LiuXingsheng
# @Date  : 2019/1/14
# @Desc  :
import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='staticBox布局', size=(300, 120))
        self.Centre()
        panel = wx.Panel(parent=self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.statictext = wx.StaticText(parent=panel, label='button1 单击')
        vbox.Add(self.statictext, proportion=2, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=10)
        b1 = wx.Button(parent=panel, id=10, label='Button1')
        b2 = wx.Button(parent=panel, id=11, label='Button2')
        self.Bind(wx.EVT_BUTTON, id=10, id2=11, handler=self.onclick)

        sb = wx.StaticBox(panel, label='按钮框')
        hsbox = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        hsbox.Add(b1, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox.Add(b2, 0, wx.EXPAND | wx.BOTTOM, 5)

        vbox.Add(hsbox, proportion=1, flag=wx.CENTER)
        panel.SetSizer(vbox)

    def onclick(self, event):
        evet_id = event.GetId()
        print(evet_id)
        if evet_id == 10:
            self.statictext.SetLabelText('button1 单击')
        else:
            self.statictext.SetLabelText('button2 单击')


class MyApp(wx.App):
    def OnInit(self):
        myfrae = MyFrame()
        myfrae.Show()
        return True


if __name__ == '__main__':
    myapp = MyApp()
    myapp.MainLoop()
