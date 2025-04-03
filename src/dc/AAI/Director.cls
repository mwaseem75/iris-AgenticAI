Include (%occInclude, Ensemble)

Class dc.AAI.Director [ Inheritance = right, ProcedureBlock, System = 4 ]
{

// Function provide Production details, used by Production agent

ClassMethod dispatchListProductions() As %String
{
	// Loop over the productions in this namespace
	Set tRS = ##class(%ResultSet).%New("Ens.Config.Production:ProductionStatus")
	If '$IsObject(tRS) Set tSC = %objlasterror Quit
	
	Set tSC = tRS.Execute()
	Quit:$$$ISERR(tSC)
	
	set tDict = ##class(%SYS.Python).Import("builtins").dict()

	While (tRS.Next()) {
		Set tProduction = tRS.Data("Production")
		Set tInfo = ##class(%SYS.Python).Import("builtins").dict()
		do tInfo."__setitem__"("Status",tRS.Data("Status"))
		do tInfo."__setitem__"("LastStartTime",tRS.Data("LastStartTime"))
		do tInfo."__setitem__"("LastStopTime",tRS.Data("LastStopTime"))
		do tInfo."__setitem__"("AutoStart",$G(^Ens.AutoStart)=tProduction)
		do tDict."__setitem__"(tProduction,tInfo)
	}

	Kill tRS

	return tDict
}

// Function used by the Production Agent in the process of stopping and starting production.

ClassMethod StatusProduction() As %String
{
	Set sc = $$$OK
	
	$$$ThrowOnError(##class(Ens.Director).GetProductionStatus(.tProdName,.tStatus))
	set status = $CASE(tStatus,$$$eProductionStateRunning:"running",
												$$$eProductionStateStopped:"stopped",
												$$$eProductionStateSuspended:"suspended",
												$$$eProductionStateTroubled:"toubled",	
 											   :"unknown")
	
	Return status
}

}
