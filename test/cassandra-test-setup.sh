export TIME="exp1, %E"
touch measurements

/usr/bin/time -o measurements geminicassandra load --test-mode -v test.query.vcf --skip-gerp-bp --skip-cadd -t snpEff -db "127.0.0.1" -ks test_query_db --cores 3 
/usr/bin/time -a -o measurements geminicassandra load --skip-gene-tables --test-mode -p test_extended_ped.ped -v test4.vep.snpeff.vcf  --skip-gerp-bp --skip-cadd -t snpEff -db "127.0.0.1" -ks extended_ped_db --cores 3
/usr/bin/time -a -o measurements geminicassandra load --skip-gene-tables --test-mode -v test.snpeff.vcf --skip-gerp-bp --skip-cadd -t snpEff -db "127.0.0.1" -ks test_snpeff_vcf_db --cores 3
geminicassandra load --skip-gene-tables --test-mode -v test.exac.vcf --skip-gerp-bp --skip-cadd -db "127.0.0.1" -ks test_exac_db --cores 3 
geminicassandra load --skip-gene-tables --test-mode -v test3.snpeff.vcf --skip-gerp-bp --skip-cadd -db "127.0.0.1" -ks test3_snpeff_db --cores 3
geminicassandra load --skip-gene-tables --test-mode -v test.vcf_id.snpeff.vcf  --skip-gerp-bp --skip-cadd -t snpEff -db "127.0.0.1" -ks test_vcf_id_snpeff_vcf_db --cores 3
geminicassandra load --skip-gene-tables --test-mode -v test2.snpeff.vcf --skip-gerp-bp --skip-cadd -db "127.0.0.1" -ks test2_snpeff_db --cores 3
geminicassandra load --skip-gene-tables --test-mode -v test.clinvar.vcf --skip-gerp-bp --skip-cadd -db "127.0.0.1" -ks test_clinvar_db
geminicassandra load --skip-gene-tables --test-mode -p test.de_novo.ped -v test.family.vcf  --skip-gerp-bp --skip-cadd -t snpEff -db "127.0.0.1" -ks test_family_db
geminicassandra load --skip-gene-tables --test-mode -v test4.vep.snpeff.vcf --skip-gerp-bp --skip-cadd -t snpEff -db "127.0.0.1" -ks test4_snpeff_db --cores 3
geminicassandra load --skip-gene-tables --test-mode -p test4.snpeff.ped -v test4.vep.snpeff.vcf --skip-gerp-bp --skip-cadd -t snpEff -db "127.0.0.1" -ks test4_snpeff_ped_db
