#!/usr/bin/python


import sys
import os
import argparse
import csv
import json
import pandas as pd
from vladiate import Vlad
from vladiate.validators import UniqueValidator, SetValidator, Ignore, IntValidator, RangeValidator
from vladiate.inputs import LocalFile

import ftputil
import ming_proteosafe_library
import ming_fileio_library

"""Validation with actual data"""
massive_host = ftputil.FTPHost("massive.ucsd.edu", "anonymous", "")

def get_dataset_files(dataset_accession, collection_name):
    try:
        massive_host.keep_alive()
    except:
        print("MassIVE connection broken, reconnecting")
        massive_host = ftputil.FTPHost("massive.ucsd.edu", "anonymous", "")

    dataset_files = ming_proteosafe_library.get_all_files_in_dataset_folder_ftp(dataset_accession, collection_name, massive_host=massive_host)
    return dataset_files

def perform_validation_against_massive(filename):
    metadata = pd.read_csv(filename, sep="\t")

    print(metadata.keys())

    if len(set(list(metadata["MassiveID"]))) > 1:
        print("Too many accessions")
        return False, "Too many accessions", 0

    accession = metadata["MassiveID"][0]
    print(accession)
    dataset_files = get_dataset_files(accession, "ccms_peak")

    all_resolved_filenames = []
    for query_filename in metadata["filename"]:
        print(query_filename)
        dataset_filename = resolve_metadata_filename_to_all_files(query_filename, dataset_files)

        if dataset_filename == None:
            continue

        all_resolved_filenames.append(dataset_filename)

    return True, "Success", len(all_resolved_filenames)

def resolve_metadata_filename_to_all_files(filename, dataset_files):
    stripped_extension = ming_fileio_library.get_filename_without_extension(filename)

    acceptable_filenames = ["f." + dataset_filename for dataset_filename in dataset_files if dataset_filename.find(stripped_extension) != -1]

    if len(acceptable_filenames) != 1:
        return None

    return acceptable_filenames[0]


def rewrite_metadata(metadata_filename):
    """
    Metadata Fields Rewrite

    Fields changed and will need to be rewritten

    """

    metadata_df = pd.read_csv(metadata_filename, sep="\t")

    #Rewriting Year of Analysis
    metadata_list = metadata_df.to_dict(orient="records")
    for metadata_obj in metadata_list:
        try:
            metadata_obj["YearOfAnalysis"] = str(int(float(metadata_obj["YearOfAnalysis"])))
        except:
            continue

    metadata_df = pd.DataFrame(metadata_list)
    metadata_df.to_csv(metadata_filename, sep="\t", index=False)

def perform_validation(filename):
    validators = {
        'filename': [
            UniqueValidator()
        ],
        "MassiveID" : [
            Ignore()
        ],
        'SampleType' : [
            SetValidator(valid_set=['animal','beverage','blank_analysis','blank_extraction','blank_QC','culture_bacterial','culture_fungal','inanimate_object','environmental','built_environment','food','plant','reference material'])
        ],
        'SampleTypeSub1' : [
            SetValidator(valid_set=['biofluid','food_source_animal','tissue','beverage_nonalcoholic','beverage_alcoholic','blank_analysis','blank_extraction','bacterial culture','blank_QC','culture_bacterial','culture_fungal','mobile phone','keys','computer','purse_or_wallet','clothing','dissolvedorganicmatter_soil','dissolvedorganicmatter_water_saline','house','marine_invertebrates_insitu','marine_cyanobacteria_insitu','food_source_plant','food_source_complex','food_source_fungi','food_source_NOS','plant_angiospermae','plant_NOS','reference material_personalcareproduct','reference material_animalfeedorsupplement','reference material_chemicalstandard','reference material_collectionmaterial_microtubes','reference material_collectionmaterial_wellplates','not specified','not applicable'])
        ],
        'NCBITaxonomy' : [
            SetValidator(valid_set=['1003843|Halcyon smyrnensis','100858|Threskiornis aethiopicus','10088|Mus','10114|Rattus','10157|Myocastor coypus','1087776|Euphorbia pithyusa','109689|Chaetodon ephippium','109695|Chaetodon melannotus','109712|Pomacanthus navarchus','110196|Bitis atropos','110555|Myxine','113544|Arapaima gigas','115645|Ducula bicolor','119419|Tauraco schalowi','121123|Alouatta sara','1243780|Pelecanus occidentalis californicus','1297064|Trichechus manatus manatus','13489|Dicentrarchus labrax','1390567|Ptilinopus cinctus','147464|Dinornis giganteus','1543402|Geocapromys brownii','170820|Hemiscyllium ocellatum','175825|Aceros corrugatus','184245|Tomistoma schlegelii','187114|Ducula aenea','194526|Gegeneophis ramaswamii','195635|Pleuronichthys verticalis','202946|Apteryx australis mantelli','227231|Himantopus mexicanus','241562|Amazona leucocephala','2711|Citrus sinensis','28713|Lanius ludovicianus','30406|Tragopan blythii','30461|Bubo bubo','311359|Cochoa','33589|Leptoptilos crumeniferus','3702|Arabidopsis thaliana','37083|Eudyptula minor','37578|Morus bassanus','377254|Megophrys nasuta','381107|Cinnyricinclus leucogaster','38626|Phascolarctos cinereus','38845|Euphorbia dendroides','403904|Onychostoma angustistomata','40833|Bucephala islandica','41691|Cygnus melancoryphus','43311|Fratercula cirrhata','43490|Gyps africanus','441894|Struthio camelus australis','444138|Ducula rufigaster','44489|Carettochelys insculpta','507972|Ptilopsis granti','51861|Corallus caninus','56072|Ardea herodias','56117|Tapirus bairdii','56549|Lycodon semicarinatus','571338|Macrochelys temminckii','57571|Salamandra salamandra','585466|Burhinus grallarius','61316|Hypentelium nigricans','62165|Chlorophanes spiza','651656|Incilius','681183|Astrapia mayeri','704175|Phoenicoparrus minor','71240|eudicotyledons','740693|Cephaloscyllium ventriosum','75024|Holacanthus ciliaris','75988|Pachymedusa dacnicolor','78394|Eptatretus cirrhatus','7897|Latimeria chalumnae','81903|Fulica americana','83391|Coryphaenoides cinereus','8450|Hypogeophis rostratus','8467|Caretta caretta','8503|Crocodylus novaeguineae','85101|Urocolius macrourus','8557|Varanus exanthematicus','86377|Taeniura lymma','8682|Hydrophis schistosus','8790|Dromaius novaehollandiae','8797|Rhea americana','8801|Struthio camelus','8863|Coscoroba coscoroba','8884|Oxyura jamaicensis','8924|Vultur gryphus','8961|Aquila audax','91789|Capito niger','9258|Ornithorhynchus anatinus','92683|Spheniscus demersus','9316|Macropus fuliginosus','9600|Pongo pygmaeus','9606|Homo sapiens','9636|Melursus ursinus','9755|Physeter catodon','not applicable','not collected','not specified'])
        ],
        'YearOfAnalysis' : [
            IntValidator(),
            RangeValidator(low=2000, high=2030)
        ],
        'SampleCollectionMethod' : [
            SetValidator(valid_set=['blood draw, capillary','blood draw, venous','blood NOS','liquid','not applicable','solid material, dried','solid material, fresh','solid material, frozen','swabs, dry','swabs, moist (50% EtOH)','urine, 24-hour','urine, NOS','urine, spot','extract, solid phase extraction (C18)','liquid, solid phase extraction (C18)','solid, solid phase extraction (C18)','solid material, NOS','not specified','liquid, solid phase extraction (PPL)'])
        ],
        "SampleExtractionMethod" : [
            SetValidator(valid_set=['ethanol-water (9:1)','methanol-water (1:1)','dichloromethane-methanol (2:1)','ethanol-water (19:1)','water (94_deg_C)','water (95_deg_C)','water (100%) (deg_C_NOS)','chloroform-methanol-water (1:3:1)','methanol (100%)','ethanol (100%)','ethanol-water (1:1)','water-acetonitrile (250:1)','methanol-acetonitrile (3:7)','methanol-water (4:1)','methanol-water (9:1)','not collected','ethyl acetate (100%)','methanol-water (7:3)','water-acetonitrile (149:1)','not specified','methanol-water (3:2)','acetonitrile (100%)','acetonitrile-water (7:3)','acetonitrile-methanol (1:1)','acetonitrile-isopropanol-water (3:3:2)'])
        ],
        'InternalStandardsUsed' : [
            SetValidator(valid_set=['sulfamethizole;sulfachloropyridazine','sulfamethazine','sulfamethazine;sulfadimethoxine','sulfadimethoxine','sulfamethizole;sulfachloropyridazine;sulfadimethoxine;sulfamethazine;coumarin-314;amitryptiline','amitryptiline','none','fluconazole','amitryptiline;fluconazole','sulfadimethoxine;sulfachloropyridazine','cholic_acid-d4;lithocholic_acid-d4','cocaine;cocaine-d3','cocaine-d3','sulfamethizole','not specified'])
        ],        
       'MassSpectrometer' : [
            SetValidator(valid_set=['Maxis_Impact','Maxis_ImpactHD','QExactive','micrOTOF-Q II','not specified','QTOF_6540','LTQ_Orbitrap_XL'])
        ],        
        'IonizationSourceAndPolarity' : [
            SetValidator(valid_set=['electrospray ionization (positive)','electrospray ionization (negative)','atmospheric pressure chemical ionization (positive)','atmospheric pressure chemical ionization (negative)','atmospheric pressure photoionization (positive)','atmospheric pressure photoionization (negative)','electrospray ionization (alternating)','not specified'])
        ],
        'ChromatographyAndPhase' : [
            SetValidator(valid_set=['reverse phase (C18)','reverse phase (C8)','reverse phase (Phenyl-Hexyl)','normal phase (HILIC)','mixed mode (Scherzo SM-C18)','not specified'])
        ],
        'BiologicalSex': [
            SetValidator(valid_set=['female','male','asexual','not collected','not applicable','not specified'])
        ],
        'Country': [
            SetValidator(valid_set=['not applicable','not collected','not specified','Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia','Bosnia and Herzegovina','Botswana','Brazil','Brunei','Bulgaria','Burkina Faso','Burundi','Cabo Verde','Cambodia','Cameroon','Canada','Central African Republic (CAR)','Chad','Chile','China','Colombia','Comoros','Congo, Democratic Republic of the','Congo, Republic of the','Costa Rica','Cote dIvoire','Croatia','Cuba','Cyprus','Czechia','Denmark','Djibouti','Dominica','Dominican Republic','Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Eswatini (formerly Swaziland)','Ethiopia','Fiji','Finland','France','Gabon','Gambia','Georgia','Germany','Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana','Haiti','Honduras','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Kiribati','Kosovo','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya','Liechtenstein','Lithuania','Luxembourg','Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands','Mauritania','Mauritius','Mexico','Micronesia','Moldova','Monaco','Mongolia','Montenegro','Morocco','Mozambique','Myanmar (formerly Burma)','Namibia','Nauru','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria','North Korea','North Macedonia (formerly Macedonia)','Norway','Oman','Pakistan','Palau','Palestine','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal','Qatar','Romania','Russia','Rwanda','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines','Samoa','San Marino','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia','Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','South Africa','South Korea','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Sweden','Switzerland','Syria','Taiwan','Tajikistan','Tanzania','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Tuvalu','Uganda','Ukraine','United Arab Emirates','United Kingdom','United States of America','Uruguay','Uzbekistan','Vanuatu','Vatican City (Holy See)','Venezuela','Vietnam','Yemen','Zambia','Zimbabwe','Isle of Man','Jersey','Czech Republic','not specified','not applicble'])
        ],
        'HumanPopulationDensity' : [
            SetValidator(valid_set=['Urban','Rural','not collected','not applicable','not specified'])
        ],
         'LifeStage' : [
            SetValidator(valid_set=['not applicable','not collected','Infancy (<2 yrs)','Early Childhood (2 yrs < x <=8 yrs)','Adolescence (8 yrs < x <= 18 yrs)','Early Adulthood (18 yrs < x <= 45 yrs)','Middle Adulthood (45 yrs < x <= 65 yrs)','Later Adulthood (>65 yrs)','not specified'])
        ],
        'UBERONOntologyIndex' : [
            SetValidator(valid_set=['UBERON:0001353','UBERON:0002427','UBERON:0015474','UBERON:0001970','UBERON:0000178','UBERON:0001969','UBERON:0001977','UBERON:0001153','UBERON:0001091','UBERON:0004148','UBERON:0001621','UBERON:0001555','UBERON:0001988','UBERON:0002110','UBERON:0012180','UBERON:0004907','UBERON:0002048','UBERON:0001045','UBERON:0001913','UBERON:0001707','not applicable','UBERON:0000167','UBERON:0002012','UBERON:0002016','UBERON:0001836','UBERON:0001511','UBERON:0001519','UBERON:0001513','UBERON:0001085','UBERON:0007311','UBERON:0004908','UBERON:0001088','UBERON:0000996','UBERON:0000955','UBERON:0002097','UBERON:0002387','UBERON:0001690','UBERON:0002106','UBERON:0002107','UBERON:0001264','UBERON:0000945','UBERON:0002114','UBERON:0002115','UBERON:0002116','UBERON:0001155','UBERON:0018707','UBERON:0002113','UBERON:0002369','UBERON:0000992','UBERON:0000995','UBERON:0000002','UBERON:0000948','UBERON:0003126','UBERON:0001043','UBERON:0002370','not applicable','UBERON:0002097'])
        ],
        'DOIDOntologyIndex' : [
            SetValidator(valid_set=['DOID:1485','DOID:9351','disease NOS','DOID:10763','DOID:0050589','no disease reported','not applicable','DOID:8893','no DOID avaliable','no DOID avaliable','DOID:12140','DOID:9970','DOID:12155','DOID:8778','DOID:13378','DOID:0050338','no DOID avaliable','no DOID avaliable','no DOID avaliable','not applicable','DOID:8577','DOID:216'])
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
    row_count = 0
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
        #raise
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
