from email import *
from time import *

def onEmailReceive(sender, subject, body):
	print("Received from: " + sender)
	print("Subject: " + subject)
	print("Body: " + body)

def onEmailSend(status):
	print("send status: " + str(status))

def main():
	EmailClient.setup(
		"mcu@cisco.com",
		"cisco.com",
		"mcu",
		"password"
	)
	
	EmailClient.onReceive(onEmailReceive)
	EmailClient.onSend(onEmailSend)
	
	EmailClient.send("pc@cisco.com", "hello", "world")

	# check email once a while
	while True:
		EmailClient.receive()
		sleep(5)

if __name__ == "__main__":
	main()