"""
This file is part of Mantra.

Mantra is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Mantra is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Etrack.  If not, see <http://www.gnu.org/licenses/>.
"""

import socket
import time

class libmantra:

	"""
	Python bindings for communicating with the Mantra server. This
	requires the Mantra server to be in UDP mode. For more
	information, see <http://www.cogsci.nl/mantra/>
	"""
	
	version = 0.4

	def __init__(self, host = "localhost", port = 40007):
	
		"""
		Constructor
		
		Keyword arguments:
		host -- a string containing a name or IP-address of the host running the Mantra server. (default = "localhost")
		port -- the port at which the Mantra server is listening (default = 40007)		
		"""
	
		self.comm_addr = host, port		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind( ("", 30007) )			
		self.connected = self.comm("HI", 1) == "HI"
		
	def comm(self, cmd, timeout = None):
	
		"""
		Sends a command string to the Mantra server
		
		Arguments:
		cmd -- the string containing a command
		
		Keyword arguments:
		timeout -- a maximum time, after which a timeout is signaled (default = None)
		
		Returns:
		The response string of the Mantra server or None if a timeout occurred
		"""

		self.sock.sendto(cmd, self.comm_addr)
		self.sock.settimeout(timeout)					
		data = ""
		while data[-1:] != "\n":		
			try:
				data, self.comm_addr = self.sock.recvfrom(128)
			except:
				return None
						
		return data[:-1]
		
	def set_fname(self, fname):
	
		"""
		Changes the name of the logfile on the server
		
		Arguments:
		fname -- The name of the logfile on the server
		"""
	
		self.sock.sendto("FILE %s\n" % fname, self.comm_addr)
		
	def add_cal_point(self, webcam_pt, world_pt, o = 0):
	
		"""		
		* note: calibration is experimental and usually not required
		
		Adds a calibration point for an object to the server.		
		
		Arguments:
		webcam_pt -- an (x,y,z) tuple containing the webcam coordinates of a point
		world_pt -- an (x,y,z) tuple containing the real-word coordinates of a point
		
		Keyword arguments:
		o -- the object nr (default = 0)		
		"""
	
		self.sock.sendto("CPT %d %d %d %d %d %d %d\n" % ( (o, ) + webcam_pt + world_pt), self.comm_addr)
		
	def calibrate(self, o = 0):
	
		"""
		* note: calibration is experimental and usually not required		
		
		Performs a calibration for an object based on previously defined calibration points
		
		Keyword arguments:
		o -- the object nr (default = 0)		
		"""
	
		self.sock.sendto("CAL %d\n" % o, self.comm_addr)
		
	def uncalibrate(self, o = 0):
	
		"""
		* note: calibration is experimental and usually not required		
		
		Forget the calibration of an object
		
		Keyword arguments:
		o -- the object nr (default = 0)		
		"""	
	
		self.sock.sendto("UCAL %d\n" % o, self.comm_addr)		
					
	def sample(self, o = 0, timeout = None):
	
		"""
		Returns a sample, containing the coordinates and movement status of an object. This
		function waits for a new sample and therefore blocks the program until a new sample
		is available.
		
		Keyword arguments:
		o -- the object nr (default = 0)
		timeout -- a maximum time, after which a timeout is signaled (default = None)
		
		Returns:
		A (moving, coordinates) tuple, where moving is 0 (not moving) or 1 (moving) and
		coordinates is a (x,y,z) tuple.		
		"""	
	
		res = self.comm("SAMP %d\n" % o, timeout)
		if res == None:
			return None
		res = res.split(" ")
		return int(res[0]), (float(res[1]), float(res[2]), float(res[3]))
		
	def nb_sample(self, o = 0, timeout = None):
	
		"""
		Returns a sample, containing the coordinates and movement status of an object. This
		function returns the latest sample right away and does not block until a new sample
		has arrived.
		
		Keyword arguments:
		o -- the object nr (default = 0)
		timeout -- a maximum time, after which a timeout is signaled (default = None)
		
		Returns:
		A (moving, coordinates) tuple, where moving is 0 (not moving) or 1 (moving) and
		coordinates is a (x,y,z) tuple.		
		"""		
	
		res = self.comm("NBSAMP %d\n" % o, timeout)
		if res == None:
			return None
		res = res.split(" ")
		return int(res[0]), (float(res[1]), float(res[2]), float(res[3]))
		
					
	def smov(self, o = 0, timeout = None):	
	
		"""
		Waits for the start of a movement.
		
		Keyword arguments:
		o -- the object nr (default = 0)
		timeout -- a maximum time, after which a timeout is signaled (default = None)		
		
		Returns:
		A (x,y,z) tuple containing the coordinates of the movement start
		"""
	
		res = self.comm("SMOV %d\n" % o, timeout)
		if res == None:
			return None
		res = res.split(" ")			
		return float(res[0]), float(res[1]), float(res[2])
	
	def emov(self, o = 0, timeout = None):
	
		"""
		Waits for the end of a movement.
		
		Keyword arguments:
		o -- the object nr (default = 0)
		timeout -- a maximum time, after which a timeout is signaled (default = None)		
		
		Returns:
		A (start_coordinates, end_coordinates) tuple, each consisting of an (x,y,z) tuple.
		"""
		
		res = self.comm("EMOV %d\n" % o, timeout)
		if res == None:
			return None
		res = res.split(" ")			
		return (float(res[0]), float(res[1]), float(res[2])), (float(res[3]), float(res[4]), float(res[5]))
		
	def log(self, msg):	
	
		"""
		Logs a message in the Mantra server logfile 
		
		Arguments:
		msg -- a string containing the log message
		"""
	
		self.sock.sendto("LOG %s\n" % msg, self.comm_addr)
		
	def close(self):
	
		"""
		Close the socket
		"""
		
		self.sock.close()
		
		
class libmantra_dummy:

	def __init__(self, host = "localhost", port = 40007):
		pass
		
	def comm(self, cmd, timeout = None):
		pass
		
	def set_fname(self, fname):
		pass
		
	def add_cal_point(self, webcam_pt, world_pt, o = 0):
		pass
		
	def calibrate(self, o = 0):
		pass
		
	def uncalibrate(self, o = 0):
		pass
					
	def sample(self, o = 0, timeout = None):
		pass
		
	def nb_sample(self, o = 0, timeout = None):
		pass	
					
	def smov(self, o = 0, timeout = None):	
		time.sleep(0.5)
		return 0,0,0
	
	def emov(self, o = 0, timeout = None):
		time.sleep(0.5)
		return (0,0,0), (0,0,0)
		
	def log(self, msg):	
		pass
		
	def close(self):
		pass	
