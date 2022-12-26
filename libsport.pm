#!/usr/bin/perl

use strict;
use utf8;
use open qw / :std :utf8 /;

{
    # Начало области видимости пакета Training
    package Training;
    
    # Данные каждого экземпляра класса
    my %data = ( 
        list => '', 
        repeats => '3',
        pause => '10s',
        relax => '60s',
    );

    # Конструктор возвращает ссылку на объект класса Training
    sub new { bless \%data, $_[0] }

    # Устанавливает параметру $_[1] значение $_[2]
    sub set_option { $data{$_[1]} = $_[2] }

    # Получаем значение конкретной опции
    sub get_option { $data{$_[1]} }

    # Возвращает массив с упражнениями
    sub do { @{$data{list}} }

    # Выводит внутренние данные объекта
    sub show_options { print "$_=", $_[0]->get_option($_), "\n" foreach ( keys %data ) }

    # Создает ссылку на массив со всеми упражненими
    sub add {
        # Избавляемся от аргумента - имени класса
        shift;
        my @files;
        
        foreach ( @_ ) {
            open my $fh, '<', $_ or die "$!";
            my @file;
            foreach ( <$fh> ) {
                chomp;
                next if /^#\s*|^\s*$/;
                push @file, $_;
            }
            push @files, \@file; 
        }
        $data{list} = \@files
    } 
    
    # Выводит список упражнений как в изначальном виде, так и в подготовленном
    sub show_exercises { 
        my $view = sub { 
            foreach ( @_ ) {
                my ( $name, $duration ) = split /\s*:\s*|\s*(?:->)\s*/;
                return "$name: $duration"
            }
        };
        
        ( ref $_ ) ? print $view->(@$_), "\n" : 
                     print $view->($_), "\n" 
                        foreach ( @{$data{list}} );
    } 

    # Расширяет массив с упражнениями таким образом, чтобы учитывались количество подходов, паузы между упражнениями и подходами
    sub prepare {
        # Константные строки
        my $prepare_str = "Приговься : " . $_[0]->get_option('pause');
        my $pause_str = "Пауза : " . $_[0]->get_option('pause');
        my $relax_str = "Время отдохнуть : " . $_[0]->get_option('relax');
        
        # Подфункция, преобразующая время в секунды
        # Возвращает строку, где первое значени - название, 
        # второе - время, приведенное в секунды
        my $conv = sub {
            my ( $name, $duration ) = split /\s*:\s*|\s*(?:->)\s*/, $_[0];
            my ( $num, $mod ) = $duration =~ /(\d+(?:\.\d)*)([ms]*)/;
            $num *= ( $mod eq 'm' ) ? 60 : 1;
            return "$name : $num"
        };

        my @final;

        for ( my $f_index = 0; $f_index <= $#{$data{list}}; $f_index++ ) { 
            my @file = @{$data{list}[$f_index]};

            for ( my $repeat = 1; $repeat <= $data{repeats}; $repeat++ ) {
                push @final, $conv->( $prepare_str ) if $repeat == 1;

                for( my $ex = 0; $ex <= $#file; $ex++) {
                    push @final, $conv->( $pause_str ) 
                        unless $ex == 0;
                    push @final, $conv->( $file[$ex] );
                }
                push @final, $conv->( $relax_str ) 
                    unless $repeat == $data{repeats};
            }    
            push @final, ""
        }
        # Перезаписываем в хеш под ключом 'list' ссылку на новый список
        # который включает все упражнения в нужно количестве, разделенные паузами
        # Перерывы между файлами определяются стркой ':'
         $data{list} = \@final
    }


# Конец области видимости пакета Training
}

1;
