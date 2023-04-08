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
        #my %parsed_files;
        my @parsed_files;

        # Для каждого файла из переданных
        foreach my $file ( @$files_ref ) {
            # Открываем файл для чтения
            open my $fh, "<", $file or die "'$file': $!";
            my %file;
            # Структура данных на каждого файл
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
            #$parsed_files{$file} = \%file
             push @parsed_files, \%file
        }
        # Создаем экземпляр класса и возвращаем ссылку на него
        #bless \%parsed_files, $class
        bless \@parsed_files, $class
    }

    sub prepare {
        my $class = shift;
        my $aref = shift;


        ДОБАВИТЬ ПАУЗЫ МЕЖДУ УПРАЖНЕНИЯМИ И ПОДХОДАМИ
    
    
    
    
    }

    ## Конец области видимости пакета Training
}
   ## Расширяет массив с упражнениями таким образом, чтобы учитывались количество подходов, паузы между упражнениями и подходами
    #sub prepare {
        ## Константные строки
        #my $prepare_str = "Приговься : " . $_[0]->get_option('pause');
        #my $pause_str = "Пауза : " . $_[0]->get_option('pause');
        #my $relax_str = "Время отдохнуть : " . $_[0]->get_option('relax');
        
        #my @final;

        #for ( my $f_index = 0; $f_index <= $#{$data{list}}; $f_index++ ) { 
            ## Разыменовываем как список элемент массива и сохраняем его в переменную
            #my @file = @{$data{list}[$f_index]};

            ## Переменная local_repeats используется для того, чтобы разминка и заминка
            ## повторялись только 1 раз
            #my $local_repeats = ( $f_index == 0 || $f_index == $#{$data{list}} ) ? 1 : $_[0]->get_option('repeats');

            #for ( my $repeat = 1; $repeat <= $local_repeats; $repeat++ ) {
                #push @final, $conv->( $prepare_str ) if $repeat == 1;

                #for( my $ex = 0; $ex <= $#file; $ex++) {
                    #push @final, $conv->( $pause_str ) 
                        #unless $ex == 0;
                    #push @final, $conv->( $file[$ex] );
                #}
                #push @final, $conv->( $relax_str ) 
                    #unless $repeat == $local_repeats;
            #}    
            #push @final, ""
        #}
        ## Перезаписываем в хеш под ключом 'list' ссылку на новый список
        ## который включает все упражнения в нужно количестве, разделенные паузами
        ## Перерывы между файлами определяются стркой ':'
         #$data{list} = \@final
    #}



1;
