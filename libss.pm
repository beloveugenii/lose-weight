use strict;
use utf8;
use open qw / :std :utf8 /;

sub to_sec { ( $_[0] =~ /([\d.]+)\s?[mM]$/ ) ? return $1 * 60 : ( $_[0] =~ /([\d.]+)[sS]?$/ ) ? return $1 : undef }
# Переводит время в секунды в зависимости от буквы после числа

sub check_list {
    # Получает ссылку на список файлов и проверяет их по некоторому условию
    my $aref = shift;
    my @return_arr;

    foreach my $file ( @$aref ){
    # Если файл соответствует некоторому условию, то генерирует предупреждение, которое записывается в log-файл.
    # Условия: файл имеет расширение сущестует и имеет *.ss
        if ( my $warn_code = ( ! -e $file ) ? -1 : ! (  $file =~ /\.ss$/ ) ? -2 : undef ) {
        
            my $warn_msg = ( $warn_code == -1 ) ? "'$file' not exist" :
                           ( $warn_code == -2 ) ? "'$file' is unsupported" :
                                                    'Unknown warning';
            open my $log, ">>", 'log';
            say $log $warn_msg;
            close $log;
            next
        }

    # Если файл проходит проверку, то его имя заносится в выходной массив
        push @return_arr, $file
    }
    # Перед выходом массив входных данных очищается
    @$aref = ();
    
    # Возвращает ссылку на список файлов, прошедших проверку
    \@return_arr
}

sub parse_files {
    # Передается ссылка на массив с файлами
    my $files_ref = shift;
    # Массив с разобранными файлами
    my @parsed_files;

    # Для каждого файла из переданных
    foreach my $file ( @$files_ref ) {
        # Открываем файл для чтения
        open my $fh, "<", $file or die "'$file': $!";
        my %file;
        # Структура данных на каждого файл
        #%file = (
            #param1 => str, 
            #param2 => str, 
            #paramN => str, 
            #aref=> [
                #[ ex1, dur1, ], 
                #[ ex2, dur2, ],
                #[ exN, durN ],
            #],
        #);
    
        # Parser
        while ( my $line = <$fh> ) {
            # читаем файл построчно
            chomp $line;
            # пропускаем строку, если она пуста, или это комментарий
            next if $line =~ /(?:^#+)|(?:^$)/;
            
            if ( $line =~ /^(.+)(?::|(?:->))(.+)$/ ) {
                # Если разделитель - двоеточие или ->
                # Перевести последнюю часть в секунды и
                # вставить как анонимный массив в хеш
                push @{$file{aref}}, [ $1, to_sec($2) ]
            }
            elsif ( $line =~ /^(.+)=(.+)$/) {
                my ($name, $val) = ($1, $2);
                $file{$name} = $val =~ /^([\d.]+[smM])$/ ? to_sec($1) : $val;
            }
        }
        # вносит ссылку на хеш с данными из файла в список разобранных файлов 
        push @parsed_files, \%file
    }

    # Возвращаем ссылку на массив с разобранными файлами. Массив содержит ссылки на хеши 
    \@parsed_files
}


1
