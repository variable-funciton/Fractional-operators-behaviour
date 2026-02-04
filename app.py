import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
# 1. メモリ上にバイナリデータを保存するためのバッファを作成
buf = io.BytesIO()

# --- UI Setup ---
st.set_page_config(page_title="Fractional Operators Behavior", layout="wide", initial_sidebar_state=480)
st.title("Fractional Operators Behavior\n Fractional integral operator vs Fractional maximal operator")

with st.sidebar:
    st.write("The definitions of fractional operators as follows (one variable):")
    st.latex(r'''
    \begin{align*}
    I_{\alpha}f(x) &:=\int_{-\infty}^{\infty} \frac{f(y)}{|x-y|^{1-\alpha}} dy,\\
    \ \\
    M_{\alpha}f(x) &:=\sup_{\substack{ I\subset \mathbb{R},\\ I: \text{interval} }} |I|^{\alpha} \frac{1}{|I|} \int_{I} | f(y) | dy\cdot \chi_{I}(x).
    \end{align*}
    ''')
    st.latex( r'''
    \text{Here,\ } 0<\alpha<1,\ |I| \text{denotes the length of }\ I\ and 
    ''')
    st.latex(r'''
    \chi_{[0,1]}(x) = \begin{cases} 1 & ( 0\leq x\leq 1)\\ 0 & (\text{otherwise}) \end{cases}.
    ''')
    st.header("Simulation Settings")
    alpha = st.slider("α (Fractional Order)", 0.01, 1.00, 0.5)
    
# --- Function Definitions ---
def fractional_integral(x, A):
    return np.piecewise(x,
        [(x > 0) & (x < 1), (x <= 0), (x >= 1)],
        [
            lambda x: (x**A + (1-x)**A) / A,
            lambda x: ((1-x)**A - (-x)**A) / A,
            lambda x: (x**A - (x-1)**A) / A
        ]
    )

def fractional_maximal(x, A):
    return np.piecewise(x,
        [(x > 0) & (x < 1), (x <= 0), (x >= 1)],
        [
            lambda x: 1.0,
            lambda x: (1-x)**(A-1) if A < 1 else 1.0,
            lambda x: x**(A-1) if A < 1 else 1.0
        ]
    )

def chi(x):
    return np.where((x >= 0) & (x <= 1), 1.0, 0.0)

# --- Plotting ---
x = np.linspace(-2, 3, 500)
fig, ax = plt.subplots(figsize=(10, 6))

# Streamlitのデフォルトでは mathtext が使われるため usetex=True なしでLaTeX表記可能
ax.plot(x, fractional_integral(x, alpha), "--", label=r'$I_{\alpha}[\chi_{[0,1]}](x)$', color="blue")
ax.plot(x, fractional_maximal(x, alpha), ":", label=r'$M_{\alpha}[\chi_{[0,1]}](x)$', color="red")
ax.plot(x, chi(x), linewidth=2, label=r'$\chi_{[0,1]}(x)$', color="black")

ax.set_title(f"Comparison for α = {alpha}", fontsize=14)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, alpha=0.3)
ax.legend()

# st.pyplotで図を表示
st.pyplot(fig)


# 2. 現在のグラフ(fig)をPDF形式でバッファに保存
fig.savefig(buf, format="pdf", bbox_inches="tight")

# 3. ダウンロードボタンを設置
st.download_button(
    label="Export a graph to PDF",
    data=buf.getvalue(),
    file_name=f"fractional_operators_alpha_{alpha}.pdf",
    mime="application/pdf"
)
