#!/usr/bin/perl

use strict;
use FindBin qw / $Bin /;
use Time::HiRes qw / time sleep /;
use feature 'say';
use utf8;
use open qw / :std :utf8 /;
use lib "$Bin";
require "$Bin/../screen.pm";
require "$Bin/libss.pm";

my $aref = parse_files (check_list( \@ARGV )) ;


foreach my $training ( @$aref ) {
    # Для каждого элемента из массива с файлами упражнений
    my ($pause, $relax, $repeats, $name) = ( $training->{pause}, $training->{relax}, $training->{repeats}, $training->{name});

    # Для каждого повтора
    for ( my $repeat_number = 1; $repeat_number <= $repeats; $repeat_number++ ) {

        Screen->header("$name: $repeat_number / $repeats");

        for ( my $ex_number = 0; $ex_number <= $#{$training->{aref}}; $ex_number++ ) {

            #### ТЕПЕРЬ КАЖДУЮ СТРОКУ НУЖНО РАЗБИТЬ НА НАЗВАНИЕ И ВРЕМЯ ВЫПОЛНЕНИЯ


            say "Приготовься $pause" if $ex_number == 0 && $repeat_number == 1;
            say "@{$training->{aref}->[$ex_number]}";
            say "Пауза $pause" unless $ex_number == $#{$training->{aref}};
            say "Время отдохнуть $relax" if $ex_number == $#{$training->{aref}} && $repeat_number != $repeats;
        
        }

        say "Конец тренировки" if $repeat_number == $repeats;
        say
    }

}

