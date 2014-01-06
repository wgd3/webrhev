from app import app
from flask import render_template
from rhevlcbridge import *


@app.route('/')
@app.route('/index')
@app.route('/hosts')
def index():
	
	'''
	When index.html is requested this will populate all hosts for testing purposes. 
	Will expand to all entities in the future
	'''
	
	# Load the database and it's hosts
	dbFile = "/home/wallace/cases/01002915/sosreport-LogCollector-20131223183303/database/sos_pgdump.tar"
	database = Database(dbFile)
	testHosts = database.get_hosts()
	# Not functional yet
	dbVerStr = "I dunno."
	
	# Create the typeahead list for the left content pane
	taHosts = []
	for host in testHosts:
		hUUID = host.get_uuid()
		taHosts.append(hUUID)
		
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
		host.findErrs(database.get_audit_messages())
		for l in host.get_err_messages():
			errMessages.append({'lTime':l.get_l_time(),'lMess':l.get_l_message(),'lSev':l.get_l_sev()})
		hostDetails = {'name':name, 'uuid':uuid, 'type':htype,'audit':errMessages}
		displayHosts.append(hostDetails)
	
	return render_template("hosts.html",
		title = 'Host Table Testing',
		dbVer = dbVerStr,
		host_list = displayHosts,
		scrHostsList = scrHosts,
		taHostsList = taHosts)

@app.route('/vms')
def vms():
	
	return render_template("index.html")