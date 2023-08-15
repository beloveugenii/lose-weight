#!/usr/bin/perl

use strict;
use utf8;
use open qw / :std :utf8 /;

our $NAME = 'simple-sport.pl';
our $VERSION = '0.1.0';

use FindBin qw / $Bin /;
use Time::HiRes qw / time sleep /;

use Getopt::Std;

# Ключи для аргументов КС
our ( $opt_h, $opt_v, $opt_s );

# Обработчики аргументов КС
sub help { system "perldoc $NAME"; exit 0 }
sub version { die "$NAME\n$VERSION\n"; exit 0 }
sub empty_start { die "No file set.\nUsage: simple-sport [OPTIONS] [FILE]\n" }


use lib "$Bin";
require 'libsport.pm';
require "screen.pm";

# Проверяем параметры КС и обрабатываем их
getopts('vhs');
help() if $opt_h;
version() if $opt_v;

# Удаляем несуществующие файлы, и проверяем что хоть какие-то файлы остались
@ARGV = grep -e, @ARGV;
empty_start() unless @ARGV;

# Ссылки на функции для изменения состояния среды Termux
my ( $sound_on, $sound_off ) = prepare_termux();
# Устанавливаем обработчик прерывания
$SIG{INT} = $sound_off;

# Если мы находимся в среде Termux
if ( $ENV{HOME} =~ /\/data.+/ && $opt_s) {
    # Включаем звук
    &$sound_on;   
}

# Создаем объект тренировок куда передаем ссылку на массив с файлами
my $t = Training->new( \@ARGV );

## Показываем стартовый экран, с программой упражнений и всеми данными
Screen->header('Simple sport', [ grep {$_ = $t->get_option($_, 'name')} 0..$#ARGV ] );



##ПОКАЗАТЬ ДАННЫЕ О ПОДХОДАХ ПАУЗАХ И ТП
chomp ( my $entered = <STDIN> ); 
exit 0 if $entered eq 'q';


## Выключаем отображение курсора
print "\033[?25l";
Screen->clear;

# Для каждого из файлов
foreach my $file_index ( 0..$#ARGV ) {
    # Получаем имя программы упражнений, количество повторов, продолжительность пауз
    my $name = $t->get_option($file_index, 'name');
    my $repeats = $t->get_option($file_index, 'repeats');

    # Для каждого повтора
    for (my $repeat = 1; $repeat <= $repeats; $repeat++ ) {
    
        # Получаем список упражнений со всеми паузами
        my $list = $t->prepare($file_index, $repeat);

        # Для каждого упражнения
        for ( my $index = 0; $index <= $#$list; $index++ )  {
            # Выводим названия упражнений и их продолжительность
            Screen->header( "$name $repeat / $repeats" );
        
            my ( $ex, $duration ) = (@{$list->[$index]});

            print "\nТекущее упражнение: $ex $duration\n" . "\n" x 6 . "\033[s" . "\n" x 12; 
            print "Следующее упражнение: @{$list->[$index + 1]}\n" if $list->[$index + 1];
            
            for (my $timer = $duration; $timer >= 0; $timer--, sleep 1 ) {
                # Перемещаем курсор в положение для печати цифр и выводим их
                print "\033[u";
                # Звуковой сигнал
                print "\a" if ( $timer < 3 || $timer == int ( $duration / 2 ) );
                Screen->print_big_nums( $timer );
            }
            # Очищаем экран между упражнениями
            Screen->clear;
            sleep 0.25;
        }
    }

}
# Включаем отображение курсора в конце выполнения программы
print "\033[?25h";
 
&$sound_off;

sub prepare_termux {
    # Функция возвращает две анонимные фукнции.
    # Одна включает в Termux звук. Другая возращает среду в исходное состояние
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
            print "\033[2J\033[H\033[?25h";
            exit 0
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

