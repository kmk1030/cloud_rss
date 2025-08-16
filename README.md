# Cloud Daily Digest
매일 AWS / Azure / Google Cloud의 최신 업데이트를 모아 **하나의 HTML/Markdown 리포트**로 생성하는 간단한 자동화 스크립트입니다.

## 구성
- `build_cloud_digest.py` — RSS/Atom 피드를 읽어 Markdown(`dist/digest.md`)과 HTML(`dist/index.html`)을 생성
- `feeds.yaml` — 수집할 피드 목록 (원하시는 소스 추가/삭제 가능)
- `template.html` — HTML 생성 템플릿 (Tailwind CDN 사용)
- `.github/workflows/publish.yml` — GitHub Actions로 매일 빌드 & GitHub Pages 배포(옵션)
- `requirements.txt` — 의존성 목록

## 설치 & 실행
```bash
# 1) 가상환경(선택)
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

# 2) 의존성 설치
pip install -r requirements.txt

# 3) 수동 실행 (오늘자 리포트 생성)
python build_cloud_digest.py
# dist/digest.md, dist/index.html 생성
```

## 자동화 (선택)
### A) 로컬 스케줄링
- macOS/Linux: `crontab -e`에 아래 추가
  ```
  5 8 * * * /usr/bin/env bash -lc 'cd /path/to/cloud-daily-digest && source .venv/bin/activate && python build_cloud_digest.py'
  ```
- Windows: 작업 스케줄러로 `python build_cloud_digest.py`를 매일 실행

### B) GitHub Actions + Pages로 매일 배포
1. 이 폴더를 새로운 GitHub 저장소로 푸시
2. 저장소의 **Settings → Pages** 에서 `gh-pages` 브랜치를 소스로 설정
3. 워크플로 파일 `.github/workflows/publish.yml`의 스케줄(cron) 확인 후 그대로 사용

## 커스터마이즈
- 더 많은 소스: `feeds.yaml`에 RSS/Atom URL 추가
- 출력 개수/정렬: `build_cloud_digest.py` 상단의 설정 값 조정
- HTML 스타일: `template.html` 수정 (Tailwind CDN)

## 피드 기본값
- **AWS What's New**: https://aws.amazon.com/new/feed/
- **Azure Updates**: https://azurecomcdn.azureedge.net/en-us/updates/feed/  (Microsoft 공식 업데이트 피드)
- **Google Cloud Blog**: https://cloud.google.com/blog/rss/

> 일부 피드는 지역/카테고리별로 나뉘기도 하니, 원하는 라인업으로 바꾸셔도 됩니다.

행운을 빌어요! 취뽀 가즈아 💪
