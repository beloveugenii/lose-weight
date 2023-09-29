package libsui;

use strict;
use utf8;
use open qw /:std :utf8 /;
use Term::ReadKey qw / GetTerminalSize /;
use base qw / Exporter /;

our @EXPORT = qw / clear promt line print_as_table header menu screen /;

our $version = '0.0.1';

my $screen_width = (Term::ReadKey::GetTerminalSize)[0];
my $line = '-' x $screen_width . "\n";

sub clear {
    # clears the screen
    print "\033[2J\033[H" 
}
sub line {
    # prints line
    print $line;
}

sub promt {
    # takes a string
    my $what = shift;
    # return gived string in looks 'String: '
    print(uc(substr($what, 0, 1)) . substr($what, 1) . ': ');
    chomp(my $input = <STDIN>);
    $input
}

sub get_fields_len {
    # takes arrayref with arrayrefs with data strings
    my $data = shift;
    my $fields;

    # defines the number of rows and columns
    my $rows = scalar @$data;
    my $cols;
    foreach (0..$rows - 1) {
          $cols = @{@$data[$_]} if @{@$data[$_]} > $cols;
    }
    # defines width of every columns
    foreach my $col (0..$cols - 1) {
        my $longest = 0;
        foreach my $row (0..$rows){
            eval { $longest = length @{@$data[$row]}[$col] if length @{@$data[$row]}[$col] > $longest };
        }
        push @$fields, $longest
    }

    my $fields_sum = 0;
    $fields_sum += $_ foreach @$fields;
    
    # defines width of empty fields
    my $sep_len = int ( ($screen_width - $fields_sum) / ( @$fields + 1) );

    $sep_len-- while (($fields_sum + (@$fields + 1) * $sep_len) > $screen_width);

    # return arrayref with columns widths and width of empty field
    ($fields, $sep_len)
}

sub print_as_table {
    # takes arrayref with arrayrefs and separator
    my ($fields, $sep_len) = &get_fields_len($_[0]);
    
    # print subarray elements in fields separating with empty spaces
    foreach my $row (@{$_[0]}) {
        printf "%s%-*s", $_[1] x $sep_len, $$fields[$_], @$row[$_] foreach (0..@$fields - 1);
        printf "%s\n", $_[1] x $sep_len
    }
}
sub header {
    # takes a string and print it in center of screen
    print $line;
    print_as_table([[$_[0]]],' ');
    print $line;
}

sub menu {
    # takes array of strings and columns number
    # convert array into arrayref of arrayrefs
    my $cols = pop;
    my $menu_lst = [];
    @_ = map '[' . substr($_, 0, 1) . ']' . substr($_, 1), @_;

    push @_, '' if @_ % 2 == 1 && $cols % 2 == 0;
    
    while ( @_ > 0) {
        my @tmp = ();
        push @tmp, shift @_ foreach (1..$cols);
        push @$menu_lst, \@tmp;
    }

    # print arrayref as menu
    print $line;
    print_as_table($menu_lst,' ');
    print $line;
}

sub screen {
    # takes array with header text, subroutine ref, strings array and menu columns
    my $header_text = shift;
    my $body_sub = shift;
    my $menu_cols = pop;
    
    # clears the screen and prints header, output of body subroutine and menu
    clear();
    header($header_text);
    &$body_sub();
    menu(@_, $menu_cols);
    
}

=head1 NAME

libsui - is a Perl library for building a simple user interface.


=head1 SYNOPSIS

It contains functions for creating simple headers, menus and entire screens.

For using put **libsui.pm** into your perl-libs directory.

Usage:

    use libsui;

    screen('Header text', sub { print "Some func\n"}, qw / menu entries,/ 2)
 

=head1 DESCRIPTION

Simple user interface The library makes it easy to create a simple user interface. All you need to do is use the I<*loop()*> function and pass it a hashref as an argument.  
Each hash element must contain an arrayref with data to create a screen: the title text, subroutine-placeholder ref, menu items and the number of columns to build it. 


=head1 DEPENDENCIES

Term::ReadKey 


=head1 AUTHOR

Eugeniy Belov, <beloveugenii@gmail.com> 


=head1 COPYRIGHT AND LICENSE

Copyright 2023 by Eugeniy Belov.
This program is free software; you can redistribute it and/or modify it under the same terms as Perl itself.



=cut

1;
  
