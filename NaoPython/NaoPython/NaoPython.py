from naoqi import ALProxy
import requests
import time

def main():
    #robot_ip = "192.168.0.110"
    robot_ip = "127.0.0.1"
    data_url = "http://naokinect.azurewebsites.net/Data"

    nao = Nao(robot_ip)
    nao.StiffnessOn()

    while 1:
        try:
            r = requests.get(data_url)
            nao.Commands[r.content]()
            print(r.content)
            time.sleep(0.1)
        except Exception, e:
            print("Error: " + str(e))
            time.sleep(1)



class Nao:
    isWalking=False
    def __init__(self, robot_ip):
        self.DefineCommands()
        self.postureProxy = ALProxy("ALRobotPosture", robot_ip, 9559)	#Positions
        self.motionProxy = ALProxy("ALMotion", robot_ip, 9559)	#Move
        self.tts = ALProxy("ALTextToSpeech", robot_ip , 9559)	#Say
	
    def StiffnessOn(self):
        self.motionProxy.setStiffnesses("Body", 1.0)  #zaseknutie klbov (aby sa mohol hybat)
    def StiffnessOff(self):
        self.motionProxy.setStiffnesses("Body", 0.0) #vypnutie motorov		
    def Set(self,command):
        self.postureProxy.post.goToPosture(command, 0.5)	#Stand
													        #StandInit
													        #StandZero
													        #Crouch
													        #Sit
													        #SitRelax
													        #LyingBelly
													        #LyingBack	
    def Move(self,kolko):	#v metroch
        self.motionProxy.moveInit()
        self.motionProxy.post.moveTo(kolko, 0, 0)

    def MoveTo(self,kolko,y,uhol):
        self.motionProxy.moveInit()
        self.motionProxy.post.moveTo(kolko, y, uhol)

    def Say(self,text):
        self.tts.say(text)

    def Wave(self, hand):
        names = list()
        times = list()
        keys = list()
        if (hand == "left" ):
            names.append("LElbowRoll")
            names.append("LElbowYaw")
            names.append("LShoulderRoll")
            names.append("LShoulderPitch")
        else:
            names.append("RElbowRoll")
            names.append("RElbowYaw")
            names.append("RShoulderRoll")
            names.append("RShoulderPitch")

        #ElbowRoll
        times.append([ 0.64000, 1.40000, 1.68000, 2.08000, 2.40000, 2.64000, 3.04000, 3.32000, 3.72000, 4.44000, 5.4000])
        keys.append([ 1.38524, 0.24241, 0.34907, 0.93425, 0.68068, 0.19199, 0.26180, 0.70722, 1.01927, 1.26559, 0.41539])

        #ElbowYaw
        times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 3.72000, 4.44000, 5.4000])
        keys.append([ -0.31298, 0.56447, 0.39113, 0.34818, 0.38192, 0.97738, 0.82678, 0.41539])

        #ShoulderRoll
        times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 4.44000, 5.4000])
        keys.append([ -0.24241, -0.95419, -0.46024, -0.96033, -0.32832, -0.25008, -0.13265])

        #ShoulderPitch
        times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 4.44000, 5.4000])
        keys.append([ 0.24702, -1.17193, -1.08910, -1.26091, -1.14892, 1.02015, 1.48178])

        if (hand == "left" ):
            for i in range(0,3):
                keys[i] = [-x for x in keys[i]]

        self.motionProxy.angleInterpolation(names, keys, times, True);


    # Dictionary commands
    def DefineCommands(self):
        self.Commands = {b'JoinedHands' : self.Stop,    # STOP
                         b'SwipeUp' : self.Stand,       # STAND
                         b'ZoomIn' : self.Sit,          # SIT
                         b'WaveRight' : self.WaveRight, # WAVE RIGHT
                         b'WaveLeft' : self.WaveLeft,   # WAVE LEFT
                         b'ZoomOut' : self.MoveForward,   # MOVE FORWARD
                         #b'SwipeLeft' : "",             # MOVE/TURN LEFT
                         #b'SwipeRight' : "",            # MOVE/TURN RIGHT
        }
    def	Stop(self):
        self.self.motionProxy.stopMove()
        isWalking=False
    def Stand(self):
        self.Stop()
        self.Set("Stand")
    def Sit(self):
        self.Stop()
        self.Set("Sit")
    def WaveRight(self):
        self.Stop()
        self.Wave("right")
    def WaveLeft(self):
        self.Stop()
        self.Wave("left")
    def MoveForward(self):
        self.Move(1.5)



	


if __name__ == "__main__":
	main()

'''
robot_ip = "127.0.0.1"
#Say
tts = ALProxy("ALTextToSpeech", robot_ip , 9559)
#Move
motionProxy = ALProxy("ALMotion", robot_ip, 9559)
#Positions
postureProxy = ALProxy("ALRobotPosture", robot_ip, 9559)





postureProxy.post.goToPosture("Sit", 0.5)
postureProxy.post.goToPosture("StandInit", 0.5)
postureProxy.stopMove()

motionProxy.moveInit()
motionProxy.post.moveTo(0.5, 0, 0)
motionProxy.stopMove()









postureProxy.post.goToPosture("StandInit", 0.5) #parallel


tts.say("Hello, world!")

motionProxy.setStiffnesses("Body", 0.0) #vypnutie motorov
motionProxy.setStiffnesses("Body", 1.0)  #zaseknutie klbov (aby sa mohol hybat)


postureProxy.goToPosture("Stand", 0.5)
postureProxy.goToPosture("StandInit", 0.5)
postureProxy.goToPosture("StandZero", 0.5)
postureProxy.goToPosture("Crouch", 0.5)
postureProxy.goToPosture("Sit", 0.5)
postureProxy.goToPosture("SitRelax", 0.5)
postureProxy.goToPosture("LyingBelly", 0.5)
postureProxy.goToPosture("LyingBack", 0.5)


postureProxy.goToPosture("StandInit", 0.5)



motionProxy.moveInit()   #priprava pozicie na pohyb
id = motionProxy.post.moveTo(0.5, 0, 0)
tts.say("I'm walking")

'''
