#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, time
import feedparser
import yaml
from datetime import datetime
import pytz
from jinja2 import Template
#from deep_translator import GoogleTranslator

# ==================== 설정 ====================
TIMEZONE = "Asia/Seoul"
SUMMARY_MAX_LEN = 280          # 아이템 요약 길이 제한
DEFAULT_MAX_ITEMS = 10         # 공급자별 최대 아이템 수 (feeds.yaml에서 override 가능)
OUTPUT_DIR = "dist"
MD_FILENAME = "digest.md"
HTML_FILENAME = "index.html"
TEMPLATE_FILE = "template.html"
TRANSLATE = False               # True면 한글 번역 적용 여부

# ==================== 유틸 ====================
def now_kst():
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz)

def human_date(dt):
    return dt.strftime("%Y년 %m월 %d일 %H:%M (KST)")

def clean_summary(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", "", s)   # HTML 태그 제거
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > SUMMARY_MAX_LEN:
        s = s[:SUMMARY_MAX_LEN-1] + "…"
    return s

def translate_text(text):
    if TRANSLATE and text:
        try:
            return GoogleTranslator(source='auto', target='ko').translate(text)
        except Exception as e:
            print("번역 실패:", e)
            return text
    return text

# ==================== 피드 파싱 ====================
def parse_feeds(provider):
    items = []
    for url in provider.get("feeds", []):
        d = feedparser.parse(url)
        for e in d.entries:
            title = e.get("title", "").strip()
            link = e.get("link", "").strip()
            ts = None
            if getattr(e, "published_parsed", None):
                ts = datetime.fromtimestamp(time.mktime(e.published_parsed))
            elif getattr(e, "updated_parsed", None):
                ts = datetime.fromtimestamp(time.mktime(e.updated_parsed))
            else:
                ts = datetime.utcnow()
            ts = pytz.utc.localize(ts).astimezone(pytz.timezone(TIMEZONE)) if ts.tzinfo is None else ts.astimezone(pytz.timezone(TIMEZONE))

            summary = e.get("summary", "") or e.get("description", "")
            summary = clean_summary(summary)

            source = d.feed.title if d and d.get("feed") and d.feed.get("title") else ""

            # 한글 번역
            title_ko = translate_text(title)
            summary_ko = translate_text(summary)

            items.append({
                "title": title_ko,
                "link": link,
                "published_dt": ts,
                "published": ts.strftime("%Y-%m-%d %H:%M"),
                "summary": summary_ko,
                "source": source,
            })
    items.sort(key=lambda x: x["published_dt"], reverse=True)
    max_items = provider.get("max_items", DEFAULT_MAX_ITEMS)
    return items[:max_items]

# ==================== 설정 로드 ====================
def load_feeds_config(path="feeds.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ==================== 출력 렌더 ====================
def render_markdown(date_str, providers_data):
    md = [f"# 클라우드 데일리 다이제스트 ({date_str} / 한국 표준시)"]
    for prov in providers_data:
        md.append(f"\n## {prov['name']}\n")
        for it in prov["items"]:
            line = f"- [{it['title']}]({it['link']})  \n  `{it['published']}`"
            if it.get("source"):
                line += f" · 출처: *{it['source']}*"
            if it.get("summary"):
                line += f"\n  \n  {it['summary']}"
            md.append(line)
    return "\n".join(md) + "\n"

def render_html(date_str, providers_data, template_path=TEMPLATE_FILE):
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    return tpl.render(date_str=date_str, data=providers_data)

# ==================== 메인 ====================
def main():
    cfg = load_feeds_config()
    now = now_kst()
    date_str = now.strftime("%Y년 %m월 %d일")

    providers_data = []
    for p in cfg.get("providers", []):
        items = parse_feeds(p)
        providers_data.append({"name": p["name"], "items": items})

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    md = render_markdown(date_str, providers_data)
    with open(os.path.join(OUTPUT_DIR, MD_FILENAME), "w", encoding="utf-8") as f:
        f.write(md)

    html_out = render_html(date_str, providers_data)
    with open(os.path.join(OUTPUT_DIR, HTML_FILENAME), "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"✅ 생성 완료: {os.path.join(OUTPUT_DIR, MD_FILENAME)}")
    print(f"✅ 생성 완료: {os.path.join(OUTPUT_DIR, HTML_FILENAME)}")

if __name__ == "__main__":
    main()
