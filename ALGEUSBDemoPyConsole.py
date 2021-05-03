# -*- coding: iso-8859-15 -*-
import sys, time
try:
   import msvcrt
except ImportError:
   print("Sorry, this is a Windows program and you seem to try to run it from a Non-Windows platform. ")
   sys.exit(-1)
import pythoncom, win32com.client
# from pywin32 import win32com


class _EventEmitter(list):
      
   def __iadd__(self, other):
      assert callable(other)
      self.append(other)
      return self
   
   def __call__(self, *args, **kwargs):
      for each in self:
         each(*args, **kwargs)


class _TimyEvents:
   
   def OnConnectionClosed(self):
      Timy_S()._OnConnectionClosed_()
      return
   
   def OnConnectionOpen(self):
      Timy_S()._OnConnectionOpen_()
      return
   
   def OnError(self, code, text):
      Timy_S()._OnError_(code, text)
      return
   
   def OnErrorInternal(self, code, text):
      Timy_S()._OnErrorInternal_(code, text)
      return
   
   def OnMessage(self, text):
      Timy_S()._OnMessage_(text)
      return
   
   def OnPnPConnect(self):
      Timy_S()._OnPnPConnect_()
      return
   
   def OnPnPRemove(self):
      Timy_S()._OnPnPRemove_()
      return
   
   def OnProgress(self, numBytes, maxNumBytes):
      Timy_S()._OnProgress_(numBytes, maxNumBytes)
      return
   
   def OnSendComplete(self):
      Timy_S()._OnSendComplete_()
      return
   
   def OnUpdateCompleted(self):
      Timy_S()._OnUpdateCompleted_()
      return
   
   def OnUSBInputRaw(self):
      data = Timy_S().RawChunk
      data = data.replace(chr(13), "\\r").replace(chr(10), "\\n").replace(chr(0), "\\0")
      Timy_S()._OnDataRaw_(data)
      return

   def OnUSBInput(self, data):
      Timy_S()._OnData_(data)
      return


class Command2Timy:
   
   def __init__(self, command):
      self._command = command
      return
   
   def __str__(self):
      s = self._command.rstrip()
      if len(s) and s[-1] != "\r":
         s += "\r"
      return s
   
   
class Timy_S:
   
   _State = {}
   

   _OnConnectionClosed_ = _EventEmitter()
   _OnConnectionOpen_ = _EventEmitter()
   _OnDataRaw_ = _EventEmitter()
   _OnData_ = _EventEmitter()
   _OnError_ = _EventEmitter()
   _OnErrorInternal_ = _EventEmitter()
   _OnMessage_ = _EventEmitter()
   _OnPnPConnect_ = _EventEmitter()
   _OnPnPRemove_ = _EventEmitter()
   _OnProgress_ = _EventEmitter()
   _OnSendComplete_ = _EventEmitter()
   _OnUpdateCompleted_ = _EventEmitter()
   

   def __init__(self):
      self.__dict__ = Timy_S._State
      if self.__dict__:
         return
      try:
         self._timy = win32com.client.DispatchWithEvents('ALGEUSB.TimyUSB', _TimyEvents)
      except Exception as e:
         print("\nERROR:\t'%s'" % str( e))
         print("\n\tDid you install the driver needed to connect to a Timy hardware?")
         t = time.time()
         while time.time() - t <= 5:
            time.sleep( 0.5)
         sys.exit( -1)
      self._timy.Init()
      return
      
   def __getattr__(self, name):
      try:
         return self.__dict__[name]
      except KeyError:
         return getattr(self._timy, name)
      
   def version(self):
      return self.Version()
   

class _Menu:
   
   _OnMenuConnect_ = _EventEmitter()
   _OnMenuDisconnect_ = _EventEmitter()
   _OnMenuExit_ = _EventEmitter()
   _OnMenuHelp_ = _EventEmitter()
   
   def __init__( self):
      self._menuLines = (("c...Connect to Timy", self._onConnect_),
                         ("d...Disconnect Timy", self._onDisconnect_),
                         ("h...Help", self._onHelp_),
                         ("x...Exit this program", self._onExit_),
                        )
      self._banner = "ALGEUSB Python Console Demo Program (Ver. 1.0.7120)"
      self._input = ""
      self._isFirstTime = 1
      return

   def awaitInput( self):
      print("> ", end=' ')
      while 1: 
         if msvcrt.kbhit():
            self._input = msvcrt.getche()
            print(self._input)
            break
         else:
            time.sleep( 0.050)
            pythoncom.PumpWaitingMessages()
      print()

   def actOnInput( self):      
      for each in self._menuLines:
         if self._input == each[0][0]:
            print(each[1]())
            each[1]()
      return
   
   def _onConnect_( self):
      self._OnMenuConnect_()
      return 
   
   def _onDisconnect_( self):
      self._OnMenuDisconnect_()
      return 
   
   def _onHelp_( self):
      print("\n" + self._banner + "\n")
      self._OnMenuHelp_()
      return 
   
   def _onExit_( self):
      self._OnMenuExit_()
      
   def show( self):
      if self._isFirstTime:
         self._isFirstTime = 0
      else:
         print("\n\n\n\n")
      print(self._banner)
      print()
      lenMax = 0
      for each in self._menuLines:
         lenMax = max( lenMax, len(each[0]))
         print(each[0])
      print("-" * lenMax)



class ALGEUSBDemoPyConsole:
   
   def __init__( self):
      Timy_S._OnConnectionClosed_ += self._onTimyDisconnected_
      Timy_S._OnConnectionOpen_ += self._onTimyConnected_
      Timy_S._OnDataRaw_ += self._onTimyDataRaw_
      Timy_S._OnData_ += self._onTimyData_
      
      self._menu = _Menu()
      self._menu._OnMenuConnect_ += self._onMenuConnect_
      self._menu._OnMenuDisconnect_ += self._onMenuDisconnect_
      self._menu._OnMenuExit_ += self._onMenuExit_
      self._menu._OnMenuHelp_ += self._onMenuHelp_

      return
   
   def _onMenuConnect_( self):
      print("Open connection. You should receive a ConnectionOpen Event now. ")
      r = Timy_S().OpenConnection( 0)
      return
   
   def _onMenuDisconnect_( self):
      print("Close connection. ")
      r = Timy_S().CloseConnection()
      return
   
   def _onMenuExit_( self):
      Timy_S().CloseConnection()
      raise KeyboardInterrupt()
   
   def _onMenuHelp_( self):
      print("""
Start by pressing 'c'. This will connect you to Timy. Timy then will continue to send 
time stamps as so-called raw/data .

To stop Timy, press 'd'.

To exit this program any time, press 'x'. In case you are still connected to Timy, this
program will close the connection for you.
""")
      return
   

   def _onTimyConnected_( self):
      print("Ackn. from Timy: Connected. You should recieve Timy Events now. ")
      return
   
   def _onTimyDisconnected_( self):
      print("Ackn. from Timy: Disconnected. ")
      return
   
   def _onTimyDataRaw_( self, data):
      print("\t" * 5, end=' ')
      print("Raw data from Timy:", data)
      return
   
   def _onTimyData_( self, data):
      print("\t" * 5, end=' ')
      print("Data from Timy    :", data)
      return
   

   def run( self):
      while 1:
         self._menu.show()
         self._menu.awaitInput()
         try: 
            self._menu.actOnInput()
         except KeyboardInterrupt:
            return
      return 
   
   
def main():
   # ALGEUSBDemoPyConsole().run()
   this_timy = Timy_S()
   print(this_timy._State)
   
if __name__ == '__main__':
   main()
   input( "Press any key to exit...")
   