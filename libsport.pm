#!/usr/bin/perl

use strict;
use utf8;
use open qw / :std :utf8 /;

{
    ## Начало области видимости пакета Training
    package Training;
    
    # Преобразует переданное значение в секунды
    sub to_sec { ( $_[1] =~ /([\d.]+)\s?[mM]$/ ) ? return $1 * 60 : ( $_[1] =~ /([\d.]+)[sS]?$/ ) ? return $1 : undef }
    
    ## Для переданного индекса в массиве(1) получаем значение переданной опции(2)
    sub get_option { $_[0]->[$_[1]]->{$_[2]} }

    # Конструктор экземпляра класса получает ссылку на список файлов
    # Возвращает ссылку на объект-массив
    sub new {  
        my ( $class, $files_ref ) = @_;
    
        # Массив с разобранными файлами
        my @parsed_files;

        # Для каждого файла из переданных
        foreach my $file ( @$files_ref ) {
            # Открываем файл для чтения
            open my $fh, "<", $file or die "'$file': $!";
            my %file;
            # Структура данных каждого файл
            # %file = (
                # param1 => str, 
                # param2 => str, 
                # paramN => str, 
                # data=> [
                    # [ ex1, dur1, ], 
                    # [ ex2, dur2, ],
                    # [ exN, durN, ],
                # ],
            # );
    
            # Parser
            while ( <$fh> ) {
                # читаем файл построчно
                chomp;
                # пропускаем строку, если она пуста, или это комментарий
                next if /(?:^#+)|(?:^$)/;
            
                # Если разделитель двоеточие или ->, то это упражнение, а вторая часть - время
                if ( /^(.+)(?::|(?:->))(.+)$/ ) {
                    # Перевести последнюю часть в секунды и вставить как анонимный массив в хеш
                    push @{$file{data}}, [ $1, $class->to_sec($2) ]
                }
                # Если разделитель символ равно, то это параметр
                elsif ( /^(.+)=(.+)$/) {
                    my ( $name, $val ) = ( $1, $2 );
                    $file{$name} = $val =~ /^([\d.]+[smM])$/ ? $class->to_sec($1) : $val;
                }
            }
            # вносит ссылку на хеш с данными из файла в список разобранных файлов 
            push @parsed_files, \%file
        }
        # Создаем экземпляр класса и возвращаем ссылку на него
        bless \@parsed_files, $class
    }

    # Метод получает имя файла с упражнениями и номер текущего подхода
    # Возвращает ссылку на массив со всеми внесенными перерывами
    sub prepare {
        my ( $class, $file, $repeat ) = ( shift, shift, shift );
        my $list = $class->get_option($file, 'data');
        my $repeats = $class->get_option($file, 'repeats');
        my @r_list = ();
    
        foreach ( @$list ) {
            # Перед каждым упражнением вне зависимости от подхода вставляется пауза
            push @r_list, ['Пауза', $class->get_option($file, 'pause')];
            push @r_list, $_
        }
        
        # Первая пауза удаляется, так-как она не всегда нужна
        shift @r_list;
        
        # При первом повторе вставляется пауза для того чтобы приготовиться
        unshift @r_list,['Приготовьтесь', $class->get_option($file, 'pause')] if ( $repeat == 1 );

        # В конец списка вставляется более длительная пауза
        ( $repeat == $repeats ) ? 
            push @r_list, ['Конец тренировки', $class->get_option($file, 'on_end')] : 
            push @r_list, ['Время отдохнуть', $class->get_option($file, 'relax')];
        
        \@r_list
    }

    ## Конец области видимости пакета Training
}

1;
