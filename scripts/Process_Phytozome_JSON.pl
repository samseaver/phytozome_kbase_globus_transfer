#!/usr/bin/env perl
use warnings;
use strict;
use JSON;
my $JSON=undef;

my $Root="Phytozome_Oct2023";
open(FH, "< ../files/${Root}.json");
while(<FH>){$JSON.=$_}close(FH);$JSON=from_json($JSON);

open(OUT, "> ../output/Oct_2023/JSON_Contents.txt");
my %Names=();
foreach my $organism (@$JSON){

#    print $organism->{organism_abbreviation},"\t",$organism->{organism_portalname},"\t";
#    print $organism->{organism_gspecies},"\t",$organism->{data_portalname},"\t";
#    print $organism->{organism_shortname},"\t",$organism->{organism_name},"\n";

#organism_abbreviation
#organism_portalname
#organism_gspecies
#transcript_count
#acronym
#data_portalname

    $Names{$organism->{organism_gspecies}."_".$organism->{annotation_version}}=$organism->{organism_name};
    $organism->{common_name}="" if !exists($organism->{common_name}) or !defined($organism->{common_name});
    $organism->{assembly_source}="na" if !exists($organism->{assembly_source});
    $organism->{annotation_source}="na" if !exists($organism->{annotation_source});
    $organism->{data_restriction_policy}="na" if !exists($organism->{data_restriction_policy});

    print OUT $organism->{organism_name},"\t",$organism->{taxon_id},"\t",$organism->{proteome_id},"\t";
    print OUT $organism->{organism_gspecies},"\t",$organism->{common_name},"\t";
    print OUT $organism->{assembly_version},"\t",$organism->{assembly_source},"\t";
    print OUT $organism->{annotation_version},"\t",$organism->{annotation_source},"\t";
    print OUT $organism->{data_restriction_policy},"\t";
    print OUT $organism->{embryophyte_busco_completeness},"\n";
}
