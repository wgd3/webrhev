'''
Created on Dec 27, 2013

@author: wallace
'''
import tarfile, os
from rhevlcbridge.host import Host # Surely there is a better way to do this
from rhevlcbridge.storagedomain import StorageDomain
from rhevlcbridge.datacenter import DataCenter
from rhevlcbridge.cluster import Cluster
from rhevlcbridge.auditmesssage import AuditMessage


class Database():
	'''
	This class should be created by passing the sos_pgdump.tar file to it
	
	It will serve the purpose of pulling information from the tar file without the need to upload to a dbviewer
	'''

	''' Start declaring variables for the class'''
	dbDir = ""
	tarFile = ""
	dat_files = [] # this is a list for all the wanted dat files
	data_centers = []
	storage_domains = []
	hosts = []
	clusters = []
	audit_messages = []

	def __init__(self, dbFile):
		'''
		Constructor
		'''
		self.dbDir = os.path.dirname(dbFile)+"/"
		tarFile = tarfile.open(dbFile)
		self.unpack(tarFile, self.dbDir)
		
		# Now that we're unpacked, move on to gathering information
		self.data_centers = self.gatherDataCenters()
		self.storage_domains = self.gatherStorageDomains()
		self.hosts = self.gatherHosts()
		self.clusters = self.gatherClusters()
		self.audit_messages = self.loadAuditLog()

	def get_audit_messages(self):
		return self.audit_messages


	def set_audit_messages(self, value):
		self.audit_messages = value


	def del_audit_messages(self):
		del self.audit_messages


	def get_clusters(self):
		return self.clusters


	def set_clusters(self, value):
		self.clusters = value


	def del_clusters(self):
		del self.clusters


	def get_data_centers(self):
		return self.data_centers


	def get_storage_domains(self):
		return self.storage_domains


	def get_hosts(self):
		return self.hosts


	
	def unpack(self, tarFile, dbDir):
		# Start with extraction
		#print "Extracting..."
		tarFile.extractall(dbDir)
		
		# then set most of the needed variables for future functions
		#print "Setting dat files..."
		self.dat_files = ["data_center_dat",
					 "storage_domain_dat",
					 "host_dat",
					 "cluster_dat",
					 "audit_log",
					 "vds_dynamic"]
		
		#print self.dat_files[0]
		self.dat_files[0] = self.dat_files[0] +","+ self.findDat(" storage_pool ", dbDir+"restore.sql")
		#print "Found dat file: " + self.dat_files[0]
		#print "Passing this to the function: " + self.dat_files[0].split(",")[1]
		self.dat_files[1] = self.dat_files[1] +","+ self.findDat(" storage_domain_static ", dbDir+"restore.sql")
		self.dat_files[2] = self.dat_files[2] +","+ self.findDat(" vds_static ", dbDir+"restore.sql")	
		self.dat_files[3] = self.dat_files[3] +","+self.findDat(" vds_groups ", dbDir+"restore.sql")
		#print self.dat_files[3]
		self.dat_files[4] = self.dat_files[4] +","+self.findDat(" audit_log ", dbDir+"restore.sql")
		self.dat_files[5] = self.dat_files[5] +","+self.findDat(" vds_dynamic ", dbDir+"restore.sql")
		
	def findDat(self,table,restFile):
		'''
		Subroutine to find the dat file name in restore.sql
		''' 
		openFile = open(restFile, "r")
		lines = openFile.readlines()
	
		# print "Looking for " + table
	
		for n in lines:
			if n.find(table) != -1:
				if n.find("dat") != -1:
					datInd = n.find("PATH")
					datFileName =  n[datInd+7:datInd+15]
					if datFileName.endswith("dat"):
						#print "Found dat line for " + table
						#logging.warning('Return dat file: ' +datFileName)
						return datFileName
	
	def loadAuditLog(self):
		'''
		This is going to put the log_time,message, and severity fields from the audit_log table and put them in a list
		'''
		
		audit_list = []
		
		dat_file = self.dbDir+self.dat_files[4].split(",")[1]
		openDat = open(dat_file)
		
		lines = openDat.readlines()
		
		for l in lines:
			if len(l.split("\t")) > 1:
				newAM = AuditMessage(l.split("\t"))
				audit_list.append(newAM)
				
		openDat.close()
		return audit_list

	def gatherDataCenters(self):
		'''
		This method returns a list of comma-separated details of the Data Center
		'''
		dc_list = []
		#print self.dbDir
		#print self.dat_files[0]
		dat_file = self.dbDir+self.dat_files[0].split(",")[1]
		openDat = open(dat_file,"r")
		
		lines = openDat.readlines()		
		
		for l in lines:
			if len(l.split("\t")) > 1:
				newDC = DataCenter(l.split("\t"))
				dc_list.append(newDC)
			
		openDat.close()
		return dc_list
	
	def gatherStorageDomains(self):
		'''
		This method returns a list of comma-separated details of the Storage Domains
		'''
		sd_list = []
		dat_file = self.dbDir+self.dat_files[1].split(",")[1]
		#print dat_file
		openDat = open(dat_file,"r")
		
		lines = openDat.readlines()
		
		for l in lines:
			if len(l.split("\t")) > 1:
				#print "Line: " + l
				newSD = StorageDomain(l.split("\t"))
				sd_list.append(newSD)
			
		openDat.close()
		return sd_list
	
	def gatherClusters(self):
		'''
		This method returns a list of comma separated details for clusters
		'''
		cl_list = []
		dat_file = self.dbDir+self.dat_files[3].split(",")[1]
		
		openDat = open(dat_file,"r")
		
		lines = openDat.readlines()
		#print len(lines) 
		
		for l in lines:
			if len(l.split("\t")) > 1:
				newCluster = Cluster(l.split("\t"))
				#print "New Cluster: " + newCluster.get_dc_uuid()
				#print "Cluster Name: " + newCluster.get_name()
				cl_list.append(newCluster)
				
		openDat.close()
		return cl_list
		
	
	def gatherHosts(self):
		'''
		This method returns a list of comma-separated details of the Data Center
		'''
		host_list = []
		dat_file = self.dbDir+self.dat_files[2].split(",")[1]
		#print dat_file
		openDat = open(dat_file,"r")
		
		lines = openDat.readlines()
		
		for l in lines:
			if len(l.split("\t")) > 1:
				#print l.split("\t")
				newHost = Host(l.split("\t"))
				#print "New Host Name: " + newHost.get_name()
				host_list.append(newHost)
			
		openDat.close()
		
		# Get host statuses and append to current csv lines
		dat_file = self.dbDir+self.dat_files[5].split(",")[1]
		openDat = open(dat_file,"r")
		
		lines = openDat.readlines()
		
		for h in host_list:
			# At this point host_list is a list/collection of 'Host' objects, no longer a csv line
			curHost = h.get_uuid()
			for l in lines:
				# Validate that the uuid of the current host matches the uuid in the current line
				if curHost in l:
					# Set host status via host method
					h.set_host_status(l.split("\t")[1])
		
		return host_list
	
	
	data_centers = property(get_data_centers, None, None, None)
	storage_domains = property(get_storage_domains, None, None, None)
	hosts = property(get_hosts, None, None, None)
	clusters = property(get_clusters, set_clusters, del_clusters, "clusters's docstring")
	audit_messages = property(get_audit_messages, set_audit_messages, del_audit_messages, "audit_messages's docstring")
	
	