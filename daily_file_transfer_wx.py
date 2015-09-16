#!/usr/bin/end python

"""daily_file_transfer_wx.py a simple wxPython program that copies files from
a source folder to a destination folder.  This module uses the functionality in
daily_file_transfer_2.py """

# gail hedberg - python drills 6 and 7
#   july 21, 2015 - submitted for drill 7

from __future__ import unicode_literals
import wx
import daily_file_transfer_3
import abc_utility_db
from datetime import datetime


# default folders
default_src_folder = 'c:\\users\\gail\\Desktop\\FolderA'
default_dst_folder = 'c:\\users\\gail\\Desktop\\FolderB'
        

class BasicFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'ABC Company',
                          size=(575, 275))
        panel = wx.Panel(self)

        #create the controls
        topLbl = wx.StaticText(panel, -1, "File Transfer Utility", (30, 10), (400, -1))
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.dateLbl = wx.StaticText(panel, -1, self.GetTransferDate(), (30, 55), (400, -1))
        self.dateLbl.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))

               
        # create the source folder controls
        src_lbl = wx.StaticText(panel, -1, 'Source Folder', (30, 90))
        self.src_text = wx.TextCtrl(panel, -1, default_src_folder, pos=(150, 90),
                              size=(250, 25), style = wx.TE_READONLY)
        self.src_text.SetBackgroundColour('pink')
        self.src_btn = wx.Button(panel, -1, 'Change Folder', pos=(425, 90))
        self.Bind(wx.EVT_BUTTON, self.ChangeSourceFolder, self.src_btn)

        
        # create the destination folder controls
        dst_lbl = wx.StaticText(panel, -1, 'Destination Folder', (30, 125))
        self.dst_text = wx.TextCtrl(panel, -1, default_dst_folder, pos=(150, 125),
                              size=(250, 25), style = wx.TE_READONLY)
        self.dst_text.SetBackgroundColour('pink')
        self.dst_btn = wx.Button(panel, -1, 'Change Folder', pos=(425, 125))
        self.Bind(wx.EVT_BUTTON, self.ChangeDestinationFolder, self.dst_btn)


        #create the results label
        self.results = wx.StaticText(panel, -1, '', (150, 175))
        self.results.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        

        #create the action buttons
        self.file_transfer_btn = wx.Button(panel, label="Run File Transfer", pos=(30, 170))
        self.Bind(wx.EVT_BUTTON, self.RunFileCheck, self.file_transfer_btn)
        button = wx.Button(panel, label=" Close ", pos=(425, 170))
        self.Bind(wx.EVT_BUTTON, self.OnClose, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def GetTransferDate(self):
        temp = datetime.strptime(str(abc_utility_db.GetFileTransferDate()), "%Y-%m-%d %H:%M:%S.%f")
        fmt = "%a, %b %d, %Y at %I:%M:%S %p"
        txt = datetime.strftime(temp, fmt)
        txt = "Last Transfer on:  " + txt
        print ('get date label - {} '.format(txt))
        return txt

    def RunFileCheck(self, event):
        daily_file_transfer_3.SetSrcPath(self.GetFolderValue('src'))
        daily_file_transfer_3.SetDstPath(self.GetFolderValue('dst'))
        daily_file_transfer_3.MainLoop()
        self.results.SetLabel("{}".format(daily_file_transfer_3.GetNumberFilesArchived())+
                              " files transferred")
        self.dateLbl.SetLabel("{}".format(self.GetTransferDate()))

    def GetFolderValue(self, src_dst):
        if src_dst == 'src':
            return self.src_text.GetValue()
        else:
            return self.dst_text.GetValue()

    def SetFolderValue(self, src_dst, text):
        if src_dst == 'src':
            self.src_text.SetValue(text)
        else:
            self.dst_text.SetValue(text)

        
    def ChangeSourceFolder(self, event):
        dlg = wx.DirDialog(None, message="Choose a directory",
                           defaultPath = str(default_src_folder),
                           style=0, pos = wx.DefaultPosition,
                           size = wx.DefaultSize,
                           name="wxDirCtrl")
        if dlg.ShowModal() == wx.ID_OK:
            self.SetFolderValue('src', dlg.GetPath())
        else: return wx.ID_CANCEL
     

    def ChangeDestinationFolder(self, event):
        dlg = wx.DirDialog(None, message="Choose a directory",
                              defaultPath = str(default_dst_folder),
                              style=0, pos = wx.DefaultPosition,
                              size = wx.DefaultSize,
                              name="wxDirCtrl")
        
        if dlg.ShowModal() == wx.ID_OK:
            self.SetFolderValue('dst', dlg.GetPath())
        else: return wx.ID_CANCEL
        
    
               
    def OnClose(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()
        


if __name__ == '__main__':
    app = wx.App()
    frame = BasicFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()

