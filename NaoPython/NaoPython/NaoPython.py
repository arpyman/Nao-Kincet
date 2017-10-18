from naoqi import ALProxy

#def main():
#    robot_ip = "192.168.0.110"
#    #robot_ip = "127.0.0.1"
#    nao = Nao(robot_ip)
#    nao.StiffnessOn()

class Nao:
    def __init__(self, robot_ip):
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

    def	Stop(self):
        self.self.motionProxy.stopMove()

    def Say(self,text):
        self.tts.say(text)
	

robot_ip = "192.168.0.110"
nao = Nao(robot_ip)
nao.StiffnessOn()
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
