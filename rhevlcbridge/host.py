'''
Created on Dec 27, 2013

@author: wallace
'''

class Host():
	'''
	This class will represent hosts in an environment
	'''
	
	uuid = ""
	name = ""
	host_dc_uuid = ""
	host_dc_name = "unknown"
	ip_addr = ""
	host_name = ""
	host_type = ""
	spm_status = ""
	releaseVer = "unknown"
	errMessages = []
	host_status = ""
	
	def __init__(self, csvList):
		'''
		This constructor assumes it is being passed a comma separated list consisting of all elements in a line from the dat file
		'''
		details = csvList
		
		if len(details) > 2:	
			self.uuid = details[0]
			self.name = details[1]
			self.host_dc_uuid = details[6]
			self.ip_addr = details[2]
			self.host_name = details[4]
			self.host_type = details[8]
			# determine host type from input
			if self.host_type == "0":
				self.set_host_type("RHEL")
			elif self.host_type == "2":
				self.set_host_type("RHEV-H")
			self.host_dc_name = 'unknown'
			self.errMessages = []
			self.host_status = self.discoverStatus(csvList)

	def get_host_status(self):
		return self.__host_status


	def set_host_status(self, value):
		self.__host_status = value


	def del_host_status(self):
		del self.__host_status

			
	def discoverStatus(self,csvLine):
		# In the database class we append the host status to the end of the csv line being fed when a host is created
		# as such, we should get the final list element from the csv line and store as status
		lastElement = len(csvLine)-1
		self.host_status = csvLine[lastElement]

	def get_err_messages(self):
		return self.errMessages


	def set_err_messages(self, value):
		#print "Setting errMessages to following: " + str(value)
		self.errMessages = value


	def del_err_messages(self):
		del self.errMessages

			
	def findErrs(self, auditArray):
		print "Looking for error messages"
		#errArray = []
		for m in auditArray:
			#print "Scanning new audit message"
			if self.name in m.get_l_message():
				#print "Sev: " + str(m.get_l_sev())
				if str(m.get_l_sev()) == "10" or str(m.get_l_sev()) == "2":
					#print "Found hostname in audit log, appending: "+m.get_l_message()+ " with a severity of " + str(m.get_l_sev())
					self.errMessages.append(m)
		#print "Finished the search"

	def get_spm_status(self):
		return self.spm_status


	def set_spm_status(self, value):
		self.spm_status = value

				
	def get_host_dc_name(self):
		return self.host_dc_name


	def set_host_dc_name(self, value):
		self.host_dc_name = value


	def del_host_dc_name(self):
		del self.host_dc_name


	def get_release_ver(self):
		return self.releaseVer

	def set_release_ver(self, value):
		self.releaseVer = value


	def del_spm_status(self):
		del self.spm_status


	def del_release_ver(self):
		del self.releaseVer


				
	
		
	def isSPM(self, spm_uuid):
		if spm_uuid == self.get_uuid():
			return True
		else:
			return False

	def get_host_type(self):
		return self.host_type


	def set_host_type(self, value):
		self.host_type = value


	def del_host_type(self):
		del self.host_type

		
	def get_uuid(self):
		return self.uuid


	def get_name(self):
		return self.name


	def get_host_dc_uuid(self):
		return self.host_dc_uuid


	def get_ip_addr(self):
		return self.ip_addr


	def get_host_name(self):
		return self.host_name


	def set_uuid(self, value):
		self.uuid = value


	def set_name(self, value):
		self.name = value


	def set_host_dc_uuid(self, value):
		self.host_dc_uuid = value


	def set_ip_addr(self, value):
		self.ip_addr = value


	def set_host_name(self, value):
		self.host_name = value


	def del_uuid(self):
		del self.uuid


	def del_name(self):
		del self.name


	def del_host_dc_uuid(self):
		del self.host_dc_uuid


	def del_ip_addr(self):
		del self.ip_addr


	def del_host_name(self):
		del self.host_name
	host_dc_name = property(get_host_dc_name, set_host_dc_name, del_host_dc_name, "host_dc_name's docstring")
	_spm_status = property(get_spm_status, set_spm_status, None, None)
	errMessages = property(get_err_messages, set_err_messages, del_err_messages, "errMessages's docstring")
	host_status = property(get_host_status, set_host_status, del_host_status, "host_status's docstring")

		
	
		