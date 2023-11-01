#!/usr/bin/perl

use strict;
use utf8;
use open qw / :std :utf8 /;
use FindBin qw / $Bin /;
use Time::HiRes qw / time sleep /;
use Getopt::Std;
use lib "$Bin";
require "libsassist.pm";
use libsui;

our $NAME = 's_assist.pl';
our $VERSION = '0.1.4a';
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
our ( $opt_h, $opt_v, $opt_s, $opt_t, $opt_i);

# Check command-line options and handle it 
getopts( 'vhsti' );
help() if $opt_h;
version() if $opt_v;
timer( $ARGV[0] ) if $opt_t;
@ARGV = interactive() if $opt_i;


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


# Construct training list
my $t = Training->new( \@ARGV );

while ( 1 ) {
    # Start screen with training program
    screen('Программа тренировки', 
            sub { 
                my $program;
                foreach my $index ( 0..$#ARGV ) {
                    $program->[$index][0] = $program->[$index][0] = $t->get_option($index, 'name');
                    {
                        $program->[$index][1] += $_->[1] foreach ( @{$t->get_option($index, 'data')});

                        $program->[$index][1] *= $t->get_option($index, 'repeats');

                        $program->[$index][1] = sec_to_hours($program->[$index][1]);
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
                #$statistic->{$ex}++ if $timer != 0;

                print_big_nums( $timer );
                sleep 1;
            }

            $statistic->{$ex} += $duration;
            
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
    while ( my ($ex, $dur) = each %$hashref ) {
        next if $ex eq 'Пауза' ||
                $ex eq 'Конец тренировки' || 
                $ex eq 'Время отдохнуть' || 
                $ex eq 'Приготовьтесь';
        $total += $dur;
        print "$ex: " . sec_to_hours($dur) . "\n"; 
    }

    print "\nОбщее время: " . sec_to_hours($total) . "\n";
}

sub sec_to_hours {
    my ( $timer, $h, $m, $s ) = ( shift, undef, undef, undef );

    use integer;
    
    while ($timer >= 3600) {
        $h++;
        $timer -= 3600; 
    }

    ( $m, $s ) = ( $timer / 60, $timer % 60 );

    ( $h ) ? sprintf "%dч %dм %dс", $h, $m, $s : 
             sprintf "%dм %dс", $m, $s;

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

sub interactive {
    # Interactive mode handler
    # It enables then program starts from parent process with '-i' option
    clear();
    header('Выберите упражнения');

    my ($num, $tmp) = (1, []);
    my @files = glob "./basics/*";

    foreach my $file ( @files ) {
        my ( $name ) = ( '' );
        open my $fh, "<", $file;
        
        while (<$fh>){
            if ( /^name=(.+)/ ) {
                $name = $1;
            }
            last if $name;
        }
        
        close $fh;
        push @$tmp, ['[' . $num++ . ']', $name];
    }

    print_as_table($tmp, ' ');
    @$tmp = ();
    line();

    my @nums;
    while ( ! @nums ) {
        my $i = promt('>>');
        exit 0 if $i =~ /.*q.*/i;

        @nums = split ' ', $i; 
    }

    push @$tmp, $files[$_ - 1] foreach ( @nums );
    @$tmp
}


# POD

=encoding utf8

=head3 Name

s_assist - minimalistic console sport assistant. It is part of fcracher


=head3 Synopsis

Usage: ./s_assist.pl [OPTIONS] [FILE]


=head3 Description

The sports assistant allows you to create training programs and carry them out according to a timer. For creating new training file you can use every text editor you like. See *File format* section below.


=head3 Options

    -s enables a sound alarm when executinag
    -t [exercise] make timer on
    -v show version of app
    -h show embedded help
    -i interactive file choosing


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

