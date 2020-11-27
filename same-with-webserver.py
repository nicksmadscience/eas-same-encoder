# EAS SAME audio file generator!
# Written in a single sitting on a lazy Saturday.
# I thought this would take WAY more time than it did
# most of the development time was getting it to work with my SAGE EAS ENDEC
# (which is understandably very prone to sanity-checking)

# TODO: per development best practices, this should be class-ified



import numpy as np
from scipy.io import wavfile
# import random # used for testing gibberish data during early development
import sys # for stdout
import subprocess # to play the resulting wave file
import datetime # EAS alerts are heavily dependent on timestamps so this makes it easy to send a thing now


class easSAMEHeader:
	def __init__(self, same_header_string):
		self.same_header_string = same_header_string

		self.fs = 43750

		# get a blank 'samples' ready; this is where we'll build up the alert
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

			# TODO: i could probably replace this with the bits() function

		return byte_data

	def generateSAMEAudio(code):

		# SAME HEADER (3x)
		for i in range(0, 3):
			signal = np.append(signal, preamble())

			# turn each character into a sequence of sine waves
			for char in code:
				signal = np.append(signal, byte(char))

			signal = np.append(signal, np.zeros(43750)) # wait the requisite one second

		# TODO: attention tone?

		# TODO: audio message?


		# EOM (3x)
		for i in range(0, 3):
			signal = np.append(signal, preamble())

			for char in "NNNN": # NNNN = End Of Message
				signal = np.append(signal, byte(char))

			signal = np.append(signal, np.zeros(43750)) # wait the requisite one second


		# signal *= -32767

		signal = np.int16(signal)

		wavfile.write(str("same.wav"), fs, signal)


	# TODO: oh shit, I guess I need to think about multi-platform compatibility
	def playLatestSAMEFIleOnMacOS():
		subprocess.call("afplay same.wav", shell=True)











# EAS alerts are heavily dependent on timestamps so this makes it easy/fun to send a thing now
sameCompatibleTimestamp = datetime.datetime.now().strftime("%j%H%M")

# known good
code = "ZCZC-PEP-EAN-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -"  # nuclear armageddon (or some other form of "we are all likely to die")
code = "ZCZC-PEP-EAT-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -"  # nuclear armageddon (or some other form of "we are all likely to die")
# code = "ZCZC-PEP-EAT-000000+0400-2142350-SCIENCE -"  # lol jk no nuclear armageddon
# code = "ZCZC-WXR-TOR-024031+0030-2150015-SCIENCE -"  # tornado warning, silver spring, md
# code = "ZCZC-WXR-SVR-024031+0030-2142200-SCIENCE -"  # severe thunderstorm warning, silver spring, md
# code = "ZCZC-WXR-EVI-024031+0030-2150010-SCIENCE -"  # evacuation immediate!!, silver spring, md
# code = "ZCZC-WXR-FFW-024031+0030-2150021-SCIENCE -"
# code = "SUCK MY F**KING B***S YOU F**KING C*********RS" # does not seem to work :'(







def requestHandler_samecode(_get):
    """Generate and play back an EAS SAME header code based on _get"""
    global clients

    print urllib2.unquote(_get[2])

    # TODO: implement same code

    # for client in clients:
    #     client.write_message(json.dumps({"messagetype": "marquee", "message": urllib2.unquote(_get[2])}))

    return "text/plain", str(_get[2])



httpRequests = {'': requestHandler_index,
                'samecode': requestHandler_samecode,
                }



#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        elements = self.path.split('/')

        responseFound = False
        for httpRequest, httpHandler in httpRequests.iteritems():
            # print elements[1] + " == " + httpRequest
            if elements[1] == httpRequest: # in other words, if the first part matches
                contentType, response = httpHandler(elements)
                responseFound = True

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header('Content-type', contentType)
                self.end_headers()

                self.wfile.write(response)
        if not responseFound:
            contentType, response = requestHandler_index('/')

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('Content-type', contentType)
            self.end_headers()

            self.wfile.write(response)
            
        return


def http():
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    server.serve_forever()

httpThread = Thread(target=http)
httpThread.daemon = True
httpThread.start()

