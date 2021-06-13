from gpio import *
from time import *

def main():
	pinMode(1, OUT)
	print("Blinking")
	while True:
		digitalWrite(1, HIGH);
		sleep(1)
		digitalWrite(1, LOW);
		sleep(0.5)

if __name__ == "__main__":
	main()