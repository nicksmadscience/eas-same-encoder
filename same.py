#!/usr/bin/env python
"""\
Generates valid EAS SAME messages and tones.

Usage: python3 same.py --code=(code) --filename=(filename) 
"""
__author__ = "Nick Piegari"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "nickpiegari@gmail.com"


import numpy as np
import scipy.io.wavfile
import datetime # EAS alerts are heavily dependent on timestamps so this makes it easy to send a thing now
import argparse



class SAME:
	"""Generates valid EAS SAME messages and tones."""

	def __init__(self):
		######## CONFIG / constants ########

		self.samplerate = 43750 # makes for easy lowest common denominatorization.  not tested at any other rate


	def markBit(self):
		"""Generates a mark bit, four cycles of 2083 1/3 Hz."""
		f = 2083.33333
		t = 1.0 / (520 + (5/6))
		
		samples = np.arange(t * self.samplerate) / self.samplerate

		return np.sin(2 * np.pi * f * samples)


	def spaceBit(self):
		"""Generates a space bit, four cycles of 1562.5Hz."""
		f = 1562.5
		t = 1.0 / (520 + (5/6))
		
		samples = np.arange(t * self.samplerate) / self.samplerate

		return np.sin(2 * np.pi * f * samples)


	def byte(self, the_byte):
		"""Turns the provided byte into FSK data!"""
		byte_data = np.zeros(0)
		for i in range(0, 8):
			if ord(the_byte) >> i & 1:
				byte_data = np.append(byte_data, self.markBit())
			else:
				byte_data = np.append(byte_data, self.spaceBit())

		return byte_data


	def preamble(self):
		"""Builds the sixteen-byte 10101011 preamble!"""
		byte_data = np.zeros(0)

		for i in range(0, 16):
			byte_data = np.append(byte_data, self.markBit())
			byte_data = np.append(byte_data, self.markBit())
			byte_data = np.append(byte_data, self.spaceBit())
			byte_data = np.append(byte_data, self.markBit())
			byte_data = np.append(byte_data, self.spaceBit())
			byte_data = np.append(byte_data, self.markBit())
			byte_data = np.append(byte_data, self.spaceBit())
			byte_data = np.append(byte_data, self.markBit())

		return byte_data


	def attentiontone(self, length=5):
		"""Generates a standard two-tone attention signal."""
		tone = np.sin(2 * np.pi * 853 * np.arange(0, length, 1/self.samplerate)) 
		tone2 = np.sin(2 * np.pi * 960 * np.arange(0, length, 1/self.samplerate)) 

		return (tone + tone2) / 2


	def noaatone(self, length=5):
		"""Generates a weather-radio-style 1050Hz tone..........."""
		return np.sin(2 * np.pi * 1050 * np.arange(0, length, 1/self.samplerate))


	def pause(self, length=1):
		"""Generates a period of silence for the specified duration."""
		return np.zeros(int(self.samplerate * length))


	def buildMessage(self, code, filename="same.wav", tone="eas", db=-3.0):
		"""Generates and writes to file a complete EAS SAME message.."""

		# STEP ONE: Insert a bit of silence
		signal = self.pause(0.5)


		# message (3x)
		for i in range(0, 3):
			signal = np.append(signal, self.preamble())

			# turn each character into a sequence of sine waves
			for char in code:
				signal = np.append(signal, self.byte(char))

			signal = np.append(signal, self.pause(1)) # wait the requisite one second


		# tone.  will be skipped if it's not 'eas' or 'tone'
		if tone == "eas":
			signal = np.append(signal, self.attentiontone())
			signal = np.append(signal, self.pause(1))
		elif tone == "noaa":
			signal = np.append(signal, self.noaatone())
			signal = np.append(signal, self.pause(1))


		# EOM (3x)
		for i in range(0, 3):
			signal = np.append(signal, self.preamble())

			for char in "NNNN": # NNNN = End Of Message
				signal = np.append(signal, self.byte(char))

			signal = np.append(signal, self.pause(1)) # wait the requisite one second


		# wave-ify and adjust trim (decibel to normal conversion)
		signal *= 32767 * (10.0 ** (db / 20.0))

		signal = np.int16(signal)

		scipy.io.wavfile.write(filename, self.samplerate, signal)





if __name__ == "__main__":
	# EAS alerts are heavily dependent on timestamps so this makes it easy/fun to send a thing now
	sameCompatibleTimestamp = datetime.datetime.now().strftime("%j%H%M")

	# parse command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--code", "-c", nargs='?',  
					 default="ZCZC-EAS-RWT-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -",
					 help="The message to be SAME-ified.  Can be anything, but only valid messages will be decoded by an EAS device.")
	parser.add_argument("--filename", "-f", default="same.wav", help="Writes to this file.")
	parser.add_argument("--tone", "-t", default="eas", help="Whether to use EAS tone, NOAA tone, or no tone.")
	parser.add_argument("--db", "-d", default=-3.0, help="Trim adjustment in decibels.  Anything over 0dB will distort and will probably not decode correctly.")
	args = parser.parse_args()

	print (args.code)

	same = SAME()

	same.buildMessage(args.code, filename=args.filename, tone=args.tone, db=float(args.db))

