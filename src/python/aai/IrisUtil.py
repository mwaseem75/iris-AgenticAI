import iris,json

#Get production status, used in starting and stoping production
def get_production_status():
	iris.cls("%ZEmbedded.Utils").SetNameSpace("USER")
	return iris.cls('dc.AAI.Director').StatusProduction()

#Get production details, call by Production agent tool
def get_production_details():
	iris.cls("%ZEmbedded.Utils").SetNameSpace("USER")
	return json.dumps(iris.cls('dc.AAI.Director').dispatchListProductions())

#Start the production
@staticmethod
def start_production(production_name=None):
	if get_production_status() == 'running':
		return "Production is already running"
	if production_name is None or production_name == '':
		production_name = get_default_production()
		
	sts = iris.cls('Ens.Director').StartProduction(production_name)
	if sts == 1:
		return "Production started Successfully"
	else:
		return "Error while starting production"

# stop the production
@staticmethod
def stop_production():
	if get_production_status() == 'stopped':
		return "Could not find running Production"
	sts=iris.cls('Ens.Director').StopProduction()
	if sts == 1:
		return "Production stoped Successfully"
	else:
		return "Error while stoping production"


@staticmethod
def get_default_production():
	glb = iris.gref("^Ens.Configuration")
	default_production_name = glb['csp', "LastProduction"]
	if default_production_name is None or default_production_name == '':
		#Assign default production for demo, If could not find the last running production
		default_production_name = 'dc.AAI.TestProduction'
	return default_production_name

#get sql statements based passed id
def get_processes():	
	query = '''
        SELECT ID, NameSpace, Routine, 
               state, PidExternal FROM %SYS.ProcessQuery ORDER BY NameSpace desc        
        '''
	statement = iris.sql.exec(query)
	df = statement.dataframe()
		
	return json.loads(df.to_json(orient="split"))

#Get dashboard statistics
def get_dashboard_stats( ):
	iris.cls("%ZEmbedded.Utils").SetNameSpace("%SYS")
	ref = iris.cls("SYS.Stats.Dashboard").Sample()
	iris.cls("%ZEmbedded.Utils").SetNameSpace("USER")

	last_backup = ref.LastBackup
	
	#check if variable is empty
	if not last_backup:
		last_backup = "Never"

	content = {
		'ApplicationErrors':ref.ApplicationErrors,
		'CSPSessions':ref.CSPSessions,
		'CacheEfficiency':ref.CacheEfficiency,
		'DatabaseSpace' : ref.DatabaseSpace,
		'DiskReads' : ref.DiskReads,
		'DiskWrites' : ref.DiskWrites,
		'ECPAppServer' : ref.ECPAppServer,
		'ECPAppSrvRate' : ref.ECPAppSrvRate,
		'ECPDataServer' : ref.ECPDataServer,
		'ECPDataSrvRate' : ref.ECPDataSrvRate,
		'GloRefs' : ref.GloRefs,
		'GloRefsPerSec' : ref.GloRefsPerSec,
		'GloSets' : ref.GloSets,
		'JournalEntries' : ref.JournalEntries,
		'JournalSpace' : ref.JournalSpace,
		'JournalStatus' : ref.JournalStatus,
		'LastBackup' : last_backup,
		'LicenseCurrent' : ref.LicenseCurrent,
		'LicenseCurrentPct' : ref.LicenseCurrentPct,
		'LicenseHigh' : ref.LicenseHigh,
		'LicenseHighPct' : ref.LicenseHighPct,
		'LicenseLimit' : ref.LicenseLimit,
		'LicenseType' : ref.LicenseType,
		'LockTable' : ref.LockTable,
		'LogicalReads' : ref.LogicalReads,
		'Processes' : ref.Processes,
		'RouRefs' : ref.RouRefs,
		'SeriousAlerts' : ref.SeriousAlerts,
		'ShadowServer' : ref.ShadowServer,
		'ShadowSource' : ref.ShadowSource,
		'SystemUpTime' : ref.SystemUpTime,
		'WriteDaemon' :  ref.WriteDaemon		

		}

	return json.dumps(content)


