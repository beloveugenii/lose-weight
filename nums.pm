#!/usr/bin/perl

use strict;
use utf8;
use open qw / :std :utf8 /;
use Term::ReadKey; 

our $term_size = (Term::ReadKey::GetTerminalSize)[0];

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

# Стартовый экран
sub welcome {
    system 'clear'; 
    my $str = 'Simple sport';
    my $l = length($str);
    my $f = int ( $term_size - $l ) / 2;
    printf "%s%s%s\n", ' ' x $f, $str, ' ' x $f;
    printf "%s\n", '-' x $term_size;

    $str = 'Программа тренировки:';
    $l = length($str);
    $f = int ( $term_size - $l ) / 5;
    printf "%s%s\n", ' ' x $f, $_ foreach ( $str, @{$_[0]} );
}

sub print_big_nums {
    my $get_digits = sub {
    # Разбираем число на отдельные цифры
        ( $_[0] =~ /^(\d)(\d)(\d)$/ ) ? ( $1, $2, $3 ) :
        ( $_[0] =~ /^(\d)(\d)$/ ) ? ( 10, $1, $2 ) :
        ( $_[0] =~ /^(\d)$/ ) ? ( 10, 10, $1 ) : 0
    };

    my $f = int ( ($term_size - 27 ) / 4 );
    my ( $l, $c, $r ) = $get_digits->($_[0]);
        printf "%s%9s%s%9s%s%9s%s\n",
            " " x $f, $nums{$l}{$_},
            " " x $f,$nums{$c}->{$_}, 
            " " x $f, $nums{$r}->{$_}, 
            " " x $f foreach ( 1..8 );
    1
}
1;
