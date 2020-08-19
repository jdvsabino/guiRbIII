class Data_Collection():
    """
    Object that receives and stores information from Adwin and provides it
    to the rest of the program.
    
    Attributes
    ----------
    receiving_flag : int
        1 if information is being read from Adwin, 0 otherwise.
    copy_flag : int
        1 if information is being copied to another 'Data_Collection' object, 0 otherwise.
    cam_flag : int
        Indicates which camera is used. 
        0 - TAndor
        1 - LAndor
        3 - VAndor   
    path     : str
        Stores the path from adwin (where pictures are stored?)
    file     : str
        ???
    scan     : str
        Number of the current scan.
    imsc     : str
        Don't remember    
    loop     : int
        Don't remember
    glob     : int
        Global count number
    status   : "None"
        Was this implemented?
    
    T_cam    : int
    L_cam    : int
    V_cam    : int
        Do we need these three?
    last_pic : int
        Number of the last stored picture.
    adwin_data_start : 5
        Chooses the starting point to read data from adwin
    
    Methods
    -------
    set_data_adwin(data)
        Reads data from Adwin and stores it in the appropriate methods
    set_data_c*(data)
    status_sending()
    status_waiting()

    """
    def __init__(self):
        ###--- Flags
        self.receiving_flag = 0
        self.copy_flag = 0
        self.cam_flag = -1
        
        self.path     = ""
        self.file     = ""
        self.scan     = -1
        self.imsc     = -1
        self.loop     = -1
        self.glob     = -1
        self.status   = "None"
        self.T_cam    = -1
        self.L_cam    = -1
        self.V_cam    = -1
        self.last_pic = -1
        self.adwin_data_start = 5
    
    def set_data_adwin(self, data):
        ''' 
        Function called when info from adwin computer is recieved;
        Chooses which field the info should be adssigned to;
        field: a string representing the field (example: "PATH",
        "IMSC", etc.).

        Parameters
        ----------
        data : str[]

        Returns
        -------
        Nothing.
        '''
        
        ###--- Make sure that info is not being copied
        while(self.copy_flag == 1):
            continue
        
        self.receiving = 1
        if "STAT_sending" in data:
            self.last_pic = -1
            self.stat_sending()
        
        elif "STAT_waiting" in data:
            self.stat_waiting()
        
        elif "PATH" in data:
            self.path = data[self.adwin_data_start:]
            # return 1
        
        elif "FILE" in data:
            self.file = data[self.adwin_data_start:]
            # return 1
        
        elif "IMSC" in data:
            self.imsc = int(data[self.adwin_data_start:])
            # self.receiving = 0
            # return 1
        
        elif "SCAN" in data:
            self.scan = int(data[self.adwin_data_start:])
            # print(self.scan)
            # return 1
        
        elif "LOOP" in data:
            self.loop = int(data[self.adwin_data_start:])
            # print(self.loop)
            # return 1
        
        elif "GLOB" in data:
            self.glob = int(data[self.adwin_data_start:])
            # print(self.glob)
            # return 1

        elif "LCAM" in data:
            self.set_data_c1(data)
        
        elif "TCAM" in data:
            self.set_data_c2(data)

        elif "VCAM" in data:
            self.set_data_c3(data)                    
        
        else:
            print("Field Not recognized. Check spelling!")
            return -1
        
        self.receiving = 0
        return 0
        
    def set_data_c1(self, data):
        """
        Sets LAndor as the current camera and stores the picture read
        from Adwin as the last one being copied.
        
        Parameters
        ----------
        data: str[]

        Returns
        -------
        int
            0 if the camera was set successfully, -1 otherwise.
        """
        self.receiving = 1
        
        if 'LCAM' in data:
            # self.L_cam = data[self.adwin_data_start:]
            self.last_pic = str(data[self.adwin_data_start:])
            self.cam_flag = 1
            self.receiving = 0
            return 0
        
        print("Signal from Celcius 1 recieved but no LCAM info.")
        self.receiving = 0
        return -1

    def set_data_c2(self, data):
        """
        Sets TAndor as the current camera and stores the picture read
        from Adwin as the last one being copied.
        
        Parameters
        ----------
        data: str[]

        Returns
        -------
        int
            0 if the camera was set successfully, -1 otherwise.
        """
        self.receiving = 1
        
        if 'TCAM' in data:
            #self.T_cam = data[self.adwin_data_start:]
            self.last_pic = str(data[self.adwin_data_start:])
            self.cam_flag = 0
            self.receiving = 0
            return 0
        
        print("Signal from Celcius 2 recieved but no TCAM info.")
        self.receiving = 0
        return -1

    def set_data_c3(self, data):
        """
        Sets VAndor as the current camera and stores the picture read
        from Adwin as the last one being copied.
        
        Parameters
        ----------
        data: str[]

        Returns
        -------
        int
            0 if the camera was set successfully, -1 otherwise.
        """        
        self.receiving = 1
        if 'VCAM' in data:
            #self.V_cam = data[self.adwin_data_start:]
            self.last_pic = str(data[self.adwin_data_start:])
            self.cam_flag = 3
            self.receiving = 0
            return 0
        
        print("Signal from Celcius 3 recieved but no VCAM info.")
        self.receiving = 0
        return -1
    
    
    def stat_sending(self):
        self.stat = "Sending"
        print("Receiving stuff!")
    
    def stat_waiting(self):
        self.stat = "Waiting"        
        print("Waiting for stuff")

data_collector = Data_Collection()


####---- Needed paths
''' 
These paths are the soure of the information.
Where to get the pics, for example.
'''

LOOP_DATA_DIR_SRC = "G:\\data\\AdWin_v2\\loop-data"
SCAN_COUNT_FILE_SRC = "G:\\data\\AdWin_v2\\loop-data\\scan_cnt.txt"
PIC_SRC = "Z:\\data\\pics\\transfer\\" #"G:\\data\\pics"
# AQ_DATA_SRC = ""
