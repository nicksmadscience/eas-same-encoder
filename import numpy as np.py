import numpy as np
from scipy.io import wavfile
import random
import sys

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
code = "ZCZC-WXR-HUW-024031+0030-2142201-SCIENCE -"
# code = "ZCZC-PEP-EAT-000000+0400-2142300-SCIENCE -"
# code = "SUCK MY FUCKING BALLS YOU FUCKING COCKSUCKERS"

# control string
# code = "ZCZC-EAS-RMT-011000+0100-2142200-KMMS FM -"

for i in range(0, 3):
	signal = np.append(signal, extramarks(10))
	signal = np.append(signal, preamble())


	for char in code:
		signal = np.append(signal, byte(char))

	signal = np.append(signal, extramarks(6))

	signal = np.append(signal, np.zeros(43750))


for i in range(0, 3):
	signal = np.append(signal, extramarks(10))
	signal = np.append(signal, preamble())

	for char in "NNNN":
		signal = np.append(signal, byte(char))

	signal = np.append(signal, extramarks(6))

	signal = np.append(signal, np.zeros(43750))

	

signal *= -32767

signal = np.int16(signal)

wavfile.write(str("same.wav"), fs, signal)


