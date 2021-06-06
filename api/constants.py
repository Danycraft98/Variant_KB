from itertools import repeat

# Constants
BRANCH_CHOICES = [
    ('no', 'No Disease'),
    ('gp', 'Germline Pathogenicity'),
    ('so', 'Somatic Oncogenicity')
]

GP_DX_CHOICES = [
    [None, 'Select'],
    ['AIP', [list(repeat('Familial isolated pituitary adenoma', 2))]],
    ['APC', [list(repeat('Familial adenomatous polyposis', 2))]],
    ['APOA1', [list(repeat('Familial amyloidosis', 2))]],
    ['APOA2', [list(repeat('Familial amyloidosis', 2))]],
    ['ATM', [list(repeat('Ataxia telangiectasia (AR)', 2)), list(repeat('ATM associated cancer suceptibility', 2))]],
    ['AXIN2', [list(repeat('Attenuated familial adenomatous polyposis', 2))]],
    ['B2M', [list(repeat('Familial amyloidosis', 2))]],
    ['BAP1', [list(repeat('BAP1 tumor presisposion syndrome', 2))]],
    ['BARD1', [list(repeat('BARD1 associated cancer suceptibility', 2))]],
    ['BMPR1A', [list(repeat('Juvenile polyposis', 2))]],
    ['BRCA1', [list(repeat('Hereditary breast/ovarian cancer syndrome', 2))]],
    ['BRCA2', [list(repeat('Hereditary breast/ovarian cancer syndrome', 2))]],
    ['BRIP1', [list(repeat('BRIP1 associated cancer suceptibility', 2))]],
    ['CACNA1S', [list(repeat('Malignant hyperthermia, Hypokalemic periodic paralysis', 2))]],
    ['CDC73', [list(repeat('Hereditary hyperparathyroidism', 2))]],
    ['CDH1', [list(repeat('Hereditary diffuse gastric cancer', 2))]],
    ['CDK4', [list(repeat('Familial melanoma', 2))]],
    ['CDKN1B', [list(repeat('Multiple endocrine neoplasia 1', 2))]],
    ['CDKN2A', [list(repeat('CDKN2A associated cancer suceptibility', 2))]],
    ['CHEK2', [list(repeat('CHEK2 associated cancer suceptibility', 2))]],
    ['CTNNA1', [list(repeat('CTNNA1 associated cancer suceptibility', 2))]],
    ['DICER1', [list(repeat('DICER1 syndrome', 2))]],
    ['EGFR', [list(repeat('Suceptibility to lung cancer', 2))]],
    ['EPCAM', [list(repeat('Lynch syndrome', 2))]],
    ['FGA', [list(repeat('Familial amyloidosis', 2))]],
    ['FH', [list(repeat('FH deficiency (AR)', 2)), list(repeat('HLRCC', 2))]],
    ['FLCN', [list(repeat('Birt-Hogg-Dube syndrome', 2))]],
    ['GALNT12', [list(repeat('GALNT12 polyposis', 2))]],
    ['GREM1', [list(repeat('GREM1 polyposis', 2))]],
    ['GSN', [list(repeat('Familial amyloidosis', 2))]],
    ['HOXB13', [list(repeat('Familial prostate cancer', 2))]],
    ['KIT', [list(repeat('Familial GIST', 2))]],
    ['LYZ', [list(repeat('Familial amyloidosis', 2))]],
    ['LZTR1', [list(repeat('Noonan syndrome (AR)', 2)), list(repeat('Suceptibility to schwannomatosis', 2))]],
    ['MAX', [list(repeat('Suceptibility to pheochromocytoma', 2))]],
    ['MEN1', [list(repeat('Multiple endocrine neoplasia 1', 2))]],
    ['MET', [list(repeat('Hereditary papillary renal cancer', 2))]],
    ['MITF', [list(repeat('Familial renal cancer and melanoma', 2))]],
    ['MLH1', [list(repeat('Lynch syndrome', 2))]],
    ['MUTYH', [list(repeat('MUTYH polyposis (AR)', 2))]],
    ['NBN', [list(repeat('Nijmegen breakage syndrome', 2))]],
    ['NF1', [list(repeat('Neurofibromatosis 1', 2))]],
    ['NF2', [list(repeat('Neurofibromatosis 2', 2))]],
    ['NTHL1', [list(repeat('Familial adenomatous polyposis', 2))]],
    ['PALB2', [list(repeat('PALB2 associated cancer suceptibility', 2))]],
    ['PDGFRA', [list(repeat('Familial GIST', 2))]],
    ['PMS2', [list(repeat('Constitutional mismatch repair deficiency syndrome (AR)', 2)), list(repeat('Lynch syndrome', 2))]],
    ['POLD1', [list(repeat('Familial colorectal cancer', 2))]],
    ['POLE', [list(repeat('Familial colorectal cancer', 2))]],
    ['POT1', [list(repeat('Familial melanoma', 2))]],
    ['PRKAR1A', [list(repeat('Carney complex', 2))]],
    ['PTCH1', [list(repeat('Basal cell nevus syndrome', 2))]],
    ['PTEN', [list(repeat('PTEN hamartoma tumour syndrome', 2))]],
    ['RAD51C', [list(repeat('RAD51C associated cancer suceptibility', 2))]],
    ['RAD51D', [list(repeat('RAD51D associated cancer suceptibility', 2))]],
    ['RB1', [list(repeat('Retinoblastoma', 2))]],
    ['RET', [list(repeat('Multiple endocrine neoplasia 2', 2))]],
    ['RNF43', [list(repeat('Sessile serated polyposis cancer syndrome', 2))]],
    ['RYR1', [list(repeat('Malignant hyperthermia', 2)), list(repeat('RYR1 myopathy', 2))]],
    ['SDHA', [list(repeat('Hereditary pheochromocytoma-paraganglioma syndrome', 2))]],
    ['SDHAF2', [list(repeat('Hereditary pheochromocytoma-paraganglioma syndrome', 2))]],
    ['SDHB', [list(repeat('Hereditary pheochromocytoma-paraganglioma syndrome', 2))]],
    ['SDHC', [list(repeat('Hereditary pheochromocytoma-paraganglioma syndrome', 2))]],
    ['SDHD', [list(repeat('Hereditary pheochromocytoma-paraganglioma syndrome', 2))]],
    ['SMAD4', [list(repeat('Juvenile polyposis', 2))]],
    ['SMARCA4', [list(repeat('Rhabdoid tumor predisposition', 2))]],
    ['SMARCB1', [list(repeat('Rhabdoid tumor predisposition', 2))]],
    ['SMARCE1', [list(repeat('Rhabdoid tumor predisposition', 2))]],
    ['STK11', [list(repeat('Peutz-Jeghers syndrome', 2))]],
    ['SUFU', [list(repeat('Basal cell nevus syndrome', 2)), list(repeat('Joubert syndrome (AR)', 2))]],
    ['TMEM127', [list(repeat('Hereditary pheochromocytoma-paraganglioma syndrome', 2))]],
    ['TP53', [list(repeat('Li-Fraumeni syndrome', 2))]],
    ['TSC1', [list(repeat('Tuberous sclerosis', 2))]],
    ['TSC2', [list(repeat('Tuberous sclerosis', 2))]],
    ['TTR ', [list(repeat('Familial amyloidosis', 2))]],
    ['VHL', [list(repeat('Von Hippel-Lindau syndrome', 2))]]
]

SO_DX_CHOICES = [
    [None, 'Select'],
    ["Hereditary Panel - Somatic DICER1", [list(repeat("Sex Cord Stromal Tumor", 2))]],
    ["BCR-ABL1 KDM", [list(repeat("BCR-ABL1 KDM", 2))]],
    ["Myeloid Panel", [list(repeat("AML", 2)), list(repeat("MPN", 2)), list(repeat("ALL", 2))]],
    ["KIT ex 17 Sanger", [list(repeat("Mastocytosis", 2)), list(repeat("JAK2/CALR", 2)), list(repeat("MPN", 2))]],
    ["TST15", [list(repeat("Colorectal Cancer", 2)), list(repeat("Skin Cancer", 2)), list(repeat("GIST", 2)),
               list(repeat("NSCLC", 2)), list(repeat("Sex Cord Stromal Tumor", 2)), list(repeat("CLL", 2))]],
    ["IDH1/2", [list(repeat("Glioma", 2)), list(repeat("AML", 2))]],
    ["Melanoma Panel", [list(repeat("Skin Cancer", 2)), list(repeat("NSCLC", 2))]],
    ["PRKD1 Sanger", [list(repeat("PLGA", 2))]],
    ["Somatic BRCA", [list(repeat("High Grade Serous Carcinoma", 2))]],
    ["Oncomine", [list(repeat("Urothelial Carcinoma", 2)), list(repeat("NSCLC", 2)), list(repeat("Breast Cancer", 2))]],
    ["BioDiva/Venus",
     [list(repeat("High Grade Serous Carcinoma", 2)), list(repeat("Cervical Cancer", 2)), list(repeat("Endometrial Cancer", 2)),
      list(repeat("Adult Ovarian Granulosa Cell Tumour", 2)), list(repeat("Hydatidiform Mole", 2))]],
    # ["OCTANE", ["Brain/CNS Cancer", "Colorectal Cancer", "Neuroendocrine Tumour", "Adrenal Carcinoma", "Bladder Cancer",
    #            "Penile Cancer", "Prostate Cancer", "Renal Cancer", "Cervical Cancer", "High Grade Serous Carcinoma",
    #            "Endometrial Cancer", "Esophageal Cancer", "Nasopharyngeal Cancer", "Oropharyngeal Cancer",
    #            "Salivary Cancer", "Thyroid Cancer", "Liver Cancer", "Lung Cancer", "Pancreatobiliary Cancer",
    #            "Sarcoma", "Cancer of Unknown Primary"]]
]

ITEMS = {  # 'PVS1 - SA': ['Stand Alone - whole gene deletion', 10],
    'PVS1': ['nonsense, fs, +/-2 splice site, start loss, whole exon deletion', 10],

    'PS1': ['same aa change as previously published, intragenic exon duplication', 7],
    'PS2': ['confirmed de novo, no FHx (rarely applied)', 7],
    'PS3': ['well-established functional studies', 7],
    'PS4': ['prevalence affected >>> controls (case control studies)', 7],

    'PM': ['previously reported in affected, not in controls', 2],
    'PM1': ['mutational hot spot, functional domain (rarely applied)', 2],
    'PM2': ['absent from or low freq in controls (gnomAD)', 2],
    'PM3': ['in trans with pathogenic in recessive disorder (rarely applied)', 2],
    'PM4': ['altered protein length (in-frame nonlist(repeat or stop loss; rarely applied)', 2],
    'PM5': ['novel aa at previously reported pathogenic codon', 2],
    'PM6': ['assumed de novo (rarely applied)', 2],

    'PP1': ['cosegregation in multiple family members (rarely applied)', 1],
    'PP2': ['missense in rarely mutated gene; missense = mechanism (rarely applied)', 1],
    'PP3': ['in silico prediction', 1],
    'PP4': ['phenotype or FHx is highly specific for a disorder (rarely applied)', 1],
    'PP5': ['reputable source (e.g. ClinVar, LSDB, etc.)', 1],

    'BA1': ['common polymorphism; allele frequency > 5%', 16],

    'BS1': ['allele frequency > expected (HW equilibrium)', 8],
    'BS2': ['observed in healthy adult (assuming full penetrance; rarely applied)', 8],
    'BS3': ['well-established functional studies', 8],
    'BS4': ['lack of segregation in affected family members', 8],

    'BP1': ['missense when truncating variants are deleterious (rarely applied)', 1],
    'BP2': ['in trans with pathogenic in AD or cis with pathogenic AD/AR', 1],
    'BP3': ['in-frame del/ins in repetitive region w/o known function (rarely applied)', 1],
    'BP4': ['in silico prediction', 1], 'BP5': ['in case with alternate basis for disease', 1],
    'BP6': ['reputable source', 1], 'BP7': ['synonymous variant (not splice)', 1]}

FUNC_SIG_CHOICES = [
    (None, 'Select'),
    ('Established', 'Established Significance'),
    ('Likely', 'Likely Significance'),
    ('Predicted', 'Predicted/Possible Significance'),
    ('VUS', 'Uncertain Significance'),
    ('Benign', 'Benign')
]

FUNC_CAT_CHOICES = [
    (None, 'Select'),
    ('GOF', 'GOF'),
    ('LOF', 'LOF'),
    ('TP53 functional', 'TP53 functional'),
    ('TP53 non-functional', 'TP53 non-functional'),
    ('BRAF Class I', 'BRAF Class I'),
    ('BRAF Class II', 'BRAF Class II'),
    ('BRAF Class III', 'BRAF Class III')
]

TIER_CHOICES = [
    (None, 'Select'),
    ('Tier I', 'Tier I'),
    ('Tier II', 'Tier II'),
    ('Tier III', 'Tier III'),
    ('Tier IV', 'Tier IV')
]

TYPE_CHOICES = [
    (None, 'Select'),
    ('PM', 'PMID'),
    ('O', 'Others')
]

EVID_SIG_CHOICES = [
    (None, 'Select'),
    ('Pred', 'Predictive'),
    ('Prog', 'Prognostic'),
    ('Diag', 'Diagnostic')
]

EVID_LEVEL_CHOICES = [
    (None, 'Select'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E')
]

EVID_DIR_CHOICES = [
    (None, 'Select'),
    (True, 'Support'),
    (False, 'Does Not Support')
]

CLIN_SIG_CHOICES = [
    (None, 'Select'),
    ('Pred: Resistance', 'Pred: Resistance'),
    ('Pred: Adverse Response', 'Pred: Adverse Response'),
    ('Pred: Reduced Sensitivity', 'Pred: Reduced Sensitivity'),
    ('Pred: Sensitivity', 'Pred: Sensitivity'),
    ('Prog: Better Outcome', 'Prog: Better Outcome'),
    ('Prog: Poorer Outcome', 'Prog: Poorer Outcome'),
    ('Dx: Positive Diagnosis', 'Dx: Positive Diagnosis'),
    ('Dx: Negative Diagnosis', 'Dx: Negative Diagnosis')
]

EVID_RATING_CHOICES = [
    (0, 'Select'),
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
]

REVIEWED_CHOICES = [
    ('n', 'Not Reviewed'),
    ('r', 'Reviewed'),
    ('m', 'Secondly Reviewed'),
    ('a', 'Approved'),
]

CLASS_TO_PREFIX = {'Disease': 'dx', 'Score': 'score', 'Evidence': 'act', 'Report': 'report'}

RETURN_TYPE = {
    'dx': ['name', 'report'], 'score': ['for_score', 'against_score', 'content'],
    'func': ['item', 'source_id', 'source_type', 'statement'],
    'path_item': ['item', 'source_id', 'source_type', 'statement'],
    'act': ['source_id', 'source_type', 'statement', 'evid_sig', 'evid_dir', 'level', 'clin_sig', 'drug_class', 'evid_rating'],
    'evid': ['source_id', 'source_type', 'statement'],
    'report': ['report_name', 'content'],
}

REPORT_NAMES = ['Gene-Descriptive', 'Variant-Descriptive', 'Gene-Disease', 'Variant-Disease',
                'Gene-Germline Implications', 'Variant-Germline Implications']
