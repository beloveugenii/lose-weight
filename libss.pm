use strict;
use utf8;
use open qw / :std :utf8 /;

sub to_sec { ( $_[0] =~ /([\d.]+)\s?[mM]$/ ) ? return $1 * 60 : ( $_[0] =~ /([\d.]+)[sS]?$/ ) ? return $1 : return $1 }
# Переводит время в секунды в зависимости от буквы после числа

sub check_list {
    # Получает ссылку на список файлов и проверяет их по некоторому условию
    my $aref = shift;
    my @return_arr;

    foreach my $file ( @$aref ){
    # Если файл соответствует некоторому условию, то генерирует предупреждение,
    # которое записывается в log-файл.
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

1
