# Acceptance of Phytozome Genomes for Loading

The key criteria for loading a Phytozome genome into KBase is whether
it is unrestricted or not. Restricted genomes come with the key
condition that they are publicly available so long as nobody publishes
any paper based on the data within. For each "release" from Phytozome,
the scripts process whether they are restricted or not and prints out
the list of accepted genomes in
`Accepted_Phytozome_Versions_GeneModels.txt`

### Report of Loading Genomes

The loading of the genomes will print out a summary into
`Phytozome_Upload_Summary_Prod.txt` (I try to generate separate files
for each environment, but will only keep the one for production). This
file confirms which genomes were loaded.

### Phytozome Releases and Genome versioning

At some point (Dec 2020) I tried to process all the versions of
Phytozome, and determine, in order, which genomes needed to be
released from which version, I did this so I could try and keep older
releases of genomes too. I found out that the version of Phytozome
itself is not linked to the versioning of the genomes, so there was no
point in doing so. I also realized that both the KBaseGenomes.Genome
spec and GFU code evolves, and as such, I should re-load every genome
when I can.

However, this means that there are a number of genomes currently
available in the `Phytozome_Genomes` workspace that are no longer
available in the latest release of Phytozome (There's currently 24 of
them). I still need to follow up and check these, it's likely that the
means of versioning the assembly and the gene models were altered so
the strings formatted for the genome workspace id no longer match.