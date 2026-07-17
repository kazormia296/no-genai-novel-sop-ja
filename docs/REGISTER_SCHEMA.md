<!-- GENERATED FILE: tools/register_schema.py --write -->
# 台帳スキーマおよび入力規則

この文書と `templates/*.tsv` のヘッダーは、規範的な機械可読定義 [`schemas/registers.schema.json`](../schemas/registers.schema.json) から生成される。直接編集せず、スキーマ変更後に `python3 tools/register_schema.py --write` を実行する。

## 共通入力規則

- 文字コードは `UTF-8`、改行は `LF`、区切りはタブとする。
- 1行目は対応テンプレートと完全一致するヘッダーとし、列の追加、削除、改名または並べ替えを行ってはならない。
- 値にタブ、CRまたはLFを含めてはならない。引用符によるエスケープは定義しない。複数行情報は別ファイルへ保存し、そのIDまたはハッシュを記録する。
- 複数IDは空白を含めず `;` で区切る。順序に意味がある場合は元資料へ明記する。
- 必須値の来歴が不明な場合は空欄ではなく `UNKNOWN` を使用する。ただし、列の形式または列挙値が `UNKNOWN` を許可しない場合、その記録は不適合とする。
- `NONE` は、確認の結果対象が存在しないことを表す。空欄は任意列の未入力、`UNKNOWN` は未確認、`NONE` は確認済み不存在であり、相互に置換してはならない。
- `date` は `YYYY-MM-DD`、`utc_datetime` は秒までの `YYYY-MM-DDThh:mm:ssZ` とし、ローカル時刻を記録してはならない。
- SHA-256は小文字16進64桁とする。IDは台帳内で一意でなければならず、外部キーは同じ検証スナップショット内の有効な行を参照する。
- 台帳を凍結した後は行を削除または上書きしない。訂正行へ新しいIDを付け、旧行を `SUPERSEDED`、新行を `ACTIVE` とし、新行の `SUPERSEDES_ID` から旧IDを参照する。誤登録を無効化する場合は `VOID` とし理由を `NOTES` に記録する。
- 台帳スナップショット全体のSHA-256と検証日時を適合記録へ固定する。

## 台帳一覧

| ID | 配布テンプレート | プロジェクト内の標準パス | 状態 |
|---|---|---|---|
| `SOURCE_REGISTER` | `templates/SOURCE_REGISTER.tsv` | `CORPUS/SOURCES.tsv` | 規範 |
| `IDEA_REGISTER` | `templates/IDEA_REGISTER.tsv` | `IDEAS/IDEAS.tsv` | 規範 |
| `SESSION_REGISTER` | `templates/SESSION_REGISTER.tsv` | `REVIEW/SESSION_LOG.tsv` | 規範 |
| `ENVIRONMENT_MANIFEST` | `templates/ENVIRONMENT_MANIFEST.tsv` | `MANIFEST/ENVIRONMENT_MANIFEST.tsv` | 規範 |
| `DICTIONARY_MANIFEST` | `templates/DICTIONARY_MANIFEST.tsv` | `MANIFEST/DICTIONARY_MANIFEST.tsv` | 規範 |
| `EXCEPTION_REGISTER` | `templates/EXCEPTION_REGISTER.tsv` | `POLICY/EXCEPTIONS.tsv` | 規範 |
| `EVIDENCE_ANCHOR_REGISTER` | `templates/EVIDENCE_ANCHOR_REGISTER.tsv` | `AUDIT/EVIDENCE_ANCHORS.tsv` | 規範 |
| `P4H_CUTOFF_REGISTER` | `templates/P4H_CUTOFF_REGISTER.tsv` | `MANIFEST/P4H_CUTOFFS.tsv` | 規範 |
| `P4H_TECHNOLOGY_REGISTER` | `templates/P4H_TECHNOLOGY_REGISTER.tsv` | `MANIFEST/P4H_TECHNOLOGIES.tsv` | 規範 |
| `P4H_EVIDENCE_REGISTER` | `templates/P4H_EVIDENCE_REGISTER.tsv` | `MANIFEST/P4H_EVIDENCE.tsv` | 規範 |
| `P4H_COMPONENT_REGISTER` | `templates/P4H_COMPONENT_REGISTER.tsv` | `MANIFEST/P4H_COMPONENTS.tsv` | 規範 |
| `P4H_COMPONENT_EVIDENCE_REGISTER` | `templates/P4H_COMPONENT_EVIDENCE_REGISTER.tsv` | `MANIFEST/P4H_COMPONENT_EVIDENCE.tsv` | 規範 |
| `P4H_BUILD_ENVIRONMENT_REGISTER` | `templates/P4H_BUILD_ENVIRONMENT_REGISTER.tsv` | `MANIFEST/P4H_BUILD_ENVIRONMENTS.tsv` | 規範 |
| `P4H_BOOTSTRAP_SEED_REGISTER` | `templates/P4H_BOOTSTRAP_SEED_REGISTER.tsv` | `MANIFEST/P4H_BOOTSTRAP_SEEDS.tsv` | 規範 |
| `P4H_EXCEPTION_LINK_REGISTER` | `templates/P4H_EXCEPTION_LINK_REGISTER.tsv` | `MANIFEST/P4H_EXCEPTION_LINKS.tsv` | 規範 |
| `HISTORICAL_CUTOFF_MANIFEST_LEGACY` | `templates/HISTORICAL_CUTOFF_MANIFEST.tsv` | `—` | 移行専用 |

## SOURCE_REGISTER

承認資料の識別、発見・入手経路、生成AI来歴および利用許可を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `SOURCE_ID` | 必須 | `source_id` | — | — |
| `AUTHOR` | 任意 | `text` | — | — |
| `TITLE` | 必須 | `text` | — | — |
| `PUBLISHER_OR_ISSUER` | 任意 | `text` | — | — |
| `PUBLICATION_DATE` | 任意 | `date_or_partial` | — | — |
| `EDITION` | 任意 | `text` | — | — |
| `ACQUISITION_PATH` | 必須 | `text` | — | — |
| `DISCOVERY_METHOD` | 必須 | `text` | — | — |
| `MEDIUM` | 必須 | `text` | — | — |
| `PAGES_OR_SECTION` | 任意 | `text` | — | — |
| `HUMAN_AUTHORSHIP_STATUS` | 必須 | `text` | H / U / A | — |
| `GENAI_STATUS` | 必須 | `text` | NONE_CONFIRMED / UNKNOWN / PRESENT / NOT_APPLICABLE | — |
| `FILE_SHA256` | 任意 | `sha256_or_unknown` | — | — |
| `PERMITTED_USE` | 必須 | `text` | — | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.SOURCE_ID |
| `NOTES` | 任意 | `text` | — | — |

## IDEA_REGISTER

着想の発生日時、場所、直接契機、選択経路、作者による変更および作品利用を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `IDEA_ID` | 必須 | `idea_id` | — | — |
| `CREATED_AT` | 必須 | `utc_datetime` | — | — |
| `PLACE` | 任意 | `text` | — | — |
| `CONTENT_SUMMARY` | 必須 | `text` | — | — |
| `DIRECT_TRIGGER` | 必須 | `text` | — | — |
| `DIRECT_SOURCE_ID` | 任意 | `text` | — | SOURCE_REGISTER.SOURCE_ID if SOURCE_CLASS=R |
| `SOURCE_CLASS` | 必須 | `text` | O / E / D / R / H / C / M / A | — |
| `SELECTION_ROUTE` | 必須 | `text` | — | — |
| `AUTHOR_MODIFICATION` | 任意 | `text` | — | — |
| `GENAI_RISK` | 必須 | `text` | LOW / MEDIUM / HIGH / PROHIBITED / UNKNOWN | — |
| `EXPRESSION_DEPENDENCY` | 任意 | `text` | — | — |
| `WORK_USE` | 任意 | `text` | — | — |
| `STATUS` | 必須 | `text` | ADOPTED / PENDING / REJECTED | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.IDEA_ID |
| `NOTES` | 任意 | `text` | — | — |

## SESSION_REGISTER

執筆セッションと参照資料、着想、制作環境、辞書および例外を結び付ける。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `SESSION_ID` | 必須 | `session_id` | — | — |
| `START_AT` | 必須 | `utc_datetime` | — | — |
| `END_AT` | 必須 | `utc_datetime` | — | — |
| `CHAPTER_OR_SCENE` | 必須 | `text` | — | — |
| `SOURCE_IDS` | 任意 | `source_id_list` | — | SOURCE_REGISTER.SOURCE_ID (複数) |
| `IDEA_IDS` | 任意 | `idea_id_list` | — | IDEA_REGISTER.IDEA_ID (複数) |
| `DEVICE_ID` | 必須 | `text` | — | — |
| `ENVIRONMENT_ID` | 必須 | `text` | — | ENVIRONMENT_MANIFEST.ENVIRONMENT_ID |
| `DICTIONARY_ID` | 必須 | `text` | — | DICTIONARY_MANIFEST.DICTIONARY_ID |
| `EXCEPTION_STATUS` | 必須 | `text` | NONE / OPEN / CLOSED | — |
| `EXCEPTION_IDS` | 任意 | `exception_id_list` | — | EXCEPTION_REGISTER.EXCEPTION_ID (複数) |
| `OPERATOR` | 必須 | `text` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.SESSION_ID |
| `NOTES` | 任意 | `text` | — | — |

## ENVIRONMENT_MANIFEST

制作環境版を構成するハードウェア、ソフトウェア、設定および来歴を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `ENVIRONMENT_ID` | 必須 | `text` | — | — |
| `CATEGORY` | 必須 | `text` | — | — |
| `COMPONENT` | 必須 | `text` | — | — |
| `VERSION_OR_COMMIT` | 必須 | `text` | — | — |
| `SOURCE` | 必須 | `text` | — | — |
| `BINARY_SHA256` | 任意 | `sha256_or_unknown` | — | — |
| `SOURCE_SHA256` | 任意 | `sha256_or_unknown` | — | — |
| `CONFIG_SHA256` | 任意 | `sha256_or_unknown` | — | — |
| `AI_PROVENANCE` | 必須 | `text` | NONE_CONFIRMED / UNKNOWN / PRESENT / NOT_APPLICABLE | — |
| `APPROVAL_STATUS` | 必須 | `text` | APPROVED / REJECTED / CONDITIONAL | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | — |
| `NOTES` | 任意 | `text` | — | — |

## DICTIONARY_MANIFEST

辞書、個人辞書および辞書データの固定版と来歴を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `DICTIONARY_ID` | 必須 | `text` | — | — |
| `FILE_NAME` | 必須 | `text` | — | — |
| `VERSION_OR_COMMIT` | 必須 | `text` | — | — |
| `SOURCE` | 必須 | `text` | — | — |
| `ACQUIRED_DATE` | 必須 | `date` | — | — |
| `FILE_SHA256` | 必須 | `sha256` | — | — |
| `COMPILER_OR_MAINTAINER` | 任意 | `text` | — | — |
| `AI_PROVENANCE` | 必須 | `text` | NONE_CONFIRMED / UNKNOWN / PRESENT / NOT_APPLICABLE | — |
| `APPROVAL_STATUS` | 必須 | `text` | APPROVED / REJECTED / CONDITIONAL | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.DICTIONARY_ID |
| `NOTES` | 任意 | `text` | — | — |

## EXCEPTION_REGISTER

逸脱、影響、重大度、是正期限、再監査および処分を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `EXCEPTION_ID` | 必須 | `exception_id` | — | — |
| `OCCURRED_AT` | 必須 | `utc_datetime` | — | — |
| `DISCOVERED_BY` | 必須 | `text` | — | — |
| `EVENT_TYPE` | 必須 | `text` | — | — |
| `DESCRIPTION` | 必須 | `text` | — | — |
| `AFFECTED_FILES` | 任意 | `text` | — | — |
| `AFFECTED_SESSIONS` | 任意 | `session_id_list` | — | SESSION_REGISTER.SESSION_ID (複数) |
| `AFFECTED_SOURCE_OR_IDEA_IDS` | 任意 | `text` | — | — |
| `IMMEDIATE_ACTION` | 必須 | `text` | — | — |
| `IMPACT_ASSESSMENT` | 必須 | `text` | — | — |
| `SEVERITY` | 必須 | `text` | MINOR / MAJOR / CRITICAL | — |
| `CORRECTIVE_ACTION` | 任意 | `text` | — | — |
| `DISPOSITION` | 必須 | `text` | OPEN / CORRECTED / ACCEPTED_LIMITATION / REJECTED_INPUT / PROFILE_DOWNGRADED / FAILED | — |
| `APPROVED_BY` | 必須 | `text` | — | — |
| `CORRECTION_DUE_AT` | 任意 | `utc_datetime_or_none` | — | — |
| `REAUDIT_REQUIRED` | 必須 | `text` | YES / NO | — |
| `CLOSED_AT` | 任意 | `utc_datetime_or_empty` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.EXCEPTION_ID |
| `NOTES` | 任意 | `text` | — | — |

## EVIDENCE_ANCHOR_REGISTER

証拠集合を第三者時刻証明、署名、追記専用ログ、書換不能媒体または立会記録へ外部固定した事実を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `ANCHOR_ID` | 必須 | `text` | — | — |
| `CREATED_AT` | 必須 | `utc_datetime` | — | — |
| `ASSURANCE_CLASS` | 必須 | `text` | SELF-ATTESTED / SECOND-PARTY / INDEPENDENT | — |
| `SUBJECT_IDS` | 必須 | `text` | — | — |
| `METHOD` | 必須 | `text` | SIGNED_COMMIT / SIGNED_TAG / TRUSTED_TIMESTAMP / APPEND_ONLY_LOG / WRITE_ONCE_MEDIA / WITNESS_ATTESTATION / OTHER | — |
| `PROVIDER_OR_WITNESS` | 必須 | `text` | — | — |
| `URI_OR_MEDIA_ID` | 必須 | `text` | — | — |
| `SUBJECT_SHA256` | 必須 | `sha256` | — | — |
| `SIGNATURE_OR_RECEIPT` | 任意 | `text` | — | — |
| `VERIFIED_BY` | 必須 | `text` | — | — |
| `VERIFIED_AT` | 必須 | `utc_datetime` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.ANCHOR_ID |
| `NOTES` | 任意 | `text` | — | — |

## P4H_CUTOFF_REGISTER

P4-Hカットオフ宣言を一意に記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `CUTOFF_ID` | 必須 | `text` | — | — |
| `CUTOFF_UTC` | 必須 | `utc_datetime` | — | — |
| `CUTOFF_BASIS` | 必須 | `text` | — | — |
| `BUILD_METHOD` | 必須 | `text` | H-BINARY / H-SOURCE / MIXED | — |
| `FIRMWARE_SCOPE` | 必須 | `text` | INCLUDED / EXCLUDED / PARTIAL | — |
| `HARDWARE_SCOPE` | 必須 | `text` | — | — |
| `APPROVAL_STATUS` | 必須 | `text` | APPROVED / REJECTED / CONDITIONAL | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.CUTOFF_ID |
| `NOTES` | 任意 | `text` | — | — |

## P4H_TECHNOLOGY_REGISTER

排除対象技術、合理的な利用可能時点および根拠をカットオフ宣言から分離して記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `TECHNOLOGY_ID` | 必須 | `text` | — | — |
| `CUTOFF_ID` | 必須 | `text` | — | P4H_CUTOFF_REGISTER.CUTOFF_ID |
| `NAME` | 必須 | `text` | — | — |
| `DEFINITION` | 必須 | `text` | — | — |
| `AVAILABLE_AT` | 必須 | `utc_datetime_or_unknown` | — | — |
| `EVIDENCE_IDS` | 必須 | `evidence_id_list` | — | P4H_EVIDENCE_REGISTER.EVIDENCE_ID (複数) |
| `DECLARATION_SUBSTITUTION_ALLOWED` | 必須 | `text` | YES / NO | — |
| `APPROVAL_STATUS` | 必須 | `text` | APPROVED / REJECTED / CONDITIONAL | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.TECHNOLOGY_ID |
| `NOTES` | 任意 | `text` | — | — |

## P4H_EVIDENCE_REGISTER

外部定義、公開記録、アーカイブ、署名および取得物を版・取得日・ハッシュ付きで記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `EVIDENCE_ID` | 必須 | `text` | — | — |
| `EVIDENCE_TYPE` | 必須 | `text` | OFFICIAL_RELEASE / ARCHIVE_CAPTURE / SIGNED_METADATA / SOURCE_SNAPSHOT / TECHNOLOGY_DEFINITION / BUILD_RECORD / OTHER | — |
| `TITLE` | 必須 | `text` | — | — |
| `ISSUER` | 必須 | `text` | — | — |
| `PUBLISHED_AT` | 必須 | `utc_datetime_or_unknown` | — | — |
| `CAPTURED_AT` | 必須 | `utc_datetime` | — | — |
| `URI` | 必須 | `text` | — | — |
| `FILE_SHA256` | 必須 | `sha256` | — | — |
| `SIGNATURE_OR_ATTESTATION` | 任意 | `text` | — | — |
| `VERIFIED_BY` | 必須 | `text` | — | — |
| `VERIFIED_AT` | 必須 | `utc_datetime` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.EVIDENCE_ID |
| `NOTES` | 任意 | `text` | — | — |

## P4H_COMPONENT_REGISTER

P4-H対象構成物と締切・ビルド・ファームウェア境界を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `ARTIFACT_ID` | 必須 | `text` | — | — |
| `CUTOFF_ID` | 必須 | `text` | — | P4H_CUTOFF_REGISTER.CUTOFF_ID |
| `SCOPE_CATEGORY` | 必須 | `text` | — | — |
| `NAME` | 必須 | `text` | — | — |
| `VERSION_OR_COMMIT` | 必須 | `text` | — | — |
| `ARTIFACT_TYPE` | 必須 | `text` | — | — |
| `FIRST_PUBLISHED_AT` | 必須 | `utc_datetime` | — | — |
| `SOURCE_URI` | 必須 | `text` | — | — |
| `SHA256` | 必須 | `sha256` | — | — |
| `BUILD_METHOD` | 必須 | `text` | H-BINARY / H-SOURCE / NOT_APPLICABLE | — |
| `BUILD_ENVIRONMENT_ID` | 任意 | `text` | — | P4H_BUILD_ENVIRONMENT_REGISTER.BUILD_ENVIRONMENT_ID |
| `BOOTSTRAP_SEED_ID` | 任意 | `text` | — | P4H_BOOTSTRAP_SEED_REGISTER.BOOTSTRAP_SEED_ID |
| `REPRODUCIBLE_BUILD_STATUS` | 必須 | `text` | PASS / FAIL / NOT_TESTED / NOT_APPLICABLE | — |
| `FIRMWARE_SCOPE` | 必須 | `text` | INCLUDED / EXCLUDED / PARTIAL / NOT_APPLICABLE | — |
| `POST_CUTOFF_INPUT_Y_N` | 必須 | `text` | YES / NO | — |
| `EXCEPTION_ID` | 任意 | `exception_id_or_empty` | — | EXCEPTION_REGISTER.EXCEPTION_ID |
| `APPROVAL_STATUS` | 必須 | `text` | APPROVED / REJECTED / CONDITIONAL | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.ARTIFACT_ID |
| `NOTES` | 任意 | `text` | — | — |

## P4H_COMPONENT_EVIDENCE_REGISTER

構成物と複数の保存・公開証拠を多対多で対応付ける。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `LINK_ID` | 必須 | `text` | — | — |
| `ARTIFACT_ID` | 必須 | `text` | — | P4H_COMPONENT_REGISTER.ARTIFACT_ID |
| `EVIDENCE_ID` | 必須 | `text` | — | P4H_EVIDENCE_REGISTER.EVIDENCE_ID |
| `PURPOSE` | 必須 | `text` | PUBLICATION_TIME / ARCHIVE_TIME / IDENTITY / SIGNATURE / SOURCE_CORRESPONDENCE / BUILD_PROVENANCE / OTHER | — |
| `VERIFIED_BY` | 必須 | `text` | — | — |
| `VERIFIED_AT` | 必須 | `utc_datetime` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.LINK_ID |
| `NOTES` | 任意 | `text` | — | — |

## P4H_BUILD_ENVIRONMENT_REGISTER

H-SOURCEのビルダーOS、ツールチェーン、全入力および再現性比較を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `BUILD_ENVIRONMENT_ID` | 必須 | `text` | — | — |
| `CUTOFF_ID` | 必須 | `text` | — | P4H_CUTOFF_REGISTER.CUTOFF_ID |
| `NAME` | 必須 | `text` | — | — |
| `VERSION_OR_COMMIT` | 必須 | `text` | — | — |
| `SOURCE_URI` | 必須 | `text` | — | — |
| `SHA256` | 必須 | `sha256` | — | — |
| `INPUT_MANIFEST_SHA256` | 必須 | `sha256` | — | — |
| `NETWORK_DISABLED_Y_N` | 必須 | `text` | YES / NO | — |
| `REPRODUCIBLE_BUILD_STATUS` | 必須 | `text` | PASS / FAIL / NOT_TESTED | — |
| `COMPARISON_RECORD_SHA256` | 任意 | `sha256_or_empty` | — | — |
| `APPROVAL_STATUS` | 必須 | `text` | APPROVED / REJECTED / CONDITIONAL | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.BUILD_ENVIRONMENT_ID |
| `NOTES` | 任意 | `text` | — | — |

## P4H_BOOTSTRAP_SEED_REGISTER

ブートストラップ種の種類、版、由来、ハッシュおよび保証境界を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `BOOTSTRAP_SEED_ID` | 必須 | `text` | — | — |
| `CUTOFF_ID` | 必須 | `text` | — | P4H_CUTOFF_REGISTER.CUTOFF_ID |
| `NAME` | 必須 | `text` | — | — |
| `VERSION` | 必須 | `text` | — | — |
| `SOURCE_URI` | 必須 | `text` | — | — |
| `SHA256` | 必須 | `sha256` | — | — |
| `FIRST_PUBLISHED_AT` | 必須 | `utc_datetime` | — | — |
| `SCOPE_STATUS` | 必須 | `text` | INCLUDED / EXCLUDED / PARTIAL | — |
| `EVIDENCE_IDS` | 必須 | `evidence_id_list` | — | P4H_EVIDENCE_REGISTER.EVIDENCE_ID (複数) |
| `APPROVAL_STATUS` | 必須 | `text` | APPROVED / REJECTED / CONDITIONAL | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.BOOTSTRAP_SEED_ID |
| `NOTES` | 任意 | `text` | — | — |

## P4H_EXCEPTION_LINK_REGISTER

P4-Hのカットオフまたは構成物と一般例外記録を対応付け、表示への影響を記録する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `LINK_ID` | 必須 | `text` | — | — |
| `CUTOFF_ID` | 必須 | `text` | — | P4H_CUTOFF_REGISTER.CUTOFF_ID |
| `ARTIFACT_ID` | 任意 | `text` | — | P4H_COMPONENT_REGISTER.ARTIFACT_ID |
| `EXCEPTION_ID` | 必須 | `text` | — | EXCEPTION_REGISTER.EXCEPTION_ID |
| `IMPACT_ON_CLAIM` | 必須 | `text` | NONE / LIMITED / PROFILE_DOWNGRADE / P4H_FAIL | — |
| `DISPOSITION` | 必須 | `text` | OPEN / CORRECTED / ACCEPTED_LIMITATION / FAILED | — |
| `REVIEWER` | 必須 | `text` | — | — |
| `REVIEW_DATE` | 必須 | `date` | — | — |
| `RECORD_STATUS` | 必須 | `text` | ACTIVE / SUPERSEDED / VOID | — |
| `SUPERSEDES_ID` | 任意 | `text` | — | self.LINK_ID |
| `NOTES` | 任意 | `text` | — | — |

## HISTORICAL_CUTOFF_MANIFEST_LEGACY

版1.1.0からの移行専用。新規プロジェクトの規範台帳として使用してはならない。

> [!WARNING]
> この台帳は版1.1.0からの移行入力専用であり、新規プロジェクトの適合証拠には使用できない。正規化P4-H台帳へ移記し、検証した後に使用する。

| 列 | 必須 | 形式 | 列挙値 | 参照先 |
|---|:---:|---|---|---|
| `CUTOFF_ID` | 任意 | `text` | — | — |
| `CUTOFF_UTC` | 任意 | `text` | — | — |
| `CUTOFF_BASIS` | 任意 | `text` | — | — |
| `PROHIBITED_TECHNOLOGY_SCOPE` | 任意 | `text` | — | — |
| `TECHNOLOGY_AVAILABLE_AT` | 任意 | `text` | — | — |
| `CUTOFF_EVIDENCE_IDS` | 任意 | `text` | — | — |
| `ARTIFACT_ID` | 任意 | `text` | — | — |
| `SCOPE_CATEGORY` | 任意 | `text` | — | — |
| `NAME` | 任意 | `text` | — | — |
| `VERSION_OR_COMMIT` | 任意 | `text` | — | — |
| `ARTIFACT_TYPE` | 任意 | `text` | — | — |
| `FIRST_PUBLISHED_AT` | 任意 | `text` | — | — |
| `ARCHIVE_CAPTURE_AT` | 任意 | `text` | — | — |
| `ARCHIVE_URI` | 任意 | `text` | — | — |
| `SOURCE_URI` | 任意 | `text` | — | — |
| `SIGNATURE_OR_ATTESTATION` | 任意 | `text` | — | — |
| `SHA256` | 任意 | `text` | — | — |
| `BUILD_METHOD` | 任意 | `text` | — | — |
| `BUILD_ENVIRONMENT_ID` | 任意 | `text` | — | — |
| `BOOTSTRAP_SEED_ID` | 任意 | `text` | — | — |
| `REPRODUCIBLE_BUILD_STATUS` | 任意 | `text` | — | — |
| `FIRMWARE_SCOPE` | 任意 | `text` | — | — |
| `POST_CUTOFF_INPUT_Y_N` | 任意 | `text` | — | — |
| `EXCEPTION_ID` | 任意 | `text` | — | — |
| `APPROVAL_STATUS` | 任意 | `text` | — | — |
| `VERIFIED_BY` | 任意 | `text` | — | — |
| `VERIFIED_DATE` | 任意 | `text` | — | — |
| `NOTES` | 任意 | `text` | — | — |
