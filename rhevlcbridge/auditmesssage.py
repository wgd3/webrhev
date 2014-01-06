'''
Created on Jan 5, 2014

@author: wallace
'''

class AuditMessage():
	'''
	This class will create an object for each message in the audit_log
	'''

	lTime = ""
	lMessage = ""
	lSev = ""

	def __init__(self, csvList):
		'''
		This will init a new audit message with the log time, message, and severity
		'''
		
		details = csvList
		
		if len(details) > 2:		
			self.lTime = details[9]
			self.lMessage = details[13]
			self.lSev = details[12]

	def get_l_time(self):
		return self.lTime


	def get_l_message(self):
		return self.lMessage


	def get_l_sev(self):
		return self.lSev


	def set_l_time(self, value):
		self.lTime = value


	def set_l_message(self, value):
		self.lMessage = value


	def set_l_sev(self, value):
		self.lSev = value


	def del_l_time(self):
		del self.lTime


	def del_l_message(self):
		del self.lMessage


	def del_l_sev(self):
		del self.lSev

	lTime = property(get_l_time, set_l_time, del_l_time, "lTime's docstring")
	lMessage = property(get_l_message, set_l_message, del_l_message, "lMessage's docstring")
	lSev = property(get_l_sev, set_l_sev, del_l_sev, "lSev's docstring")
		
		
		
		