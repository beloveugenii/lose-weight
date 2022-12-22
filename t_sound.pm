#!/usr/bin/perl

use strict;
use utf8;
use open qw / :std :utf8 /;

{
    package T_sound;
    # Начало области видимости пакета Termux
    # Пакет создан для управления окружением Termux
    my $termux = "$ENV{HOME}/.termux/termux.properties";
   
    # Конструктор 
    sub new { bless \$termux, $_[0] }

    sub enable {
        # Задаем имя бэкап-файла
        my $backup = $termux . '.bak';

        # Проверяем, существует ли директория .termux
        mkdir "$ENV{HOME}/.termux" 
            unless ( -d "$ENV{HOME}/.termux" );

        # Делаем резервную копию оригинала
        rename $termux, $backup 
            or die "$!";

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
    # Конец области видимости пакета t_sound
}

1;
