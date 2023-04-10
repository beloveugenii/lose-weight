#!/usr/bin/perl

# Simple-sport.pl

use strict;
use utf8;
use open qw / :std :utf8 /;

use FindBin qw / $Bin /;
use Time::HiRes qw / time sleep /;
use Getopt::Std;

use lib "$Bin";
require 'libsport.pm';
require 'nums.pm';
require "$Bin/../screen.pm";


#my $VERSION = '0.1.0';
#print "$VERSION\n";
#sub EMPTY_START_MESSAGE { die "No file set.\nUsage: simple-sport [OPTIONS] [FILE]\n" unless @{$_[0]} }




# Ссылки на функции для изменения состояния среды Termux
#my ( $sound_on, $sound_off ) = prepare_termux();
#$SIG{INT} = $sound_off;


## Если мы находимся в среде Termux
#if ( $ENV{HOME} =~ /\/data.+/ ) {
    # Включаем звук
    #&$sound_on;   
    # Устанавливаем обработчик прерывания
    #$SIG{INT} = $sound_off
#}



# Удаляем несуществующие файлы, и проверяем что хоть какие-то файлы остались
my @files = grep -e, @ARGV;
@ARGV = ();


## Показываем стартовый экран, с программой упражнений и всеми данными
#welcome( \@files );


##ПОКАЗАТЬ ДАННЫЕ О ПОДХОДАХ ПАУЗАХ И ТП
#chomp ( my $entered = <STDIN> ); 
#exit 0 if $entered eq 'q';








# Создаем объект тренировок куда передаем ссылку на массив с файлами
my $t = Training->new( \@files );

## Выключаем отображение курсора
print "\033[?25l";
print "\033[2J\033[H";

# Для каждого из файлов
foreach my $file( 0..$#files ) {
    # Получаем имя программы упражнений, количество повторов, продолжительность пауз
    my $name = $t->get_option($file, 'name');
    my $repeats = $t->get_option($file, 'repeats');

    # Для каждого повтора
    for (my $repeat = 1; $repeat <= $repeats; $repeat++ ) {
    
        # Получаем список упражнений со всеми паузами
        my $list = $t->prepare($file, $repeat);

        # Для каждого упражнения
        for ( my $index = 0; $index <= $#$list; $index++ )  {
            # Выводим названия упражнений и их продолжительность
            Screen->header("$name $repeat / $repeats");
        
            my ( $ex, $duration ) = (@{$list->[$index]});

            print "\nТекущее упражнение: $ex $duration\n" . "\n" x 6 . "\033[s" . "\n" x 12; 
            print "Следующее упражнение: @{$list->[$index + 1]}\n" if $list->[$index + 1];
            
            for (my $timer = $duration; $timer >= 0; $timer--, sleep 1 ) {
                # Перемещаем курсор в положение для печати цифр и выводим их
                print "\033[u";
                print_big_nums( $timer );
                # Звуковой сигнал
                print "\a" if ( $timer < 2 || $timer == int ( $duration / 2 ) );
            }
            # Очищаем экран между упражнениями
            print "\033[2J\033[H";
            sleep 0.25;
        }
    }

}
# Включаем отображение курсора в конце выполнения программы
print "\033[?25h";
 
#&$sound_off;


# Функция возвращает две анонимные фукнции.Одна включает в Termux звук. Другая возращает среду в исходное состояние
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
            print "\033[2J\033[H\033[?25h";
            exit 0
        }
}


# POD

=encoding utf8

=head3 NAME 

    Simple sport - minimalistic console  sport assistant 

=head3 SYNOPSIS

    Usage: simple-sport [OPTIONS] [FILE]

=head3 DESCRIPTION 

    This program will help you to do sport everytime and everythere: the program reads the files transferred to it and makes a list of exercises from them. The duration of pauses between exercises and repetitions, as well as the number of repetitions can be passed to the program as options (see below).

    If no exercise files are transferred to the program, then warm-up and hitch files will be automatically started.  

=head3 OPTIONS


    TODO 


=head3 FILE FORMAT

    In the new version, the exercise file contains all the necessary information to build a workout plan: the number of repetitions, time intervals and the set of exercises itself. 

    The execution time must be specified with a time modifier (s or m), the separator for the exercise is either a colon symbol or a small arrow ( -> ).

    The same principle is used to set parameters, but the separator is the equality symbol ( = ). If the parameter is set by a simple number, like the number of approaches, then the time modifier cannot be set. Parameters used: name, pause, relax, repiats, on_end.

    The grid symbol ( # ) is used to create comments.
