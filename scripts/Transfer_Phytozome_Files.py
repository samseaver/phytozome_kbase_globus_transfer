#!/usr/bin/env python
import sys
import globus_sdk

root="../output/Oct_2023"
version="V13"
f=open('../files/Species_to_Transfer.txt')
Accepted_Species=dict()
for line in f:
	line=line.strip('\r\n')
	array = line.split('\t')

	#If there's no model version
	if(array[3]==''):
		print(array)
		continue

	if(array[1] not in Accepted_Species):
		Accepted_Species[array[1]]=dict()

	if(array[2] not in Accepted_Species[array[1]]):
		Accepted_Species[array[1]][array[2]]=dict()

	Accepted_Species[array[1]][array[2]]['model_version']=array[3]
	Accepted_Species[array[1]][array[2]]['phytozome_version']="Phytozome"+array[0]

for species in Accepted_Species:
	for proteome in Accepted_Species[species]:
		print(species,proteome,Accepted_Species[species][proteome])

f=open(root+'/Phytozome_Versions_GeneModels_PhytozomeV13.txt')
Extra_Folder=dict()
Accepted_Paths=dict()
for line in f:
	line=line.strip()
	array = line.split('\t')

	species=array[1]

	if(species not in Accepted_Species):
		continue

	if(species not in Accepted_Paths):
		Accepted_Paths[species]=dict()

	if(len(array)>3):
		if(array[0] not in Extra_Folder):
			Extra_Folder[array[0]]=dict()
		Extra_Folder[array[0]][species]=array[3]

	for number in Accepted_Species[species]:
		if(number not in Accepted_Paths[species]):
			Accepted_Paths[species][number]=dict()

		if(number in array[2] and array[0] == Accepted_Species[species][number]['phytozome_version']):
			extra_folder=None
			if(array[0] in Extra_Folder and species in Extra_Folder[array[0]]):
				extra_folder=Extra_Folder[array[0]][species]

			if(array[2].endswith(".fa.gz")):
				Accepted_Paths[species][number]['assembly'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/assembly/'+array[2]
				if(extra_folder):
					Accepted_Paths[species][number]['assembly'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/'+extra_folder+'/assembly/'+array[2]
			if(array[2].endswith(".gene.gff3.gz")):
				Accepted_Paths[species][number]['annotation'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/annotation/'+array[2]
				if(extra_folder):
					Accepted_Paths[species][number]['annotation'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/'+extra_folder+'/annotation/'+array[2]
			if(array[2].endswith(".annotation_info.txt")):
				Accepted_Paths[species][number]['ontology'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/annotation/'+array[2]
				if(extra_folder):
					Accepted_Paths[species][number]['ontology'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/'+extra_folder+'/annotation/'+array[2]
			if(array[2].endswith(".defline.txt")):
				Accepted_Paths[species][number]['functions'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/annotation/'+array[2]
				if(extra_folder):
					Accepted_Paths[species][number]['functions'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/'+extra_folder+'/annotation/'+array[2]
			if(array[2].endswith(".synonym.txt")):
				Accepted_Paths[species][number]['synonyms'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/annotation/'+array[2]
				if(extra_folder):
					Accepted_Paths[species][number]['synonyms'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/'+extra_folder+'/annotation/'+array[2]
			if(array[2].endswith(".protein.fa.gz")):
				Accepted_Paths[species][number]['proteins'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/annotation/'+array[2]
				if(extra_folder):
					Accepted_Paths[species][number]['proteins'] = Accepted_Species[species][number]['phytozome_version']+'/'+array[1]+'/'+extra_folder+'/annotation/'+array[2]

for species in Accepted_Paths:
	for proteome in Accepted_Paths[species]:
		print(species,proteome,Accepted_Paths[species][proteome])

f=open('globus_transfer_token.txt')
Transfer_Token=f.read().rstrip()
f.close()

authorizer = globus_sdk.AccessTokenAuthorizer(Transfer_Token)
transfer_client = globus_sdk.TransferClient(authorizer=authorizer)

f=open('../globus/origin.txt')
JGI_Endpoint=""
JGI_Path=""
for line in f.readlines():
	line=line.rstrip()
	(key,value)=line.split("=")
	if(key=="origin_id"):
		JGI_Endpoint=value
	if(key=="origin_path"):
		JGI_Path=value
f.close

f=open('../globus/kbase_dtn_id.txt')
DTN_Endpoint=f.read().rstrip()
f.close

tasks=open('Task_IDs.txt','w')
files=open('Tasked_Files.txt','w')
Transfer_Data = globus_sdk.TransferData(transfer_client, JGI_Endpoint, DTN_Endpoint)
Global_Data_Count=1
Data_Count=1
for species in sorted(Accepted_Paths.keys()):
	for number in sorted(Accepted_Paths[species].keys()):
		for type in ("annotation","assembly","ontology","synonyms","functions","proteins"):
			if(type not in Accepted_Paths[species][number]):
				continue
			file = JGI_Path+Accepted_Paths[species][number][type]
			files.write(file+'\n')
			Transfer_Data.add_item(file,'/seaver/'+file)
			Data_Count+=1
			Global_Data_Count+=1
			if(Data_Count==100):
				transfer_result = transfer_client.submit_transfer(Transfer_Data)
				tasks.write(transfer_result["task_id"]+'\n')
				
				#reset
				Transfer_Data = globus_sdk.TransferData(transfer_client, JGI_Endpoint, DTN_Endpoint)
				Data_Count=1

#Last one
transfer_result = transfer_client.submit_transfer(Transfer_Data)
tasks.write(transfer_result["task_id"]+'\n')
tasks.close()
files.close()
print("Transferred "+str(Global_Data_Count)+" files")
