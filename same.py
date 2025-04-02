import numpy as np
import scipy.io.wavfile
import datetime # EAS alerts are heavily dependent on timestamps so this makes it easy to send a thing now
import argparse




######## CONFIG / constants ########

samplerate = 43750 # makes for easy lowest common denominatorization





def markBit():
	f = 2083.33333
	t = 1.0 / (520 + (5/6))
	
	samples = np.arange(t * samplerate) / samplerate

	return np.sin(2 * np.pi * f * samples)



def spaceBit():
	f = 1562.5
	t = 1.0 / (520 + (5/6))
	
	samples = np.arange(t * samplerate) / samplerate

	return np.sin(2 * np.pi * f * samples)




def byte(the_byte):
	byte_data = np.zeros(0)
	for i in range(0, 8):
		if ord(the_byte) >> i & 1:
			byte_data = np.append(byte_data, markBit())
		else:
			byte_data = np.append(byte_data, spaceBit())

	return byte_data



def preamble():
	byte_data = np.zeros(0)

	for i in range(0, 16):
		byte_data = np.append(byte_data, markBit())
		byte_data = np.append(byte_data, markBit())
		byte_data = np.append(byte_data, spaceBit())
		byte_data = np.append(byte_data, markBit())
		byte_data = np.append(byte_data, spaceBit())
		byte_data = np.append(byte_data, markBit())
		byte_data = np.append(byte_data, spaceBit())
		byte_data = np.append(byte_data, markBit())

	return byte_data



def attentiontone(length=5):
	tone = np.sin(2 * np.pi * 853 * np.arange(0, length, 1/samplerate)) 
	tone2 = np.sin(2 * np.pi * 960 * np.arange(0, length, 1/samplerate)) 

	return (tone + tone2) / 2


def noaatone(length=5):
	return np.sin(2 * np.pi * 1050 * np.arange(0, length, 1/samplerate))


def pause(length=1):
	return np.zeros(int(samplerate * length))




# EAS alerts are heavily dependent on timestamps so this makes it easy/fun to send a thing now
sameCompatibleTimestamp = datetime.datetime.now().strftime("%j%H%M")

# known good
code = "ZCZC-PEP-EAN-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -"  # nuclear armageddon (or some other form of "we are all likely to die")



def buildMessage(code, filename="same.wav", attention="eas"):

	# STEP ONE: Insert a bit of silence
	signal = pause(0.5)


	# message
	for i in range(0, 3):
		signal = np.append(signal, preamble())

		# turn each character into a sequence of sine waves
		for char in code:
			signal = np.append(signal, byte(char))

		signal = np.append(signal, pause(1)) # wait the requisite one second


	if attention == "eas":
		signal = np.append(signal, attentiontone())
		signal = np.append(signal, pause(1))

	
	if attention == "noaa":
		signal = np.append(signal, noaatone())
		signal = np.append(signal, pause(1))


	# EOM (3x)
	for i in range(0, 3):
		signal = np.append(signal, preamble())

		for char in "NNNN": # NNNN = End Of Message
			signal = np.append(signal, byte(char))

		signal = np.append(signal, pause(1)) # wait the requisite one second

		
	# wave-ify
	signal *= 32767

	signal = np.int16(signal)

	scipy.io.wavfile.write(filename, samplerate, signal)





if __name__ == "__main__":
	# parse command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--code", "-c", nargs='?', default="none")
	args = parser.parse_args()

	buildMessage(code)

