#!/usr/bin/perl

use strict;
use utf8;
use open qw / :std :utf8 /;
use FindBin qw / $Bin /;
use Time::HiRes qw / time sleep /;
use Getopt::Std;
use lib "$Bin";
require "libsport.pm";
use libsui;

our $NAME = 'simple-sport.pl';
our $VERSION = '0.1.3';
my $in_termux = 1 if $ENV{HOME} =~ /\/data.+/; 
my $statistic = {};
my %nums = ( 
        0 => { 1=>"#########", 2=>"#########", 3=>"###   ###", 4=>"###   ###", 5=>"###   ###", 6=>"###   ###", 7=>"#########", 8=>"#########", },
        1 => { 1 => "    ###  ", 2=>"    ###  ", 3=>"    ###  ", 4=>"    ###  ", 5=>"    ###  ", 6=>"    ###  ", 7=>"    ###  ", 8=>"    ###  " }, 
        2  => { 1=>"#########", 2=>"#########", 3=>"      ###", 4=>"#########", 5=>"#########", 6=>"###      ", 7=>"#########", 8=>"#########", },
        3  => { 1=>"#########", 2=>"#########", 3=>"      ###", 4=>"  #######", 5=>"  #######", 6=>"      ###", 7=>"#########", 8=>"#########", },
        4 => { 1=>"###   ###", 2=>"###   ###", 3=>"###   ###", 4=>"#########", 5=>"#########", 6=>"      ###", 7=>"      ###", 8=>"      ###", },
        5 => { 1=>"#########", 2=>"#########", 3=>"###      ", 4=>"#########", 5=>"#########", 6=>"      ###", 7=>"#########", 8=>"#########", },
        6 => { 1=>"#########", 2=>"#########", 3=>"###      ", 4=>"#########", 5=>"#########", 6=>"###   ###", 7=>"#########", 8=>"#########", },
        7 => { 1=>"#########", 2=>"#########", 3=>"      ###", 4=>"      ###", 5=>"      ###", 6=>"      ###", 7=>"      ###", 8=>"      ###", },
        8 => { 1=>"#########", 2=>"#########", 3=>"###   ###", 4=>"#########", 5=>"#########", 6=>"###   ###", 7=>"#########", 8=>"#########", },
        9 => { 1=>"#########", 2=>"#########", 3=>"###   ###", 4=>"#########", 5=>"#########", 6=>"      ###", 7=>"#########", 8=>"#########", },
        10 => { 1=>"         ", 2=>"         ", 3=>"         ", 4=>"         ", 5=>"         ", 6=>"         ", 7=>"         ", 8=>"         ", },
    );

# Command-line keys
our ( $opt_h, $opt_v, $opt_s, $opt_t);

# Check command-line options and handle it 
getopts( 'vhst' );
help() if $opt_h;
version() if $opt_v;
timer( $ARGV[0] ) if $opt_t;

# Remove bad files and handle empty start
@ARGV = grep -e, @ARGV;
empty_start() unless @ARGV;

# In Termux sound handler
if ( $in_termux && $opt_s ) {
    my $termux_config = "$ENV{HOME}/.termux/termux.properties";
    my $backup = $termux_config . '.bak';

    # Enable Termux beep
    rename $termux_config, $backup or die "$!";
    open my $new_file, '>', $termux_config;
    open my $old_file, '<', $backup;
    while ( <$old_file> ) {
        s/#(.+\s)(beep)/$1$2/;
        print $new_file $_
    }
    system 'termux-reload-settings';
    print "\a";

    # Set SIGINT for Termux
    $SIG{INT} = sub {
        rename $backup, $termux_config if -e $backup;
        system 'termux-reload-settings';
        print "\033[2J\033[H\033[?25h\n";
        show_statistic($statistic);
        <STDIN>;
        exit 0
    };
}
else {
    # Set SIGINT NOT for Termux
    $SIG{INT} = sub { 
        print "\033[2J\033[H\033[?25h\n";
        show_statistic($statistic);
        <STDIN>;
        exit 0
    };
}



# Constract training list
my $t = Training->new( \@ARGV );

while ( 1 ) {
    # Start screen with training program
    screen('Программа тренировки', 
            sub { 
                my $program;
                foreach my $index ( 0..$#ARGV ) {
                    $program->[$index][0] = $program->[$index][0] = $t->get_option($index, 'name');
                    {
                        use integer;
                        $program->[$index][1] += $_->[1] foreach ( @{$t->get_option($index, 'data')});

                        $program->[$index][1] *= $t->get_option($index, 'repeats');

                        $program->[$index][1] = sprintf '%sm %ss', $program->[$index][1] / 60, $program->[$index][1] % 60;
                    }
                }

                print_as_table($program, ' ');
            }, 
            ( 'start training', 'create new training', 'quit' ), 2 );

    my $choice = promt('>>');

    if ( $choice =~ /^q$/i ){
        exit 0
    }
    elsif ( $choice =~ /^s$/i ) {
        sleep 1;
        last
    }
    elsif ( $choice =~ /^c$/i ) {
        print "Not implemented yet\n";
        sleep 1;
    }

    else {
        print "Unsupported action\n";
        sleep 1
    }
}

# hide the cursor and clears the screen
print "\033[?25l";
clear();

foreach my $file_index ( 0..$#ARGV ) {
    
    # For each file gets training name, repeats count and pauses duration
    my $name = $t->get_option($file_index, 'name');
    my $repeats = $t->get_option($file_index, 'repeats');

    for (my $repeat = 1; $repeat <= $repeats; $repeat++ ) {

        # For each repeat gets training list with pauses
        my $list = $t->prepare($file_index, $repeat);

        for ( my $index = 0; $index <= $#$list; $index++ )  {

            my ( $ex, $duration ) = (@{$list->[$index]});
            header( "$name $repeat / $repeats" );

            # Prints title and duration for each exercise and name of next exercise
            print "\nТекущее упражнение: $ex $duration\n" . "\n" x 6 . "\033[s" . "\n" x 14;
            print "Следующее упражнение: @{$list->[$index + 1]}\n" if $list->[$index + 1];

            for ( my $timer = $duration; $timer >= 0; $timer-- ) {
                
                # Move hide cursor to the position and prints big digits
                print "\033[u";
                
                # Sound signal if enabled
                print "\a" if ( $timer < 3 || $timer == int ( $duration / 2 ) );
                $statistic->{$ex}++ if $timer != 0;

                print_big_nums( $timer );
                sleep 1;
            }
            # lears the screen
            clear();
            sleep 0.25;
        }
    }

}

$SIG{INT}();

sub show_statistic {
    # This subroutine get statistic hashref
    # Prints statistic in a convenient form
    my $hashref = shift;
    my $total = 0;
    clear();
    header('Статистика тренировки');
    use integer;
    while ( my ($ex, $dur) = each %$hashref ) {
        next if $ex eq 'Пауза' ||
                $ex eq 'Конец тренировки' || 
                $ex eq 'Время отдохнуть' || 
                $ex eq 'Приготовьтесь';
                $total += $dur;
                $dur =  ( $dur >= 60 ) ? sprintf "%sм %sс", $dur / 60, $dur % 60 : sprintf "%sс", $dur;
        print "$ex: $dur\n" 
    }
    my ( $h, $m ,$s ) = ( $total / 3600, $total / 60, $total % 60 );
    ( $h ) ? printf "\nОбщее время: %sч %sм %sс\n", $h, $m, $s : printf "\nОбщее время: %sм %sс\n", $m, $s;
}

sub print_big_nums {
    # This subroutine get number and prints big digits of it
    my $digit = shift;
    my ( $l, $c, $r ) = ($digit =~ /^(\d)(\d)(\d)$/ ) ? ( $1, $2, $3 ) :
                        ( $digit =~ /^(\d)(\d)$/ ) ? ( 10, $1, $2 ) :
                        ( $digit =~ /^(\d)$/ ) ? ( 10, 10, $1 ) : ( 10, 10, 10 );

    print_as_table([[$nums{$l}{$_}, $nums{$c}{$_}, $nums{$r}{$_}]], ' ') foreach (1..8);    
}



# Command line options handlers
# Show help handler
sub help { exec "perldoc $NAME" }

# Show version handler
sub version { die "$NAME\n$VERSION\n" }

sub empty_start { 
    # Fileless startup handler
    die "No file set.\nUsage: simple-sport [OPTIONS] [FILE]\n" 
}

sub timer {
    # This subroutine is a Timer mode handler
    # Get the name of the exercise from the command line
    use Encode;
    my $ex = decode( 'utf8', shift );
    
    # hide the cursor 
    print "\033[?25l";
    
    # timing
    for ( my $timer = 0, $SIG{INT} = sub { print "\033[?25h\n" . "\n" x 8; <STDIN>; exit 0 }; ; $timer ++ ) {
        clear();
        header( 'Таймер' );
        print "\nТекущее упражнение: $ex\n" . "\n" x 6 . "\033[s" . "\n" x 14 . "\033[u"; 
        print_big_nums( $timer );
        print "\033[u";
        sleep(1)
    }
}

# POD

=encoding utf8

=head3 Name

Simple-sport - minimalistic console sport assistant

=head3 Synopsis

Usage: simple-sport [OPTIONS] [FILE]

=head3 Description

This program will help you to do sport everytime and everythere: the program reads the files transferred to it and makes a list of exercises from them. The duration of pauses between exercises and repetitions, as well as the number of repetitions can be passed to the program as options (see below).

=head3 Options

    -s enables a sound alarm when executinag
    -t [exercise] make timer on
    -v show version of app
    -h show embedded help

=head3 File format

In the new version, the exercise file contains all the necessary data to build a workout plan: the number of repeats, time intervals and the set of exercises itself.

The grid symbol ( # ) is used to create comments, empty lines will skip.

The execution time must be specified with a time modifier (s or m), the separator for the exercises is either a colon symbol ( : ) or a small arrow ( -E<gt> ).

The same principle is used to set parameters, but the separator is the equality symbol ( = ). If the parameter is set by a simple number, like the number of approaches, then the time modifier cannot be set.

=head3 Example

    name='Warm-up'
    pause=5s
    relax=0s
    repiats=1
    on\_end=10s

    ex1:30s
    ex2->0.5m
    ex3->40s
    ex5:1m

