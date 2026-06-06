import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from PIL import Image
import io

st.set_page_config(
    page_title="Detalle Precios Plan Aliados",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SAVE_DIR  = Path(__file__).parent
FOTOS_DIR = Path(r"C:\Users\LENOVO\OneDrive - Anheuser-Busch InBev\Escritorio\Analisis\LICS Y LDACS\fotos")

# ── Helpers de imagen ─────────────────────────────────────────────────────────
@st.cache_data
def img_b64(filename: str, max_h: int = 120) -> str:
    path = FOTOS_DIR / filename
    if not path.exists():
        return ""
    try:
        img = Image.open(path).convert("RGBA" if path.suffix.lower() == ".png" else "RGB")
        ratio = max_h / img.height
        new_w = int(img.width * ratio)
        img = img.resize((new_w, max_h), Image.LANCZOS)
        buf = io.BytesIO()
        fmt = "PNG" if path.suffix.lower() == ".png" else "JPEG"
        img.save(buf, format=fmt, quality=85)
        mime = "png" if fmt == "PNG" else "jpeg"
        return f"data:image/{mime};base64,{base64.b64encode(buf.getvalue()).decode()}"
    except Exception:
        return ""

def _pkl_mtime(*names):
    return tuple((SAVE_DIR / n).stat().st_mtime for n in names)

@st.cache_data
def load_data(mtimes):
    data_promos  = pd.read_pickle(SAVE_DIR / "data_promos.pkl")
    grid_maestro = pd.read_pickle(SAVE_DIR / "grid_maestro.pkl")
    grid_melt    = pd.read_pickle(SAVE_DIR / "grid_melt.pkl")
    return data_promos, grid_maestro, grid_melt

data_promos, grid_maestro, grid_melt = load_data(
    _pkl_mtime("data_promos.pkl", "grid_maestro.pkl", "grid_melt.pkl")
)

# ── CSS global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #1B3A6B 60%, #0a1628 100%);
}
[data-testid="stSidebar"] * { color: #e8edf5 !important; }
[data-testid="stSidebar"] .stMultiSelect label { color: #F6C842 !important; font-weight: 600; }

/* Main */
.block-container { padding-top: 0.8rem; }
.main-bg { background: #0d1117; }

/* Tablas más compactas */
[data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {
    font-size: 0.72rem !important;
    padding: 2px 6px !important;
}

/* Banner de productos */
.brand-strip {
    display: flex; gap: 10px; align-items: center;
    justify-content: center; flex-wrap: wrap;
    background: linear-gradient(90deg, #0a1628, #1B3A6B, #0a1628);
    padding: 12px 20px; border-radius: 10px; margin-bottom: 6px;
}
.brand-strip img {
    height: 64px; object-fit: contain;
    border-radius: 6px; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5));
    transition: transform 0.2s;
}

/* Encabezado de tabla */
.table-header {
    background: linear-gradient(90deg, #1B3A6B, #2a5298);
    color: white; padding: 8px 16px; border-radius: 6px;
    font-size: 1rem; font-weight: 700; margin-bottom: 10px;
    letter-spacing: 0.03em;
}

/* Tarjeta resultado */
.card-result {
    background: linear-gradient(135deg, #1B3A6B 0%, #2a5298 50%, #1B3A6B 100%);
    border: 1px solid #F6C842;
    border-radius: 14px; padding: 24px 36px;
    color: white; text-align: center; margin-top: 18px;
    box-shadow: 0 8px 32px rgba(27,58,107,0.5);
}
.card-title  { font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; opacity: 0.75; }
.card-value  { font-size: 3rem; font-weight: 900; color: #F6C842; margin: 6px 0; line-height: 1; }
.card-detail { font-size: 0.78rem; opacity: 0.6; margin-top: 8px; }
.card-pills  { display: flex; justify-content: center; gap: 16px; margin-top: 10px; flex-wrap: wrap; }
.pill {
    background: rgba(255,255,255,0.1); border-radius: 20px;
    padding: 4px 14px; font-size: 0.78rem;
}

/* Hint */
.card-hint {
    background: rgba(255,255,255,0.04); border: 1px dashed #444;
    border-radius: 10px; padding: 14px 22px;
    text-align: center; color: #666; margin-top: 14px; font-size: 0.87rem;
}
</style>
""", unsafe_allow_html=True)

# ── MAIN — Banner de productos ────────────────────────────────────────────────
banner_files = [
    "P.CALLAO SS.png", "corona 473.jpg", "csq.jpg",
    "golden.png", "GD 355.png", "bud share.webp",
    "mikes.webp", "nolo.webp", "ss.png", "litro.jpg",
]
banner_parts = []
for f in banner_files:
    b64 = img_b64(f, max_h=80)
    if b64:
        banner_parts.append(f'<img src="{b64}">')

if banner_parts:
    st.markdown(
        f'<div class="brand-strip">{"".join(banner_parts)}</div>',
        unsafe_allow_html=True
    )

# ── Título ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:18px 0 14px;
    background:linear-gradient(90deg,#0a1628,#1B3A6B,#0a1628);
    border-radius:10px; margin-bottom:14px;">
    <div style="font-size:0.75rem; letter-spacing:0.2em; text-transform:uppercase;
        color:#F6C842; opacity:0.8; margin-bottom:4px;">Anheuser-Busch InBev · Sur Perú</div>
    <div style="font-size:2.2rem; font-weight:900; letter-spacing:0.06em; color:#ffffff;">
        Dashboard Precios <span style="color:#F6C842;">Aliados y DSD</span>
    </div>
</div>
""", unsafe_allow_html=True)
# ── Segmentador BrandPack centrado ───────────────────────────────────────────
_, col_c, _ = st.columns([1, 2, 1])
with col_c:
    st.markdown("**Filtro Principal — BrandPack**")
    bp_opts = sorted(grid_maestro["brandpack_grid"].dropna().unique().tolist())
    selected_bp = st.multiselect(
        "Selecciona o escribe para buscar:",
        options=bp_opts,
        placeholder="Buscar BrandPack...",
        key="bp"
    )

GERENCIAS_SUR_KEYWORDS = ["Arequipa", "Ayacucho", "Cusco", "Puno", "Sur Chico", "Tacna"]
DEAL_CONDITION = ["Relatividad", "Linealidad", "Táctico", "Tactico"]
NOTA_CREDITO   = ["Rebate", "Challenge", "Rebate Corona", "Rebate SS"]

# ── Filtros globales Canal y Gerencia ─────────────────────────────────────────
_, col_f1, col_f2, _ = st.columns([1, 1, 1, 1])
with col_f1:
    canal_opts = sorted(data_promos["canal"].dropna().unique().tolist()) if "canal" in data_promos.columns else []
    selected_canal = st.multiselect("Canal:", options=canal_opts, placeholder="Todos", key="g_canal")
with col_f2:
    ger_col = next((c for c in data_promos.columns if c.lower() == "gerencia"), None)
    if ger_col:
        pattern = "|".join(GERENCIAS_SUR_KEYWORDS)
        ger_opts = sorted(
            data_promos[ger_col][data_promos[ger_col].str.contains(pattern, case=False, na=False)]
            .dropna().unique().tolist()
        )
    else:
        ger_opts = []
    selected_ger = st.multiselect("Gerencia:", options=ger_opts, placeholder="Todas", key="g_ger")

st.divider()

# ── Filtrado base ─────────────────────────────────────────────────────────────
if selected_bp:
    mat_ids     = grid_maestro.loc[grid_maestro["brandpack_grid"].isin(selected_bp), "material_id"].unique()
    base_melt   = grid_melt[grid_melt["material_id"].isin(mat_ids)].copy()
    base_promos = data_promos[data_promos["material_id"].isin(mat_ids)].copy()
else:
    base_melt   = grid_melt.copy()
    base_promos = data_promos.copy()

if selected_canal:
    base_promos = base_promos[base_promos["canal"].isin(selected_canal)] if "canal" in base_promos.columns else base_promos
if selected_ger and ger_col:
    base_promos = base_promos[base_promos[ger_col].isin(selected_ger)]

# Plan Aliados solo visible cuando Canal incluye Terceros (o no hay filtro de canal)
TERCEROS_CANAL = "terceros"
show_aliados = (not selected_canal) or any(TERCEROS_CANAL in c.lower() for c in selected_canal)

def find_col(df, *names):
    low = {c.lower().strip(): c for c in df.columns}
    for n in names:
        if n in df.columns: return n
        if n.lower().strip() in low: return low[n.lower().strip()]
    return None

ev_promos      = None
ev_aliados     = None
promos_display = pd.DataFrame()
pivot_data     = pd.DataFrame()

col_promos, col_aliados = st.columns([9, 11], gap="medium")

# ══════════════════ IZQUIERDA — Promos y Combos ═══════════════════════════════
with col_promos:
    st.markdown('<div class="table-header">Promos y Combos</div>', unsafe_allow_html=True)

    c_canal = find_col(base_promos, "canal",    "Canal")
    c_cat   = find_col(base_promos, "categoria","Categoria","Categoría","category")
    c_list  = find_col(base_promos, "listado",  "Listado")
    c_ger   = find_col(base_promos, "Gerencia", "gerencia")
    c_ptr   = find_col(base_promos, "SUR PTR",  "SUR V.Venta", "PTR")
    c_dsc   = find_col(base_promos, "Descuento","descuento")
    c_bp    = find_col(base_promos, "brandpack","BrandPack")

    df_p = base_promos.copy()
    if c_ger:
        pattern = "|".join(GERENCIAS_SUR_KEYWORDS)
        df_p = df_p[df_p[c_ger].str.contains(pattern, case=False, na=False)]

    if c_list:
        s = st.multiselect("Listado:", sorted(df_p[c_list].dropna().unique()), placeholder="Todos", key="p_list")
        if s: df_p = df_p[df_p[c_list].isin(s)]
    if c_cat:
        s = st.multiselect("Categoria:", sorted(df_p[c_cat].dropna().unique()), placeholder="Todos", key="p_cat")
        if s: df_p = df_p[df_p[c_cat].isin(s)]

    grp = [c for c in [c_ger, c_bp, c_list] if c]

    if grp and c_ptr and c_dsc and not df_p.empty:
        agg = (
            df_p.groupby(grp, as_index=False)
            .agg(**{"_ptr": (c_ptr, "first"), "_dsc": (c_dsc, "max")})
        )
        agg["PTR FINAL"] = (agg["_ptr"] - agg["_dsc"]).round(2)
        agg = agg.rename(columns={"_dsc": "Dsct S/."}).drop(columns=["_ptr"])

        rename_map = {}
        if c_ger:  rename_map[c_ger]  = "Gerencia"
        if c_bp:   rename_map[c_bp]   = "brandpack"
        if c_list: rename_map[c_list] = "listado"
        agg = agg.rename(columns=rename_map)

        show_cols = [c for c in ["Gerencia", "brandpack", "listado", "Dsct S/.", "PTR FINAL"] if c in agg.columns]
        promos_display = agg[show_cols].sort_values("PTR FINAL").reset_index(drop=True)

        ev_promos = st.dataframe(
            promos_display,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            column_config={
                "Gerencia":  st.column_config.TextColumn(width="small"),
                "brandpack": st.column_config.TextColumn(width="small"),
                "listado":   st.column_config.TextColumn(width="small"),
                "Dsct S/.":  st.column_config.NumberColumn(format="S/. %.2f", width="small"),
                "PTR FINAL": st.column_config.NumberColumn(format="S/. %.2f", width="small"),
            }
        )
    else:
        st.info("Sin datos para los filtros seleccionados.")

# ══════════════════ DERECHA — Plan Aliados ═══════════════════════════════════
with col_aliados:
    st.markdown('<div class="table-header">Plan Aliados — Descuentos</div>', unsafe_allow_html=True)

    if not show_aliados:
        st.info("Plan Aliados disponible solo para canal **Terceros**.")
    else:
        gv_opts = sorted(base_melt["GV"].dropna().unique().tolist())
        sel_gv  = st.multiselect("GV:", options=gv_opts, placeholder="Todos", key="gv")
        df_melt = base_melt[base_melt["GV"].isin(sel_gv)].copy() if sel_gv else base_melt.copy()

        if not df_melt.empty:
            pivot = (
                df_melt
                .pivot_table(index=["GV", "Sku", "Listado"], columns="Descuento", values="Dsct S/.", aggfunc="max")
                .reset_index()
            )
            pivot.columns.name = None

            ex_dc = [d for d in ["Relatividad", "Linealidad", "Táctico", "Tactico"] if d in pivot.columns]
            ex_nc = [d for d in NOTA_CREDITO if d in pivot.columns]

            pivot_data    = pivot[["Listado"] + ex_dc + ex_nc].reset_index(drop=True)
            pivot_display = pivot_data.copy()
            pivot_display.columns = pd.MultiIndex.from_tuples(
                [("", "Listado")]
                + [("Deal Condition", d) for d in ex_dc]
                + [("Nota de Credito", d) for d in ex_nc]
            )

            ev_aliados = st.dataframe(
                pivot_display,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row"
            )
        else:
            st.info("Sin datos para los filtros seleccionados.")

# ══════════════════ TARJETA DE RESULTADO ═════════════════════════════════════
st.markdown("---")

sel_p = ev_promos.selection.rows  if ev_promos  is not None else []
sel_a = ev_aliados.selection.rows if ev_aliados is not None else []

if sel_p and sel_a and not promos_display.empty and not pivot_data.empty:
    row_p = promos_display.iloc[sel_p[0]]
    row_a = pivot_data.iloc[sel_a[0]]

    ptr_final       = row_p.get("PTR FINAL")
    dsc_aliados_cols = [c for c in pivot_data.columns if c != "Listado"]
    total_aliados   = row_a[dsc_aliados_cols].sum()
    resultado       = round(ptr_final - total_aliados, 2)

    bp_sel   = row_p.get("brandpack", "")
    list_sel = row_p.get("listado", "")
    list_ali = row_a.get("Listado", "")

    _, card_col, _ = st.columns([1, 2, 1])
    with card_col:
        st.markdown(f"""
        <div class="card-result">
            <div class="card-title">PTR Final incluido el Plan Aliados</div>
            <div class="card-value">S/. {resultado:,.2f}</div>
            <div class="card-pills">
                <span class="pill">📦 {bp_sel}</span>
                <span class="pill">📋 Promo: {list_sel}</span>
                <span class="pill">📋 Aliados: {list_ali}</span>
            </div>
            <div class="card-detail" style="margin-top:12px;">
                PTR solo con promo/combo &nbsp;<strong style="color:#F6C842;">S/. {ptr_final:,.2f}</strong>
                &nbsp;&nbsp;−&nbsp;&nbsp;
                Desc. Aliados &nbsp;<strong style="color:#F6C842;">S/. {total_aliados:,.2f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    _, hint_col, _ = st.columns([1, 2, 1])
    with hint_col:
        st.markdown("""
        <div class="card-hint">
            Selecciona una fila en <strong>Promos y Combos</strong> y una en
            <strong>Plan Aliados</strong> para ver el
            <strong>PTR Final incluido el Plan Aliados</strong>
        </div>
        """, unsafe_allow_html=True)
