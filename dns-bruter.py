#!/usr/bin/python

"""DNS Subdomain Bruteforcer.

Usage:
  dns-bruter.py <domain> [options]

Options:
  -h --help                  Show this screen.
  --thread <thread>          Thread count. [default: 100]
  --characters <characters>  Characters to use permutation [default: qwertyuopasdfghjklizxcvbnm0123456789-_]
  --length <length>          Maximum subdomain length [default: 7]
  --min-length <min-length>  Minimum subdomain length [default: 1]
  --dns-servers <servers>    DNS servers for requesting iterativly, comma for multiple [default: 8.8.8.8]
  --output-path <file>       Save outputs to file
  --statistics               Show request statistics

"""

from docopt import docopt
import dns.resolver
from multiprocessing.pool import ThreadPool
from threading import Thread
from Queue import Queue
from itertools import permutations
import datetime
import sys

class Record:
	def __init__(self, fqdn, resolvedIps, recordType, dnsServers):
		self.fqdn = fqdn
		self.resolvedIps = resolvedIps
		self.recordType = recordType
		self.dnsServers = dnsServers
		
class Output:
	
	def __init__(self, outputPath = None):
		self.startTime = datetime.datetime.now()
		
		if outputPath is None:
			self.outputInterface = sys.stdout
		else:
			self.outputInterface = open(outputPath, "a")

	def put(self, message):
		self.outputInterface.write("[*] Found : " + message.fqdn + " (" + str(message.resolvedIps) + ")\n")
		
	def notify(self, message):
		self.outputInterface.write("[*] " + message + "\n")
		
	def raw(self, message):
		self.outputInterface.write(message)

	def trigger_statistics(self, totalQuery):
		timeDiff = ((datetime.datetime.now() - self.startTime).seconds)
		if not timeDiff:
			return
		
		sys.stdout.write("\n".join([
			"---------------Statistics-------------------",
			"Query In Seconds: " + str(totalQuery / timeDiff),
			"Total Query: " + str(totalQuery),
			"Time Spent (Second): " + str(timeDiff),
			"--------------------------------------------\n"
		]))

def askFor(resultInterface, fqdn, dnsServers, recordType="A"):
	r = dns.resolver.Resolver()
	r.nameservers = dnsServers
	try:
		answers = r.query(fqdn, recordType)
	except:
		return
	
	answersArray = []
	for d in answers:
		answersArray.append(str(d))
	
	if len(answers):
		resultInterface.put(Record(fqdn, answersArray, recordType, dnsServers)) 

class Bruter:
	def __init__(self, arguments):		
		self.baseFqdn = arguments["<domain>"]
		self.concurrentThreadLimit = int(arguments["--thread"])
		self.characters = str(arguments["--characters"])
		self.maximumLength = int(arguments["--length"])
		self.minimumLength = int(arguments["--min-length"])
		self.showStatistics = bool(arguments["--statistics"])
		self.dnsServers = arguments["--dns-servers"].split(",")
		
		outputPath = arguments["--output-path"]
		self.outputHandler = Output(outputPath)
		
		self.currentThreads = []
		self.currentThreadsCount = 0
		self.totalQuery = 0

		self.outputHandler.raw("""
~~~~~~ DNS Bruter V0.1 ~~~~~~
   I will brute them all ! 
        Be patient :)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

""")
		
	def analyse(self):
		self.outputHandler.notify("Analyse starting for : " + str(self.baseFqdn))
		self.outputHandler.notify("\t Thread Limit: " + str(self.concurrentThreadLimit))
		self.outputHandler.notify("\t Minimum Length: " + str(self.minimumLength))
		self.outputHandler.notify("\t Maximum Length: " + str(self.maximumLength))
		self.outputHandler.notify("\t DNS Servers: " + str(self.dnsServers))
		self.outputHandler.notify("\t Characters: " + str(self.characters))
		for fqdn in self.generateFqdn():
			self.totalQuery += 1
			if self.currentThreadsCount < self.concurrentThreadLimit:
				self.currentThreadsCount += 1
			else:
				if self.showStatistics:
					self.outputHandler.trigger_statistics(self.totalQuery)

				self.reset()				
			
			t = Thread(
				target=askFor,
				name="t-A-" + fqdn,
				args=[self.outputHandler, fqdn, self.dnsServers]
			);

			t.start()
			self.currentThreads.append(t)

		
	def reset(self):
		for i in self.currentThreads:
			i.join()
			
		self.currentThreadsCount = 0
		self.currentThreads = []
		
	def generateFqdn(self):
		for i in range(self.minimumLength, self.maximumLength):
			for c in permutations(self.characters, i):
				yield "".join(c) + '.' + self.baseFqdn

		

if __name__ == '__main__':
	arguments = docopt(__doc__, version='DNS - Subdomain Bruteforcer 0.1')
	b = Bruter(arguments)
	
	try:
		b.analyse()
	except KeyboardInterrupt:
		print "[!] Stoping application, waiting current threads."
		b.reset()