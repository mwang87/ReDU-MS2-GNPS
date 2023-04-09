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

    """   
    python $TOOL_FOLDER/gnps_downloader.py $input 
    """
}
workflow {
    data = Channel.fromPath(params.input)
    processData(data)
}