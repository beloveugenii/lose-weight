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
        relax => '1m',
        between_repeats => '30s',
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

    sub set_stored_options {
        # Устанавливает параметры, прочитанные из файла
        open my $fh, '<', $_[1] or die;
        while ( <$fh> ) {
            chomp;
            # Параметры должны быть разделены символом '=' 
            $_[0]->set_option( split /\s*=\s*/ )
        }
    }

    sub store_options {
        # Сохраняет параметры в файле
        open my $fh, '>', $_[1] or die;
        print $fh "$_=", $_[0]->get_option($_), "\n" foreach ( keys %data )
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
        my %files;
        
        # Читаем каждый файл в массив и записываем ссылку на него в хеш
        foreach ( @_ ) {
            open my $fh, '<', $_ or die "$!";
            chomp ( my @file = <$fh> );
            $files{$_} = \@file;
        }
        $data{list} = \%files
    } 

    sub prepare {
        # Избавляемся от имени класса в первом аргументе
        shift;

    }

    sub show_exercises { 
        # Для каждой ссылки на файл с упражнениями
        foreach my $file ( keys %{$data{list}} ) {
            # Для каждого упражнения из файла
            print "Файл $file\n";
            foreach ( @{$data{list}{$file}} ) {
                    my ( $name, $duration ) = split /\s*:\s*|\s*(?:->)\s*/;
                    print "$name : $duration\n";
            }  
            print "\n"
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

