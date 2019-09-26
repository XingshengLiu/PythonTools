# @File  : secretWordPushTool.py
# @Author: LiuXingsheng
# @Date  : 2019/5/27
# @Desc  :

import wx, requests, time
from gui import tuiTest


class SecretFrame(tuiTest.MyFrame3):
    def __init__(self):
        super().__init__(parent=None)

    def onclick(self, event):
        resultList = []
        self.m_textCtrl_log.SetLabelText(' ')
        url = 'https://api-develop.robot.okii.com/robot/api/secretSend/sendSecret'
        if self.m_textCtrl_clock.GetValue() == '':
            clock = 5
        else:
            clock = self.m_textCtrl_clock.GetValue()
        if self.m_textCtrl_times.GetValue() == '':
            times = 1
        else:
            times = self.m_textCtrl_times.GetValue()
        if self.m_textCtrl_secretContent.GetValue() == '' or self.m_textCtrl_phoneSysver.GetValue() == '':
            header = {'phoneModel': 'iphone X',
                      'phoneSysver': 'IOS 12.1'}
        else:
            header = {'phoneModel': self.m_textCtrl_phoneModel.GetValue(),
                      'phoneSysver': self.m_textCtrl_phoneSysver.GetValue()}
        if self.m_textCtrl_accountId.GetValue() == '' or self.m_textCtrl_machineId.GetValue() == '' or self.m_textCtrl_secretContent.GetValue() == '' or self.m_comboBox_type.GetValue() == '':
            self.m_textCtrl_log.SetLabelText('请求体中参数为空')
        else:
            if self.m_comboBox_type.GetValue() == '1文本':
                sendtype = 1
            elif self.m_comboBox_type.GetValue() == '2表情':
                sendtype = 2
            elif self.m_comboBox_type.GetValue() == '3爱的约定':
                sendtype = 3
            else:
                sendtype = 4
            param = {'accountId': self.m_textCtrl_accountId.GetValue(),
                     'machineId': self.m_textCtrl_machineId.GetValue(),
                     'secretContent': self.m_textCtrl_secretContent.GetValue(),
                     'secretType': str(sendtype)}
            for i in range(int(times)):
                time.sleep(int(clock))
                result = requests.post(url=url, params=param, headers=header)
                resultList.append(result.text)
            with open('result.txt', 'w')as f:
                f.write(str(resultList))


class SecretApp(wx.App):

    def OnInit(self):
        frame = SecretFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    Myapp = SecretApp()
    Myapp.MainLoop()
