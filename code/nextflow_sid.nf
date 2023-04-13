#!/usr/bin/env nextflow
nextflow.enable.dsl=2

params.input = "README.md"

TOOL_FOLDER = "$baseDir"

process processData {
    publishDir "./nf_output", mode: 'copy'

    conda "$TOOL_FOLDER/conda_env.yml"

    input:
    file input 

    output:
    file 'outputs.tsv.*'
    file 'file_paths.tsv'
    file 'passed_file_names.tsv'
    file 'check.tsv'

    """
    python $TOOL_FOLDER/gnps_downloader.py $input     
    python $TOOL_FOLDER/gnps_validator.py $input passed_file_names.tsv
    python $TOOL_FOLDER/gnps_name_matcher.py $input check.tsv
    """
}

workflow {
    data = Channel.fromPath(params.input)
    processData(data)
}

// 