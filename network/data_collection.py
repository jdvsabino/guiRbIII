class Data_Collection():

    def __init__(self):

        self.path = ""
        self.scan = ""
        self.imsc = ""
        self.loop = -1
        self.glob = -1
        self.T_cam = -1
        self.L_cam = -1
        self.V_cam = -1

        ###---- Chosses the starting point to read data from adwin
        self.adwin_data_start = 5
        
    def set_data_adwin(self, data):
        ''' 
        Function called when info from adwin computer is recieved.
        Chooses which field the info should be adssigned to.
        field: a string representing the field (example: "PATH", "IMSC", etc.)
        '''
        if "STAT_sending" in data:
            self.stat_sending()
        elif "PATH" in data:
            self.path = data[self.adwin_data_start:]
            return 1
        
        elif "IMSC" in data:
            self.imsc = int(data[self.adwin_data_start:])
            return 1
        
        elif "SCAN" in data:
            self.scan = int(data[self.adwin_data_start:])
            return 1
        
        elif "LOOP" in data:
            self.loop = int(data[self.adwin_data_start:])
            return 1
        
        elif "GLOB" in data:
            self.glob = int(data[self.adwin_data_start:])
            return 1
        
        else:
            print("Field Not recognized. Check spelling!")
            return 0
        

    def st_data_c1(self, data):
        if 'LCAM' in data:
            self.L_cam = data[self.adwin_data_start:]
            return 1

        print("Signal from Celcius 1 recieved but no LCAM info.")
        return 0

    def st_data_c2(self, data):
        if 'TCAM' in data:
            self.T_cam = data[self.adwin_data_start:]
            return 1

        print("Signal from Celcius 2 recieved but no TCAM info.")
        return 0

    def st_data_c3(self, data):
        if 'VCAM' in data:
            self.V_cam = data[self.adwin_data_start:]
            return 1

        print("Signal from Celcius 3 recieved but no VCAM info.")
        return 0

    
    def stat_sending():
        print("Receiving stuff!")

data_collector = Data_Collection()


####---- Needed paths - TALK TO THOMAS!!!
''' 
These paths are the soure of the information.
Where to get the pics, for example.
'''

LOOP_DATA_DIR_SRC = ""
SCAN_COUNT_FILE_SRC = ""
PIC_SRC = ""
AQ_DATA_SRC = ""
