#####################################################################################
#                                                                                   #
# Program:......... Connect_to_Cisco.py                                             #
# Author:.......... Jorge Rodriguez                                                 #
# Creare Date:..... March 1st, 2020                                                 #
# Last Modified:... March 8th, 2020                                                 #
# Purpose:......... Use Netmiko API to connect to Cisco Routers                     #
#                                                                                   #
#####################################################################################
#--------------- Libraries <BEGIN>-----------------------------------------
from netmiko import ConnectHandler
import datetime
import time
#--------------- Libraries <END>-------------------------------------------
#--------------- Global Variables <BEGIN> ---------------------------------
LogFile = open("VPNLOG.txt", "a+")
Username = "Username"
Password = "Password"
Do_We_Clear_Counters = False
Do_Enabel_Mode = True
Type_Of_Device = 'cisco_asa' # ['cisco_ios' | 'cisco_asa']
HostIPList = ["10.1.1.1","10.2.2.2","10.3.3.3.","10.4.4.4."]
Config_Commands = ['show vpn-sessiondb summary','show cpu detailed',' sh interface gigabitEthernet 0/0 | i 1 min',
                    'sh interface gigabitEthernet 0/0 | i 5 min']
#--------------- Global Variables <BEGIN> ---------------------------------

def CRLF():
    LogFile.write("\r\n")

def WriteToFile(output):
    #output = output + "\r\n"
    LogFile.write(output)
    CRLF()
    
def bootstrapper(dev_type, dev_ip, dev_un, dev_pw, config):
    try:
        config_file = open(config, 'r') # open the file object described by config argument
        config_lines = config_file.read().splitlines() # create a list of the file lines without \n
        config_file.close() # close the file object

        open_connection = ConnectHandler(device_type=dev_type, ip=dev_ip, username=dev_un, password=dev_pw)
        open_connection.enable() # this sets the connection in enable mode
        output = open_connection.send_config_set(config_lines) # pass the config to the send_config_set() method
        print(output) # print the config to the screen # output to the screen
        open_connection.send_command_expect('write memory') # write the memory (okay if this gets done twice)
        open_connection.disconnect() # close the open connection

        return True # Everything worked! - "Return TRUE when complete"
    except:
        return False # Something failed during the configuration process - "Return FALSE if fails"

def Connect(HostIP):
    global device
    output = "Connecting to...[" + HostIP + "]"
    print (output)
    WriteToFile(output)
    try:
#        device = ConnectHandler(device_type='cisco_ios',ip=HostIP,
#                                username=Username,password=Password)
        device = ConnectHandler(device_type=Type_Of_Device,ip=HostIP,
                                username=Username,password=Password)
        print ("Connected!")
        WriteToFile("Connected!")
        return True
    except:
        print ("**** Error Connecting with Device *****")
        WriteToFile("**** Error Connecting with Device *****")
        return False

def Disconnect():
    global device
    print ("Disconnecting.......")
    WriteToFile("Disconnecting.......")
    device.disconnect()
    print ("Disconnected")
    WriteToFile("Disconnected")

def Enable_Mode():
    global device
    print ("Going to Enabel Mode...")
    WriteToFile("Going to Enabel Mode...")
    try:
        device.enable()
        print ("Enable Mode active")
        WriteToFile("Enable Mode active")
    except:
        print ("Enable Mode NOT active")
        WriteToFile("Enable Mode NOT active")
        
def Clear_Counters():
    print ("-----> " + "Clearing counters..."+ " <-----")
    WriteToFile("-----> " + "Clearing counters..."+ " <-----")
    print ("-"*100)
    LogFile.write("-"*100)
    CRLF()
    output = device.send_command("clear counters", expect_string = "\[confirm\]")
    output = device.send_command("\n", expect_string = "#")
    print (output)
    WriteToFile(output)
    print ("-----> " + "Cleared"+ " <-----")
    WriteToFile("-----> " + "Cleared"+ " <-----")
    print ("-"*100)
    LogFile.write("-"*100)
    CRLF()

def Send_Command(Command):
    print ("-----> " + Command + " <-----")
    WriteToFile("-----> " + Command + " <-----")
    print ("-"*100)
    LogFile.write("-"*100)
    CRLF()
    try:
        output = device.send_command(Command)
        #print ("The Total Characters are: " + str(len(output)))
        print (output)
        WriteToFile(output)
    except:
        output = "******* The Commad was not executes *******"
        print (output)
        WriteToFile(output)
    print ("-"*100)
    LogFile.write("-"*100)
    CRLF()
    
def Main():
    global device
    Total_Hosts = len(HostIPList)
    x = 0
    while (x < Total_Hosts):
        HostIP = HostIPList[x]
        x = x + 1
        if (Connect(HostIP)):
            print ("#"*100)
            LogFile.write("-"*100)
            CRLF()
            if (Do_Enabel_Mode):
                Enable_Mode()
            if (Do_We_Clear_Counters):
                Clear_Counters()
            i = 0
            while (i < len(Config_Commands)):
                Send_Command(Config_Commands[i])
                i = i + 1
            Disconnect()
            print ("#"*100)
            LogFile.write("-"*100)
            CRLF()
            
if __name__ == '__main__':
    x = 0
    total =  1288 # 96 per day * 3
    while (x <= total):
        print ("*"*100)
        LogFile.write("-"*100)
        CRLF()
        print ("                               <  B   E   G   I   N  >")
        WriteToFile("                               <  B   E   G   I   N  >")
        print ("*"*100)
        LogFile.write("-"*100)
        CRLF()
        now = datetime.datetime.now()
        print ("Current date and time : ")
        WriteToFile("Current date and time : ")
        print (now.strftime("%Y-%m-%d %H:%M:%S"))
        WriteToFile(now.strftime("%Y-%m-%d %H:%M:%S"))
        Main()
        print ("*"*100)
        LogFile.write("-"*100)
        CRLF()
        print ("                              <  F   I   N   I   S   H  >")
        WriteToFile("                              <  F   I   N   I   S   H  >")
        print ("*"*100)
        LogFile.write("-"*100)
        CRLF()
        # Wait for 30 minutes
        print ("Waitting 15 minutes.....")
        WriteToFile("Waitting 15 minutes.....")
        LogFile.close()
        j = 60*15 # 15 mintes wait
        x = x + 1
        print ("Cycle No: [" + str(x)+"] of [" +str(total) + "]")
        total_sleep_time = 15 # minutes
        sleep_min = 0
        while (sleep_min < total_sleep_time):
            time.sleep(300) # 60 Seconds => 1 Min
            print (".", end='')
            sleep_min = sleep_min + 5
        print("Next Cycle Now...")
        LogFile = open("VPNLOG.txt", "a+")
    LogFile.close()
    
    
