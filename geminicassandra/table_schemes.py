#!/usr/bin/env python

def get_column_names(table):
    return tables[table]

tables = dict([
                   
('variant_impacts', ['variant_id',
                'anno_id',
                'gene',
                'transcript',
                'is_exonic',
                'is_coding',
                'is_lof',
                'exon',
                'codon_change',
                'aa_change',
                'aa_length',
                'biotype',
                'impact',
                'impact_so',
                'impact_severity',
                'polyphen_pred',
                'polyphen_score',
                'sift_pred',
                'sift_score']),
                
('samples', ['sample_id',
                'family_id',
                'name',
                'paternal_id',
                'maternal_id',
                'sex',
                'phenotype']),

('gene_detailed', ['uid',
                'chrom',
                'gene',
                'is_hgnc',
                'ensembl_gene_id',
                'transcript',
                'biotype',
                'transcript_status',
                'ccds_id',
                'hgnc_id',
                'entrez_id',
                'cds_length',
                'protein_length',
                'transcript_start',
                'transcript_end',
                'strand',
                'synonym',
                'rvis_pct',
                'mam_phenotype_id']),

('gene_summary', ['uid',
                'chrom',
                'gene',
                'is_hgnc',
                'ensembl_gene_id',
                'hgnc_id',
                'transcript_min_start',
                'transcript_max_end',
                'strand',
                'synonym',
                'rvis_pct',
                'mam_phenotype_id',
                'in_cosmic_census']),

('vcf_header',  ['vcf_header']),

('version', ['version']),
 
('resources',  ['name',
             'resource']),
                
('variants_by_sub_type_call_rate', ['variant_id',
                                   'sub_type',
                                   'call_rate']),
                
('variants_by_chrom_depth', ['variant_id',
                             'chrom',
                             'depth']),
('variants', ['variant_id',
            'chrom',
            'start',
            '\"end\"',
            'vcf_id',
            'anno_id',
            'ref',
            'alt',
            'qual',
            'filter',
            'type',
            'sub_type',
            'call_rate',
            'in_dbsnp',
            'rs_ids',
            'sv_cipos_start_left',
            'sv_cipos_end_left',
            'sv_cipos_start_right',
            'sv_cipos_end_right',
            'sv_length',
            'sv_is_precise',
            'sv_tool',
            'sv_evidence_type',
            'sv_event_id',
            'sv_mate_id',
            'sv_strand',
            'in_omim',
            'clinvar_sig',
            'clinvar_disease_name',
            'clinvar_dbsource',
            'clinvar_dbsource_id',
            'clinvar_origin',
            'clinvar_dsdb',
            'clinvar_dsdbid',
            'clinvar_disease_acc',
            'clinvar_in_locus_spec_db',
            'clinvar_on_diag_assay',
            'clinvar_causal_allele',
            'pfam_domain',
            'cyto_band',
            'rmsk',
            'in_cpg_island',
            'in_segdup',
            'is_conserved',
            'gerp_bp_score',
            'gerp_element_pval',
            'num_hom_ref',
            'num_het',
            'num_hom_alt',
            'num_unknown',
            'aaf',
            'hwe',
            'inbreeding_coeff',
            'pi',
            'recomb_rate',
            'gene',
            'transcript',
            'is_exonic',
            'is_coding',
            'is_lof',
            'exon',
            'codon_change',
            'aa_change',
            'aa_length',
            'biotype',
            'impact',
            'impact_so',
            'impact_severity',
            'polyphen_pred',
            'polyphen_score',
            'sift_pred',
            'sift_score',
            'anc_allele',
            'rms_bq',
            'cigar',
            'depth',
            'strand_bias',
            'rms_map_qual',
            'in_hom_run',
            'num_mapq_zero',
            'num_alleles',
            'num_reads_w_dels',
            'haplotype_score',
            'qual_depth',
            'allele_count',
            'allele_bal',
            'in_hm2',
            'in_hm3',
            'is_somatic',
            'somatic_score',
            'in_esp',
            'aaf_esp_ea',
            'aaf_esp_aa',
            'aaf_esp_all',
            'exome_chip',
            'in_1kg',
            'aaf_1kg_amr',
            'aaf_1kg_eas',
            'aaf_1kg_sas',
            'aaf_1kg_afr',
            'aaf_1kg_eur',
            'aaf_1kg_all',
            'grc',
            'gms_illumina',
            'gms_solid',
            'gms_iontorrent',
            'in_cse',
            'encode_tfbs',
            'encode_dnaseI_cell_count',
            'encode_dnaseI_cell_list',
            'encode_consensus_gm12878',
            'encode_consensus_h1hesc',
            'encode_consensus_helas3',
            'encode_consensus_hepg2',
            'encode_consensus_huvec',
            'encode_consensus_k562',
            'vista_enhancers',
            'cosmic_ids',
            'info',
            'cadd_raw',
            'cadd_scaled',
            'fitcons',
            'in_exac',
            'aaf_exac_all',
            'aaf_adj_exac_all',
            'aaf_adj_exac_afr',
            'aaf_adj_exac_amr',
            'aaf_adj_exac_eas',
            'aaf_adj_exac_fin',
            'aaf_adj_exac_nfe',
            'aaf_adj_exac_oth',
            'aaf_adj_exac_sas'])])    
