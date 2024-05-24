import sys
sys.dont_write_bytecode = True

import GUI
import CreateDatabase

CreateDatabase.Construct_Database()
app = GUI.App()
app.mainloop()