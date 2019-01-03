#!/usr/bin/python


import sys
import os
import argparse
import csv
import json
from vladiate import Vlad
from vladiate.validators import UniqueValidator, SetValidator, Ignore
from vladiate.inputs import LocalFile

def perform_validation(filename):
    validators = {
        'Filename': [
            UniqueValidator()
        ],
        "MassiveID" : [
            Ignore()
        ],
        "ATTRIBUTE_Subject_LifeStage" : [
            Ignore()
        ],
        'ATTRIBUTE_Subject_Sex': [
            SetValidator(valid_set=["female", "male", "not collected", "not applicable"])
        ],
        'ATTRIBUTE_Subject_HumanPopulationDensity' : [
            SetValidator(valid_set=["Urban", "Rural", "not collected", "not applicable"])
        ],
        'ATTRIBUTE_Analysis_MassSpectrometer' : [
            SetValidator(valid_set=["Maxis_Impact", "Maxis_ImpactHD", "QExactive", "micrOTOF-Q II"])
        ],
        'ATTRIBUTE_Curated_SampleType' : [
            SetValidator(valid_set=["animal_arachnida_NOS",
            "animal_aves_NOS",
            "animal_insecta_NOS",
            "animal_malacostraca_NOS",
            "animal_mammalia_NOS",
            "animal_NOS",
            "animal_osteichthyes_NOS",
            "animal_reptilia_NOS",
            "beverage",
            "blank_analysis",
            "blank_extraction",
            "blank_QC",
            "culture_bacterial",
            "culture_fungal",
            "environmental",
            "food",
            "human",
            "mouse",
            "plant_angiospermae",
            "plant_gymnospermae",
            "plant_NOS",
            "rat",
            "reference material"])
        ],
        'ATTRIBUTE_Curated_SampleType_Sub1' : [
            SetValidator(valid_set=["anal region"
            "bacterial culture",
            "beverage_alcoholic",
            "beverage_nonalcoholic",
            "blank_analysis",
            "blank_extraction",
            "blank_QC",
            "blood",
            "blood plasma",
            "blood serum",
            "environmental_brackish_dissolvedorganicmatter",
            "environmental_clothing",
            "environmental_freshwater_dissolvedorganicmatter",
            "environmental_house",
            "environmental_saline_dissolvedorganicmatter",
            "environmental_soil_dissolvedorganicmatter",
            "feces",
            "food_source_animal",
            "food_source_complex",
            "food_source_fungi",
            "food_source_NOS",
            "food_source_plant",
            "fungal culture",
            "gall bladder",
            "nasal cavity",
            "oral cavity",
            "plant",
            "reference material_chemicalstandard",
            "reference material_drugsorsupplement",
            "reference material_personalcareproduct",
            "reference material_animalfeedorsupplement",
            "skin",
            "sputum",
            "tooth",
            "urine",
            "vagina",
            "saliva",
            "caecum",
            "breast milk",
            "midgut",
            "lung"])
        ],
        'ATTRIBUTE_Curated_BodyPartOntologyIndex' : [
            SetValidator(valid_set=['UBERON:0001353',
            'UBERON:0002427',
            'UBERON:0015474',
            'UBERON:0000178',
            'UBERON:0001969',
            'UBERON:0001977',
            'UBERON:0001091',
            'UBERON:0001988',
            'UBERON:0002110',
            'UBERON:0012180',
            'UBERON:0001707',
            'not applicable',
            'UBERON:0000167',
            'UBERON:0001511',
            'UBERON:0001519',
            'UBERON:0001513',
            'UBERON:0001085',
            'UBERON:0007311',
            'UBERON:0001088',
            'UBERON:0000996',
            'UBERON:0001836',
            'UBERON:0001153',
            'UBERON:0001555',
            'UBERON:0004907',
            'UBERON:0004908',
            'UBERON:0001045',
            'UBERON:0002048'])
        ],
        'ATTRIBUTE_Curated_DiseaseOntologyIndex' : [
            SetValidator(valid_set=["DOID:1485",
            "DOID:9351",
            "disease NOS",
            "DOID:10763",
            "DOID:0050589",
            "no disease reported",
            "not applicable",
            "DOID:8893",
            "no DOID avaliable",
            "DOID:12140",
            "DOID:9970",
            "DOID:12155",
            "DOID:8778"
            ])
        ],
        "Analysis_SampleExtractionMethod" : [
            SetValidator(valid_set=['ethanol-water (9:1)',
            'methanol-water (1:1)',
            'dichloromethane-methanol (2:1)',
            'ethanol-water (19:1)',
            'water (94_deg_C)',
            'water (95_deg_C)',
            'water (100%) (deg_C_NOS)',
            'chloroform-methanol-water (1:3:1) ',
            'methanol (100%)',
            'ethanol (100%)',
            'ethanol-water (1:1)',
            'ethanol-water (9:1)',
            'water-acetonitrile (250:1)',
            'methanol-acetonitrile (3:7)',
            'methanol-water (4:1)'
            ])
        ],
        'Analysis_InternalStandardsUsed' : [
            SetValidator(valid_set=["sulfamethizole;sulfachloropyridazine",
            "sulfamethazine",
            "sulfamethazine;sulfadimethoxine",
            "sulfadimethoxine",
            "sulfamethizole;sulfachloropyridazine;sulfadimethoxine;sulfamethazine;coumarin-314;amitryptiline",
            "amitryptiline",
            "none",
            "fluconazole",
            "amitryptiline;fluconazole",
            "sulfadimethoxine;sulfachloropyridazine"
            ])
        ],
        'Analysis_IonizationSourceAndPolarity' : [
            SetValidator(valid_set=["electrospray ionization (positive)",
            "electrospray ionization (negative)",
            "atmospheric pressure chemical ionization (positive)",
            "atmospheric pressure chemical ionization (negative)",
            "atmospheric pressure photoionization (positive)",
            "atmospheric pressure photoionization (negative)"
            ])
        ],
        'Analysis_ChromatographyAndPhase' : [
            SetValidator(valid_set=["reverse phase (C18)",
            "reverse phase (C8)",
            "reverse phase (Phenyl-Hexyl)",
            "normal phase (HILIC)"
            ])
        ]
    }

    my_validator = Vlad(source=LocalFile(filename),delimiter="\t",ignore_missing_validators=True,validators=validators)
    passes_validation = my_validator.validate()

    errors_list = []
    for column in my_validator.failures:
        for line_number in my_validator.failures[column]:
            error_dict = {}
            error_dict["header"] = column
            error_dict["line_number"] = line_number + 1 #0 Indexed with 0 being the header row
            error_dict["error_string"] = str(my_validator.failures[column][line_number])

            errors_list.append(error_dict)

    for missing_field in my_validator.missing_fields:
        error_dict = {}
        error_dict["header"] = "Missing Header"
        error_dict["line_number"] = "N/A"
        error_dict["error_string"] = "Missing column %s" % (missing_field)

        errors_list.append(error_dict)

    valid_rows = []
    #Read in the good rows
    try:
        no_validation_lines = [int(error["line_number"]) for error in errors_list]
        row_count = 0
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                row_count += 1
                if row_count in no_validation_lines:
                    continue
                valid_rows.append(row)
    except:
        raise
        print("error reading file")


    return passes_validation, my_validator.failures, errors_list, valid_rows, row_count

def perform_summary(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")

        summary_dict = {}
        summary_dict["row_count"] = sum([1 for row in reader])

        summary_list = []
        summary_list.append({"type" : "row_count", "value" : summary_dict["row_count"]})

        return summary_dict, summary_list

def main():
    parser = argparse.ArgumentParser(description='Validate Stuff.')
    parser.add_argument('inputmetadata', help='inputmetadata')
    args = parser.parse_args()

    passes_validation, failures, errors_list, valid_rows, total_rows = perform_validation(args.inputmetadata)
    no_validation_lines = [int(error["line_number"]) for error in errors_list]

    output_list = ["MING", os.path.basename(args.inputmetadata), str(total_rows), str(len(valid_rows))]
    print("\t".join(output_list))


    #with open(args.inputmetadata, 'rb') as csvfile:
        #dialect = csv.Sniffer().sniff(csvfile.read(1024))
        #csvfile.seek(0)
        #reader = csv.DictReader(csvfile, dialect=dialect)
        #for row in reader:
        #    print(row)

if __name__ == "__main__":
    main()