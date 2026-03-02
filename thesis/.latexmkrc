# .latexmkrc — latexmk configuration for thesis build with glossaries
#
# Adds makeglossaries as a custom dependency so that latexmk automatically
# runs makeglossaries between XeLaTeX passes whenever glossary files change.
# This produces the sorted .gls / .acr files that \printglossary reads.

use File::Basename;

add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
add_cus_dep('glo-abr', 'gls-abr', 0, 'run_makeglossaries');

sub run_makeglossaries {
    my ($base_name, $path) = fileparse( $_[0] );
    my $orig_dir = Cwd::cwd();
    chdir $path;
    my $return;
    if ( $silent ) {
        $return = system "makeglossaries -q '$base_name'";
    } else {
        $return = system "makeglossaries '$base_name'";
    }
    chdir $orig_dir;
    return $return;
}
