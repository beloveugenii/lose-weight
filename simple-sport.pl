#!/usr/bin/perl

# Simple-sport.pl

use strict;
use warnings;
use utf8;
use open qw / :std :utf8 /;
use Time::HiRes qw / time sleep /;
use Getopt::Long qw / GetOptions /;

require "./libsport.pm";

our $version = '0.0.1';

## ДОПОЛНИТЕЛЬНЫЕ ПЕРЕМЕННЫЕ ДЛЯ ВНЕШНИХ КЛЮЧЕЙ
my ( $training, $termux );

# Создаем объект тренировок
$training = Training->new;

## ОБРАБОТКА ВНЕШНИХ КЛЮЧЕЙ КС

# Если мы в Termux и звук включен
if ( $ENV{HOME} =~ /\/data.+/ &&
         $training->get_option( 'sound' ) eq 'enable' ) {
    
    # Создаем объект и включаем звук
    $termux = Termux->new;
    $termux->store;
    # Устанавливаем обработчик прерывания
    $SIG{INT} = \$termux->restore;
}

$training->add( grep -r $_, @ARGV );
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

