from app import app
from flask import render_template
from rhevlcbridge import *


'''
During server init, here is what should happen:

 - Create database object
 - Create list of hosts, including their error messages 
 TODO:
   - Create list of disks
 - Define list of all object UUID and Names to be used in the left area and search field (only using UUID right now)
'''

# Load the database and it's hosts
#dbFile = "/home/wallace/cases/01002915/sosreport-LogCollector-20131223183303/database/sos_pgdump.tar"
dbFile = "/home/wallace/cases/00945926/LogCollector/database/sos_pgdump.tar"
database = Database(dbFile)


# Getting host information
testHosts = database.get_hosts()
for h in testHosts:
	h.findErrs(database.get_audit_messages())
	
	
# Create typeahead list for search
taHosts = []
for host in testHosts:
	hUUID = host.get_uuid()
	taHosts.append(hUUID)

# Not functional yet
dbVerStr = "I dunno."

@app.route('/')
@app.route('/index')
@app.route('/hosts')
def index():
	
	# Create the list entries for the (scrollable) left content pane
	scrHosts = []
	for host in testHosts:
		hName = host.get_name()
		hUUID = host.get_uuid()
		hTup = {'name':hName,'uuid':hUUID}
		scrHosts.append(hTup)
	
	# Create list entries for the tabs on the right content pane
	displayHosts = []
	for host in testHosts:
		errMessages = []
		name  = host.get_name()
		uuid = host.get_uuid()
		htype = host.get_host_type()
		for l in host.get_err_messages():
			errMessages.append({'lTime':l.get_l_time(),'lMess':l.get_l_message(),'lSev':l.get_l_sev()})
		hostDetails = {'name':name, 'uuid':uuid, 'type':htype,'audit':errMessages}
		displayHosts.append(hostDetails)
	
	return render_template("body.html",
		title = 'Host Table Testing',
		dbVer = dbVerStr,
		host_list = displayHosts,
		hostEnt = displayHosts[0],
		taHostsList = taHosts)
	
@app.route('/host/<ident>')
def host(ident):
	'''
	This is meant to either be a name or UUID. We need to first validate that the name of UUID exists, then return the body.html
	'''
	for h in testHosts:
		if h.get_uuid() == ident:
			return render_template()



@app.route('/vms')
def vms():
	
	return render_template("index.html")