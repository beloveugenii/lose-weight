#!/usr/bin/perl

use strict;
use feature 'say';
use utf8;
use open qw / :std :utf8 /;
use lib qw ( home/eugeniibelov/Документы/my_learning/Perl/src/ );
require "../screen.pm";
my $screen = Screen->new;

my @reserved_words = qw / name repeats pause relax on_end aref /;
sub check_list {
    my @arr = @_;
    my @return_arr;
    foreach my $file ( @arr ){
        if ( my $warn_code = ( ! -e $file ) ? -1 : ! (  $file =~ /\.ss$/ ) ? -2 : undef ) {
        
            my $warn_msg = ( $warn_code == -1 ) ? "'$file' not exist" :
                           ( $warn_code == -2 ) ? "'$file' is unsupported" :
                                                    'Unknown warning';
            open my $log, ">>", 'log';
            say $log $warn_msg;
            close $log;
            next
        }
        push @return_arr, $file
    }
    @return_arr
}



sub parse_files {
    my @files = @_;
    my @parsed_files;

    foreach my $file ( @files ) {

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
                $file{$1} = $2 : 
                push @{$file{aref}}, [ split /:|(?:->)/, $line ];
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

my $aref = parse_files( check_list( @ARGV ) );


$screen->header('Simple-sport');
$screen->message(undef,$str->($aref));
$screen->menu( qw / start quit /);
