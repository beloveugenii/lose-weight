#!/usr/bin/perl

use strict;
use FindBin qw / $Bin /;
use feature 'say';
use utf8;
use open qw / :std :utf8 /;
use lib "$Bin";
require "$Bin/../screen.pm";
require "$Bin/libss.pm";
my $screen = Screen->new;

my @reserved_words = qw / name repeats pause relax on_end aref /;



sub parse_files {

    my $files_ref = shift;
    my @parsed_files;

    foreach my $file ( @$files_ref ) {

        open my $fh, "<", $file or die "'$file': $!";
        my %file;
        #%file = (
            #param1 => str, 
            #param2 => str, 
            #paramN => str, 
            #aref=> [
                #[ ex1, dur1, ], 
                #[ ex2, dur2, ], 
                #[ exN, durN ],
            #],
        #);
    
        # Parser
        while ( my $line = <$fh> ) {
            chomp $line;
            next if $line =~ /(?:^#+)|(?:^$)/;

            $line =~ /^(.+)(?::|(?:->))(.+)$/;

            ( grep { $1 eq $_} @reserved_words ) ? 
            ###!!!!!!!!!!!!1
            #
            #    КАК ОТЛИЧАЕТСЯ СТРОКА С ПАРАМЕТРОМ И СТРОКА С УПРАЖНЕНИЕМ?????
            #
            ##
                    $file{$1} = to_sec($2) :
                    push @{$file{aref}}, [ $1, to_sec($2) ];
            
        }
        push @parsed_files, \%file
    }

       
    \@parsed_files
    #@parsed_files = (
        #href1,
        #href2,
    #);
}


my $str = sub {
    my $out_str;
    foreach my $href ( @{$_[0]} ) {
        my $name = ( $href->{name} =~ /^['"](.+)['"]$/ ) ? $1 : $href->{name};
        my $duration;
        $duration += $_->[1] foreach @{$href->{aref}};
        $out_str .= "$name: " . int ( $duration / 60 ) . 'm ' . $duration % 60 . "s\n";
    }
    $out_str
};

my $aref = parse_files (check_list( \@ARGV )) ;


for my $key ( keys %{$aref->[0]} ) {

say "$key = $aref->[0]{$key}";

}

