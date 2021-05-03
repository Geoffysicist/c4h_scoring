import win32com.client

class Timy():
    def __init__(self):
        try:
            xl = win32com.client.Dispatch("Excel.Application")
            xl.Visible = 1
            xl.Workbooks.Add() # for office 97 – 95 a bit different!
            xl.Cells(1,1).Value = "Hello"
            self._timy = win32com.client.Dispatch("ALGEUSB.TimyUSB")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    this_timy = Timy()

