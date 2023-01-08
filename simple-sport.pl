#!/usr/bin/perl

# Simple-sport.pl

use strict;
#use warnings;
use utf8;
use open qw / :std :utf8 /;

use Time::HiRes qw / time sleep /;
use Getopt::Long qw / GetOptions /;

use subs qw / prepare_termux mysplit /;

require "./libsport.pm";
require "./nums.pm";

# Prepared exercises blocks
my ( $prepare_f, $ending_f ) = qw ( tr/prepare tr/ending );

my $version = '0.0.5';

# Создаем объект тренировок
my $training = Training->new;

# Обработчики для внешних опций
sub handler { $training->set_option( @_ ) }

# Ссылки на функции для изменения состояния среды Termux
my ( $sound_on, $sound_off ) = prepare_termux;

# Если мы находимся в среде Termux
if ( $ENV{HOME} =~ /\/data.+/ ) {
    # Включаем звук
    &$sound_on if $training->get_option('sound');   
    # Устанавливаем обработчик прерывания
    $SIG{INT} = $sound_off
}

GetOptions (
    'repeats=i' => \&handler,
    'pause=s' => \&handler,
    'relax=s' => \&handler,
    'sound' => $sound_on,
    'h|help' => sub { system "perldoc $0"; exit 0 }, 
    'v|version' => sub { print "$version\n"; exit 0 },
);

my @files = grep -e $_, @ARGV;

# Разминка и заминка добавляются по умолчанию
unshift @files, $prepare_f if -e $prepare_f;
push @files, $ending_f if -e $ending_f;

$training->add(@files);
$training->prepare;

# Показываем стартовый экран, с программой упражнений и всеми данными
welcome( \@files );
#ПОКАЗАТЬ ДАННЫЕ О ПОДХОДАХ ПАУЗАХ И ТП
chomp ( my $entered = <STDIN> ); 
exit 0 if $entered eq 'q';

my @ex = $training->do;

for ( my $n = 0; $n <= $#ex; $n++ ) {
    # Если есть упражнение в этом индексе
    if ( $ex[$n] ) {
        # Получаем название и продолжительность текущего и
        # следующего упражнений
        my ( $c_name, $c_dur ) = mysplit( $ex[$n] );
        my ( $n_name, $n_dur ) = ( $ex[$n + 1] ) ? 
            mysplit( $ex[$n + 1] ) : ('Конец блока','');
        
            # Цикл выполнения самого упражнения
            for ( my $t = $c_dur; $t >= 0; $t-- ) {
                system 'clear';
                print "Текущее упражнение: $c_name $c_dur\n";
                print "\n" x 6;
                print_big_nums( $t );
                print "\n" x 6;
                print "\a" if ( $t < 2 || $t == int ( $c_dur / 2 ) );
                print "Следующее упражнение: $n_name $n_dur\n";
                sleep 1;
            }
            sleep 0.25;
    }
    else {
        # ПОКАЗАТЬ СТАТИСТИКУ
            last if $n == $#ex;
            print "Нажатие клавиши для перехода к следующему блоку";
            <STDIN>;
    }
}
&$sound_off;


# Вспомогательная функция для разделения полученного аргумента
# на две составляющие
sub mysplit { split /\s*:\s*|\s*(?:->)\s*/, $_[0] }

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
            system 'clear';
            exit 0
        }
}


# POD

=encoding utf8

=head3 NAME 

    Simple sport - very minimalistic sport assistant 

=head3 SYNOPSIS

    Usage: simple-sport [OPTIONS] [FILE]

=head3 DESCRIPTION 

    This program will help you to do sport everytime and everythere: the program reads the files transferred to it and makes a list of exercises from them. The duration of pauses between exercises and repetitions, as well as the number of repetitions can be passed to the program as options (see below).

    If no exercise files are transferred to the program, then warm-up and hitch files will be automatically started.  

=head3 OPTIONS

=over

=item help

show this help  

=item version 

show version of app  

=item sound 

enables sound in Termux  

=item repeats NUM

set repeats NUM  

=item pause VALUE

set pause between exerises at VALUE  

=item relax VALUE

set relax duration at VALUE  

=item You can set VALUE like 15s for 15 secons, or 15m for 15 minutes  

=back

=head3 FILE FORMAT

    The exercise file must be formatted in a certain way. It should contain lines like "exercise"->"duration". 
    The colon symbol ":" can also act as a separator. The margins don't matter.
    The duration of each exercise can be specified as a number or a number with a suffix. For example: "15m" and "40s".

