import sys

import option_parsers

from version import TOMBO_VERSION

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    commands = [
        ('Resquiggle (Must be run before any other commands):', [
            ('resquiggle','Re-annotate raw signal with ' +
             'genomic alignment from existing basecalls.',
             option_parsers.get_eventless_resquiggle_parser()),
        ]),
        ('Statistical Testing Command:',[
            ('test_significance','Test for shifts in signal against a ' +
             'reference, an alternative reference or another set of reads.',
             option_parsers.get_test_signif_parser()),
        ]),
        ('Text Output Commands:', [
            ('write_wiggles','Write wiggles from tombo results.',
             option_parsers.get_wiggle_parser()),
            ('write_most_significant_fasta',
             'Write sequences centered on most significant positions.',
             option_parsers.get_write_signif_diff_parser()),
        ]),
        ('Genome Anchored Plotting Commands:', [
            ('plot_max_coverage',
             'Plot signal in regions with maximal coverage.',
             option_parsers.get_max_cov_parser()),
            ('plot_genome_location',
             'Plot signal at defined genomic locations.',
             option_parsers.get_genome_loc_parser()),
            ('plot_motif_centered',
             'Plot signal centered on a specific motif.',
             option_parsers.get_motif_loc_parser()),
            ('plot_max_difference',
             'Plot signal where signal differs the most ' +
             'between two groups.',
             option_parsers.get_max_diff_parser()),
            ('plot_most_significant',
             'Plot signal with most significant test result.',
             option_parsers.get_signif_diff_parser()),
            ('plot_motif_with_stats',
             'Plot signal centered on a motif of interest including ' +
             'distribution of statistics around motif.',
             option_parsers.get_signif_motif_parser()),
            ('plot_per_read',
             'Plot per read non-standard base statistics.',
             option_parsers.get_per_read_parser()),
        ]),
        ('Sequencing Time Anchored Plotting Commands (event_resquiggle only):', [
            ('plot_correction',
             'Plot segmentation before and after correction.',
             option_parsers.get_correction_parser()),
            ('plot_multi_correction',
             'Plot multiple raw signals anchored by genomic location.',
             option_parsers.get_multi_correction_parser()),
        ]),
        ('Other Plotting Commands:', [
            ('cluster_most_significant',
             'Clustering traces at bases with most significant stats.',
             option_parsers.get_cluster_signif_diff_parser()),
            ('plot_kmer','Plot signal distributions acorss kmers.',
             option_parsers.get_kmer_dist_parser()),
        ]),
        ('Read Filtering (Only effects tombo index file):', [
            ('clear_filters',
             'Clear filters to process all successfully re-squiggled reads.',
             option_parsers.get_clear_filters_parser()),
            ('filter_stuck',
             'Apply filter based on observations per base thresholds.',
             option_parsers.get_filter_stuck_parser()),
        ]),
        ('Event-based Re-squiggle and Model Estimation:', [
            ('event_resquiggle', 'Re-annotate raw signal with genomic ' +
             'alignment from existing basecalls using event table.',
             option_parsers.get_event_resquiggle_parser()),
            ('model_resquiggle', 'Re-annotate raw signal after ' +
             'event_resquiggle to more closely match a tombo model.',
             option_parsers.get_model_resquiggle_parser()),
            ('estimate_kmer_reference',
             'Estimate reference tombo model derived from the provided reads.',
             option_parsers.get_write_kmer_ref_parser()),
            ('estimate_alt_reference', 'Estimate alternative tombo model from ' +
             'a sample containing standard bases spiked with a single ' +
             'non-standard base at random positions.',
             option_parsers.get_write_alt_ref_parser()),
        ]),
    ]
    desc = '\n\n'.join([
        grp + '\n' + '\n'.join([
            '\t{0: <30}{1}'.format(cmd, cmd_help)
            for cmd, cmd_help, cmd_parser in cmds])
        for grp, cmds in commands])

    import argparse
    parser = argparse.ArgumentParser(
        prog='tombo',
        description='Tombo is a command line python toolset ' +
        'to analyze and visualize raw nanopore sequencing data ' +
        'including the identification of non-standard nucleotides.',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-v', '--version', action='version',
        version='tombo version: {}'.format(TOMBO_VERSION),
        help='show tombo version and exit.')
    subparsers = parser.add_subparsers(
        title='commands', description=desc,
        help='Additional help available for subcommands.')

    # fill subparser with parsers and linked main functions
    for grp, cmds in commands:
        for cmd, cmd_help, cmd_parser in cmds:
            subparser_cmd = subparsers.add_parser(
                cmd, parents=[cmd_parser,], add_help=False)
            subparser_cmd.set_defaults(subcmd=cmd, group=grp)

    args = parser.parse_args(args)

    if args.subcmd == 'resquiggle':
        import resquiggle
        resquiggle.eventless_resquiggle_main(args)
    elif args.subcmd == 'event_resquiggle':
        import event_resquiggle
        event_resquiggle.event_resquiggle_main(args)
    elif args.subcmd == 'model_resquiggle':
        import model_resquiggle
        model_resquiggle.model_resquiggle_main(args)
    elif args.subcmd == 'test_significance':
        import tombo_stats
        tombo_stats.test_shifts_main(args)
    elif args.subcmd == 'estimate_kmer_reference':
        import tombo_stats
        tombo_stats.write_kmer_ref_main(args)
    elif args.subcmd == 'estimate_alt_reference':
        import tombo_stats
        tombo_stats.write_alt_ref_main(args)
    elif args.subcmd == 'clear_filters':
        import tombo_helper
        tombo_helper.clear_filters_main(args)
    elif args.subcmd == 'filter_stuck':
        import tombo_helper
        tombo_helper.filter_stuck_main(args)
    elif args.group == 'Text Output Commands:':
        import text_output_commands
        if args.subcmd == 'write_wiggles':
            text_output_commands.wiggle_main(args)
        else:
            text_output_commands.write_signif_diff_main(args)
    else:
        import plot_commands
        plot_commands.plot_main(args)

    return

if __name__ == "__main__":
    main()
