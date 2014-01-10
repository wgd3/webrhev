from app import app
from flask import render_template, flash, request, redirect
from rhevlcbridge import *
import json


'''
During server init, here is what should happen:

 - Create database object
 - Create list of hosts, including their error messages 
 - Define list of scrollable entities for the left content area
 TODO:
   - Create list of disks
 - Define list of all object UUID and Names to be used in the left area and search field (only using UUID right now)
'''

# Load the database and it's hosts
#dbFile = "/home/wallace/cases/01002915/sosreport-LogCollector-20131223183303/database/sos_pgdump.tar"
#dbFile = "/home/wallace/cases/00945926/LogCollector/database/sos_pgdump.tar"
dbFile = "/home/wallace/cases/00986768/sosreport-LogCollector-comp-wguo-20131120115048-5fd4/database/sos_pgdump.tar"
database = Database(dbFile)

# get other lists of information for reference
dc_list = database.get_data_centers()
cluster_list = database.get_clusters()
sd_list = database.get_storage_domains()


# Getting host information
testHosts = database.get_hosts()
for h in testHosts:
	h.findErrs(database.get_audit_messages())

for h in testHosts:
	for d in dc_list:
		if h.get_uuid() == d.get_spm_uuid():
			h.set_spm_status(True)
		else:
			h.set_spm_status(False)

	for c in cluster_list:
		if c.get_uuid() == h.get_host_dc_uuid():
			for d in dc_list:
				if c.get_dc_uuid() == d.get_uuid():
					h.set_host_dc_name(d.get_name())

	
	
# Create typeahead list for search
taHosts = []
for host in testHosts:
	hUUID = host.get_uuid()
	taHosts.append(hUUID)
#taHostData=json.dumps(taHosts)
print taHosts
	
	
# Create the list entries for the (scrollable) left content pane
scrHosts = []
for host in testHosts:
	hName = host.get_name()
	hUUID = host.get_uuid()
	hTup = {'name':hName,'uuid':hUUID}
	scrHosts.append(hTup)

# Not functional yet
dbVerStr = "I dunno."

@app.route('/')
@app.route('/index')
@app.route('/hosts')
def index():

	displayHosts = get_host_details()
	print "Found " + str(len(displayHosts)) + " entries in displayHosts list"

	return render_template("body.html",
		title = 'Host Table Testing',
		dbVer = dbVerStr,
		host_list = scrHosts,
		#on init page load, just display information for first host in array
		hostEnt = displayHosts[0],
		taHostsList = taHosts)
	
@app.route('/host/<ident>')
def host(ident):
	'''
	This is meant to either be a name or UUID. We need to first validate that the name of UUID exists, then return the body.html
	'''
	
	hostDetails = get_host_details(ident)
	print "number of hosts details passed: " + str(len(hostDetails))
	
	if len(hostDetails) > 1:
		#flash('Something went wrong with host detail populating. Good luck debugging it...')
		return redirect('/')

	return render_template("body.html",
					title = 'Host Table Testing',
					dbVer = dbVerStr,
					host_list = scrHosts,
					#on init page load, just display information for first host in array
					hostEnt = hostDetails[0],
					taHostsList = taHosts)



@app.route('/vms')
def vms():
	
	return render_template("index.html")




'''
Helper functions
'''
def get_host_details(*args):
		
	print "Number of args passed: " + str(len(args))
	print args
	displayHosts = []
	
	if len(args) != 0:
		newHostUUID = args[0]
		for host in testHosts:
			if host.get_uuid() == newHostUUID:
				errMessages = []
				name  = host.get_name()
				uuid = host.get_uuid()
				htype = host.get_host_type()
				dc_name = host.get_host_dc_name()
				spmStatus = host.get_spm_status()
				host_status = host.get_host_status()
				for l in host.get_err_messages():
					errMessages.append({'lTime':l.get_l_time(),'lMess':l.get_l_message(),'lSev':l.get_l_sev()})
				hostDetails = {'name':name, 'uuid':uuid, 'type':htype,'audit':errMessages,'dc_name':dc_name,'spmStatus':spmStatus,'host_status':host_status,'htype':htype}
				displayHosts.append(hostDetails)
		
		return displayHosts
	elif len(args) == 0:				
				
		for host in testHosts:
			errMessages = []
			name  = host.get_name()
			uuid = host.get_uuid()
			htype = host.get_host_type()
			dc_name = host.get_host_dc_name()
			spmStatus = host.get_spm_status()
			host_status = host.get_host_status()
			for l in host.get_err_messages():
				errMessages.append({'lTime':l.get_l_time(),'lMess':l.get_l_message(),'lSev':l.get_l_sev()})
			hostDetails = {'name':name, 'uuid':uuid, 'type':htype,'audit':errMessages,'dc_name':dc_name,'spmStatus':spmStatus,'host_status':host_status,'htype':htype}
			displayHosts.append(hostDetails)
		
		return displayHosts
	else: 
		print "Something went really wrong when trying to call get_host_details"
		return Nones