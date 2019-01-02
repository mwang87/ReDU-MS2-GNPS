#!/usr/bin/python


import sys
import os
import argparse
import csv
import json
from vladiate import Vlad
from vladiate.validators import UniqueValidator, SetValidator
from vladiate.inputs import LocalFile

def perform_validation(filename):
    validators = {
        'Filename': [
            UniqueValidator()
        ],
        "MassiveID" : [],
        "ATTRIBUTE_Subject_LifeStage" : [],
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
            SetValidator(valid_set=[])
        ],
        'ATTRIBUTE_Curated_DiseaseOntologyIndex' : [
            SetValidator(valid_set=[])
        ],
        "Analysis_SampleExtractionMethod" : [],
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
            print(column, line_number)

            error_dict = {}
            error_dict["header"] = column
            error_dict["line_number"] = line_number
            error_dict["error_string"] = str(my_validator.failures[column][line_number])

            errors_list.append(error_dict)

    for missing_field in my_validator.missing_fields:
        error_dict = {}
        error_dict["header"] = "Missing Header"
        error_dict["line_number"] = "N/A"
        error_dict["error_string"] = "Missing column %s" % (missing_field)

        errors_list.append(error_dict)

    return passes_validation, my_validator.failures, errors_list

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

    passes_validation, failures, errors_list = perform_validation(args.inputmetadata)
    if passes_validation:
        summary_dict = perform_summary(args.inputmetadata)
        print(summary_dict)

    #with open(args.inputmetadata, 'rb') as csvfile:
        #dialect = csv.Sniffer().sniff(csvfile.read(1024))
        #csvfile.seek(0)
        #reader = csv.DictReader(csvfile, dialect=dialect)
        #for row in reader:
        #    print(row)

if __name__ == "__main__":
    main()
