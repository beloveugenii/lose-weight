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
        sound => 'disable',
    );

    sub new { 
        # Конструктор возвращает ссылку на объект класса Training
        bless \%data, $_[0] 
    }


    sub set_option {
        # Устанавливает параметру $_[1] значение $_[2]
        $data{$_[1]} = $_[2]
    }


    sub get_option {
        # Получаем значение конкретной опции
        $data{$_[1]}
    }

  sub get_options {
        # Выводит внутренние данные объекта
        print "$_=", $_[0]->get_option($_), "\n" foreach ( keys %data ) 
    }

    sub add {
        # Избавляемся от имени объекта в первом аргументе
        shift;

        # Хеш для хранения ссылок на содержимое файлов. 
        # Ключи - имена файлов
        my @files;
        
        # Читаем каждый файл в массив и записываем ссылку на него в хеш
        foreach ( @_ ) {
            open my $fh, '<', $_ or die "$!";
            chomp ( my @file = <$fh> );
            push @files, \@file; 
        }
        $data{list} = \@files
    } 

    sub prepare {
        # Избавляемся от имени класса в первом аргументе
        my @final;
        for ( my $file_index= 0; $file_index <= $#{$data{list}}; $file_index++ ) { 
            
            my @file = @{$data{list}[$file_index]};

            for ( my $repeat = 1; $repeat <= $data{repeats}; $repeat++ ) {

                push @final, "Prepare : " . $_[0]->get_option('pause') if $repeat == 1;

                
                for( my $ex = 0; $ex <= $#file; $ex++) {
                    push @final, "Pause : " . $_[0]->get_option('pause') unless $ex == 0;
                    push @final, $file[$ex];

                }
                push @final, "Time to relax : " . $_[0]->get_option('relax')  unless $repeat == $data{repeats};
            }    
        }
        $data{list} = \@final
    }

    sub show_exercises { 
        # Для каждой ссылки на файл с упражнениями
        foreach ( @{$data{list}} ) {
            if ( ref $_ ) {
            # Для каждого упражнения из файла
                foreach ( @$_ ) {
                    my ( $name, $duration ) = split /\s*:\s*|\s*(?:->)\s*/;
                    print "$name : $duration\n";
                }
            }
            else {
                #chomp;
                my ( $name, $duration ) = split /\s*:\s*|\s*(?:->)\s*/;
                print "$name : $duration";
            }
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

