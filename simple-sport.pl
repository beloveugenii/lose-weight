#!/usr/bin/perl

# Simple-sport.pl

use strict;
use warnings;
use utf8;
use open qw / :std :utf8 /;
use Time::HiRes qw / time sleep /;
use Getopt::Long qw / GetOptions /;

require "./libsport.pm";

our $version = '0.0.2';

my ( $training );

# Создаем объект тренировок
$training = Training->new;

# Обработчики для внешних опций
sub handler { $training->set_option( @_ ) }
sub sound { 
    $training->set_option( 'sound', 1 );

    # Если мы в Termux и звук включен
    if ( $ENV{HOME} =~ /\/data.+/ ) {
        # Создаем объект и включаем звук
        my $termux = Termux->new;
        $termux->store;
        # Устанавливаем обработчик прерывания
        $SIG{INT} = \$termux->restore
    }
}

GetOptions (
    'repeats=i' => \&handler,
    'pause=s' => \&handler,
    'relax=s' => \&handler,
    'sound' => \&sound,
);


$training->add(grep -e $_, @ARGV);
$training->prepare;
$training->show_exercises;


# POD

=encoding utf8

=head1 NAME Simple-sport - simple sport assistant
Z<>

=head1 SYNOPSIS Usage: simple-sport [OPTIONS] [FILE]
Z<>

=head1 DESCRIPTION This program will help you to do sport everytime and everythere)
Z<>

=head1 TODO
Z<>

=cut

