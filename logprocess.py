
# player log class to hold the record of attributes

class LogInfo():
    def __init__(self, fileName):
        self.fileName = fileName
        self.corruptFile = False
        if fileName:
            self.fileName = fileName
        self.input_list = self.readFile()
        self.attributeNameList = ["Name", "Level", "BestScore", "Coins", "HealthUp", "HitSpeedUp", "HitDamageUp", "Health", "PunchWait", "KickWait", "PunchDamage", "KickDamage"]
        self.profileLog = {}
        if self.input_list:
            for idx, ii in enumerate(self.attributeNameList):
                if idx == 0:
                    try:
                        self.profileLog[self.attributeNameList[idx]] = str(self.input_list[idx])
                    except:
                        print("Can't get name from file")
                        self.corruptFile = True
                        break
                elif idx > 0 and idx <= 6:
                    try:
                        self.profileLog[self.attributeNameList[idx]] = int(self.input_list[idx])
                    except:
                        print("Not a Number: ",self.input_list[idx])
                        self.corruptFile = True
                        break
                    if not self.corruptFile and int(self.input_list[idx]) < 0:
                        print("Unexpected Negative Number")
                        self.corruptFile = True
                else:
                    try:
                        self.profileLog[self.attributeNameList[idx]] = round(float(self.input_list[idx]),2)
                    except:
                        print("Not a Number: ", self.input_list[idx])
                        self.corruptFile = True
                        break
                    if not self.corruptFile and float(self.input_list[idx]) < 0:
                        print("Unexpected Negative Number")
                        self.corruptFile = True
        else:
            self.corruptFile = True


    def readFile(self):
        f=open(self.fileName)
        lineList = [line.rstrip('\n') for line in f]
        val = []
        for entry in lineList:
            if entry.find(',') != -1:
                try:
                    tmp = str(entry).split(",")
                except:
                    print("Comma not found")
                    self.corruptFile = True
                    break
                if not self.corruptFile:
                    val.append(str(tmp[1]))
                else:
                    self.corruptFile = True
                    break
        f.close()
        return val


    def writeFile(self):
        openSuccess = True
        try:
            f = open(self.fileName, 'w')
        except:
            openSuccess = False
            print("No Such File")

        if openSuccess:
            f.seek(0)
            f.truncate()
            for ele in self.profileLog:
                #print(ele, self.profileLog[ele])
                line = ele + "," + str(self.profileLog[ele])
                f.write(line + '\n')
            f.close()

