from __future__ import absolute_import

import argparse
import logging
import re

from past.builtins import unicode

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


def run(argv=None):
    """Main entry point; defines and runs the wordcount pipeline."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--input',
                        dest='input',
                        help='Input file to process.')
    parser.add_argument('--output',
                        dest='output',
                        help='Output file to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    with beam.Pipeline(options=pipeline_options) as p:
        # Read the text file[pattern] into a PCollection.
        lines = p | ReadFromText(known_args.input)

        # Count the occurrences of each word.
        counts = (
                lines
                | 'Split' >> (beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x))
                              .with_output_types(unicode))
                | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
                | 'GroupAndSum' >> beam.CombinePerKey(sum))

        # Format the counts into a PCollection of strings.
        def format_result(word_count):
            (word, count) = word_count
            return '%s: %s' % (word, count)

        output = counts | 'Format' >> beam.Map(format_result)

        # Write the output using a "Write" transform that has side effects.
        # pylint: disable=expression-not-assigned
        output | WriteToText(known_args.output)
    print("results: " + known_args.output)



if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
