import numpy as np
import scipy.io.wavfile
import datetime # EAS alerts are heavily dependent on timestamps so this makes it easy to send a thing now
import argparse



class SAME:
	"""Generates valid EAS SAME messages and tones."""

	def __init__(self):
		######## CONFIG / constants ########

		self.samplerate = 43750 # makes for easy lowest common denominatorization





	def markBit(self):
		f = 2083.33333
		t = 1.0 / (520 + (5/6))
		
		samples = np.arange(t * self.samplerate) / self.samplerate

		return np.sin(2 * np.pi * f * samples)



	def spaceBit(self):
		f = 1562.5
		t = 1.0 / (520 + (5/6))
		
		samples = np.arange(t * self.samplerate) / self.samplerate

		return np.sin(2 * np.pi * f * samples)




	def byte(self, the_byte):
		byte_data = np.zeros(0)
		for i in range(0, 8):
			if ord(the_byte) >> i & 1:
				byte_data = np.append(byte_data, self.markBit())
			else:
				byte_data = np.append(byte_data, self.spaceBit())

		return byte_data



	def preamble(self):
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
		tone = np.sin(2 * np.pi * 853 * np.arange(0, length, 1/self.samplerate)) 
		tone2 = np.sin(2 * np.pi * 960 * np.arange(0, length, 1/self.samplerate)) 

		return (tone + tone2) / 2


	def noaatone(self, length=5):
		return np.sin(2 * np.pi * 1050 * np.arange(0, length, 1/self.samplerate))


	def pause(self, length=1):
		return np.zeros(int(self.samplerate * length))




	



	def buildMessage(self, code, filename="same.wav", tone="eas", db=-3.0):

		# STEP ONE: Insert a bit of silence
		signal = self.pause(0.5)


		# message
		for i in range(0, 3):
			signal = np.append(signal, self.preamble())

			# turn each character into a sequence of sine waves
			for char in code:
				signal = np.append(signal, self.byte(char))

			signal = np.append(signal, self.pause(1)) # wait the requisite one second


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

		# wave-ify
		signal *= 32767 * (10.0 ** (db / 20.0))

		signal = np.int16(signal)

		scipy.io.wavfile.write(filename, self.samplerate, signal)





if __name__ == "__main__":
	# EAS alerts are heavily dependent on timestamps so this makes it easy/fun to send a thing now
	sameCompatibleTimestamp = datetime.datetime.now().strftime("%j%H%M")

	# parse command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--code", "-c", nargs='?',
					 default="ZCZC-PEP-EAN-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -")
	parser.add_argument("--filename", "-f", default="same.wav")
	parser.add_argument("--tone", "-t", default="eas")
	parser.add_argument("--db", "-d", default=-3.0)
	args = parser.parse_args()

	print (args.code)

	same = SAME()

	same.buildMessage(args.code, filename=args.filename, tone=args.tone, db=float(args.db))

