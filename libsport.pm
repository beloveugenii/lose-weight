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
        relax => '30s',
        sound => 0,
    );

    # Конструктор возвращает ссылку на объект класса Training
    sub new { bless \%data, $_[0] }

    # Устанавливает параметру $_[1] значение $_[2]
    sub set_option { $data{$_[1]} = $_[2] }

    # Получаем значение конкретной опции
    sub get_option { $data{$_[1]} }

    # Выводит внутренние данные объекта
    sub show_options { print "$_=", $_[0]->get_option($_), "\n" foreach ( keys %data ) }

    # Создает ссылку на массив со всеми упражненими
    sub add {
        shift;
        my @files;
        
        foreach ( @_ ) {
            open my $fh, '<', $_ or die "$!";
            chomp ( my @file = <$fh> );
            push @files, \@file; 
        }
        $data{list} = \@files
    } 

    # Расширяет массив с упражнениями таким образом, чтобы учитывались количество подхходов, паузы между упражнениями и подходами
    sub prepare {
        my @final;
        for ( 
            my $file_index = 0;
            $file_index <= $#{$data{list}}; 
            $file_index++ ) { 
            
            my @file = @{$data{list}[$file_index]};

            for ( my $repeat = 1; $repeat <= $data{repeats}; $repeat++ ) {

                push @final, "Prepare : " . $_[0]->get_option('pause') if $repeat == 1;

                
                for( my $ex = 0; $ex <= $#file; $ex++) {
                    push @final, "Pause : " . $_[0]->get_option('pause') unless $ex == 0;
                    push @final, $file[$ex];

                }
                push @final, "Time to relax : " . $_[0]->get_option('relax')  unless $repeat == $data{repeats};
            }    
            push @final, ""
        }
        $data{list} = \@final
    }

    # Выводит список упражнений как в изначальном виде, так и в подготовленном
    sub show_exercises { 
            my $view = sub { 
            foreach ( @_ ) {
                my ( $name, $duration ) = split /\s*:\s*|\s*(?:->)\s*/;
                return "$name:$duration"
            }
        };

        foreach ( @{$data{list}} ) {
                    (ref $_)  ? 
                    print $view->(@$_):
                    print $view->($_);
                    print "\n";
        }
        } 
    
# Конец области видимости пакета Training
}


{
    package Termux;
    # Начало области видимости пакета Termux
    # Пакет создан для управления окружением Termux
    my $termux = "$ENV{HOME}/.termux/termux.properties";
   
    # Конструктор 
    sub new { bless \$termux, $_[0] }

    sub store {
        # Задаем имя бэкап-файла
        my $backup = $termux . '.bak';

        # Проверяем, существует ли директория .termux
        mkdir "$ENV{HOME}/.termux" unless ( -d "$ENV{HOME}/.termux" );

        # Делаем резервную копию оригинала
        rename $termux, $backup or die "$!";

        open my $new_file, '>', $termux;
        open my $old_file, '<', $backup;
        # Читаем файл резервной копии и одновременно записываем данные оттуда в новый файл. Когда будет найдена строка с 'beep' она будет изменена и записана в новом виде
        while ( <$old_file> ) {
            s/#(.+\s)(beep)/\1\2/;
            print $new_file $_
        }

        # Перезагружаем настройки Termux и подаем звуковой сигнал
        system 'termux-reload-settings';
        print "\a"
    }

    sub restore {
        # При остановке выполнения возвращает среду Termux в изначальное состояние
        my $backup = $termux . '.bak';
        rename $backup, $termux if -e $backup or die "$!";
        system 'termux-reload-settings';
        exit 0
    }
    # Конец области видимости пакета Termux
}

# Функции общего назначения

