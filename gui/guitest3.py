# @File  : guitest3.py
# @Author: LiuXingsheng
# @Date  : 2019/1/14
# @Desc  :
import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Box布局', size=(300, 120))
        self.Centre()
        panel = wx.Panel(parent=self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.statictext = wx.StaticText(parent=panel, label='button1 单击')
        vbox.Add(self.statictext, proportion=2, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=10)
        b1 = wx.Button(parent=panel, id=10, label='Button1')
        b2 = wx.Button(parent=panel, id=11, label='Button2')
        self.Bind(event=wx.EVT_BUTTON, handler=self.onClick, id=10, id2=11)
        # 创建水平方向的Box布局管理器对象
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # 添加B1 到水平Box布局管理
        hbox.Add(b1, 0, flag=wx.EXPAND | wx.BOTTOM, border=5)
        hbox.Add(b2, 0, flag=wx.EXPAND | wx.BOTTOM, border=5)
        vbox.Add(hbox, proportion=1, flag=wx.CENTER)
        panel.SetSizer(vbox)

    def onClick(self, event):
        evetn_id = event.GetId()
        print(evetn_id)
        if evetn_id == 10:
            self.statictext.SetLabelText('Button1 点击')
        else:
            self.statictext.SetLabelText('Button2 点击')


class MyApp(wx.App):

    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    myapp = MyApp()
    myapp.MainLoop()
