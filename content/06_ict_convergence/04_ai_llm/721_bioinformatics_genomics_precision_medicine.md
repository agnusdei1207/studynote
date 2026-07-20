---
title: "Bioinformatics Genomics Precision Medicine"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 721
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NGS(Next-Generation Sequencing) 기반의 WGS/WES/RNA-seq 데이터로부터 BWA-MEM -> GATK HaplotypeCaller/DeepVariant 기반의 변이 호출(Variant Calling)과 VEP/ANNOVAR를 통한 임상 주석(Annotation), PharmGKB/ClinVar 기반의 의학적 해석(Clinical Interpretation)을 거쳐 환자에게 최적화된 약물·예후·위험도를 도출하는 GA4GH/VCF 표준 기반의 정밀의료 파이프라인이다.
> 2. **가치**: 전장유전체 분석 시간은 2003년 Human Genome Project의 13년/$3B에서 2024년 NovaSeq X Plus 기준 24시간/$200 수준으로 1,500만 배 이상 단가 절감이 실현되었으며, 약물유전체(Pharmacogenomics) 적용 시 항응고제·항암제 등에서 입원 30%·이상반응 40% 감소 등 임상적 효용이 입증되었다.
> 3. **판단 포인트**: 단축 변이(short variant)·구조 변이(SV)·복제수 변이(CNV)·미세 위성 불안정성(MSI)·TMB(Tumor Mutational Burden)·HLA 타이핑 등 분석 범위에 따라 BAM/CRAM(±30~150GB/WGS), 참조 패널(gnomAD, 1000 Genomes, Kaviar) 선택, Germline/Somatic 분리, gVCB Joint-calling, 그리고 CAP/CLIA/HIPAA·유전체법(2023.8 시행)·생명윤리법 준수 여부가 핵심 의사결정 사항이다.

---

## Ⅰ. 개요 및 필요성

정밀의료(Precision Medicine)는 2015년 오바마 행정부의 PMI(Precision Medicine Initiative, $215M 예산)와 2016년 미국 NCI의 NCI-MATCH, 2017년 FDA의 FoundationOne CDx 승계 이후 본격화되었으며, 국내에서는 2023년 8월 5일 「유전체의료법」(이하 유전체법) 시행으로 보건복지부 지정 유전체의료기관(현재 약 30개소)을 중심으로 임상에 정착되고 있다. 핵심 패러다임 전환은 "증상->약 처방"의 Reactive 의료에서 "유전체 정보->위험 예측/약물 반응성/맞춤 치료"의 Proactive 의료로의 이동이며, 이를 가능케 하는 것이 바이오인포매틱스 파이프라인이다.

과거 Sanger sequencing(±1kb/run, $0.5/bp, ABI 3730xl) 기반의 단일 유전자 검사는 BRCA1/2, EGFR 등 일부 유전자에 국한되었으나, NGS(예: Illumina NovaSeq 6000, 6Tb/3일, DNBSEQ T7, PacBio Revio HiFi, Oxford Nanopore PromethION)의 등장으로 1인당 30× WGS 약 120GB raw data, 30× WES 약 12GB, RNA-seq 약 10~30GB 규모에서 multi-gene panel(예: Illumina TruSight Oncology 500, 523-gene, 1.94Mb) -> WES -> WGS로 분석 해상도가 비약적으로 확대되었다. 이에 따라 데이터 폭증(데이터lake, 1병원 연 5PB+), 변이 해석의 복잡도(평균 1인당 4.1~5M 변이, 100~400 rare variant), 그리고 임상 보고서 작성(CAP/AMP/NCCN 가이드라인, AMP/ASCO/CAP 4-tier system)·유전상담·결과 통보의 임상적 책임 문제가 대두되었다.

```text
[정밀의료 데이터 파이프라인 End-to-End Flow]

   +--------------------------------------------------------------------------+
   |                          1차 임상 데이터 입력 단계                        |
   +--------------------------------------------------------------------------+
   환자 임상정보 -+
   가족력(Pedigree)-+
   약물이력(PDDF)---+    +----------+    +--------------+
   표본(혈액/조직)--+---->| LIMS     |---->|   NGS 장비   |
   동의서(Informed)-+    |(Lab Info)|    |(NovaSeq/ONT) |
                         +----------+    +------+-------+
                                                | FASTQ.gz (Phred Q30>85%)
                                                v
   +--------------------------------------------------------------------------+
   |                  2차 데이터 처리 (Primary/Secondary)                      |
   +--------------------------------------------------------------------------+
   +--------------------------+
   | Raw Data QC              |  FastQC, MultiQC, fastp, Trimmomatic
   | Adapter/Quality Trim     |  Q20>95%, Adapter trim, N-base cut
   +-------------+------------+
                 v
   +--------------------------+
   | Alignment & BQSR        |  BWA-MEM2 / minimap2 / STAR
   |  Reference: GRCh38/CHM13|  -> SAM/BAM/CRAM(CRAM 50% 절감)
   |  MarkDuplicates(UMI?)   |  Picard / Sambamba / biobambam2
   |  BQSR(GATK), Recal      |  Base Quality Score Recalibration
   +-------------+------------+
                 v
   +--------------------------+
   | Variant Calling          |  GATK HaplotypeCaller (gvcf)
   |  Germline: DeepVariant,  |  Strelka2, GLnexus(Joint-call)
   |  Somatic: Mutect2,VarScan|  CNVKit, DELLY, Manta(SV)
   +-------------+------------+
                 v
   +--------------------------+
   | Annotation               |  VEP, ANNOVAR, SnpEff
   |  ClinVar/COSMIC/gnomAD   |  OncoKB, CIViC, PharmGKB
   |  SpliceAI, REVEL, AlphaMissense (Missense)
   +-------------+------------+
                 v
   +--------------------------------------------------------------------------+
   |                  3차 임상 해석 (Tertiary)                                |
   +--------------------------------------------------------------------------+
   +--------------------------+
   | Variant Classification   |  AMP/ASCO/CAP 4-tier
   |  TMB, MSI, HRD, signature|  Signal/Noise filter (gnomAD AF<0.001)
   |  Tumor-only/Tumor-Normal |  Panel-of-Normal(PoN) contamination check
   +-------------+------------+
                 v
   +--------------------------+
   | Clinical Report          |  TSV/JSON->PDF (PgKB 연동, NCCN 가이드)
   |  Therapy, Trial, Prognosis|  IRB review, Genetic counselor sign-off
   +-------------+------------+
                 v
   +--------------------------------------------------------------------------+
   |                  4차 임상의사 결정지원 (CDS)                              |
   +--------------------------------------------------------------------------+
   EHR(전자의무기록) <-- FHIR Genomics Extension  <-- 알림/권고 (CPIC level A)
   약사 시스템    <-- PDDI (pharmaco-ddi)         <-- 용량 자동조정
   유전상담사    <-- 결과 통보(Counseling workflow)
```

- **📢 섹션 요약 비유**: 환자의 유전체 데이터는 마치 **5,000만 권의 백과사전**(3.2Gb base pair = 약 6×10⁹ 문자)을 한 번에 읽는 것과 같아서, 이를 정확하고 빠르게 해독하는 NGS 장비와 '교정 시스템'인 바이오인포매틱스 파이프라인이 필수적인 시대가 도래한 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) NGS 시퀀싱 원리 및 데이터 포맷

NGS는 (a) 라이브러리 준비(Fragmentation -> End-repair -> Adapter ligation -> PCR/PCR-free), (b) 클러스터 생성(Bridge PCR, Illumina / DNB, MGI / ONT: motor protein nanopore / PacBio: SMRT Cell ZMW), (c) 시그널 검출(Optical/electrical/electrophoresis), (d) Base-calling(Guppy 6.4, Dorado 0.5+, Bonito, Illumina DRAGEN OLB v4) 단계를 거친다. Phred Quality Score(Q = -10log₁₀P) 기준 Q30은 1,000 base당 오류 1회 의미하며, NovaSeq X Plus의 Q30 ≥ 85%, ONT R10.4.1의 Q20(median) ≥ 99.3% (Hifi/CLR mode) 등이 보증된다.

| File Format | 단계 | 핵심 사양 | 평균 크기 (WGS 30×) |
| :--- | :--- | :--- | :--- |
| **FASTQ** | Raw read | Phred+33, 4-line/record, @SEQ_ID + sequence + + + quality | 80~150GB (.gz) |
| **uBAM / BAM** | Unaligned/aligned | SAM spec 1.6, BAI index, FLAG 0xN, MAPQ, CIGAR | 100~180GB |
| **CRAM** | Compressed ref-based | ECRAM v3.1(Reference-based), lossless/lossy mode(CRAM3 + bzip) | 50~70GB |
| **VCF / gVCF** | Variant | VCFv4.4 spec, ##INFO, ##FORMAT, ##FILTER, BCFtools, tabix(.tbi) | 1~10GB |
| **BigWig/BedGraph** | Coverage track | UCSC binary, block-gzip | 0.5~2GB |

### 2) Secondary Analysis - Alignment & Variant Calling 핵심 알고리즘

```text
[Reference-Based Alignment & Variant Calling의 단계별 동작]

   Read 1 ---> +------------------------------------------------+
   Read 2 ---> |  ① BWA-MEM2 (v2.2.1) / minimap2 (v2.27)        |
   Read N ---> |     • Seed-and-Extend (SMEM, k-mer)            |
              |     • BWT(FM-index) + SA  탐색                 |
              |     • Chaining, Smith-Waterman local alignment  |
              |     • MAPQ = -10·log10(P(wrong_pos))           |
              +--------------------+---------------------------+
                                   v
              +------------------------------------------------+
              |  ② Post-Alignment Processing                    |
              |     • FixMateInformation                       |
              |     • MarkDuplicates (Sambamba markdup)        |
              |     • BQSR (GATK BaseRecalibrator)             |
              |       - Known Sites: dbSNP146, Mills, 1000G     |
              |     • ApplyBQSR                                |
              +--------------------+---------------------------+
                                   v
              +------------------------------------------------+
              |  ③ Variant Calling                             |
              |  +--------------+  +-------------+              |
              |  | Germline     |  |  Somatic    |              |
              |  |• GATK HapC   |  |• Mutect2    |              |
              |  |• DeepVariant |  |• Strelka2   |              |
              |  |• Strelka2    |  |• VarScan2   |              |
              |  |• Octopus     |  |• VarDict    |              |
              |  +------+-------+  +------+------+              |
              |         |                 |                     |
              |         v                 v                     |
              |  VQSR/Hard-Filter    Filter (PoN, gnomad AF)   |
              |  (SNP: QD>2,FS<60,   (clustered=False,        |
              |   MQ>40,MQRankSum,   t_lod_fstar<5.0)          |
              |   ReadPosRankSum)                            |
              +------------------------------------------------+
```

- **BWA-MEM2**: BWA-MEM 대비 2.5~3.0배 빠르며, AVX2/AVX-512 SIMD 최적화, 80GB RAM 권장(WGS 30×)
- **GATK HaplotypeCaller**: Active region 재조립(De-Bruijn graph, k=25)을 통해 Indel 부근 정확도 ^, GVCF 모드(GenotypeGVCFs + GLnexus/GenotypeGVCFs merge)로 코호트 joint-calling 시 1,000 sample급 가능
- **DeepVariant (Google, v1.6)**: CNN 기반 Pileup + Haplotype + Locus image 입력, GIAB benchmark에서 SNP F1 ≥ 99.95%, Indel F1 ≥ 99.5%
- **Mutect2 / Mutect2 + FilterMutectCalls**: Somatic 모드, Panel-of-Normal(±30 정상 샘플)로 germline·artefact 제거, FFPE의 OxoG/FFPE-artifact artifact filter, TMB 계산(`CalculateContamination` -> 1−α, beta-binomial)

### 3) Tertiary - Annotation & Clinical Interpretation

```text
[Clinical Variant Interpretation Pipeline - AMP/ASCO/CAP 4-tier]

   VCF Input
      |
      v
  +--------------------------------------------------------+
  |  VEP (Ensembl v111) / SnpEff / ANNOVAR                 |
  |   • Gene/Transcript (RefSeq, MANE Select)               |
  |   • Consequence: missense, nonsense, splice, frameshift |
  |   • CADD(>20), REVEL, AlphaMissense(am_pathogenicity)  |
  |   • SpliceAI(>0.8), MaxEntScan, dbscSNV                |
  |   • Population: gnomAD v3.1.2 (AF, nhom, hemi)         |
  |   • Disease: ClinVar(2024 release), COSMIC v101, OMIM  |
  |   • Drug: PharmGKB, CPIC level A/B, FDA Pharm Tox      |
  |   • Functional: SIFT, PolyPhen-2, MutationTaster        |
  |   • Conservation: PhyloP(>2.0), PhastCons               |
  +---------------------+----------------------------------+
                        v
  +--------------------------------------------------------+
  |  Filtering & Triage (Noise reduction)                  |
  |   • Remove: AF(gnomAD)>0.001, non-coding depth<10      |
  |   • Keep:  PTV, missense CADD>25, ClinVar P/LP/VUS      |
  |   • Internal: house-keeping panel, recurrent DB         |
  +---------------------+----------------------------------+
                        v
  +--------------------------------------------------------+
  |  Tier Classification (AMP/ASCO/CAP 2017)               |
  |   • Tier I   - Strong clinical significance            |
  |     (FDA-approved therapy, professional guideline)     |
  |   • Tier II  - Potential clinical significance         |
  |     (Phase III, well-powered study)                    |
  |   • Tier III - Variants of Unknown Significance (VUS)   |
  |   • Tier IV  - Benign/Likely benign, artefacts         |
  +---------------------+----------------------------------+
                        v
  +--------------------------------------------------------+
  |  TMB / MSI / HRD