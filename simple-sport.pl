#!/usr/bin/perl

# Simple-sport.pl

use strict;
use warnings;
use utf8;
use open qw / :std :utf8 /;
use Time::HiRes qw / time sleep /;
use Getopt::Long qw / GetOptions /;
use subs qw / prepare_termux /;

require "./libsport.pm";

my $version = '0.0.2';

# Создаем объект тренировок
my $training = Training->new;

# Обработчики для внешних опций
sub handler { $training->set_option( @_ ) }

my ( $sound_on, $sound_off );

# Если мы находимся в среде Termux
if ( $ENV{HOME} =~ /\/data.+/ ) {
    ( $sound_on, $sound_off ) = prepare_termux;
    
    # Устанавливаем обработчик прерывания
    $SIG{INT} = $sound_off
}

GetOptions (
    'repeats=i' => \&handler,
    'pause=s' => \&handler,
    'relax=s' => \&handler,
    'sound' => $sound_on,
    'v|version' => sub { print "$version\n" },
);


$training->add(grep -e $_, @ARGV);
$training->prepare;
$training->show_exercises;
<STDIN>;

&$sound_off;




# Функция возвращает две анонимные фукнции
# Одна включает в Termux звук
# Другая возращает среду в исходное состояние
sub prepare_termux {
    my $termux = "$ENV{HOME}/.termux/termux.properties";
    my $backup = $termux . '.bak';
    return 
        sub {
            rename $termux, $backup or die "$!";
            open my $new_file, '>', $termux;
            open my $old_file, '<', $backup;
            # Читаем файл резервной копии и одновременно записываем данные оттуда в новый файл. 
            # Когда будет найдена строка с 'beep' она будет изменена и записана в новом виде
            while ( <$old_file> ) {
                s/#(.+\s)(beep)/$1$2/;
                print $new_file $_
            }
            # Перезагружаем настройки Termux и подаем звуковой сигнал
            system 'termux-reload-settings';
            print "\a"
        },
        sub {
            rename $backup, $termux if -e $backup;
            system 'termux-reload-settings';
            exit 0
        }
}


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

