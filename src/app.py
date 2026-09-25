import csv
import streamlit as st
from answer import answer, by_id, THRESH
from agent import route, draft_email, audit

@st.cache_data
def load_meta():
    with open("data/metadata.csv", encoding="utf-8") as f:
        return {r["doc_id"]: r for r in csv.DictReader(f)}
meta = load_meta()

st.title("UniGuide (prototype)")
st.caption("Answers come only from official documents. If a document and this tool disagree, the document prevails.")
q = st.text_input("Ask about fees, calendar, regulations...")

if q:
    if st.session_state.get("last_q") != q:          # compute once per question
        st.session_state.last_q = q
        kind = route(q)
        st.session_state.kind = kind
        audit({"query": q, "route": kind})
        st.session_state.draft = draft_email(q) if kind == "service" else None
        st.session_state.result = answer(q, THRESH) if kind == "info" else None

    kind = st.session_state.kind
    if kind == "out_of_scope":
        st.warning("That's outside what I can help with.")
    elif kind == "service":
        draft = st.text_area("Draft email (edit if needed)", st.session_state.draft, height=220, key=f"draft_{q}")
        if st.button("Confirm and send"):
            audit({"action": "email_confirmed", "query": q, "draft": draft})
            st.success("Confirmed. (Demo only: nothing was actually sent.)")
    else:
        res = st.session_state.result
        if res["status"] == "abstain":
            st.info(res["message"])
        else:
            for c in res["claims"]:
                st.write("• " + c["claim"])
                ch = by_id[c["chunk_id"]]
                m = meta.get(ch["doc_id"], {})
                st.caption(f"{m.get('title', ch['doc_id'])} · page {ch['page']} · dated {m.get('date', '?')}")
                with st.expander("Show source passage"):
                    st.write(ch["text"])
                    if m.get("url"):
                        st.markdown(f"[Open original document]({m['url']})")