from naoqi import ALProxy
import requests

#def main():
#    robot_ip = "192.168.0.110"
#    #robot_ip = "127.0.0.1"
#    nao = Nao(robot_ip)
#    nao.StiffnessOn()

class Nao:
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

    def MoveTo(self,kolko,x,y):
        self.motionProxy.moveInit()
        self.motionProxy.post.moveTo(kolko, x, y)

    def Say(self,text):
        self.tts.say(text)

    # Dictionary commands
    def DefineCommands(self):
        self.Commands = {b'JoinedHands' : self.Stop,    # STOP
                         b'SwipeUp' : self.Stand,       # STAND
                         b'ZoomIn' : self.Sit,          # SIT
                         #b'WaveRight' : "",             # WAVE RIGHT
                         #b'WaveLeft' : "",              # WAVE LEFT
                         #b'ZoomOut' : "",               # MOVE FORWARD
                         #b'SwipeLeft' : "",             # MOVE/TURN LEFT
                         #b'SwipeRight' : "",            # MOVE/TURN RIGHT
        }
    def	Stop(self):
        self.self.motionProxy.stopMove()
    def Stand(self):
        self.Set("Stand")
    def Sit(self):
        self.Set("Sit")

	
data_url = "http://naokinect.azurewebsites.net/Data"
robot_ip = "192.168.0.110"
nao = Nao(robot_ip)
nao.StiffnessOn()

try:
    r = requests.get(data_url)
    nao.Commands[r.content]()
except Exception, e:
    print("Error: " + str(e))



#if __name__ == "__main__":
#	main()

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
