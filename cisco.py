import time
import json
import getpass

class Switch_Field:
    """Use to organize the switch class data fields"""
    """ the first word in command line"""
    DeviceName = "Switch"
    """user mode: global conf mode etc..."""
    Sign = [">", "#", "(config)#"]
    command = ""
    text = ""
    level = 0
    banner = ""
    secret_password = ""
    secret_password_flag = 0
    fields_list = ["banner-","DeviceName-","SecretPassword-","secret_password_flag-","level-"]
    switch_initial_text_file = r"SwitchInitialText.txt"
    switch_commands_file = r"SwichCommands.txt" 
    config_file_name = r"ConfigFile.txt"


    def copy_runningConfig_startupConfig(self):
        """
        Saves all fields from RAM to disk
        """
        f = open(self.config_file_name, "w")
        f.write("Switch config file  " + time.asctime() + "\n")
        f.write("banner-" + self.banner + "\n")
        f.write("DeviceName-" + self.DeviceName + "\n")
        f.write("SecretPassword-" + self.secret_password + "\n")
        f.write("secret_password_flag-" + str(self.secret_password_flag) + "\n")
        f.write("level-" + str(self.level) + "\n")
        f.write("\n")

        
        

        return
    
    def copy_startupConfig_runningConfig(self):
        """
        Load all fields from file to RAM
        """
        f = open(self.config_file_name, "r")
        text = f.read()
        
        field = self.fields_list[0]
        if (field in text):
            startIndex = text.find(field)
            self.banner= text[startIndex + len(field):text.find("\n",startIndex) ] 
        
        field = self.fields_list[1]
        if (field in text):
            startIndex = text.find(field)
            self.DeviceName= text[startIndex + len(field):text.find("\n",startIndex) ]
        
        field = self.fields_list[2]
        if (field in text):
            startIndex = text.find(field)
            self.secret_password= text[startIndex + len(field):text.find("\n",startIndex) ]
        
        field = self.fields_list[3]
        if (field in text):
            startIndex = text.find(field)
            self.secret_password_flag= int(text[startIndex + len(field):text.find("\n",startIndex) ])
        
        field = self.fields_list[4]
        if (field in text):
            startIndex = text.find(field)
            self.level= int(text[startIndex + len(field):text.find("\n",startIndex) ])
        
        return (1)


class Switch:
    """Simulator of CISCO Switch OS"""

    def print_switch_initial_text(self,d):
        """print initial switch text"""
        f = open(d.switch_initial_text_file, "r")
        text = f.read()
        print(text)
        

    def readSwitchCommandsFromFile(self,d):
        """open file with switch commands"""
        f = open(d.switch_commands_file, "r")
        text = f.read()
        listExecCommands = text.split(sep="\n")
        return listExecCommands

    def createCommandsLists(self,d):
        ListExecCommands = self.readSwitchCommandsFromFile(d)
        indexOfExec = ListExecCommands.index("Exec commands:")
        indexOfEnable = ListExecCommands.index("Enable commands:")
        indexOfConfig = ListExecCommands.index("Configure commands:")

        ExecCommands = ListExecCommands[indexOfExec + 1:indexOfEnable]
        EnableCommands = ListExecCommands[indexOfEnable + 1:indexOfConfig]
        ConfigureCommands = ListExecCommands[indexOfConfig + 1:]
        return ExecCommands, EnableCommands, ConfigureCommands

    def printCommandInList(self,CommandsList,level,command):
        i = 0
        counter = 0
        while i < len(CommandsList[level]):
            # the commands shifted to index- 2
            if (CommandsList[level][i].find(command[:-1]) == 2):
                print(CommandsList[level][i])
                counter += 1
            i += 1
        return counter

    def findCommandInList(self, CommandsList, level, command):
        i = 0
        counter = 0
        commandList = []
        while i < len(CommandsList[level]):
            # the commands shifted to index- 2
            if CommandsList[level][i].find(command) == 2:
                commandList.append(CommandsList[level][i])
                counter += 1
            i += 1
        return counter, commandList

    def _complete_commad_tab(self, CommandsList, level, command):
        """Looks for an entered command in command list

           :return the command from list, or empty string if not found
        """
        text = ""
        if self.findCommandInList(CommandsList, level, command[:-1])[0] == 1:
            text = str(self.findCommandInList(CommandsList, level, command[:-1])[1])
            text = text[4:text.index(" ", 4)]
        return text

    def print_ping(self, ip_address="127.0.0.1"):
        """simulates the ping command in cisco router
        """
        ip_list = ["127.0.0.1", "192.168.1.1", "10.0.0.200"]

        if ip_address in ip_list:
            """Type escape sequence to abort.
               Sending 5, 100-byte ICMP Echos to 197.197.197.2, timeout is 2 seconds:
               !!!!!
               Success rate is 100 percent (5/5), round-trip min/avg/max = 0/8/12 ms"""
            print("Type escape sequence to abort.\n" +
                  "Sending 5, 100-byte ICMP Echos to " + ip_address + ", timeout is 2 seconds:")
            time.sleep(1)
            print(".",end="")
            for i in range(4):
                time.sleep(1)
                print("!" , end="")
            print()
            print("Success rate is 80 percent (4/5), round-trip min/avg/max = 0/0/1 ms) \n")
        else:
            print("Type escape sequence to abort.\n" +
                  "Sending 5, 100-byte ICMP Echos to " + ip_address + ", timeout is 2 seconds:")
            for i in range(5):
                time.sleep(1)
                print(".", end="")
            print()
            print("Success rate is 0 percent(0 / 5)")
        return

    def prints_commands_of_current_level(self, Sign, level, CommandsList ):
        # prints the commands of current level
        if (Sign[level] == ">"):
            print("\n".join(CommandsList[level]))
        if (Sign[level] == "#"):
            print("\n".join(CommandsList[level]))
        if (Sign[level] == "(config)#"):
            print("\n".join(CommandsList[level]))


    def ping_command(self, command):
        for i in range(24):
            print("!", end="")
            time.sleep(0.25 - i / 100)
        print()
        self.print_ping(command[5:])

    def copy_RunnigConfig_StartupConfig_command(self, d):
        """
        copy the configurations made in console to HardDisk
        copy running-config startup-config
        :return:
        """
        input("Destination filename [startup-config]?")
        d.copy_runningConfig_startupConfig()
        print("Building configuration...")
    
    def copy_StartupConfig_RunnigConfig_command(self,d):
        """
        copy the configurations from file to RAM
        and changes switch's parameters
        """
        if (d.copy_startupConfig_runningConfig()  !=1):
            print("%% Non-volatile configuration memory invalid or not present")

        
    def set_enable_secret_password(self,d):
        """
        this function sets secret password on device
        will appear after writing "Switch>enable"
        :param d:
        :return:
        """
        d.secret_password = d.command[len("enable secret "):]
        d.secret_password_flag = 1


    def validate_secret(self,d):
        """
        blocks the user to continue until the correct password entered
        after 3 failed tries print...

        Password:
        Password:
        Password:
        % Bad passwords

        :param d:ena    
        :return:
        """
        password = getpass.getpass("Password:")
        tries = 1
        while (password != d.secret_password) and (tries < 3):
            password = getpass.getpass("Password:")
            tries = tries + 1

        if(password == d.secret_password):
            d.level += 1
        else:
            print("% Bad passwords")




    def set_banner(self,d):
        """
        set the text that will appear when starting the device
        :param d:
        :return:
        """
        d.banner = d.command[13:-1]


    def mainLoop(self):
        """the loop of the command line"""
        d = Switch_Field()
        self.print_switch_initial_text(d)
        CommandsList = self.createCommandsLists(d)

        while True:
            print(d.DeviceName + d.Sign[d.level] + str(d.text), end="")
            d.command = d.text + input()
            d.text = ""

            # changes between user modes
            if (d.Sign[d.level] == ">") and (d.command == "enable"):
                if (d.secret_password_flag == 1):
                    self.validate_secret(d)
                else:
                    d.level += 1
            elif (d.Sign[d.level] == "#") and (d.command in ["configure terminal", "configure",  "conf term","conf ter","con ter"]):
                d.level += 1
            elif (d.command == "exit") and (d.level != 0):
                d.level -= 1

            # "?" sign, prints the commands of current level
            elif d.command == "?":
                self.prints_commands_of_current_level(d.Sign, d.level, CommandsList)

            # looking for command beginning, like "s?"
            elif (len(d.command) > 1) and (d.command.find("?") >= 0):
                self.printCommandInList(CommandsList, d.level, d.command)

            # tab command
            elif "\t" in d.command:
                d.text = self._complete_commad_tab(CommandsList, d.level, d.command)

            # ping command
            elif "ping " in d.command:
                self.ping_command(d.command)

            # "copy running-config startup-config" command
            elif (d.command == "copy running-config startup-config") and (d.level == 1):
                self.copy_RunnigConfig_StartupConfig_command(d)

            # "copy startup-config running-config" command
            elif (d.command == "copy startup-config running-config") and (d.level == 1):
                self.copy_StartupConfig_RunnigConfig_command(d)

            # hostname command - changing the device name
            elif ("hostname " in d.command) and (d.level == 2):
                d.DeviceName = d.command[len("hostname ") : ]

            elif ("enable secret" in d.command) and (d.level == 2):
                self.set_enable_secret_password(d)

            elif ("banner motd " in d.command) and (d.level == 2):
                self.set_banner(d)

            elif ("exit" in d.command) and (d.level == 0):
                print(d.banner)


            elif ("" == d.command):
                continue
            elif (True):
                print ("% Invalid input detected") #at '^' marker."
                
                








#==================================================================================
#==================================================================================


s = Switch()
s.mainLoop()












