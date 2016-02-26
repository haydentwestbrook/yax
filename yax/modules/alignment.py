"""Alignment Module
This module is responsible for aligning the trimmed reads to the
reduced set of gi references output by the aggregation module and
generating a .sam file with the alignment data
"""

import subprocess
import configparser


class Alignment:

    def __init__(self, input_artifact, output_artifact, config):
        """Initializes an Alignment object and sets variables
        based on values in the artifacts and config file

        Args:
            input_artifact: contains the location of the reads and references
            output_artifact: contains the output location
        Returns:
            An initialized Alignment object
        """
        self.module_name = "alignment"

        # Get reads and reference locations from input artifact
        self.gi_reference_set = input_artifact.gi_reference_set
        self.trimmed_reads = input_artifact.trimmed_reads

        # Get output location from the output artifact
        self.output_directory = output_artifact.file_path

        # Parse the config and set parameters
        parser = configparser.ConfigParser()
        parser.read_file(open(config))
        self.bowtie_location = parser.get(self.module_name, "bowtie_location")
        self.bowtie_arguments = parser.get(self.module_name,
                                           "bowtie_arguments")
        self.bowtie_build_arguments = parser.get(self.module_name,
                                                 "bowtie_build_arguments")
        self.working_directory = parser.get(self.module_name,
                                            "working_directory")

    def __call__(self):
        return self.run_alignment()

    def verify_params(self):
        """To do: verifies the validity of the config parameters
        Returns:
            Boolean representing whether the params are valid or not
        """
        pass

    def run_alignment(self):
        """Calls bowtie2 and executes the alignment. Outputs a .sam file"""
        index_directory = self.working_directory + "index/index"
        subprocess.call([self.bowtie_location + "bowtie2-build",
                         self.gi_reference_set, index_directory])
        subprocess.call([self.bowtie_location + "bowtie2-align", "-x",
                         index_directory, "-U", self.trimmed_reads, "-S",
                         self.output_directory])
        self.output_artifact.complete = True
