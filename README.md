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

## 커스터마이즈
- 더 많은 소스: `feeds.yaml`에 RSS/Atom URL 추가
- 출력 개수/정렬: `build_cloud_digest.py` 상단의 설정 값 조정
- HTML 스타일: `template.html` 수정 (Tailwind CDN)

## 피드 기본값
- **AWS What's New**: https://aws.amazon.com/new/feed/
- **Azure Updates**: https://www.microsoft.com/releasecommunications/api/v2/azure/rss
- **Google Cloud Blog**: https://cloudblog.withgoogle.com/rss
