#!/usr/bin/env perl
use warnings;
use strict;
my @temp=undef;

my $Root = "Oct_2023";
my $Release = "V13";

open(FH, "< ../output/${Root}/JSON_Contents.txt");
my %Unrestricted=();
my %Restricted=();
my %Names=();
while(<FH>){
    chomp;
    @temp=split(/\t/,$_,-1);

    $Names{$temp[3]}=$temp[0];
    
    if($temp[9] eq "restricted"){

	$Restricted{$temp[3]}{$temp[7]}=$temp[1];

    }elsif($temp[0] =~ "Brachypodium distachyon"){

	$Unrestricted{$temp[3]}{$temp[7]}=$temp[1];

	$temp[3] =~ s/BdistachyonS8iic/BdistachyonS8iiC/;
	$temp[3] =~ s/Pangenome/pangenome/;
	$Names{$temp[3]}=$temp[0];
	
	my $spp_ver = $temp[3];
	$spp_ver =~ s/Bdistachyon//;
	next if $spp_ver eq "";

	$spp_ver =~ s/Ron2/RON2/;
	$spp_ver =~ s/Bd3-1/Bd3-1_r/;

	foreach my $id ("BdTR2g","BdTR10c","BdTR2b","BdTR11i",
			"BdTR3c","BdTR11g","BdTR13c","BdTR9k",
			"BdTR11a","BdTR5i"){
	    my $new_id = $id;
	    $new_id =~ s/(\w)$/\U$1\E/;
	    $spp_ver =~ s/${id}/${new_id}/;
	}

	$spp_ver =~ s/Pangenome/pangenome/;
	$spp_ver = "v1.".$spp_ver.".1" if $spp_ver !~ /Ctrl$/;
	$spp_ver =~ s/(v1\.ABR[69])\.1$/$1/;
	
	$Unrestricted{$temp[3]}{$spp_ver}=$temp[1];
	
    }elsif($temp[9] eq "unrestricted"){

	#Exception
	$temp[3] =~ s/CsubellipsoideaC-169/CsubellipsoideaC169/;
	$Names{$temp[3]}=$temp[0];
	
	$Unrestricted{$temp[3]}{$temp[7]}=$temp[1];

    }

}
close(FH);

my %Phytozome=();
open(FH, "< ../output/${Root}/Phytozome_Versions_GeneModels_Phytozome".${Release}.".txt");

while(<FH>){
    chomp;
    @temp=split(/\t/,$_,-1);
    next if $temp[2] !~ /gene\.gff3\.gz/;
    
    $temp[1].="_".$temp[3] if $temp[3];
    
    $Phytozome{$temp[0]}{$temp[1]}=$temp[2];
}
close(FH);

my %Species_Releases=();
foreach my $species (keys %{$Phytozome{"Phytozome".$Release}}){

    #Parse version and gene model number
    my $file = $Phytozome{"Phytozome".$Release}{$species};
    $file =~ s/\.?gene.gff3.gz$//;

    @temp=split(/_/,$file);
    my $model_number = $temp[1];
    my $model_version = $temp[2];
    
    my $temp_version = undef;
    if($species =~ /_/){
	($species,$temp_version)=split(/_/,$species);
    }

    #Exceptions
    if($temp[0] eq "CsubellipsoideaC"){
	$species=$temp[0].$temp[1];
	$model_number = $temp[2];
	$model_version = $temp[3];
    }
    
    if($temp[0] eq "Zmays" && $temp[3]){
	$model_version .="_".$temp[3];
    }

    if($temp[0] =~ /Bdistachyon/ && $species =~ /-/){
	$species=$temp[0]."-".$temp[1];
	$model_number = $temp[2];
	$model_version = join("_",@temp[3...$#temp]);
    }

    if($temp[0] eq "Bvulgaris"){
	$model_version.="_1.0";
    }

    if($temp[0] eq "Lsativa"){
	$model_version="V8";
    }

    if(!exists($Unrestricted{$species})){
	print "Out as restricted species: ",$Release,"\t",$species,"\t",$model_version,"\n";
	next;
    }

    if(!exists($Unrestricted{$species}{$model_version})){
	print "Out as restricted model version: ",$Release,"\t",$species,"\t",$model_version,"\n";
	next;
    }

    push(@{$Species_Releases{$species}{$Release}},{'number'=>$model_number,
						   'version'=>$model_version,
						   'tax_id'=> $Unrestricted{$species}{$model_version}});
}

my %Final_Numbers = ();
my %Tax_IDs = ();
foreach my $species (sort keys %Species_Releases){
    my %Release_Combination=();
    if(exists($Species_Releases{$species}{$Release})){

	foreach my $hash (@{$Species_Releases{$species}{$Release}}){
	    my $combo_string = $hash->{'number'}.$hash->{'version'};
	    if(!exists($Release_Combination{$combo_string})){
		$Release_Combination{$combo_string}=$Release;
		$Final_Numbers{$species}{$hash->{'number'}}{$hash->{'version'}}=$Release;
		$Tax_IDs{$species}=$hash->{'tax_id'};
	    }
	}
    }
}

open(FH, "> ../output/${Root}/Accepted_Phytozome_Versions_GeneModels.new");
foreach my $species (sort keys %Final_Numbers){
    foreach my $number (sort keys %{$Final_Numbers{$species}}){
	foreach my $version (sort keys %{$Final_Numbers{$species}{$number}}){
	    print FH $Final_Numbers{$species}{$number}{$version},"\t",$species,"\t",$number,"\t",$version,"\t";
	    print FH $Tax_IDs{$species},"\t",$Names{$species},"\n";
	}
    }
}
close(FH);
