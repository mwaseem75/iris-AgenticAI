import iris,json

def get_production_status():
	iris.cls("%ZEmbedded.Utils").SetNameSpace("USER")
	return json.dumps(iris.cls('dc.AAI.Director').dispatchListProductions())
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


