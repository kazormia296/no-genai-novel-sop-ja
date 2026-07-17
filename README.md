# 生成AI非使用による小説制作 標準作業手順書

調査、着想、構成、執筆、推敲、校正および記録保存について、生成AIまたはAIによる情報媒介を、選択した保証範囲に従って排除・管理するための日本語SOPです。

## 重要な来歴表示

このリポジトリの初版文書は、生成AIを用いた対話を通じて作成されました。したがって、このSOPを採用した作品について「制作手順の設計段階から生成AIを一切使用していない」と表示することはできません。対象作品のAI非使用期間は、人間の責任者がSOPを精査・必要に応じて修正し、正式承認した後に開始してください。

## 文書

- 正式手順書: [`docs/SOP.md`](docs/SOP.md)
- 版管理規則: [`VERSIONING.md`](VERSIONING.md)
- 改訂履歴: [`CHANGELOG.md`](CHANGELOG.md)
- 生成来歴: [`PROVENANCE.md`](PROVENANCE.md)
- GitHub公開手順: [`PUBLISHING.md`](PUBLISHING.md)
- 規範的な台帳スキーマ: [`schemas/registers.schema.json`](schemas/registers.schema.json)
- 台帳入力規則: [`docs/REGISTER_SCHEMA.md`](docs/REGISTER_SCHEMA.md)
- 適合記録様式: [`templates/CONFORMANCE_RECORD.md`](templates/CONFORMANCE_RECORD.md)
- 環境版台帳: [`templates/ENVIRONMENT_MANIFEST.tsv`](templates/ENVIRONMENT_MANIFEST.tsv)
- P4-Hカットオフ台帳: [`templates/P4H_CUTOFF_REGISTER.tsv`](templates/P4H_CUTOFF_REGISTER.tsv)
- 版1.1.0互換移行用台帳: [`templates/HISTORICAL_CUTOFF_MANIFEST.tsv`](templates/HISTORICAL_CUTOFF_MANIFEST.tsv)

## P4-H：歴史的カットオフ環境

P4-Hは、P4の供給網監査を基礎として、OS、ツールチェーン、依存部品および必要に応じてファームウェアを指定日時以前の証拠付き構成物へ限定する追加プロファイルです。明示した排除対象技術について、構成物がその合理的な利用可能時点より前に確定していたことを示せる場合は、作成者の非使用表明を歴史的証拠で代替できます。P4-Hは締切日以後の混入経路を閉じるためのものであり、締切日以前のAI利用、非公開先行利用または決定論的な自動生成まで不存在であることを保証しません。

版1.2.0では、カットオフ、排除対象技術、根拠、構成物、構成物と根拠の対応、ビルド環境、ブートストラップ種および例外リンクを別台帳へ正規化しました。旧28列台帳は移行専用であり、新規適合記録には使用できません。

## 保証軸と監査保証区分

P1～P5の番号は単純な強弱順ではありません。案件ごとに、直接利用、協力者、情報発見、資料来歴、制作端末、供給網、ファームウェア、外部監査および証拠固定の各軸を記録します。監査保証区分は `SELF-ATTESTED / SECOND-PARTY / INDEPENDENT` のいずれかを、プロファイルとは別に表示します。

## 使用時に固定する識別子

単に「最新版へ準拠」と記録してはいけません。プロジェクト開始前に、最低限、次を固定します。

1. SOPの版番号
2. Gitタグ
3. GitコミットSHA
4. `docs/SOP.md` のSHA-256
5. 基礎プロファイル（P1、P2、P3またはP5）と追加プロファイル（P4、P4-HまたはNONE）
6. 制作環境版、辞書版および資料群スナップショット
7. ローカル修正の有無と、その差分またはハッシュ

現行版の識別値は次のとおりです。

- SOP version: `1.2.0`
- Git tag: `sop-v1.2.0`
- Status: 人間の承認後に発効可能

完全なコミットSHAはタグから取得し、文書ハッシュは `checksums/SHA256SUMS` または検証スクリプトで確認します。リポジトリ内に自己参照的なコミットSHAを固定せず、タグが指すコミットを正本とします。

## 推奨する参照表現

> 本プロジェクトは、SOP `1.2.0`、タグ `sop-v1.2.0`、コミット `<40桁SHA>`、SOP文書SHA-256 `<64桁ハッシュ>` を基準版として採用し、基礎プロファイル `<P2／P3>` と追加プロファイル `P4-H` に従って運用した。監査保証区分は `<SELF-ATTESTED／SECOND-PARTY／INDEPENDENT>`、最終結果は `<PASS／CONDITIONAL PASS>` であり、ローカル修正は `<なし／識別子>` である。

## ライセンス

本リポジトリは [MIT License](LICENSE) の下で提供します。ライセンスが適用できるのは、著作権者が権利を有する範囲に限られます。

## 検証

POSIX互換シェル、Python 3、`git` および `sha256sum` が利用できる環境では、次を実行します。

```sh
./tools/verify-release.sh
```

この検証は、厳密なSemVer、作業ツリー、チェックサム対象の完全性、注釈付きタグ、版識別子、Markdown内部リンク、TSV・Markdown様式のスキーマ同期を確認します。正式タグを必須にする場合は `./tools/verify-release.sh --require-tag` を使用します。プロジェクト台帳の値と参照整合性は `python3 tools/register_schema.py --validate-root /path/to/NOVEL` で検証します。

正式な適合記録には、スクリプトが表示する完全なコミットSHAとSOP文書SHA-256を転記します。
