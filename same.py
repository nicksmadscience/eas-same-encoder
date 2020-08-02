import numpy as np
from scipy.io import wavfile
import random
import sys
import subprocess # to play the resulting wave file
import datetime # EAS alerts are heavily dependent on timestamps so this makes it easy to send a thing now

fs = 43750

# t = 1.0 / (520 + (5/6))


# f = 2083.33333
	
samples = np.zeros(0)


def markBit():
	f = 2083.33333
	t = 1.0 / (520 + (5/6))
	
	samples = np.arange(t * fs) / fs

	roffle = np.sin(2 * np.pi * f * samples)
	return roffle * 0.8

def spaceBit():
	f = 1562.5
	t = 1.0 / (520 + (5/6))
	
	samples = np.arange(t * fs) / fs

	return np.sin(2 * np.pi * f * samples)



signal = np.zeros(20000)


def byte(the_byte):
	sys.stdout.write(the_byte)
	sys.stdout.write(" ")
	byte_data = np.zeros(0)
	for i in range(0, 8):
		if ord(the_byte) >> i & 1:
			sys.stdout.write("1")
			byte_data = np.append(byte_data, markBit())
		else:
			sys.stdout.write("0")
			byte_data = np.append(byte_data, spaceBit())

	sys.stdout.write("\n")
	sys.stdout.flush()

	return byte_data


def extramarks(numberOfMarks):
	"""SAGE encoders seem to add a few mark bits at the beginning and end"""
	byte_data = np.zeros(0)

	for i in range(0, numberOfMarks):
		byte_data = np.append(byte_data, markBit())

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




# ZCZC-WXR-RWT-020103-020209-020091-020121-029047-029165-029095-029037+0030-1051700-KEAX/NWS

# code = "ZCZC-EAS-RMT-011000+0100-2141800-SCIENCE-"
# code = "ZCZC-WXR-TOR-000000+0030-2142200-SCIENCE -"
# code = "ZCZC-PEP-EAN-000000+0400-2142350-SCIENCE -"
# code = "SUCK MY FUCKING BALLS YOU FUCKING COCKSUCKERS"

# control string
# code = "ZCZC-EAS-RMT-011000+0100-2142200-KMMS FM -"

# useful FIPS codes
# 000000 - the whole fucking united states
# 024031 - silver spring, md / montgomery county
# 011001 - district of columbia

# EAS alerts are heavily dependent on timestamps so this makes it easy/fun to send a thing now
sameCompatibleTimestamp = datetime.datetime.now().strftime("%j%H%M")

# known good
# OH SHIT it's all time-dependent
# which i can now do since the time works on the box
code = "ZCZC-PEP-EAN-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -"  # nuclear armageddon (or some other form of "we are all likely to die")
code = "ZCZC-PEP-EAT-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -"  # nuclear armageddon (or some other form of "we are all likely to die")
# code = "ZCZC-PEP-EAT-000000+0400-2142350-SCIENCE -"  # lol jk no nuclear armageddon
# code = "ZCZC-WXR-TOR-024031+0030-2150015-SCIENCE -"  # tornado warning, silver spring, md
# code = "ZCZC-WXR-SVR-024031+0030-2142200-SCIENCE -"  # severe thunderstorm warning, silver spring, md
# code = "ZCZC-WXR-EVI-024031+0030-2150010-SCIENCE -"  # evacuation immediate!!, silver spring, md
# code = "ZCZC-WXR-FFW-024031+0030-2150021-SCIENCE -"

# testing
# code = "ZCZC-CIV-LAE-024031+0030-2150022-SCIENCE -"
# code = "ZCZC-CIV-CDW-024031+0400-" + sameCompatibleTimestamp + "-SCIENCE -"




for i in range(0, 3):
	# signal = np.append(signal, extramarks(10))
	signal = np.append(signal, preamble())

	# turn each character into a sequence of sine waves
	for char in code:
		signal = np.append(signal, byte(char))

	# signal = np.append(signal, extramarks(6)) # ENDEC might not be as picky about this as I once thought

	signal = np.append(signal, np.zeros(43750)) # wait the requisite one second


# EOM (3x)
for i in range(0, 3):
	# signal = np.append(signal, extramarks(10))
	signal = np.append(signal, preamble())

	for char in "NNNN": # NNNN = End Of Message
		signal = np.append(signal, byte(char))

	# signal = np.append(signal, extramarks(6))

	signal = np.append(signal, np.zeros(43750)) # wait the requisite one second

	

signal *= -32767

signal = np.int16(signal)

wavfile.write(str("same.wav"), fs, signal)


subprocess.call("afplay same.wav", shell=True)


