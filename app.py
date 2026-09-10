import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="유묘 탐정 사무소", page_icon="🐈", layout="wide", initial_sidebar_state="expanded")
BASE=Path(__file__).parent
CASES=json.loads((BASE/"data/cases.json").read_text(encoding="utf-8"))
STATS=json.loads((BASE/"data/stats.json").read_text(encoding="utf-8"))
THEMES={"mist":("#e9eeee","#f8fbfb","#28383a","#6e8588","♨","Georgia,serif"),"lantern":("#211b1a","#302523","#f5e7ca","#d49b4d","⛩","Georgia,serif"),"storybook":("#f7efd9","#fffaf0","#493c33","#a86f55","✦","Georgia,serif"),"fog":("#cfd3d7","#edf0f1","#334047","#71808a","☁","Arial,sans-serif"),"theater":("#24191f","#36242d","#f2dce5","#c78b9f","✦","Georgia,serif"),"clock":("#182127","#222d34","#d9ecec","#75b6b6","◷","monospace"),"lake":("#201b31","#30274a","#eee5ff","#ad8fe0","◌","Georgia,serif"),"press":("#e6e0d3","#f7f2e8","#2d2a25","#8b6d42","▣","monospace"),"gothic":("#151515","#232323","#e6e1d8","#9d9a92","†","Georgia,serif"),"archive":("#dedbd1","#f2efe7","#3e403d","#6e746e","▤","monospace"),"garden":("#e7efd9","#f8fbf1","#394636","#76905d","❀","Georgia,serif"),"detective":("#d9d4c7","#f1ede3","#252d33","#5f6d75","⌕","Georgia,serif"),"neon":("#100e18","#1d1727","#eee5ff","#c58dff","◈","Arial,sans-serif"),"terminal":("#0b100d","#111a14","#cdebd3","#78c58c","◉","monospace"),"deepsea":("#071822","#0e2733","#d7eef3","#65b3c0","≈","Arial,sans-serif"),"court":("#ded8ca","#f5f0e4","#302d29","#816f57","⚖","Georgia,serif"),"victorian":("#1d2020","#2b2c2a","#e8ddc7","#b6a078","♜","Georgia,serif"),"tokyo":("#121419","#20232a","#e9edf2","#8ea7c2","◆","Arial,sans-serif")}
def css(theme="detective"):
    bg,panel,ink,accent,symbol,font=THEMES.get(theme,THEMES["detective"])
    st.markdown(f'''<style>:root{{--bg:{bg};--panel:{panel};--ink:{ink};--accent:{accent};}}.stApp{{background:var(--bg);color:var(--ink)}}[data-testid="stSidebar"]{{background:var(--panel)}}.hero{{padding:2rem 2.4rem;border:1px solid var(--accent);border-radius:24px;background:var(--panel);margin-bottom:1.3rem}}.hero-kicker,.case-no,.section-label{{font-family:monospace;letter-spacing:.16em;opacity:.65}}.hero h1{{font-family:{font};font-size:clamp(2rem,5vw,4rem);color:var(--ink)}}.case-card,.sheet{{border:1px solid var(--accent);border-left:6px solid var(--accent);border-radius:18px;padding:1.2rem;background:var(--panel);margin-bottom:1rem;color:var(--ink)}}.case-symbol{{font-size:2rem}}.case-title{{font-family:{font};font-size:1.4rem;font-weight:700;color:var(--ink)}}.badge{{display:inline-block;border:1px solid var(--accent);border-radius:999px;padding:.25rem .55rem;margin:.2rem;font-size:.75rem}}.quote{{font-family:{font};font-size:1.1rem;line-height:1.8;padding:1rem;border-left:3px solid var(--accent)}}</style>''',unsafe_allow_html=True)
def get_case(title): return next(c for c in CASES if c["title"]==title)
def case_page(c):
    css(c["theme"]); st.markdown(f'<div class="hero"><div class="hero-kicker">CASE FILE · {c["theme"].upper()}</div><h1>{c["symbol"]} {c["title"]}</h1><p>{c["subtitle"]} · <b>유묘 탐정 사무소</b></p></div>',unsafe_allow_html=True)
    a,b=st.columns([1.3,1])
    with a:
        st.markdown(f'<div class="sheet"><div class="section-label">YUMYO’S NOTE</div><div class="quote">“{c["blurb"]}”</div><div class="section-label">CHARACTER</div><p><b>역할:</b> {c["role"] or "기록 없음"}</p><p><b>플레이어:</b> {c["players"] or "기록 없음"}</p></div>',unsafe_allow_html=True)
    with b:
        st.markdown(f'<div class="sheet"><div class="section-label">CASE RESULT</div><p><b>내가 범인:</b> {"예" if c["killer_me"]=="O" else "아니오"}</p><p><b>검거:</b> {"성공" if c["caught"]=="O" else "실패"}</p><p><b>기록된 범인:</b> {c["killer"] or "기록 없음"}</p><div class="section-label">THEME</div><p>{c["subtitle"]}</p></div>',unsafe_allow_html=True)
    if st.button("← 사건 목록으로"): st.session_state.page="cases"; st.rerun()
def home():
    css(); st.markdown('<div class="hero"><div class="hero-kicker">PRIVATE DETECTIVE ARCHIVE</div><h1>🐈 유묘 탐정 사무소</h1><p>내가 지나온 머더 미스터리 사건들을 기록하는 개인 사건 보관소.</p></div>',unsafe_allow_html=True)
    a,b,c=st.columns(3); a.metric("기록된 사건",f"{len(CASES)}건"); b.metric("내가 범인",f'{sum(x["killer_me"]=="O" for x in CASES)}건'); c.metric("검거 성공",f'{sum(x["caught"]=="O" for x in CASES)}건')
    st.markdown("### 최근 사건 기록"); cols=st.columns(3)
    for i,x in enumerate(CASES[:6]):
        with cols[i%3]:
            st.markdown(f'<div class="case-card"><div class="case-symbol">{x["symbol"]}</div><div class="case-no">CASE {i+1:03d}</div><div class="case-title">{x["title"]}</div><div>{x["subtitle"]}</div></div>',unsafe_allow_html=True)
            if st.button("파일 열기",key=f"h{i}"): st.session_state.selected=x["title"];st.session_state.page="case";st.rerun()
def cases_page():
    css(); st.markdown("## 사건 파일"); q=st.text_input("🔎 사건 검색",placeholder="사건명, 역할, 플레이어 등"); arr=[x for x in CASES if not q or q.lower() in json.dumps(x,ensure_ascii=False).lower()]; st.caption(f"{len(arr)}건 표시 / 전체 {len(CASES)}건")
    for i,x in enumerate(arr):
        n=CASES.index(x)+1; st.markdown(f'<div class="case-card"><div class="case-symbol">{x["symbol"]}</div><div class="case-no">CASE {n:03d}</div><div class="case-title">{x["title"]}</div><div>{x["subtitle"]}</div><span class="badge">역할 · {x["role"] or "기록 없음"}</span><span class="badge">범인 · {x["killer"] or "기록 없음"}</span></div>',unsafe_allow_html=True)
        if st.button("사건 파일 열기",key=f"c{i}"): st.session_state.selected=x["title"];st.session_state.page="case";st.rerun()
def stats_page():
    css("archive"); st.markdown("## 수사 통계"); st.caption("원본 기록의 통계 시트를 옮긴 개인용 통계."); cols=st.columns(len(STATS))
    for col,s in zip(cols,STATS):
        with col: st.metric(s["name"],f'{s["games"]}회'); st.caption(f'범인 {s["killer_count"]}회 · 검거 {s["caught_count"]}회')
    st.dataframe(STATS,use_container_width=True,hide_index=True)
with st.sidebar:
    st.image(str(BASE/"assets/yumyo.png"),use_container_width=True); st.markdown("## 🐈 유묘 탐정 사무소"); st.caption("PRIVATE MURDER MYSTERY ARCHIVE"); nav=st.radio("이동",["사건 보관소","사건 파일","수사 통계"]); st.divider(); st.caption("사건마다 다른 세계관으로 기록합니다.")
if "page" not in st.session_state: st.session_state.page="cases"
if nav=="사건 보관소": st.session_state.page="cases"
elif nav=="사건 파일": st.session_state.page="case"
else: st.session_state.page="stats"
if st.session_state.page=="cases": home(); st.markdown("---"); cases_page()
elif st.session_state.page=="case": case_page(get_case(st.session_state.get("selected",CASES[0]["title"])))
else: stats_page()
