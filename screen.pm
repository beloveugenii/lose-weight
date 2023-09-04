use strict;
use utf8;
use open qw /:std :utf8 /;
use Term::ReadKey qw / GetTerminalSize /;
use Term::Completion qw / Complete /;

{
    package Screen; 

    my $screen;

     my %nums = ( 
        0 => { 1=>"#########", 2=>"#########", 3=>"###   ###", 4=>"###   ###", 5=>"###   ###", 6=>"###   ###", 7=>"#########", 8=>"#########", },
        1 => { 1 => "    ###  ", 2=>"    ###  ", 3=>"    ###  ", 4=>"    ###  ", 5=>"    ###  ", 6=>"    ###  ", 7=>"    ###  ", 8=>"    ###  " }, 
        2  => { 1=>"#########", 2=>"#########", 3=>"      ###", 4=>"#########", 5=>"#########", 6=>"###      ", 7=>"#########", 8=>"#########", },
        3  => { 1=>"#########", 2=>"#########", 3=>"      ###", 4=>"  #######", 5=>"  #######", 6=>"      ###", 7=>"#########", 8=>"#########", },
        4 => { 1=>"###   ###", 2=>"###   ###", 3=>"###   ###", 4=>"#########", 5=>"#########", 6=>"      ###", 7=>"      ###", 8=>"      ###", },
        5 => { 1=>"#########", 2=>"#########", 3=>"###      ", 4=>"#########", 5=>"#########", 6=>"      ###", 7=>"#########", 8=>"#########", },
        6 => { 1=>"#########", 2=>"#########", 3=>"###      ", 4=>"#########", 5=>"#########", 6=>"###   ###", 7=>"#########", 8=>"#########", },
        7 => { 1=>"#########", 2=>"#########", 3=>"      ###", 4=>"      ###", 5=>"      ###", 6=>"      ###", 7=>"      ###", 8=>"      ###", },
        8 => { 1=>"#########", 2=>"#########", 3=>"###   ###", 4=>"#########", 5=>"#########", 6=>"###   ###", 7=>"#########", 8=>"#########", },
        9 => { 1=>"#########", 2=>"#########", 3=>"###   ###", 4=>"#########", 5=>"#########", 6=>"      ###", 7=>"#########", 8=>"#########", },
        10 => { 1=>"         ", 2=>"         ", 3=>"         ", 4=>"         ", 5=>"         ", 6=>"         ", 7=>"         ", 8=>"         ", },
    );

   
    my $size = (Term::ReadKey::GetTerminalSize)[0];
    my $line = '-' x $size;

    sub new { bless \$screen, $_[0] }
    
    sub clear { print "\033[2J\033[H" }
    
    sub header {
        my ( $class, $header, $aref ) = @_;
        my $size = (Term::ReadKey::GetTerminalSize)[0];

        my $hl = length $header;
        $hl = ( $hl % 2 == 0 ) ? $hl :  $hl + 1;
        my $hf = ' ' x ( ( $size - $hl) / 2 );
        $class->clear;
        printf "%s\n%s%*s%s\n%s\n", $line, $hf, $hl, $header, $hf, $line;
        
        if ( $aref ) {
            my $str = 'Программа тренировки:';
            my $l = length($str);
            $hf = int ( $size - $l ) / 5;
            print "\n" x 4;
            printf "%s%s\n", ' ' x $hf, $_ foreach ( $str, @{$aref} );
            print "\n" x 4;
            printf "%s\n", '-' x $size
     }
    }

    # Получает число и возвращает массив из цифр, составляющих это число
    # Максимальное число - трехзначное, минимальное - однозначное
    sub get_digit {
        my ( $class, $digit ) = @_;
        ( $digit =~ /^(\d)(\d)(\d)$/ ) ? ( $1, $2, $3 ) :
        ( $digit =~ /^(\d)(\d)$/ ) ? ( 10, $1, $2 ) :
        ( $digit =~ /^(\d)$/ ) ? ( 10, 10, $1 ) : 0
    }



    sub print_big_nums {
        my ( $class, $digit ) = ( shift, shift );
        my $size = (Term::ReadKey::GetTerminalSize)[0];
        my $f = int ( ($size - 27 ) / 4 );
        my ( $l, $c, $r ) = $class->get_digit( $digit );
            printf "%s%9s%s%9s%s%9s%s\n",
                " " x $f, $nums{$l}{$_},
                " " x $f,$nums{$c}->{$_}, 
                " " x $f, $nums{$r}->{$_}, 
                " " x $f foreach ( 1..8 );
    }



















    sub menu {
        my $class = shift;
        my @items = @_;
        my $size = (Term::ReadKey::GetTerminalSize)[0];
        push @items, ' ' unless ( @items % 2 == 0 );

        my $longest;
        foreach ( @items ) {
            $longest = length $_ if length $_ > $longest;
        }

        my $mf = ' ' x ( ( $size - $longest * 2 ) / 4 );

        print $line;
        for ( my $k = 0; $k <= $#items; $k++ ) {
            printf "%-s%-*s%-s%-*s%s\n",
                   $mf,
                   $longest, $items[$k++],
                   $mf x 2,
                   $longest, $items[$k],
                   $mf ;
        }
        print "$line\n";
    
    }
}
1;



       
