import requests

def get_covid_data(num_records):
    """Returns list of full study records from cinicaltrials.gov
        
        Parameters
        num_records(int): number of studies desired (note: may return fewer) 
        
        For additional information:
        https://clinicaltrials.gov/api/gui/ref/api_urls
        
        Data dictionary:
        https://prsinfo.clinicaltrials.gov/definitions.html
        
        Browser demo:
        https://clinicaltrials.gov/api/gui/demo/simple_full_study
    """
    records = []
    count = 0
    
    while count < num_records:
        min_rank = count+1
        max_rank = count+10
        url = f"https://clinicaltrials.gov/api/query/full_studies?expr=covid-19+vaccine%0D%0A&min_rnk={min_rank}&max_rnk={max_rank}&fmt=json"
        r = requests.get(url)
        data = r.json()
        try:
            for study in data['FullStudiesResponse']['FullStudies']:
                records.append(study)
                count += 1
        except KeyError:
            break
    
    print(f"totaly records returned: {count}")
    return records


li = get_covid_data(30)

for study in li:
    
    orgName = study['Study']['ProtocolSection']['IdentificationModule']['Organization']['OrgFullName']
    bTitle = study['Study']['ProtocolSection']['IdentificationModule']['BriefTitle']
    oTitle = study['Study']['ProtocolSection']['IdentificationModule']['OfficialTitle']
    
    try:
        phase = study['Study']['ProtocolSection']['DesignModule']['PhaseList']['Phase']
    except KeyError:
        phase = 'Not a clinical trial'
    
    try:
        interventionName = ', '.join(i['InterventionName'] for i in study['Study']['ProtocolSection']['ArmsInterventionsModule']['InterventionList']['Intervention'])
    except KeyError:
        interventionName = "No intervention"
    
    lastUpdate = study['Study']['ProtocolSection']['StatusModule']['LastUpdateSubmitDate']
    currentStatus = study['Study']['ProtocolSection']['StatusModule']['OverallStatus']
    startDate = study['Study']['ProtocolSection']['StatusModule']['StartDateStruct']['StartDate']
    compDate = study['Study']['ProtocolSection']['StatusModule']['CompletionDateStruct']['CompletionDate']
    compType = study['Study']['ProtocolSection']['StatusModule']['CompletionDateStruct']['CompletionDateType']
    leadSponsor = study['Study']['ProtocolSection']['SponsorCollaboratorsModule']['LeadSponsor']['LeadSponsorName']
    leadSponsorClass = study['Study']['ProtocolSection']['SponsorCollaboratorsModule']['LeadSponsor']['LeadSponsorClass']
    
    briefSummary = study['Study']['ProtocolSection']['DescriptionModule']['BriefSummary']

    print(
    f"""Brief Title: {bTitle}

Official Title: {oTitle}
Trial Phase: {phase}
Intervention Name: {interventionName}
Organization: {orgName}
As of {lastUpdate} the current status for this trial is '{currentStatus}', which began on {startDate}
The {compType.lower()} completion date is {compDate}.
The trial is {leadSponsorClass} sponsored, and the lead sponsor is {leadSponsor}.

Brief description of Trial: 
{briefSummary}
{'-'*80}
""")
