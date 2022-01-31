# Phytozome to KBase DTN Transfer

### Nota Bene

    The scripts were developed under a different folder hierarchy before being transferred into this repository so they will currently not work out of the box but it will take minimal editing.

## Overview

To load a set of large reference genomes into a KBase workspace, I
like to use KBase's data transfer node for several reasons:
1. It has the memory to run GFU to process and save large genomes.
2. It has the docker desktop CLI available to run the KBase SDK.
3. It's a Globus endpoint so its straightforward to transfer the
selected files from the JGI Globus endpoint.

The last point is the aim of the code in this repository

## General Flow

1.  Identify the list of unrestricted genomes that can be loaded
2.  Find the appropriate files that match each genome assembly and gene model versions
3.  Transfer the files

### Identify the list of unrestricted genomes in Phytozome

* Go to the home page of Phytozome https://phytozome-next.jgi.doe.gov,
  click on the "Release Notes" tab, and click Export.  That’ll give
  you the full spreadsheet in tab-separated format to download. I'm
  keeping them in "files".

* To download the metadata for each genome, you can run
  ./scripts/Get_Genome_MetaData.sh on the downloaded file. The output
  is in JSON format will have to be re-directed into another
  file. Again, these are to be found in "files".

* The JSON metadata lists the assembly version and gene model version
  for each genome (note that there may be multiple versions for
  different species) and whether they are restricted or unrestricted.

### Set up access to Globus endpoint

* I need to iterate through the files available at the Globus endpoint
  in order to find the right ones to transfer and use.

* You'll need the Globus python API so run pip install globus-sdk

* First, for the Globus API to work, I run
  ./globus/Retrieve_Transfer_Token.py to get the necessary tokens. The
  script generates a URL that must be accessed using a browser, and
  from which the user then gets the token to input into the script to
  save the appropriate information. There has to be a better way to do
  this programmatically, but I remember getting stuck on Python
  requests.

### Ask JGI to stage necessary files

* The files aren't immediately accessible at the JGI Globus endpoint
  so you need to make the request online

* Log in at https://phytozome-next.jgi.doe.gov/ (top-right corner)

* Go to
  https://genome.jgi.doe.gov/portal/pages/dynamicOrganismDownload.jsf?organism=Phytozome
  and click on "Download via Globus". You'll get an email when the
  data is ready (this has typically taken somewhere between 15 minutes
  to a couple of hours so don't hold your breath.

* I don't use Globus in the browser, so I don't click on the Globus
  URL that you get in the email, but it can be parsed for several key
  attributes that you can use with the API: origin_id, origin_path,
  and add_identity. These are all stored locally in origin.txt. The
  current file in the repository has examples that I use, but I changed some
  digits in case.
  
* I then run ./scripts/List_Phytozome_Species_GeneModels.py which uses the
  transfer token and the contents of origin.txt to access the staged
  data and parses all the files that I could use for each genome. The
  file has to be edited so that the output is saved in a new
  directory. The latest context is listed in "output".

### Find appropriate files

* The number of different files that are available on the Globus
  endpoint, and the size of some of them (Phytozome V13 currently
  stands as >2TB in total) means it's unreasonable just to transfer a
  single directory. The list of acceptable file types is retrieved in
  the previous step.

* However, I not only have to find the right files that work with the
  GFU, but I have to make sure that they match the versioning in the
  JSON metadata so that I know I am not uploading any restricted
  genomes, and this takes some manual work to review.

* I run ./scripts/Process_Phytozome_JSON.pl which parses the JSON
  metadata into a flat-file. This step is kind of redundant, but the
  "flat" output has made it easier for me to review the metadata.

* I run ./scripts/Process_Phytozome_Species.pl which combines
  the JSON metadata with the list of Phytozome files to find the files
  that match. It will declare which genomes are rejected for transfer
  because they are unrestricted, or which genomes are rejected because
  the versioning doesn't match. I manually review the versioning, (and
  in some cases I'll have to email David Goodstein to double-check)
  and edit the regex in the code so I can "force" a match if
  necessary.

### Transfer the files

* With everything in place, I run
  ./scripts/Transfer_Phytozome_Files.py. It takes the accepted list of
  files and initates a globus transfer for sets of files, transferring
  them to the KBase Globus Endpoint which is hosted on the data
  transfer node (DTN).

* Finally, because the files in the DTN are cleaned out regularly, I
  log onto the DTN and I copy the files into my home directory so I
  can hold onto them when running and testing GFU. So, on the DTN, I
  run: $ cp -r /data/bulk/seaver/14474/9/Phytozome ~/genomes/