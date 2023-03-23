#!/usr/bin/perl

use strict;
use feature 'say';

sub parse_files {
    my @files = @_;
    my %parsed_files;

    foreach my $file ( @files ) {

        # Validator
        if ( my $warn_code = ( ! -e $file ) ? -1 : ! (  $file =~ /\.ss$/ ) ? -2 : undef ) {
        
            my $warn_msg = ( $warn_code == -1 ) ? "'$file' not exist" :
                           ( $warn_code == -2 ) ? "'$file' is unsupported" :
                                                    'Unknown warning';

            open my $log, ">>", 'log';
            say $log $warn_msg;
            close $log;
            next
        }

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
            my @reserved_words = qw / name pause repeats relax on_end /;
            chomp $line;
            next if $line =~ /(?:^#+)|(?:^$)/;

            $line =~ /^(.+)(?::|(?:->))(.+)$/;

            ( grep { $1 eq $_} @reserved_words ) ? 
                $file{$1} = $2 : 
                push @{$file{aref}}, [ split /:|(?:->)/, $line ];
        }
        $parsed_files{$file} = \%file
    }

       
    \%parsed_files
    #%parsed_files = (
        #file1 => href1,
        #file2 => href2,
    #);
}

my $href = parse_files(@ARGV);

use Data::Dumper;

print Dumper $href;

