import sys
sys.dont_write_bytecode = True

import GUI
import CreateDatabase
import InsertData

CreateDatabase.Construct_Database()
InsertData.byHand()
app = GUI.App()
app.mainloop()