---
title: "MDVR-KCL Dataset Data Card"
dataset_name: "Mobile Device Voice Recordings at King's College London"
alias: "Dataset A"
last_updated: "2026-01-14"

source:
  repository: "Zenodo"
  doi: "10.5281/zenodo.2867215"
  url: "https://zenodo.org/records/2867215"

local_path: "assets/DATASET_MDVR_KCL/"

creators:
  - "Hagen Jaeger"
  - "Dhaval Trivedi"
  - "Michael Stadtschnitzer"

collection:
  period: "26-29 September 2017"
  location: "King's College London Hospital, Denmark Hill, London, UK"
  device: "Motorola Moto G4 smartphone"
  environment: "Clinical examination room (~10 m²)"

audio_specs:
  format: "WAV"
  sample_rate: 44100
  bit_depth: 16
  channels: "Mono"

tasks:
  - name: "ReadText"
    description: "The North Wind and the Sun passage"
    subjects: { total: 37, HC: 21, PD: 16 }
  - name: "SpontaneousDialogue"
    description: "Spontaneous conversation with examiner"
    subjects: { total: 36, HC: 21, PD: 15 }

filename_format: "ID{XX}_{label}_{H&Y}_{UPDRS_speech}_{UPDRS_total}.wav"

labels:
  hc: "Healthy Control"
  pd: "Parkinson's Disease"
---

# MDVR-KCL Dataset Documentation

## Overview

| Property | Value |
|----------|-------|
| **Name** | Mobile Device Voice Recordings at King's College London |
| **Source** | [Zenodo](https://zenodo.org/records/2867215) |
| **DOI** | 10.5281/zenodo.2867215 |
| **Local Path** | `assets/DATASET_MDVR_KCL/` |
| **Type** | Raw audio (WAV) |

## Creators

- Hagen Jaeger
- Dhaval Trivedi
- Michael Stadtschnitzer

## Collection Context

| Property | Value |
|----------|-------|
| **Period** | 26–29 September 2017 |
| **Location** | King's College London Hospital |
| **Device** | Motorola Moto G4 smartphone |
| **Environment** | Clinical examination room (~10 m²) |
| **Reverberation** | ~500 ms |

Recordings were captured within the reverberation radius directly from the microphone signal (not GSM-compressed), resulting in acoustically clean audio.

## Audio Specifications

| Property | Value |
|----------|-------|
| Format | WAV |
| Sample Rate | 44.1 kHz |
| Bit Depth | 16-bit |
| Channels | Mono |
| Compression | None |

## Speech Tasks

### ReadText

Participants read "The North Wind and the Sun" passage.

| Class | Count |
|-------|-------|
| HC | 21 |
| PD | 16 |
| **Total** | **37** |

### SpontaneousDialogue

Spontaneous conversation with test executor.

| Class | Count |
|-------|-------|
| HC | 21 |
| PD | 15 |
| **Total** | **36** |

## Filename Format

```
ID{XX}_{label}_{H&Y}_{UPDRS_speech}_{UPDRS_total}.wav
```

| Field | Description |
|-------|-------------|
| `ID{XX}` | Subject identifier (00-99) |
| `label` | `hc` or `pd` |
| `H&Y` | Hoehn & Yahr stage (0 for HC) |
| `UPDRS_speech` | UPDRS Item 18 score (0 for HC) |
| `UPDRS_total` | Total UPDRS score (0 for HC) |

**Example:** `ID05_pd_2_1_45.wav`

## Directory Structure

```
assets/DATASET_MDVR_KCL/
├── ReadText/
│   ├── HC/
│   │   ├── ID00_hc_0_0_0.wav
│   │   ├── ID01_hc_0_0_0.wav
│   │   └── ... (21 files)
│   └── PD/
│       ├── ID02_pd_2_1_32.wav
│       └── ... (16 files)
└── SpontaneousDialogue/
    ├── HC/
    │   └── ... (21 files)
    └── PD/
        └── ... (15 files)
```

## Usage in This Thesis

- **Pipeline:** Raw audio → Feature extraction → Classification
- **Cross-validation:** Grouped Stratified 5-Fold (subject-level splits)
- **Unit of analysis:** One recording per subject per task

## Methodological Constraints

1. All recordings from same subject must stay in same CV fold
2. Tasks must be analyzed separately or task encoded as feature
3. No mixing with Dataset B at subject level

## Citation

```bibtex
@misc{mdvr_kcl_2019,
  author = {Jaeger, Hagen and Trivedi, Dhaval and Stadtschnitzer, Michael},
  title = {Mobile Device Voice Recordings at King's College London (MDVR-KCL)},
  year = {2019},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.2867215},
  url = {https://zenodo.org/records/2867215}
}
```

---

## Dataset Metadata

```json
{
  "access": {
    "embargo": {
      "active": false,
      "reason": null
    },
    "files": "public",
    "record": "public",
    "status": "open"
  },
  "created": "2019-06-06T13:28:27.401819+00:00",
  "custom_fields": {},
  "deletion_status": {
    "is_deleted": false,
    "status": "P"
  },
  "files": {
    "count": 1,
    "enabled": true,
    "entries": {
      "26_29_09_2017_KCL.zip": {
        "access": {
          "hidden": false
        },
        "checksum": "md5:98c51bdd2b092b93f8bb038dea4505fa",
        "ext": "zip",
        "id": "46456379-c17a-4927-964d-271da36cfd7e",
        "key": "26_29_09_2017_KCL.zip",
        "links": {
          "content": "https://zenodo.org/api/records/2867216/files/26_29_09_2017_KCL.zip/content",
          "self": "https://zenodo.org/api/records/2867216/files/26_29_09_2017_KCL.zip"
        },
        "metadata": null,
        "mimetype": "application/zip",
        "size": 606144431,
        "storage_class": "L"
      }
    },
    "order": [],
    "total_bytes": 606144431
  },
  "id": "2867216",
  "is_draft": false,
  "is_published": true,
  "links": {
    "access": "https://zenodo.org/api/records/2867216/access",
    "access_grants": "https://zenodo.org/api/records/2867216/access/grants",
    "access_links": "https://zenodo.org/api/records/2867216/access/links",
    "access_request": "https://zenodo.org/api/records/2867216/access/request",
    "access_users": "https://zenodo.org/api/records/2867216/access/users",
    "archive": "https://zenodo.org/api/records/2867216/files-archive",
    "archive_media": "https://zenodo.org/api/records/2867216/media-files-archive",
    "communities": "https://zenodo.org/api/records/2867216/communities",
    "communities-suggestions": "https://zenodo.org/api/records/2867216/communities-suggestions",
    "doi": "https://doi.org/10.5281/zenodo.2867216",
    "draft": "https://zenodo.org/api/records/2867216/draft",
    "file_modification": "https://zenodo.org/api/records/2867216/file-modification",
    "files": "https://zenodo.org/api/records/2867216/files",
    "latest": "https://zenodo.org/api/records/2867216/versions/latest",
    "latest_html": "https://zenodo.org/records/2867216/latest",
    "media_files": "https://zenodo.org/api/records/2867216/media-files",
    "parent": "https://zenodo.org/api/records/2867215",
    "parent_doi": "https://doi.org/10.5281/zenodo.2867215",
    "parent_doi_html": "https://zenodo.org/doi/10.5281/zenodo.2867215",
    "parent_html": "https://zenodo.org/records/2867215",
    "preview_html": "https://zenodo.org/records/2867216?preview=1",
    "request_deletion": "https://zenodo.org/api/records/2867216/request-deletion",
    "requests": "https://zenodo.org/api/records/2867216/requests",
    "reserve_doi": "https://zenodo.org/api/records/2867216/draft/pids/doi",
    "self": "https://zenodo.org/api/records/2867216",
    "self_doi": "https://doi.org/10.5281/zenodo.2867216",
    "self_doi_html": "https://zenodo.org/doi/10.5281/zenodo.2867216",
    "self_html": "https://zenodo.org/records/2867216",
    "self_iiif_manifest": "https://zenodo.org/api/iiif/record:2867216/manifest",
    "self_iiif_sequence": "https://zenodo.org/api/iiif/record:2867216/sequence/default",
    "versions": "https://zenodo.org/api/records/2867216/versions"
  },
  "media_files": {
    "count": 0,
    "enabled": false,
    "entries": {},
    "order": [],
    "total_bytes": 0
  },
  "metadata": {
    "creators": [
      {
        "affiliations": [
          {
            "name": "Fraunhofer IAIS, Department NetMedia, Sankt Augustin, Germany"
          }
        ],
        "person_or_org": {
          "family_name": "Hagen Jaeger",
          "name": "Hagen Jaeger",
          "type": "personal"
        }
      },
      {
        "affiliations": [
          {
            "name": "King's College London, London, United Kingdom"
          }
        ],
        "person_or_org": {
          "family_name": "Dhaval Trivedi",
          "name": "Dhaval Trivedi",
          "type": "personal"
        }
      },
      {
        "affiliations": [
          {
            "name": "Fraunhofer IAIS, Department NetMedia, Sankt Augustin, Germany"
          }
        ],
        "person_or_org": {
          "family_name": "Michael Stadtschnitzer",
          "name": "Michael Stadtschnitzer",
          "type": "personal"
        }
      }
    ],
    "description": "<p><strong>Dataset description</strong></p>\n\n<p>The dataset description will start with describing the local conditions and other metadata, then will continue with describing the recording procedure and annotation methodology. Finally, a brief description of the dataset deployment and publication will be given.</p>\n\n<p><strong>Meta Information</strong></p>\n\n<p>The dataset was recorded at King&#39;s College London (KCL) Hospital, Denmark Hill, Brixton, London SE5 9RS in the period from 26 to 29 September 2017. We used a typical examination room with about ten square meters area and a typical reverberation tome of approx. 500ms to perform the voice recordings. Due to the fact, that the voice recordings are performed in the realistic situation of doing a phone call (i.e. participant holds the phone to the preferred ear and microphone is in direct proximity to the mouth), one can assume that all recordings were performed within the reverberation radius and thus can be considered as &ldquo;clean&rdquo;.</p>\n\n<p><strong>Recording Procedure</strong></p>\n\n<p>We used a Motorola Moto G4 Smartphone as recording device. To perform the voice recordings on the device, we developed a &ldquo;Toggle Recording App&rdquo;, which uses the same functionalities as the voice recording module used within the i-PROGNOSIS Smartphone application, but deployed as a standalone android application. This means, that the voice capturing service runs as a standalone background service on the recording device and triggers voice recordings via on- and off-hook signals of the Smartphone. Due to the fact, that we directly record the microphone signal, and not the GSM (&ldquo;Global System for Mobile Communications&rdquo;) compressed stream, we end up with high quality recordings with a sample rate of 44.1 kHz and a bit depth of 16 Bit (audio CD quality). The raw, uncompressed data is directly written to the external storage of the Smartphone (SD-card) using the well-known WAVE file format (.wav). We used the following workflow to perform a voice recording:</p>\n\n<ul>\n\t<li>Ask the participant to relax a bit and then to make a phone call to the test executor (off-hook signal triggered).}</li>\n\t<li>Ask the participant to read out &ldquo;The North Wind and the Sun&rdquo;</li>\n\t<li>Depending on the constitution of the participant either ask to read out &ldquo;Tech. Engin. Computer applications in geography snippet&rdquo;</li>\n\t<li>Start a spontaneous dialog with the participant, the test executor starts asking random questions about places of interest, local traffic, or personal interests if acceptable.</li>\n\t<li>Test executor ends call by farewell (on-hook signal triggered).</li>\n</ul>\n\n<p><strong>Annotation Scheme</strong></p>\n\n<p>For each HC and PD participant, we labeled the data regarding scores on the Hoehn &amp; Yahr (H&amp;Y), as well as the UPDRS II part 5 and UPDRS III part 18 scale. The voice recordings are labeled in the following scheme:</p>\n\n<p>SI_ HS_ HYR_ UPDRS II-5_UPDRS III-18</p>\n\n<p>with</p>\n\n<ul>\n\t<li>SI as subject identification in the form ID<em>NN</em>, <em>N</em> in [0, 9]</li>\n\t<li>HS as the health status label (hc or pd accordingly)</li>\n\t<li>HYR as the expert assessed H&amp;Y scale rating</li>\n\t<li>UPDRS II-5 as the according expert peer-reviewed score</li>\n\t<li>UPDRS III-18 as the according expert assessed score</li>\n</ul>\n\n<p>For example, an audio recording with the file name &ldquo;ID02_pd_1_2_1.wav&rdquo; represents a recording of the third participant (First participant was anonymized as ID00), which has PD and a H&amp;Y rating of 1, a UPDRS II-5 score of 2 and a UPDRS III-18 score of 1. At this point, it should be noted, that also all healthy controls were evaluated with regard to the introduced scales, because Parkinson&#39;s disease and voice degradation correlate, but don&#39;t match exactly. This means, that the data set includes one HC participant (ID31) with UPDRS II-5 and III-18 rating of 1, and also includes PD patients with UPDRS II-5 and III-18 ratings of 0. It should be emphasized, that this does not mean the data set includes ambiguous information, but that an expert was not able to hear voice degradation that would end up in a UPDRS rating greater than zero. Machine learning approaches may be able to nevertheless classify correctly, or at least learn to correlate, but not match PD and voice degradation at any time.</p>\n\n<p><strong>Appendix</strong></p>\n\n<p>North Wind and the Sun (Orthographic Version):</p>\n\n<p>&ldquo;The North Wind and the Sun were disputing which was the stronger, when a traveler came along wrapped in a warm cloak. They agreed that the one who first succeeded in making the traveler take his cloak off should be considered stronger than the other. Then the North Wind blew as hard as he could, but the more he blew the more closely did the traveler fold his cloak around him; and at last the North Wind gave up the attempt. Then the Sun shone out warmly, and immediately the traveler took off his cloak. And so the North Wind was obliged to confess that the Sun was the stronger of the two.&rdquo;</p>\n\n<p>BNC &ndash; Tech. Engin. Computer applications in geography snippet:</p>\n\n<p>&ldquo;[...] This is because there is less scattering of blue light as the atmospheric path length and consequently the degree of scattering of the incoming radiation is reduced. For the same reason, the sun appears to be whiter and less orange-coloured as the observer&#39;s altitude increases; this is because a greater proportion of the sunlight comes directly to the observer&#39;s eye. Figure 5.7 is a schematic representation of the path of electromagnetic energy in the visible spectrum as it travels from the sun to the Earth and back again towards a sensor mounted on an orbiting satellite. The paths of waves representing energy prone to scattering (that is, the shorter wavelengths) as it travels from sun to Earth are shown. To the sensor it appears that all the energy has been reflected from point P on the ground whereas, in fact, it has not, because some has been scattered within the atmosphere and has never reached the ground at all. [...]&rdquo;</p>",
    "funding": [
      {
        "award": {
          "acronym": "i-PROGNOSIS",
          "id": "00k4n6c32::690494",
          "identifiers": [
            {
              "identifier": "https://cordis.europa.eu/projects/690494",
              "scheme": "url"
            }
          ],
          "number": "690494",
          "program": "H2020-EU.3.1.",
          "title": {
            "en": "Intelligent Parkinson eaRly detectiOn Guiding NOvel Supportive InterventionS"
          }
        },
        "funder": {
          "id": "00k4n6c32",
          "name": "European Commission"
        }
      }
    ],
    "languages": [
      {
        "id": "eng",
        "title": {
          "en": "English"
        }
      }
    ],
    "publication_date": "2019-05-17",
    "publisher": "Zenodo",
    "resource_type": {
      "id": "dataset",
      "title": {
        "de": "Datensatz",
        "en": "Dataset"
      }
    },
    "rights": [
      {
        "description": {
          "en": "The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited."
        },
        "icon": "cc-by-icon",
        "id": "cc-by-4.0",
        "props": {
          "scheme": "spdx",
          "url": "https://creativecommons.org/licenses/by/4.0/legalcode"
        },
        "title": {
          "en": "Creative Commons Attribution 4.0 International"
        }
      }
    ],
    "subjects": [
      {
        "subject": "Parkinson's disease"
      },
      {
        "subject": "Early detection"
      },
      {
        "subject": "Telephone speech"
      },
      {
        "subject": "Read speech"
      },
      {
        "subject": "Spontaneous speech"
      },
      {
        "subject": "Speech corpus"
      }
    ],
    "title": "Mobile Device Voice Recordings at King's College London (MDVR-KCL) from both early and advanced Parkinson's disease patients and healthy controls"
  },
  "parent": {
    "access": {
      "owned_by": {
        "user": "28713"
      }
    },
    "communities": {
      "entries": [
        {
          "access": {
            "member_policy": "open",
            "members_visibility": "restricted",
            "record_submission_policy": "open",
            "review_policy": "closed",
            "visibility": "public"
          },
          "children": {
            "allow": true
          },
          "created": "2022-11-23T15:53:29.436323+00:00",
          "custom_fields": {},
          "deletion_status": {
            "is_deleted": false,
            "status": "P"
          },
          "id": "f0a8b890-f97a-4eb2-9eac-8b8a712d3a6c",
          "links": {},
          "metadata": {
            "curation_policy": "<h2>Curation policy</h2>\n<p>The EU Open Research Repository serves as a repository for research outputs (data, software, posters, presentations, publications, etc) which have been funded under an EU research funding programme such as Horizon Europe, Euratom or earlier Framework Programmes.</p>\n<p>The community is managed by CERN on behalf of the European Commission.&nbsp;</p>\n<p><a href=\"https://about.zenodo.org/policies/\">Zenodo&rsquo;s general policies</a> and <a href=\"https://about.zenodo.org/terms/\">Terms of Use</a> apply to all content.</p>\n<h3>Scope</h3>\n<p>The EU Open Research Repository accepts all digital research objects which is a research output stemming from one of EU&rsquo;s research and innovation funding programmes. The funding programmes currently include:</p>\n<ul>\n<li>\n<p>Horizon Europe (including ERC, MSCA), earlier Framework Programmes (eg Horizon 2020) as well as Euratom.</p>\n</li>\n</ul>\n<p>In line with the principle as open as possible, as closed as necessary both public and restricted content is accepted. See note on how <a href=\"https://about.zenodo.org/infrastructure/\">Zenodo handles restricted content</a>.</p>\n<h3>Content submission</h3>\n<p>EU programme beneficiaries are eligible to submit content to the community. The community supports three types of content submissions:</p>\n<ul>\n<li>\n<p>Submission via an EU Project Community (through user interface or programmatic APIs).</p>\n</li>\n<li>\n<p>Submission directly to the EU Open Research Repository.</p>\n</li>\n<li>\n<p>Automated harvesting from existing Zenodo content.</p>\n</li>\n</ul>\n<h4>Project community (preferred)</h4>\n<p>A representative of an EU project may request an EU Project Community and invite other project participants as members of the community. The project community is linked to one or more European Commission grants. All records in the project community are automatically integrated into the EU Open Research Repository immediately upon acceptance into the project community.&nbsp;</p>\n<h4>Direct submission</h4>\n<p>Any user may submit a record directly to the EU Open Research Repository. The submission will be moderated by Zenodo staff for compliance with the minimal required metadata requirements and its correctness.</p>\n<h4>Automated harvesting</h4>\n<p>Records found among Zenodo&rsquo;s existing content will on a regular basis automatically be integrated if they are found to comply with the requirements. The submissions through this method are integrated into the EU Open Research Repository with delay in a fully automated way.</p>\n<h3>Descriptive information</h3>\n<h4>Minimal metadata requirements</h4>\n<p>Records in the EU Open Research Repository are required to comply with the following minimal metadata requirements:</p>\n<ul>\n<li>\n<p>Visibility: Both public and restricted (with or without embargo and/or access request)</p>\n</li>\n<li>\n<p>Resource types: All resource types.</p>\n</li>\n<li>\n<p>Licenses: Public and embargoed records MUST specify a license. The chosen license SHOULD be compliant with the Horizon Europe open science requirements (see <a href=\"/communities/eu/pages/open-science\">Open Science in Horizon Europe</a>)</p>\n</li>\n<li>\n<p>Funding information: Records MUST specify at least one grant from the European Commission.</p>\n</li>\n<li>Journal articles: Records MUST specify at the publishing venue (e.g. the journal the article was published in).</li>\n<li>\n<p>Creators: Creators SHOULD be identified with a persistent identifier (e.g. ORCID, GND, &hellip;), and affiliations SHOULD be identified with a persistent identifier (e.g. ROR, ISNI, &hellip;)</p>\n</li>\n<li>\n<p>Subjects: Records SHOULD specify one or more fields of science from the <a href=\"https://op.europa.eu/en/web/eu-vocabularies/euroscivoc\">European Science Vocabulary</a>.</p>\n</li>\n</ul>\n<p>These metadata requirements comes from the related open science requirements in Horizon Europe which are detailed in each project's grant agreement.</p>\n<h3>Review &amp; moderation</h3>\n<p>All submissions undergo automated curation checks for compliance with the policy. Submissions through project communities are in addition reviewed by the project community. Submission directly to the EU Open Research Repository is in addiotn reviewed by Zenodo staff.</p>\n<p>Community curators may at any point edit metadata of the records in the community without notice through human or automated processing. The curators may at their sole discretion remove records from the community that are deemed not to comply with the content and curation policy or which are deemed of insufficient quality.</p>\n<h3>Updates</h3>\n<p>The content and curation policy is subject to change by the community owner at any time and without notice, other than through updating this page.</p>",
            "description": "Open repository for EU-funded research outputs from Horizon Europe, Euratom, and earlier Framework Programmes.",
            "funding": [
              {
                "funder": {
                  "id": "00k4n6c32"
                }
              }
            ],
            "organizations": [
              {
                "id": "00k4n6c32"
              }
            ],
            "page": "<h2>About</h2>\n<p>The EU Open Research Repository is a Zenodo-community dedicated to fostering open science and enhancing the visibility and accessibility of research outputs funded by the European Union. The community is managed by CERN on behalf of the European Commission.</p>\n<h3>Mission</h3>\n<p>The mission of the repository is to support the implementation of the EU's open science policy, providing a trusted and comprehensive space for researchers to share their research outputs such as data, software, reports, presentations, posters and more. The EU Open Research Repository simplifies the process of complying with open science requirements, ensuring that research outputs from Horizon Europe, Euratom, and earlier Framework Programmes are freely accessible, thereby accelerating scientific discovery and innovation.</p>\n<h3>EU Open Research Repository vs Open Research Europe (ORE)</h3>\n<p>The EU Open Research Repository serves as a complementary platform to the <a href=\"https://open-research-europe.ec.europa.eu/\">Open Research Europe</a> (ORE) publishing platform. Open Research Europe focuses on providing a publishing venue for peer-reviewed articles, ensuring that research meets rigorous academic standards. The EU Open Research Repository provides a space for all the other research outputs including data sets, software, posters, and presentations that are out of scope for ORE. This holistic approach enables researchers to not only publish their findings but also share the underlying data and materials that support their work, fostering transparency and reproducibility in the scientific process.&nbsp;</p>\n<h3>Funding</h3>\n<p>The EU Open Research Repository is funded by the European Union under grant agreement no. <a href=\"https://cordis.europa.eu/project/id/101122956\">101122956</a> (HORIZON-ZEN). For more information about the project see&nbsp;<a href=\"https://about.zenodo.org/projects/horizon-zen/\">https://about.zenodo.org/projects/horizon-zen/.</a></p>",
            "title": "EU Open Research Repository",
            "type": {
              "id": "organization"
            },
            "website": "https://research-and-innovation.ec.europa.eu"
          },
          "revision_id": 23,
          "slug": "eu",
          "theme": {
            "brand": "horizon",
            "enabled": true,
            "style": {
              "font": {
                "family": "Arial, sans-serif",
                "size": "16px",
                "weight": 600
              },
              "mainHeaderBackgroundColor": "#FFFFFF",
              "primaryColor": "#004494",
              "primaryTextColor": "#FFFFFF",
              "secondaryColor": "#FFD617",
              "secondaryTextColor": "#000000",
              "tertiaryColor": "#e3eefd",
              "tertiaryTextColor": "#1c5694"
            }
          },
          "updated": "2025-03-30T18:32:53.868593+00:00"
        }
      ],
      "ids": [
        "f0a8b890-f97a-4eb2-9eac-8b8a712d3a6c"
      ]
    },
    "id": "2867215",
    "pids": {
      "doi": {
        "client": "datacite",
        "identifier": "10.5281/zenodo.2867215",
        "provider": "datacite"
      }
    }
  },
  "pids": {
    "doi": {
      "client": "datacite",
      "identifier": "10.5281/zenodo.2867216",
      "provider": "datacite"
    },
    "oai": {
      "identifier": "oai:zenodo.org:2867216",
      "provider": "oai"
    }
  },
  "revision_id": 4,
  "stats": {
    "all_versions": {
      "data_volume": 3327732926190.0,
      "downloads": 5490,
      "unique_downloads": 3383,
      "unique_views": 12343,
      "views": 13963
    },
    "this_version": {
      "data_volume": 3315610037570.0,
      "downloads": 5470,
      "unique_downloads": 3371,
      "unique_views": 12276,
      "views": 13877
    }
  },
  "status": "published",
  "swh": {},
  "updated": "2020-01-24T19:24:30.521993+00:00",
  "versions": {
    "index": 1,
    "is_latest": true
  }
}
```