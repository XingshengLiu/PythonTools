# @File  : guitest2.py
# @Author: LiuXingsheng
# @Date  : 2019/1/12
# @Desc  :

import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='鼠标时间处理', size=(400, 300))
        self.Centre()
        self.Bind(event=wx.EVT_LEFT_DOWN, handler=self.onLeftDown)
        self.Bind(event=wx.EVT_LEFT_UP, handler=self.onLeftUp)
        self.Bind(event=wx.EVT_MOTION, handler=self.onMouseMove)

    def onLeftDown(self,evt):
        print('鼠标按下')

    def onLeftUp(self,evt):
        print('鼠标释放')

    def onMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            pos = event.GetPosition()
            print(pos)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
