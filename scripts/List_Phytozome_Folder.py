#!/usr/bin/env python
import sys
import globus_sdk

Root="../output/Oct_2023"
Version="V13"
f=open('globus_transfer_token.txt')
Transfer_Token=f.read().rstrip()
f.close()

authorizer = globus_sdk.AccessTokenAuthorizer(Transfer_Token)
transfer_client = globus_sdk.TransferClient(authorizer=authorizer)

print("Client instantiated")

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
list_response = transfer_client.operation_ls(JGI_Endpoint,**{"path":JGI_Path})

print("Listing received")

for Phytozome_Version in list_response['DATA']:
	if(Version not in Phytozome_Version['name']):
		continue
	
	species_list = transfer_client.operation_ls(JGI_Endpoint,**{"path":JGI_Path+Phytozome_Version['name']})
	for species in species_list:
		if('Creinhardtii' not in species['name']):
			continue

		if(species['type'] != 'dir'):
			continue

		if('early_release' in species['name'] or 'global_analysis' in species['name']):
			if('early_release' in species['name']):
				print("Skipping early_release: "+species['name'])
			continue

		print("Processing "+species['name']+" in "+Phytozome_Version['name'])
		versions_list = transfer_client.operation_ls(JGI_Endpoint,**{"path":JGI_Path+Phytozome_Version['name']+"/"+species['name']})
		assembly=0
		annotation=0
		gene_file=0
		#If no version numbering, check now
		for version in versions_list:
			if(version['name']=='annotation'):
				annotation=1
				annotation_list = transfer_client.operation_ls(JGI_Endpoint,**{"path":JGI_Path+Phytozome_Version['name']+"/"+species['name']+"/"+version['name']})
				for annotation in annotation_list:
					if(annotation['name'].endswith('gene.gff3.gz') or \
						   annotation['name'].endswith('annotation_info.txt') or \
						   annotation['name'].endswith('defline.txt') or \
						   annotation['name'].endswith('synonym.txt') or \
							annotation['name'].endswith('protein.fa.gz')):
						print(annotation['name'])
						gene_file=1
			if(version['name']=='assembly'):
				assembly=1
				assembly_list = transfer_client.operation_ls(JGI_Endpoint,**{"path":JGI_Path+Phytozome_Version['name']+"/"+species['name']+"/"+version['name']})
				for assembly in assembly_list:
					if('.fa' in assembly['name'] and 'mask' not in assembly['name']):
						print(assembly['name'])

		#Go through versions
		if(annotation==0):
			for version in versions_list:
				print(version['name'])
				dir_list = transfer_client.operation_ls(JGI_Endpoint,**{"path":JGI_Path+Phytozome_Version['name']+"/"+species['name']+"/"+version['name']})
				for dir in dir_list:
					print(dir['name'])
					if(dir['name']=='annotation'):
						annotation_list = transfer_client.operation_ls(JGI_Endpoint,**{"path":JGI_Path+Phytozome_Version['name']+"/"+species['name']+"/"+version['name']+"/"+dir['name']})
						for annotation in annotation_list:
							print(annotation['name'])
							if(annotation['name'].endswith('gene.gff3.gz') or \
								   annotation['name'].endswith('annotation_info.txt') or \
								   annotation['name'].endswith('defline.txt') or \
								   annotation['name'].endswith('synonym.txt') or \
									annotation['name'].endswith('protein.fa.gz')):
								gene_file=1
								print(annotation['name'])
					if(dir['name']=='assembly'):
						assembly_list = transfer_client.operation_ls(JGI_Endpoint,**{"path":JGI_Path+Phytozome_Version['name']+"/"+species['name']+"/"+version['name']+"/assembly"})
						for assembly in assembly_list:
							if('.fa' in assembly['name'] and 'mask' not in assembly['name'] and 'Mask' not in assembly['name']):
								print(assembly['name'])
		if(gene_file==0):
			print("Warning: no gene file for "+Phytozome_Version['name']+" "+species['name'])

