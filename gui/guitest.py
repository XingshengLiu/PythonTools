# @File  : guitest.py
# @Author: LiuXingsheng
# @Date  : 2019/1/12
# @Desc  :
import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='一对一时间处理', size=(300, 180))
        self.Centre()
        panel = wx.Panel(parent=self)
        self.statictext = wx.StaticText(parent=panel, pos=(110, 15))
        btn1 = wx.Button(parent=panel, id=10, pos=(100, 45), label='Button1')
        btn2 = wx.Button(parent=panel, id=11, pos=(100, 85), label='Button2')
        self.Bind(event=wx.EVT_BUTTON, handler=self.onClick, source=btn1)
        self.Bind(event=wx.EVT_BUTTON, handler=self.onClick, source=btn2)

    def onClick(self, event):
        event_id = event.GetId()
        print(event_id)
        if event_id == 10:
            self.statictext.SetLabelText('btn 1被点击')
        else:
            self.statictext.SetLabelText('btn 2被点击')


class App(wx.App):

    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
