import modulo1

print("modulo2 __name__ = %s" % __name__)

def main():
	print("invocazione del main()")

if __name__ == "__main__":
	print("modulo2 is being run directly")
	main()
else:
	print("modulo2 is being imported")
