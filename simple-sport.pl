#!/usr/bin/perl

# Simple-sport.pl

use strict;
use warnings;
use utf8;
use open qw / :std :utf8 /;
use Time::HiRes qw / time sleep /;
use Getopt::Long qw / GetOptions /;

require "./libsport.pm";
require "./t_sound.pm";


our $version = '0.0.2';

# Создаем объект тренировок
my $training = Training->new;

# Обработчики для внешних опций
sub handler { $training->set_option( @_ ) }
sub sound { 
    # Если мы в Termux и звук включен
    if ( $ENV{HOME} =~ /\/data.+/ ) {
        # Создаем объект и включаем звук
        my $termux = T_sound->new;
        $termux->enable;
        # Устанавливаем обработчик прерывания
        $SIG{INT} = \$termux->restore
    }
}

GetOptions (
    'repeats=i' => \&handler,
    'pause=s' => \&handler,
    'relax=s' => \&handler,
    'sound' => \&sound,
    'v|version' => sub { print "$version\n" },
);


$training->add(grep -e $_, @ARGV);
$training->prepare;
$training->show_exercises;


# POD

=encoding utf8

=head1 NAME 

    Simple-sport - simple sport assistant

=head1 SYNOPSIS

    Usage: simple-sport [OPTIONS] [FILE]

=head1 DESCRIPTION 

    This program will help you to do sport everytime and everythere)

=head1 TODO



=cut

