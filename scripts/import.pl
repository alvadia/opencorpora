#!/usr/bin/perl
use strict;
use warnings;
use utf8;

use FindBin;
use lib "$FindBin::Bin/../perl/lib";

use Config::INI::Reader;
use OpenCorpora::Dict::Importer;

@ARGV or die "Usage: $0 <config>";

my $conf      = Config::INI::Reader->read_file($ARGV[0]);
my $root_path = $conf->{project}{root};

binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

my $importer = new OpenCorpora::Dict::Importer;
$importer->read_rules("$root_path/scripts/import_rules.txt");
$importer->read_bad_lemma_grammems("$root_path/scripts/bad_lemma_grammems.txt");
$importer->preload_list('anim0', "$root_path/scripts/lists/Del_anim-inan&Add_ANim.txt");
$importer->preload_list('anim1', "$root_path/scripts/lists/remove_ANim.txt");
$importer->preload_list('numr0', "$root_path/scripts/lists/list_numr_dupl_gent.txt");
$importer->preload_list('adjf_fixd_del', "$root_path/scripts/lists/list_adjf_fixd_delete.txt");
$importer->preload_list('adjf_fixd_advb', "$root_path/scripts/lists/list_adjf_fixd_ADVB.txt");
$importer->preload_list('adjf_fixd_noun', "$root_path/scripts/lists/list_adjf_fixd_NOUN.txt");
$importer->preload_list('nouns_subst', "$root_path/scripts/lists/nouns_subst.txt");
$importer->preload_list('arch_adj', "$root_path/scripts/lists/add_Arch_ADJF.txt");
$importer->preload_list('litr', "$root_path/scripts/lists/add_Litr.txt");
$importer->preload_list('dist_prts', "$root_path/scripts/lists/add_Dist_PRTS.txt");
$importer->preload_list('dist_aux', "$root_path/scripts/lists/add_Dist_aux.txt");
$importer->preload_list('infr0', "$root_path/scripts/lists/add_Infr_nomn_plur.txt");
$importer->preload_list('infr1', "$root_path/scripts/lists/add_Infr_gent_plur.txt");
$importer->preload_list('infr_abl_sg', "$root_path/scripts/lists/add_Infr_ablt_sing.txt");
$importer->preload_list('infr_abl_pl', "$root_path/scripts/lists/add_Infr_ablt_plur.txt");
$importer->preload_list('infr3', "$root_path/scripts/lists/add_Infr_ADJS.txt");
$importer->preload_list('infr_comp', "$root_path/scripts/lists/add_Infr_COMP.txt");
$importer->preload_list('pred_del', "$root_path/scripts/lists/pred_del.txt");
$importer->preload_list('adjs_del', "$root_path/scripts/lists/adjs_forms_del.txt");
$importer->preload_list('pred_intj', "$root_path/scripts/lists/pred_to_intj.txt");
$importer->preload_list('erro_adjs', "$root_path/scripts/lists/add_Erro_ADJS.txt");
$importer->preload_list('erro_prts', "$root_path/scripts/lists/add_Erro_PRTS.txt");
$importer->preload_list('count', "$root_path/scripts/lists/add_Coun_gent_plur.txt");
$importer->preload_list('abbr_del', "$root_path/scripts/lists/abbr_del.txt");
$importer->read_aot("bzcat /corpus/files/aot_dump.7.bz2 |");
