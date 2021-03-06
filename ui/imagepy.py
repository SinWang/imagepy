# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:23:30 2017

@author: yxl
"""
import wx, os, sys
import time, threading
from .. import IPy
# TODO: @2017.05.01
#from ui import pluginloader, toolsloader
from . import pluginloader, toolsloader
from ..core.manager import ConfigManager, PluginsManager
from .. import root_dir

class FileDrop(wx.FileDropTarget):
    def OnDropFiles(self, x, y, path):
        print(["Open>{'path':'%s'}"%repr(i) for i in path])
        IPy.run_macros(["Open>{'path':'%s'}"%i for i in path])

class ImagePy(wx.Frame):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'ImagePy', 
                            size = wx.Size(560,-1), pos = wx.DefaultPosition, 
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.Size( 560,-1 ), wx.DefaultSize )
        IPy.curapp = self
        # Todo:Fixed absolute/relative path!
        # print("menuspath:{}".format( os.path.join(IPyGL.root_dir,"menus")))
        # print("toolspath:{}".format(os.path.join(IPyGL.root_dir,"tools"))
        menuspath = os.path.join(root_dir,"menus")
        toolspath = os.path.join(root_dir,"tools")
        self.menubar = pluginloader.buildMenuBarByPath(self,menuspath)
        self.SetMenuBar( self.menubar )
        self.shortcut = pluginloader.buildShortcut(self)
        self.SetAcceleratorTable(self.shortcut)
        self.busy = 'first'
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = toolsloader.build_tools(self, toolspath)

        #self.toolbar.Realize()
        #sizertool.Add(self.toolbar, 1, 0, 5 )
        #sizertool.Add(self.morebar, 0, 0, 5)
        sizer.Add(self.toolbar, 0, wx.EXPAND, 5 )
        #sizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        self.line_color = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        #self.line_color.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        sizer.Add(self.line_color, 0, wx.EXPAND |wx.ALL, 0 )
        stapanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizersta = wx.BoxSizer( wx.HORIZONTAL )
        self.txt_info = wx.StaticText( stapanel, wx.ID_ANY, "ImagePy  v0.2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_info.Wrap( -1 )
        #self.txt_info.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
        sizersta.Add( self.txt_info, 1, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 2 )
        self.pro_bar = wx.Gauge( stapanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 100,15 ), wx.GA_HORIZONTAL )
        sizersta.Add( self.pro_bar, 0, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 2 )
        stapanel.SetSizer(sizersta)
        stapanel.SetDropTarget(FileDrop())
        sizer.Add(stapanel, 0, wx.EXPAND, 5 )
        self.SetSizer( sizer )

        self.Centre( wx.BOTH )
        self.Layout()
        self.Fit()
        self.update = False

        self.Bind(wx.EVT_CLOSE, self.on_close)
        thread = threading.Thread(None, self.hold, ())
        thread.setDaemon(True)
        thread.start()

    def reload_plugins(self):
        for i in range(self.menubar.GetMenuCount()): self.menubar.Remove(0)
        menuspath = os.path.join(root_dir,"menus")
        pluginloader.buildMenuBarByPath(self, menuspath, self.menubar)

    def hold(self):
        i = 0
        while True:
            if time == None: break
            time.sleep(0.05)

            if self.busy==False: continue
            i += 5
            wx.CallAfter(self.set_progress, i)
            if i>=100:i=0
            if i==0 and self.busy=='first':
                self.busy = False
                wx.CallAfter(self.set_progress, 0)

    def set_info(self, value):
        self.txt_info.SetLabel(value)

    def set_progress(self, value):
        self.pro_bar.SetValue(value)
        if value==0 and self.busy!=True:
            self.pro_bar.Hide()
        elif not self.pro_bar.IsShown():
            self.pro_bar.Show()
        self.pro_bar.Update()

    def set_color(self, value):
        self.line_color.SetBackgroundColour(value)

    def on_close(self, event):
        ConfigManager.write()
        self.Destroy()

    def __del__( self ):
        pass

if __name__ == '__main__':
    app = wx.App(False)
    mainFrame = ImagePy(None)
    mainFrame.Show()
    app.MainLoop()
