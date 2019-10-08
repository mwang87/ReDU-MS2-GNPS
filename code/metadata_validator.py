#!/usr/bin/python


import sys
import os
import argparse
import csv
import json
import pandas as pd
from vladiate import Vlad
from vladiate.validators import UniqueValidator, SetValidator, Ignore, IntValidator, RangeValidator, NotEmptyValidator
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
            NotEmptyValidator()
        ],
        "MassiveID" : [
            Ignore()
        ],
        'SampleType' : [
            SetValidator(valid_set=['animal','beverage','blank_analysis','blank_extraction','blank_QC','culture_bacterial','culture_fungal','inanimate_object','environmental','built_environment','food','plant','reference material','culture_mammalian','culture_multiplespecies'])
        ],
        'SampleTypeSub1' : [
            SetValidator(valid_set=['biofluid','food_source_animal','tissue','beverage_nonalcoholic','beverage_alcoholic','blank_analysis','blank_extraction','bacterial culture','blank_QC','culture_bacterial','culture_fungal','mobile phone','keys','computer','purse_or_wallet','clothing','dissolvedorganicmatter_soil','dissolvedorganicmatter_water_saline','house','marine_invertebrates_insitu','marine_cyanobacteria_insitu','food_source_plant','food_source_complex','food_source_fungi','food_source_NOS','plant_angiospermae','plant_NOS','reference material_personalcareproduct','reference material_animalfeedorsupplement','reference material_chemicalstandard','reference material_collectionmaterial_microtubes','reference material_collectionmaterial_wellplates','not specified','not applicable','culture_mammalian','culture_multiplespecies','office','research lab','commercial_building','hospital'])
        ],
        'NCBITaxonomy' : [
            SetValidator(valid_set=['1003843|Halcyon smyrnensis','100858|Threskiornis aethiopicus','10088|Mus','10114|Rattus','10157|Myocastor coypus','1027292|Sporosarcina newyorkensis','1032505|Fusobacterium sp. OBRC1','1046468|Euphorbia hyssopifolia','1046491|Euphorbia ophthalmica','1054213|Acetobacteraceae bacterium AT-5844','1073351|Bacteroides stercoris','1073372|Streptococcus parasanguinis','1073373|Streptococcus sanguinis','1073376|Ruminococcus lactaris','1078085|Paenisporosarcina sp. HGH0030','1078764|Corynebacterium sp. HFH0082','1087772|Euphorbia nicaeensis','1087776|Euphorbia pithyusa','1095733|Streptococcus parasanguinis','109689|Chaetodon ephippium','109695|Chaetodon melannotus','109712|Pomacanthus navarchus','1100072|Eudistoma vannamei','110196|Bitis atropos','1105031|Clostridium sp. MSTE9','110555|Myxine','1111133|Peptoniphilus sp. BV3AC2','1111134|Peptoniphilus sp. BV3C26','1111454|Megasphaera sp. BV3C16-1','1115805|Staphylococcus epidermidis','1125693|Proteus mirabilis','1125694|Proteus mirabilis','1125718|Actinomyces massiliensis','1125724|Rothia aeria','1125778|Lachnoanaerobaculum sp. OBRC5-5','1129970|Euphorbia ammak','1129973|Euphorbia balsamifera subsp. balsamifera','1129992|Euphorbia fiherenensis','1129997|Euphorbia gymnocalycioides','1134785|Enterococcus faecalis','1134804|Enterococcus faecium','1134811|Enterococcus faecium','1134817|Enterococcus faecium','1134820|Enterococcus faecium','1134822|Enterococcus faecium','1134827|Enterococcus faecium','1134842|Staphylococcus aureus','113544|Arapaima gigas','1138341|Euphorbia bubalina','1138348|Euphorbia lactea','1138350|Euphorbia mammillaris','1138355|Euphorbia ornithopus','115645|Ducula bicolor','1161409|Bifidobacterium sp. MSTE12','1161413|Streptococcus sp. ACC21','1161414|Streptococcus sp. BS21','1161415|Streptococcus sp. BS29a','1161416|Streptococcus sp. SR1','1190621|Olsenella uli','119419|Tauraco schalowi','1203540|Bifidobacterium breve','1203544|Klebsiella pneumoniae','1203545|Klebsiella pneumoniae','1203546|Klebsiella pneumoniae','1203549|Microbacterium sp. oral taxon 186','1203550|Prevotella oralis','1203578|Pseudomonas sp. HPB0071','121123|Alouatta sara','1226325|Clostridium sp. KLE 1755','1227262|Actinomyces johnsonii','1227272|Porphyromonas sp. oral taxon 278','1227275|Streptococcus sobrinus','1243780|Pelecanus occidentalis californicus','1261057|Gardnerella vaginalis','1261058|Gardnerella vaginalis','1261059|Gardnerella vaginalis','1261061|Gardnerella vaginalis','1261062|Gardnerella vaginalis','1261063|Gardnerella vaginalis','1261064|Gardnerella vaginalis','1261065|Gardnerella vaginalis','1261066|Gardnerella vaginalis','1261067|Gardnerella vaginalis','1261068|Gardnerella vaginalis','1261071|Gardnerella vaginalis','1261072|Bifidobacterium breve','1280|Staphylococcus aureus','1297064|Trichechus manatus manatus','130080|Oculina patagonica','1321778|Clostridiales bacterium oral taxon 876','1334443|Chamaesyce','13442|Coffea','13489|Dicentrarchus labrax','1382|Atopobium parvulum','1386|Bacillus','1390567|Ptilinopus cinctus','1423|Bacillus subtilis','147464|Dinornis giganteus','1502|Clostridium perfringens','1543402|Geocapromys brownii','154990|Euphorbia helioscopia','168694|Salinispora','1696|Brevibacterium','170820|Hemiscyllium ocellatum','1715253|Trichoderma sp.','175825|Aceros corrugatus','184245|Tomistoma schlegelii','187114|Ducula aenea','1883|Streptomyces','190893|Vibrio coralliilyticus','194526|Gegeneophis ramaswamii','195635|Pleuronichthys verticalis','2013|Nocardiopsis','202946|Apteryx australis mantelli','209321|Euphorbia cylindrifolia','209333|Euphorbia alluaudii','209356|Euphorbia stenoclada','212836|Euphorbia prostrata','212842|Euphorbia abdelkuri','212844|Euphorbia acanthothamnos','212900|Euphorbia graminea','212925|Euphorbia lathyris','212941|Euphorbia myrsinites','212944|Euphorbia obesa','212960|Euphorbia platyclada','212981|Euphorbia sipolisii','213002|Euphorbia weberbaueri','213047|Euphorbia globosa','216475|Euphorbia dentata','216478|Euphorbia ingens','216816|Bifidobacterium longum','216998|Euphorbia jansenvillensis','216999|Euphorbia horrida','227231|Himantopus mexicanus','241562|Amazona leucocephala','2711|Citrus sinensis','28125|Prevotella bivia','28713|Lanius ludovicianus','30406|Tragopan blythii','30461|Bubo bubo','311359|Cochoa','318061|Euphorbia thymifolia','318062|Euphorbia hirta','334663|Euphorbia aeruginosa','334676|Euphorbia grandicornis','334689|Euphorbia neriifolia','33589|Leptoptilos crumeniferus','34433|Leucoagaricus','34720|Trachymyrmex septentrionalis','357276|Bacteroides dorei','3635|Gossypium hirsutum','3702|Arabidopsis thaliana','37083|Eudyptula minor','3750|Malus domestica','37578|Morus bassanus','377254|Megophrys nasuta','381107|Cinnyricinclus leucogaster','38626|Phascolarctos cinereus','38843|Euphorbia amygdaloides','38844|Euphorbia cyparissias','38845|Euphorbia dendroides','38846|Euphorbia peplus','38847|Euphorbia segetalis','403904|Onychostoma angustistomata','40833|Bucephala islandica','411481|Bifidobacterium adolescentis','411486|Clostridium sp. M62/1','41691|Cygnus melancoryphus','43311|Fratercula cirrhata','43490|Gyps africanus','435830|Actinomyces graevenitzii','435832|Neisseria mucosa','435838|Staphylococcus caprae','435842|Streptococcus sp. C150','441894|Struthio camelus australis','4441|Camellia','444138|Ducula rufigaster','44489|Carettochelys insculpta','450749|Veillonella sp. 6_1_27','457243|Euphorbia cotinifolia','457387|Bacteroides sp. 1_1_30','457393|Bacteroides sp. 4_1_36','457395|Bacteroides sp. 9_1_42FAA','457396|Clostridium sp. 7_2_43FAA','457402|Eubacterium sp. 3_1_31','457416|Veillonella sp. 3_1_44','457424|Bacteroides fragilis','469586|Bacteroides sp. 1_1_6','469587|Bacteroides sp. 2_1_16','469588|Bacteroides sp. 2_1_22','469592|Bacteroides sp. 3_1_19','469594|Bifidobacterium sp. 12_1_47BFAA','469595|Citrobacter sp. 30_2','469597|Coprobacillus sp. 8_2_54BFAA','469598|Escherichia sp. 3_2_53FAA','469599|Fusobacterium sp. 2_1_31','469608|Klebsiella sp. 1_1_55','491074|Enterococcus faecalis','491075|Enterococcus faecalis','491076|Lactobacillus crispatus','493209|Atta texana','507972|Ptilopsis granti','51861|Corallus caninus','525278|Enterococcus faecalis','525279|Enterococcus faecium','525329|Lactobacillus jensenii','525341|Lactobacillus reuteri','525361|Lactobacillus rhamnosus','525376|Staphylococcus epidermidis','525377|Staphylococcus lugdunensis','526192|Euphorbia characias subsp. wulfenii','537972|Helicobacter pullorum','545774|Streptococcus gallolyticus','54672|Euphorbia lagascae','553199|Propionibacterium acnes','553209|Enterococcus faecalis','553212|Staphylococcus capitis','556259|Bacteroides sp. D2','556266|Escherichia coli','559301|Lactobacillus gasseri','56072|Ardea herodias','56117|Tapirus bairdii','562971|Achromobacter xylosoxidans','562973|Actinomyces viscosus','562981|Gemella haemolysans','562983|Gemella sanguinis','563032|Rothia dentocariosa','563191|Acidaminococcus sp. D21','563193|Parabacteroides sp. D13','56549|Lycodon semicarinatus','5693|Trypanosoma cruzi','571338|Macrochelys temminckii','575593|Lachnospiraceae bacterium oral taxon 500','575595|Lactobacillus crispatus','575596|Lactobacillus crispatus','575597|Lactobacillus crispatus','575603|Lactobacillus gasseri','575604|Lactobacillus gasseri','575605|Lactobacillus jensenii','575607|Lactobacillus jensenii','575609|Peptoniphilus sp. oral taxon 386','575611|Prevotella buccae','575612|Prevotella melaninogenica','575615|Prevotella sp. oral taxon 317','57571|Salamandra salamandra','585466|Burhinus grallarius','585501|Oribacterium sinus','585538|Helicobacter pylori','585543|Bacteroides sp. D20','596309|Rhodococcus erythropolis','596312|Micrococcus luteus','596317|Staphylococcus epidermidis','596318|Acinetobacter radioresistens','596320|Neisseria flavescens','596322|Streptococcus salivarius','596325|Lactobacillus jensenii','596327|Porphyromonas uenonis','596330|Peptoniphilus lacrimalis','61316|Hypentelium nigricans','619693|Prevotella sp. oral taxon 472','62165|Chlorophanes spiza','629742|Staphylococcus hominis','641149|Neisseria sp. oral taxon 014','649742|Actinomyces odontolyticus','649743|Actinomyces sp. oral taxon 848','649760|Prevotella oris','649761|Prevotella veroralis','651656|Incilius','65559|Euphorbia milii','658080|Ralstonia sp. 5_2_56FAA','658082|Lachnospiraceae bacterium 2_1_58FAA','658085|Lachnospiraceae bacterium 5_1_57FAA','658087|Lachnospiraceae bacterium 7_1_58FAA','658663|Porphyromonas sp. 31_2','661087|Olsenella sp. oral taxon 809','665937|Anaerostipes sp. 3_2_56FAA','665944|Klebsiella sp. 4_1_44FAA','665945|Lactobacillus sp. 7_1_47FAA','665948|Pseudomonas sp. 2_1_26','665952|Bacillus smithii','665953|Bacteroides eggerthii','665954|Bacteroides ovatus','679189|Prevotella timonensis','679191|Prevotella amnii','679193|Propionibacterium acnes','679196|Lactobacillus gasseri','679198|Aggregatibacter aphrophilus','679202|Escherichia coli','679204|Escherichia coli','679205|Escherichia coli','679206|Escherichia coli','681183|Astrapia mayeri','689|Vibrio mediterranei','693991|Fusobacterium nucleatum','699185|Enterococcus faecalis','699186|Enterococcus faecalis','702437|Selenomonas noxia','702439|Prevotella nigrescens','704175|Phoenicoparrus minor','706437|Streptococcus anginosus','7102|Helicoverpa virescens','71240|eudicotyledons','740693|Cephaloscyllium ventriosum','742722|Collinsella sp. 4_8_47FAA','742730|Citrobacter freundii','742732|[Clostridium] bolteae','742735|Clostridium clostridioforme','742736|Clostridium clostridioforme','742737|Clostridium hathewayi','742738|Clostridium orbiscindens','742740|Clostridium symbiosum','742741|Clostridium symbiosum','749491|Enterococcus faecalis','749523|Enterococcus faecium','749527|Escherichia coli','749529|Escherichia coli','749531|Escherichia coli','749535|Klebsiella sp. MS 92-3','749536|Escherichia coli','749537|Escherichia coli','749542|Escherichia coli','749548|Escherichia coli','749549|Escherichia coli','749550|Escherichia coli','75024|Holacanthus ciliaris','754025|Staphylococcus aureus','754026|Staphylococcus aureus','75988|Pachymedusa dacnicolor','762963|Actinomyces sp. oral taxon 170','762965|Haemophilus sp. oral taxon 851','765065|Propionibacterium acnes','765066|Propionibacterium acnes','765067|Propionibacterium acnes','765068|Propionibacterium acnes','765069|Propionibacterium acnes','765070|Propionibacterium acnes','765071|Propionibacterium acnes','765072|Propionibacterium acnes','765073|Propionibacterium acnes','765074|Propionibacterium acnes','765077|Propionibacterium acnes','765079|Propionibacterium acnes','765080|Propionibacterium acnes','765084|Propionibacterium acnes','765085|Propionibacterium acnes','765089|Propionibacterium acnes','765090|Propionibacterium acnes','765091|Propionibacterium acnes','765092|Propionibacterium acnes','765093|Propionibacterium acnes','765095|Propionibacterium acnes','765096|Propionibacterium acnes','765097|Propionibacterium acnes','765098|Propionibacterium acnes','765099|Propionibacterium acnes','765100|Propionibacterium acnes','765101|Propionibacterium acnes','765102|Propionibacterium acnes','765103|Propionibacterium acnes','765104|Propionibacterium acnes','765105|Propionibacterium acnes','765106|Propionibacterium acnes','765107|Propionibacterium acnes','765108|Propionibacterium acnes','765109|Propionibacterium acnes','765110|Propionibacterium acnes','765111|Propionibacterium acnes','765112|Propionibacterium acnes','765113|Propionibacterium acnes','765114|Propionibacterium acnes','765115|Propionibacterium acnes','765116|Propionibacterium acnes','765117|Propionibacterium acnes','765118|Propionibacterium acnes','765119|Propionibacterium acnes','765121|Propionibacterium acnes','765122|Propionibacterium acnes','765123|Propionibacterium acnes','767100|Parvimonas sp. oral taxon 110','768724|Peptoniphilus sp. oral taxon 836','78394|Eptatretus cirrhatus','7897|Latimeria chalumnae','797473|Cardiobacterium valvarum','797515|Lactobacillus parafarraginis','797516|Lactobacillus kisonensis','81903|Fulica americana','83391|Coryphaenoides cinereus','8450|Hypogeophis rostratus','8467|Caretta caretta','8503|Crocodylus novaeguineae','85101|Urocolius macrourus','8557|Varanus exanthematicus','857291|Prevotella histicola','86377|Taeniura lymma','864566|Campylobacter coli','8682|Hydrophis schistosus','873517|Capnocytophaga ochracea','8790|Dromaius novaehollandiae','879296|Lactobacillus iners','879301|Lactobacillus iners','879302|Lactobacillus iners','879304|Lactobacillus iners','879307|Gardnerella vaginalis','879309|Veillonella sp. oral taxon 158','8797|Rhea americana','8801|Struthio camelus','883109|Eubacterium infirmum','883116|Klebsiella oxytoca','883117|Klebsiella oxytoca','883118|Klebsiella oxytoca','883119|Klebsiella oxytoca','883120|Klebsiella oxytoca','883121|Klebsiella oxytoca','883123|Klebsiella oxytoca','883124|Klebsiella oxytoca','883125|Klebsiella oxytoca','883167|Streptococcus intermedius','8863|Coscoroba coscoroba','888050|Actinomyces cardiffensis','888051|Actinomyces sp. oral taxon 178','8884|Oxyura jamaicensis','888825|Streptococcus sanguinis','888826|Campylobacter upsaliensis','888827|Arcobacter butzleri','8924|Vultur gryphus','8961|Aquila audax','904293|Streptococcus downei','904306|Streptococcus vestibularis','908340|Clostridium sp. HGF2','91789|Capito niger','9258|Ornithorhynchus anatinus','92683|Spheniscus demersus','928327|Lactobacillus iners','9316|Macropus fuliginosus','936556|Peptostreptococcaceae bacterium AS15','936562|Fusobacterium sp. CM21','936563|Fusobacterium sp. CM22','936565|Klebsiella sp. OBRC7','936575|Streptococcus sp. AC15','936576|Streptococcus sp. ACS2','936578|Streptococcus sp. AS20','936580|Streptococcus sp. CM6','936581|Streptococcus sp. CM7','936587|Streptococcus sp. OBRC6','936588|Veillonella sp. ACP1','936589|Veillonella sp. AS16','936594|Lachnoanaerobaculum sp. ICM7','944562|Lactobacillus oris','944564|Veillonella sp. oral taxon 780','9600|Pongo pygmaeus','9606|Homo sapiens','9636|Melursus ursinus','9755|Physeter catodon','979202|Staphylococcus epidermidis','979203|Staphylococcus epidermidis','979211|Staphylococcus epidermidis','979213|Staphylococcus epidermidis','979214|Staphylococcus epidermidis','979215|Staphylococcus epidermidis','979216|Staphylococcus epidermidis','979217|Staphylococcus epidermidis','979218|Staphylococcus epidermidis','979219|Staphylococcus epidermidis','979221|Staphylococcus epidermidis','979222|Staphylococcus epidermidis','9913|Bos taurus','997346|Desmospora sp. 8437','997873|Bacteroides caccae','997874|Bacteroides cellulosilyticus','997875|Bacteroides dorei','997876|Bacteroides dorei','997879|Bacteroides fragilis','997882|Bacteroides fragilis','997883|Bacteroides fragilis','997887|Bacteroides salyersiae','997888|Bacteroides finegoldii','997891|Bacteroides vulgatus','999414|Fusobacterium nucleatum','999419|Parabacteroides johnsonii','999420|Parabacteroides merdae','999421|Parabacteroides merdae','999427|Treponema denticola','999440|Treponema denticola','none specified|Euherdmania','not applicable','not collected','not specified','not specified|Euphorbia pithyusa ssp. cupanii','73337|Ceratotherium simum simum','70919|Sarcophyton glaucum','205097|Sarcophyton trocheliophorum','358796|Sarcophyton cinereum'])
        ],
        'YearOfAnalysis' : [
            IntValidator(),
            RangeValidator(low=2000, high=2030)
        ],
        'SampleCollectionMethod' : [
            SetValidator(valid_set=['blood draw, capillary','blood draw, venous','blood NOS','liquid','not applicable','solid material, dried','solid material, fresh','solid material, frozen','swabs, dry','swabs, moist (50% EtOH)','urine, 24-hour','urine, NOS','urine, spot','extract, solid phase extraction (C18)','liquid, solid phase extraction (C18)','solid, solid phase extraction (C18)','solid material, NOS','not specified','liquid, solid phase extraction (PPL)'])
        ],
        "SampleExtractionMethod" : [
            SetValidator(valid_set=['ethanol-water (9:1)','methanol-water (1:1)','dichloromethane-methanol (2:1)','ethanol-water (19:1)','water (94_deg_C)','water (95_deg_C)','water (100%) (deg_C_NOS)','chloroform-methanol-water (1:3:1)','methanol (100%)','ethanol (100%)','ethanol-water (1:1)','water-acetonitrile (250:1)','methanol-acetonitrile (3:7)','methanol-water (4:1)','methanol-water (9:1)','not collected','ethyl acetate (100%)','methanol-water (7:3)','water-acetonitrile (149:1)','not specified','methanol-water (3:2)','acetonitrile (100%)','acetonitrile-water (7:3)','acetonitrile-methanol (1:1)','acetonitrile-isopropanol-water (3:3:2)','dichloromethane-methanol (3:1)','dichloromethane-methanol (1:1)'])
        ],
        'InternalStandardsUsed' : [
            SetValidator(valid_set=['sulfamethizole;sulfachloropyridazine','sulfamethazine','sulfamethazine;sulfadimethoxine','sulfadimethoxine','sulfamethizole;sulfachloropyridazine;sulfadimethoxine;sulfamethazine;coumarin-314;amitryptiline','amitryptiline','none','fluconazole','amitryptiline;fluconazole','sulfadimethoxine;sulfachloropyridazine','cholic_acid-d4;lithocholic_acid-d4','cocaine;cocaine-d3','cocaine-d3','sulfamethizole','not specified'])
        ],        
       'MassSpectrometer' : [
            SetValidator(valid_set=['impact|MS:1002077','impact HD|MS:1002667','Q Exactive|MS:1001911','Q Exactive Plus|MS:1002634','micrOTOF-Q II|MS:1000704','not specified','6540 Q-TOF LC/MS|MS:1002789','LTQ Orbitrap XL|MS:1000556','maXis II|MS:1003004','Xevo G2 XS Tof|MS:1002729'])
        ],        
        'IonizationSourceAndPolarity' : [
            SetValidator(valid_set=['electrospray ionization (positive)','electrospray ionization (negative)','atmospheric pressure chemical ionization (positive)','atmospheric pressure chemical ionization (negative)','atmospheric pressure photoionization (positive)','atmospheric pressure photoionization (negative)','electrospray ionization (alternating)','not specified'])
        ],
        'ChromatographyAndPhase' : [
            SetValidator(valid_set=['reverse phase (C18)','reverse phase (C8)','reverse phase (Phenyl-Hexyl)','normal phase (HILIC)','mixed mode (Scherzo SM-C18)','not specified','reverse phase (polar-C18)'])
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
