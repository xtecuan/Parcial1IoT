from gpio import *
from time import *

def main():
	pinMode(0, IN)
	while True:
		if digitalRead(0) == HIGH:
			print("Calling Police");
			digitalWrite(1, HIGH)
		else:
			digitalWrite(1, LOW)
		sleep(1)

if __name__ == "__main__":
	main()