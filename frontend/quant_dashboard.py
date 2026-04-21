import os, streamlit as st, plotly.graph_objects as go, pandas as pd, requests

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(
    page_title="VectorBT",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Instrument+Serif:ital@0;1&family=Syne:wght@400;600;700;800&display=swap');
:root{--bg:#0a0c10;--surface:#10141c;--surface2:#161b26;--border:rgba(255,255,255,0.07);--accent:#00e5a0;--accent2:#3b7dff;--accent3:#f7c948;--text:#e8eaf0;--muted:#5a6175;--danger:#ff4f6a}
html,body,[data-testid="stAppViewContainer"]{background-color:var(--bg)!important;color:var(--text)!important;font-family:'Syne',sans-serif!important}
[data-testid="stAppViewContainer"]>.main,[data-testid="stHeader"]{background-color:var(--bg)!important}
section[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important}
[data-testid="stSidebarNav"]{display:none!important}
.logo{font-family:'Instrument Serif',serif;font-size:22px;color:var(--text);display:flex;align-items:center;gap:8px}
.logo-badge{background:var(--accent);color:#000;font-family:'DM Mono',monospace;font-size:9px;padding:2px 6px;border-radius:3px;text-transform:uppercase}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:10px 0 18px;border-bottom:1px solid var(--border);margin-bottom:24px}
.run-status{display:flex;align-items:center;gap:8px;font-family:'DM Mono',monospace;font-size:11px;color:var(--muted)}
.pulse{width:8px;height:8px;border-radius:50%;background:var(--accent);display:inline-block;animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.8)}}
.page-title{font-family:'Instrument Serif',serif;font-size:30px;letter-spacing:-.5px;line-height:1.1}
.page-title em{color:var(--accent);font-style:italic}
.page-subtitle{font-family:'DM Mono',monospace;font-size:11px;color:var(--muted);margin-top:6px}
.stat-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:18px 20px;position:relative;overflow:hidden}
.stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px}
.stat-card.green::before{background:var(--accent)}.stat-card.blue::before{background:var(--accent2)}
.stat-card.yellow::before{background:var(--accent3)}.stat-card.red::before{background:var(--danger)}.stat-card.grey::before{background:var(--muted)}
.stat-label{font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.stat-value{font-family:'Instrument Serif',serif;font-size:28px;letter-spacing:-1px;line-height:1}
.stat-value.pos{color:var(--accent)}.stat-value.neg{color:var(--danger)}.stat-value.blue{color:var(--accent2)}
.stat-delta{font-family:'DM Mono',monospace;font-size:10px;color:var(--muted);margin-top:6px}.stat-delta span{color:var(--accent)}
.dash-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden}
.card-header{display:flex;align-items:center;justify-content:space-between;padding:14px 20px;border-bottom:1px solid var(--border)}
.card-title{font-size:13px;font-weight:700;letter-spacing:.02em;display:flex;align-items:center;gap:8px}
.dot{width:6px;height:6px;border-radius:50%;display:inline-block}.card-body{padding:18px 20px}
.trade-table{width:100%;border-collapse:collapse}
.trade-table thead th{font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;padding:0 0 10px;border-bottom:1px solid var(--border)}
.trade-table tbody tr{border-bottom:1px solid var(--border)}.trade-table tbody tr:last-child{border-bottom:none}
.trade-table tbody td{padding:10px 0;font-family:'DM Mono',monospace;font-size:11px}
.tag{display:inline-block;font-size:9px;font-weight:700;padding:2px 7px;border-radius:3px;text-transform:uppercase;letter-spacing:.05em}
.tag-long{background:rgba(0,229,160,.15);color:var(--accent)}.tag-short{background:rgba(255,79,106,.15);color:var(--danger)}
.pos-val{color:var(--accent)}.neg-val{color:var(--danger)}
.sb-item{display:flex;align-items:center;gap:10px;padding:9px 20px;color:var(--muted);font-size:13px;font-weight:600;border-left:2px solid transparent}
.sb-item.active{color:var(--accent);border-left-color:var(--accent);background:rgba(0,229,160,.06)}
.sb-label{font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);padding:0 20px 8px;display:block;margin-top:14px}
.sb-divider{height:1px;background:var(--border);margin:8px 20px}
.sb-badge{margin-left:auto;background:rgba(0,229,160,.15);color:var(--accent);font-family:'DM Mono',monospace;font-size:9px;padding:2px 6px;border-radius:3px}
.error-box{background:rgba(255,79,106,.1);border:1px solid rgba(255,79,106,.3);border-radius:8px;padding:16px;color:var(--danger);font-family:'DM Mono',monospace;font-size:12px;white-space:pre-wrap}
[data-testid="stSlider"]>div>div>div{background:var(--accent)!important}[data-testid="stSlider"]>div>div{background:var(--surface2)!important}
.stSelectbox>div>div,.stTextInput>div>div>input,.stNumberInput>div>div>input{background:var(--surface2)!important;border:1px solid var(--border)!important;color:var(--text)!important;font-family:'DM Mono',monospace!important}
label[data-testid="stWidgetLabel"] p{font-family:'DM Mono',monospace!important;font-size:9px!important;text-transform:uppercase!important;color:var(--muted)!important}
.stButton>button{width:100%;background:var(--accent)!important;border:none!important;border-radius:8px!important;font-family:'Syne',sans-serif!important;font-size:13px!important;font-weight:800!important;color:#000!important;text-transform:uppercase!important;padding:12px 0!important}
.block-container{padding:1.5rem 2rem 2rem!important;max-width:100%!important}.stMarkdown p{margin:0}
</style>""",
    unsafe_allow_html=True,
)


def fmt_pct(v):
    return f"+{v*100:.1f}%" if v >= 0 else f"{v*100:.1f}%"


def fmt_val(v):
    return f"${v:,.0f}"


def pct_cls(v):
    return "pos" if v >= 0 else "neg"


@st.cache_data(ttl=120, show_spinner=False)
def call_backend(strategy, asset, start_date, end_date, capital, params_tuple):
    params = dict(params_tuple)
    try:
        r = requests.post(
            f"{API_BASE}/run",
            json={
                "strategy": strategy,
                "asset": asset,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "initial_capital": float(capital),
                "parameters": params,
            },
            timeout=90,
        )
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return (
            None,
            "Cannot reach the backend. Is it running?\n\nStart it with:\n  uvicorn src.engine.main:app --reload --port 8000",
        )
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except:
            detail = str(e)
        return None, f"Backend error: {detail}"
    except Exception as e:
        return None, str(e)


# ── SIDEBAR
with st.sidebar:
    st.markdown(
        """<div style="padding:8px 20px 16px"><div class="logo">VectorBT <span class="logo-badge">ALPHA</span></div></div>
    <span class="sb-label">Workspace</span>
    <div class="sb-item active">⬡ &nbsp;Dashboard <span class="sb-badge">NEW</span></div>
    <div class="sb-item">◈ &nbsp;Strategy Builder</div><div class="sb-item">⟳ &nbsp;Backtests</div><div class="sb-item">⇅ &nbsp;Optimizer</div>
    <div class="sb-divider"></div><span class="sb-label">Analysis</span>
    <div class="sb-item">△ &nbsp;Performance</div><div class="sb-item">◻ &nbsp;Risk Metrics</div>
    <div class="sb-item">◉ &nbsp;Trade Log</div>
    <div class="sb-divider"></div><span class="sb-label">Data</span>
    <div class="sb-item">↑ &nbsp;Upload CSV</div><div class="sb-item">⊟ &nbsp;Data Sources</div>
    <div class="sb-divider"></div><span class="sb-label">System</span>
    <div class="sb-item">⚙ &nbsp;Settings</div><div class="sb-item">⊡ &nbsp;API Keys</div>""",
        unsafe_allow_html=True,
    )

# ── TOPBAR
meta = st.session_state.get("last_meta", {})
if meta:
    status = (
        f"Last backtest: <strong style='color:#e8eaf0'>"
        f"{meta.get('strategy','—')} — {meta.get('asset','—')} "
        f"{str(meta.get('start_date',''))[:4]}–{str(meta.get('end_date',''))[:4]}"
        f"</strong> &nbsp;·&nbsp; source: {meta.get('data_source','—')}"
    )
else:
    status = "No backtest run yet — configure below and click Run"

st.markdown(
    f"""<div class="topbar"><div class="run-status"><span class="pulse"></span> {status}</div></div>""",
    unsafe_allow_html=True,
)

# ── CONFIG
STRATEGIES = [
    "SMA Crossover",
    "RSI Reversion",
    "Bollinger Bands",
    "MACD Signal Cross",
    "Volume Breakout",
    "Buy and Hold",
]
st.markdown(
    """<div class="dash-card" style="margin-bottom:16px"><div class="card-header"><div class="card-title"><span class="dot" style="background:#f7c948"></span> Strategy Configuration</div></div></div>""",
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
strategy = c1.selectbox("STRATEGY", STRATEGIES)
asset = c2.text_input("ASSET", value="AAPL")
sd = c3.date_input("START DATE", value=pd.Timestamp("2018-01-01"))
ed = c4.date_input("END DATE", value=pd.Timestamp("2024-06-30"))
capital = c5.number_input("CAPITAL ($)", value=100000, step=10000)

params = {}
if strategy == "SMA Crossover":
    p1, p2 = st.columns(2)
    params["short_window"] = p1.slider("FAST SMA", 5, 50, 20)
    params["long_window"] = p2.slider("SLOW SMA", 20, 200, 50)
elif strategy == "RSI Reversion":
    p1, p2, p3 = st.columns(3)
    params["window"] = p1.slider("RSI WINDOW", 5, 30, 14)
    params["lower_bound"] = p2.slider("OVERSOLD", 10, 40, 30)
    params["upper_bound"] = p3.slider("OVERBOUGHT", 60, 90, 70)
elif strategy == "Bollinger Bands":
    p1, p2 = st.columns(2)
    params["window"] = p1.slider("WINDOW", 5, 50, 20)
    params["num_std"] = p2.slider("STD DEVS", 1, 4, 2)
elif strategy == "MACD Signal Cross":
    p1, p2, p3 = st.columns(3)
    params["fast"] = p1.slider("FAST EMA", 5, 20, 12)
    params["slow"] = p2.slider("SLOW EMA", 20, 50, 26)
    params["signal"] = p3.slider("SIGNAL", 5, 15, 9)
elif strategy == "Volume Breakout":
    p1, p2 = st.columns(2)
    params["volume_window"] = p1.slider("VOL WINDOW", 5, 50, 20)
    params["volume_multiplier"] = p2.slider("MULTIPLIER", 1.0, 3.0, 1.5, 0.1)

if st.button("▶   RUN BACKTEST"):
    with st.spinner("Running backtest on backend…"):
        result, err = call_backend(
            strategy, asset, sd, ed, capital, tuple(sorted(params.items()))
        )
    if err:
        st.markdown(f'<div class="error-box">{err}</div>', unsafe_allow_html=True)
    elif result:
        st.session_state["last_result"] = result
        st.session_state["last_meta"] = result.get("meta", {})

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

data = st.session_state.get("last_result")
has_data = data is not None
metrics = data["metrics"] if has_data else {}
charts = data["charts"] if has_data else {}
trades = data["trades"] if has_data else []
meta = st.session_state.get("last_meta", {})
ts = meta.get("strategy", strategy)
ta = meta.get("asset", asset)
ss = str(meta.get("start_date", sd))[:10]
es = str(meta.get("end_date", ed))[:10]

st.markdown(
    f"""<div style="margin-bottom:22px"><div class="page-title">{ts} &nbsp;<em>vs</em>&nbsp; Benchmark</div>
<div class="page-subtitle">{ta} · {ss} → {es} · Initial capital: {fmt_val(capital)}</div></div>""",
    unsafe_allow_html=True,
)

cols5 = st.columns(5)
if has_data:
    cards = [
        (
            "green",
            "Total Return",
            metrics["cumulativeReturn"],
            fmt_pct(metrics["cumulativeReturn"]),
            f"Alpha: <span>{fmt_pct(metrics['alpha'])}</span>",
        ),
        (
            "blue",
            "Sharpe Ratio",
            metrics["sharpeRatio"],
            f"{metrics['sharpeRatio']:.2f}",
            "Annualised risk-adj.",
        ),
        (
            "yellow",
            "Max Drawdown",
            metrics["maxDrawdown"],
            fmt_pct(metrics["maxDrawdown"]),
            "Peak → Trough",
        ),
        (
            "red",
            "Win Rate",
            metrics["winRate"],
            f"{metrics['winRate']*100:.1f}%",
            "Daily positive sessions",
        ),
        (
            "grey",
            "Sortino Ratio",
            metrics["sortinoRatio"],
            f"{metrics['sortinoRatio']:.2f}",
            "Downside dev. adjusted",
        ),
    ]
    for col, (cls, label, raw, val, delta) in zip(cols5, cards):
        vc = pct_cls(raw) if "%" in val else ""
        col.markdown(
            f"""<div class="stat-card {cls}"><div class="stat-label">{label}</div><div class="stat-value {vc}">{val}</div><div class="stat-delta">{delta}</div></div>""",
            unsafe_allow_html=True,
        )
else:
    for col, label in zip(
        cols5,
        ["Total Return", "Sharpe Ratio", "Max Drawdown", "Win Rate", "Sortino Ratio"],
    ):
        col.markdown(
            f"""<div class="stat-card grey"><div class="stat-label">{label}</div><div class="stat-value" style="color:var(--muted)">—</div><div class="stat-delta">Run a backtest</div></div>""",
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

st.markdown(
    """<div class="dash-card"><div class="card-header"><div class="card-title"><span class="dot" style="background:#00e5a0"></span> Equity Curve</div></div></div>""",
    unsafe_allow_html=True,
)

if has_data and charts.get("strategy"):
    sdf = pd.DataFrame(charts["strategy"])
    bdf = pd.DataFrame(charts["benchmark"])
    sdf["time"] = pd.to_datetime(sdf["time"])
    bdf["time"] = pd.to_datetime(bdf["time"])
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=bdf["time"],
            y=bdf["value"],
            name="Benchmark",
            line=dict(color="#3b7dff", width=1.5, dash="dot"),
            fill="tozeroy",
            fillcolor="rgba(59,125,255,0.05)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=sdf["time"],
            y=sdf["value"],
            name=ts,
            line=dict(color="#00e5a0", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(0,229,160,0.08)",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono", color="#5a6175", size=9),
        margin=dict(l=10, r=10, t=10, b=10),
        height=240,
        legend=dict(
            orientation="h",
            x=1,
            xanchor="right",
            y=1.05,
            font=dict(color="#e8eaf0", size=10),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="#5a6175", size=9),
            tickformat="%Y",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.04)",
            zeroline=False,
            tickformat="$,.0f",
            tickfont=dict(color="#5a6175", size=9),
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
else:
    st.markdown(
        "<div style='height:240px;display:flex;align-items:center;justify-content:center;color:var(--muted);font-family:DM Mono;font-size:12px'>Run a backtest to see the equity curve</div>",
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

ct, cr = st.columns(2, gap="medium")
with ct:
    st.markdown(
        """<div class="dash-card"><div class="card-header"><div class="card-title"><span class="dot" style="background:#3b7dff"></span> Recent Trades</div></div>""",
        unsafe_allow_html=True,
    )
    if has_data and trades:
        rows = ""
        for t in trades[:8]:
            pc = "pos-val" if t["return"] >= 0 else "neg-val"
            rs = (
                f"+{t['return']*100:.2f}%"
                if t["return"] >= 0
                else f"{t['return']*100:.2f}%"
            )
            tag = f"<span class='tag tag-{t['action']}'>{t['action'].upper()}</span>"
            rows += f"<tr><td>{t['entryDate']}</td><td>{tag}</td><td>${t['entryPrice']:,.2f}</td><td>${t['exitPrice']:,.2f}</td><td class='{pc}'>{rs}</td><td>{t.get('days','—')}d</td></tr>"
        st.markdown(
            f"""<div class="card-body"><table class="trade-table"><thead><tr><th>Entry</th><th>Side</th><th>Entry $</th><th>Exit $</th><th>Return</th><th>Hold</th></tr></thead><tbody>{rows}</tbody></table></div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='card-body' style='color:var(--muted);font-family:DM Mono;font-size:12px'>No trade data yet</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with cr:
    st.markdown(
        """<div class="dash-card"><div class="card-header"><div class="card-title"><span class="dot" style="background:#f7c948"></span> Risk Metrics</div></div>""",
        unsafe_allow_html=True,
    )
    if has_data:
        rows_data = [
            (
                "Cumulative Return",
                fmt_pct(metrics["cumulativeReturn"]),
                metrics["cumulativeReturn"],
            ),
            (
                "Annualised Return",
                fmt_pct(metrics["annualizedReturn"]),
                metrics["annualizedReturn"],
            ),
            ("Annualised Volatility", fmt_pct(metrics["annualizedVolatility"]), None),
            ("Sharpe Ratio", f"{metrics['sharpeRatio']:.2f}", None),
            ("Sortino Ratio", f"{metrics['sortinoRatio']:.2f}", None),
            ("Max Drawdown", fmt_pct(metrics["maxDrawdown"]), metrics["maxDrawdown"]),
            ("Win Rate", f"{metrics['winRate']*100:.1f}%", None),
            ("Beta", f"{metrics['beta']:.2f}", None),
            ("Alpha", fmt_pct(metrics["alpha"]), metrics["alpha"]),
            ("Final Portfolio Value", fmt_val(metrics["finalPortfolioValue"]), None),
        ]
        trows = ""
        for label, val, raw in rows_data:
            color = (
                "color:var(--accent)"
                if (raw is not None and raw >= 0)
                else ("color:var(--danger)" if raw is not None else "")
            )
            trows += f"<tr style='border-bottom:1px solid var(--border)'><td style='padding:8px 0;font-family:DM Mono;font-size:10px;color:var(--muted)'>{label}</td><td style='padding:8px 0;font-family:DM Mono;font-size:11px;text-align:right;{color}'>{val}</td></tr>"
        st.markdown(
            f"""<div class="card-body"><table style="width:100%;border-collapse:collapse"><tbody>{trows}</tbody></table></div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='card-body' style='color:var(--muted);font-family:DM Mono;font-size:12px'>Run a backtest to see metrics</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
