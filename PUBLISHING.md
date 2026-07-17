# GitHub公開手順

この文書は、完成済みのローカルGitリポジトリをGitHubへ新規作成・送信するための手順である。公開前に、リポジトリ所有者が内容、公開範囲およびライセンス未設定であることを確認する。

## 前提

- GitHub CLI `gh` が導入されている。
- `gh auth status` が対象アカウントへの認証成功を示す。
- カレントディレクトリが本リポジトリのルートである。
- `./tools/verify-release.sh` が `VERIFICATION=PASS` を返す。
- Git作業ツリーがクリーンである。

## 非公開リポジトリの新規作成

```sh
gh auth login
gh auth status
./tools/verify-release.sh

gh repo create kazormia296/no-genai-novel-sop-ja \
  --private \
  --description "生成AI非使用による小説制作の標準作業手順書" \
  --source=. \
  --remote=origin \
  --push

git push origin sop-v1.0.0
```

`--push` 後にも、正式版タグがリモートへ存在することを明示的に確認する。

```sh
git ls-remote --heads origin main
git ls-remote --tags origin sop-v1.0.0
```

## 公開後の確認

```sh
gh repo view kazormia296/no-genai-novel-sop-ja \
  --json nameWithOwner,isPrivate,defaultBranchRef,url
```

確認項目:

- 所有者とリポジトリ名が正しい。
- 非公開設定になっている。
- 既定ブランチが `main` である。
- `sop-v1.0.0` が想定コミットを指している。
- リモートの `docs/SOP.md` がローカルのSHA-256と一致する。

## タグの取扱い

公開済みの正式版タグは移動、上書きまたは再利用しない。内容変更が必要な場合は、`VERSIONING.md` に従って新しい版番号を付与する。

## 公開範囲の変更

公開リポジトリへ変更する場合は、SOP本文、生成来歴、メールアドレス、個人名、作品情報、資料台帳およびテンプレート内の実データが公開可能であることを人間が再確認する。確認前に可視性を変更してはならない。
