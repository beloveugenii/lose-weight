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

my $version = '0.0.4';

# Создаем объект тренировок
my $training = Training->new;

# Обработчики для внешних опций
sub handler { $training->set_option( @_ ) }

# Ссылки на функции для изменения состояния среды Termux
my ( $sound_on, $sound_off ) = prepare_termux;

# Если мы находимся в среде Termux
if ( $ENV{HOME} =~ /\/data.+/ ) {
    # Включаем звук
    &$sound_on;   
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

my @files = grep -e $_, @ARGV;
die "Usage:\n./simple-sport.pl [options] [files]\n" unless @files;

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
            mysplit( $ex[$n + 1] ) : ('Конец тренировки','');
        
            # Цикл выполнения самого упражнения
            for ( my $t = $c_dur; $t >= 0; $t-- ) {
                system 'clear';
                print "Текущее упражнение: $c_name $c_dur\n";
                print_big_nums( $t );
                print "Следующее упражнение: $n_name $n_dur\n";
                sleep 1;
            }
            sleep 0.25;
    }
    else {
        # ПОКАЗАТЬ СТАТИСТИКУ
            last if $n == $#ex;
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

