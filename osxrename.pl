#!/usr/bin/perl -w
#
# Simulate the 'rename' file utility
#

use strict;

my $usage = "usage: $0 FROM_SPEC TO_SPEC filespec1 filespec2 filespec3\n";
$usage .= "Example: $0 _ - *.txt *.log this_file.c\n\n";

my $specFrom = shift || die "[Missing FROM_SPEC.]\n\n$usage";
my $specTo = shift || die "[Missing TO_SPEC.]\n\n$usage";
if ($#ARGV <= 0){
die "[Missing filespec(s).]\n\n$usage";
}

while($#ARGV >= 0){
my $fileSource = shift;
my $fileTarget = $fileSource;
$fileTarget =~ s/$specFrom/$specTo/g;
next if ("$fileSource" eq "$fileTarget");
print "\t[Processing $fileSource => $fileTarget]\n";
if ( -e $fileTarget ){
print "\t\t[$fileTarget aleady exists. Skipping.]\n";
}
else{
rename $fileSource, $fileTarget;
}
}
