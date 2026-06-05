import streamlit as st
import requests
import json
import time
import random
import os
import datetime

# 嘗試載入預設的 API 密鑰（從環境變數或 Streamlit Secrets）
DEFAULT_HF_TOKEN = os.getenv("HF_TOKEN", "")
DEFAULT_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

if not DEFAULT_HF_TOKEN:
    try:
        DEFAULT_HF_TOKEN = st.secrets.get("HF_TOKEN", "")
    except:
        pass
if not DEFAULT_GEMINI_KEY:
    try:
        DEFAULT_GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    except:
        pass

# 設定頁面資訊與寬度
st.set_page_config(
    page_title="Cosmos 3 AI Image Studio - 物理圖像生成學堂",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入自定義 Premium CSS 樣式
st.markdown("""
<style>
/* Fonts & Global Styles */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #090d16;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0c1220;
    border-right: 1px solid #1e293b;
}

/* Custom header */
.app-header {
    background: linear-gradient(135deg, #0c1220 0%, #0e172a 100%);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}
.logo-container {
    display: flex;
    align-items: center;
    gap: 16px;
}
.logo-box {
    background-color: #76b900;
    color: #000;
    padding: 10px;
    border-radius: 12px;
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px rgba(118, 185, 0, 0.4);
    animation: pulse 2s infinite alternate;
}
@keyframes pulse {
    0% { transform: scale(1); box-shadow: 0 0 10px rgba(118, 185, 0, 0.4); }
    100% { transform: scale(1.05); box-shadow: 0 0 25px rgba(118, 185, 0, 0.7); }
}
.title-row {
    display: flex;
    align-items: center;
    gap: 12px;
}
.main-title {
    font-family: 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
}
.badge {
    background-color: rgba(118, 185, 0, 0.1);
    color: #76b900;
    border: 1px solid rgba(118, 185, 0, 0.2);
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
}
.subtitle {
    font-size: 13px;
    color: #94a3b8;
    margin: 4px 0 0 0;
}

/* Styled containers / cards */
.custom-card {
    background-color: rgba(12, 18, 32, 0.6);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(8px);
}

/* Input boxes & Textareas */
div[data-baseweb="textarea"] textarea, div[data-baseweb="input"] input {
    background-color: #05080f !important;
    border: 1px solid #1e293b !important;
    color: #f1f5f9 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}
div[data-baseweb="textarea"] textarea:focus, div[data-baseweb="input"] input:focus {
    border-color: #76b900 !important;
    box-shadow: 0 0 0 1px #76b900 !important;
}

/* Tabs customization */
div[data-baseweb="tab-list"] {
    background-color: rgba(15, 23, 42, 0.8);
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 4px;
    margin-bottom: 20px;
}
div[data-baseweb="tab"] {
    color: #94a3b8;
    font-weight: 500;
    font-size: 13px;
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.2s;
}
div[data-baseweb="tab"]:hover {
    color: #ffffff;
}
div[data-baseweb="tab"][aria-selected="true"] {
    background-color: #1e293b;
    color: #76b900 !important;
}

/* Custom buttons styling */
div.stButton > button {
    background-color: #76b900;
    color: #000000;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    transition: all 0.2s ease-in-out;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #87cf03;
    color: #000000;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(118, 185, 0, 0.3);
}
div.stButton > button:active {
    transform: translateY(1px);
}

/* Specific styling for helper buttons like copy, example cards */
.example-btn-container button {
    background-color: #05080f !important;
    border: 1px solid #1e293b !important;
    color: #cbd5e1 !important;
    text-align: left !important;
    display: block !important;
    width: 100% !important;
    padding: 12px !important;
    border-radius: 12px !important;
    font-size: 11px !important;
    white-space: normal !important;
    height: auto !important;
    line-height: 1.4 !important;
}
.example-btn-container button:hover {
    border-color: rgba(118, 185, 0, 0.5) !important;
    color: #76b900 !important;
    background-color: #0c1220 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* System architecture styled steps */
.arch-container {
    background-color: #05080f;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
}
.arch-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    align-items: stretch;
}
.arch-card {
    background-color: #0c1220;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.arch-icon {
    font-size: 24px;
    margin-bottom: 8px;
}
.arch-title {
    font-size: 12px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}
.arch-desc {
    font-size: 10px;
    color: #94a3b8;
    line-height: 1.4;
}

/* History thumbnails style */
.history-btn button {
    padding: 0 !important;
    border: 2px solid #1e293b !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    aspect-ratio: 1 !important;
    width: 100% !important;
}
.history-btn-selected button {
    border-color: #76b900 !important;
    box-shadow: 0 0 10px rgba(118, 185, 0, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# 初始化 Session State 狀態
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "negative_prompt" not in st.session_state:
    st.session_state.negative_prompt = "blurry, low quality, distorted, bad physics, text, watermark"
if "engine" not in st.session_state:
    st.session_state.engine = "cosmos3"
if "hf_token" not in st.session_state:
    st.session_state.hf_token = DEFAULT_HF_TOKEN
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = DEFAULT_GEMINI_KEY
if "aspect_ratio" not in st.session_state:
    st.session_state.aspect_ratio = "1:1"
if "guidance_scale" not in st.session_state:
    st.session_state.guidance_scale = 7.0
if "inference_steps" not in st.session_state:
    st.session_state.inference_steps = 25
if "seed" not in st.session_state:
    st.session_state.seed = -1
if "history" not in st.session_state:
    st.session_state.history = [
        {
            "id": "sample-1",
            "prompt": "An advanced industrial robotic arm assembling an electric vehicle battery in a pristine futuristic Gigafactory. Intense physical realism, detailed pneumatic tubes, metallic reflections, glowing status LEDs, precise cinematic lighting.",
            "engine": "cosmos3 (Demo)",
            "aspect_ratio": "16:9",
            "image_url": "https://images.unsplash.com/photo-1616401784845-180882ba9ba8?auto=format&fit=crop&w=1024&q=80",
            "timestamp": "12:00:00 PM",
            "steps": 25,
            "cfg": 7.0,
            "seed": -1
        },
        {
            "id": "sample-2",
            "prompt": "A breathtaking wide-angle shot of Milford Sound, New Zealand. Mirror-like water reflecting massive fjords and waterfalls, dramatic mist rolling between the peaks, golden hour sunlight piercing through the storm clouds, hyper-detailed moss.",
            "engine": "cosmos3 (Demo)",
            "aspect_ratio": "16:9",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1024&q=80",
            "timestamp": "12:05:00 PM",
            "steps": 25,
            "cfg": 7.0,
            "seed": -1
        }
    ]
if "selected_image_index" not in st.session_state:
    st.session_state.selected_image_index = 0

# --- 後端 API 輔助函式 ---

def fetch_with_retry(url, headers, json_payload, max_retries=5):
    delay = 1.0
    for i in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=json_payload, timeout=60)
            # 遇到 429 或 5xx 伺服器錯誤時進行指數退避重試
            if response.status_code == 429 or response.status_code >= 500:
                if i == max_retries - 1:
                    return response
                time.sleep(delay)
                delay *= 2
                continue
            return response
        except Exception as e:
            if i == max_retries - 1:
                raise e
            time.sleep(delay)
            delay *= 2
    return None

def optimize_prompt(user_prompt, api_key):
    """呼叫 Gemini 2.0 Flash 進行 Prompt 擴寫與優化"""
    system_prompt = (
        "你是一個專業的 AI 繪圖 Prompt 提示詞優化專家。\n"
        "請將用戶輸入的簡單想法或提示詞，擴寫為適合 NVIDIA Cosmos 3 超高畫質物理圖像生成模型使用的詳細英文 Prompt。\n"
        "Cosmos 3 是一個物理真實性極高、世界模擬能力極強的模型，特別擅長細節、材質、物理光學、空間感。\n"
        "請輸出一個高水準的結構化英文 Prompt，包含：主體(Subject)、物理細節(Physical details)、光影(Lighting)、材質與質地(Textures & Materials)、相機透視(Camera perspective)。\n"
        "注意：請直接輸出最終的英文 Prompt 內容即可，千萬不要包含任何額外的解釋、引言、Markdown 標籤或符號。"
    )
    user_query = f"請優化以下提示詞：\n\"{user_prompt}\""
    
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(endpoint, json=payload, headers=headers, timeout=20)
    # 若 gemini-2.0-flash 回傳錯誤，嘗試備份的 gemini-1.5-flash 模型
    if response.status_code != 200:
        backup_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        response = requests.post(backup_endpoint, json=payload, headers=headers, timeout=20)
        
    if response.status_code != 200:
        raise Exception(f"Gemini API 呼叫失敗 ({response.status_code}): {response.text}")
        
    result = response.json()
    try:
        enhanced_text = result['candidates'][0]['content']['parts'][0]['text']
        return enhanced_text.strip()
    except KeyError:
        raise Exception("無法解析優化後的提示詞，請確認 API 格式或金鑰。")

def generate_cosmos3_image(prompt, negative_prompt, guidance_scale, steps, width, height, seed, token):
    """呼叫 Hugging Face 上的 nvidia/Cosmos3-Super-Text2Image"""
    url = "https://api-inference.huggingface.co/models/nvidia/Cosmos3-Super-Text2Image"
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Content-Type": "application/json"
    }
    
    # 決定隨機種子
    final_seed = seed if seed != -1 else random.randint(0, 100000)
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "guidance_scale": float(guidance_scale),
            "num_inference_steps": int(steps),
            "width": int(width),
            "height": int(height),
            "seed": final_seed
        }
    }
    
    response = fetch_with_retry(url, headers, payload)
    
    if response is None:
        raise Exception("連結 Hugging Face 伺服器超時。")
        
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            err_json = response.json()
            raise Exception(err_json.get("error", "Hugging Face 回傳錯誤，請確認 Token 與權限。"))
        return response.content
    else:
        try:
            err_json = response.json()
            raise Exception(err_json.get("error", f"HTTP {response.status_code}: {response.reason}"))
        except:
            raise Exception(f"HTTP {response.status_code}: {response.reason}")

def generate_imagen_image(prompt, api_key):
    """呼叫 Gemini 內建 Imagen 4.0 圖像生成模型"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={api_key}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1}
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    
    if response.status_code == 200:
        res_json = response.json()
        try:
            base64_data = res_json['predictions'][0]['bytesBase64Encoded']
            import base64
            image_bytes = base64.b64decode(base64_data)
            return image_bytes
        except KeyError:
            raise Exception("未接收到有效的圖像編碼數據。")
    else:
        try:
            err_json = response.json()
            error_msg = err_json.get("error", {}).get("message", f"HTTP {response.status_code}")
            raise Exception(f"Google Imagen API 錯誤: {error_msg}")
        except:
            raise Exception(f"HTTP {response.status_code}: {response.reason}")

# --- UI 頂部 Header 區塊 ---

st.markdown("""
<div class="app-header">
  <div class="logo-container">
    <div class="logo-box">⚙️</div>
    <div class="title-container">
      <div class="title-row">
        <h1 class="main-title">Cosmos 3 AI</h1>
        <span class="badge">NVIDIA Model Base</span>
      </div>
      <p class="subtitle">學生創新專題：高真物理影像生成學堂 (Streamlit版)</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# --- 側邊欄控制面板 (Sidebar) ---

with st.sidebar:
    st.markdown("### ⚙️ 核心設定與權杖")
    
    # 1. 選擇生成引擎
    engine_option = st.selectbox(
        "1. 選擇生成模型",
        ["Cosmos 3 Super (Hugging Face)", "Imagen 4.0 (Google API)"],
        index=0 if st.session_state.engine == "cosmos3" else 1
    )
    new_engine = "cosmos3" if "Cosmos 3" in engine_option else "gemini"
    if new_engine != st.session_state.engine:
        st.session_state.engine = new_engine
        
    # 2. Token 輸入框
    if st.session_state.engine == "cosmos3":
        hf_token_input = st.text_input(
            "🔑 Hugging Face Access Token",
            value=st.session_state.hf_token,
            type="password",
            help="請至 Hugging Face 申請 Read 權限的 Token 以呼叫服務"
        )
        if hf_token_input != st.session_state.hf_token:
            st.session_state.hf_token = hf_token_input
            
        # 顯示 Token 狀態
        if st.session_state.hf_token:
            st.markdown('<span style="color:#10b981; font-size:12px;">● HF Token: 已配置</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#f59e0b; font-size:12px;">● HF Token: 未設定 (將無法生成 Cosmos3 影像)</span>', unsafe_allow_html=True)
    else:
        st.info("💡 目前使用 Imagen 4.0 內建沙盒引擎，不需要 Hugging Face 權杖。")
        
    # Gemini Key 輸入框 (AI 智慧擴寫與 Imagen 皆需要)
    gemini_key_input = st.text_input(
        "🔑 Gemini API Key",
        value=st.session_state.gemini_key,
        type="password",
        help="擴寫提示詞與呼叫 Imagen API 需使用此 API Key"
    )
    if gemini_key_input != st.session_state.gemini_key:
        st.session_state.gemini_key = gemini_key_input
        
    if st.session_state.gemini_key:
         st.markdown('<span style="color:#10b981; font-size:12px;">● Gemini Key: 已配置</span>', unsafe_allow_html=True)
    else:
         st.markdown('<span style="color:#f59e0b; font-size:12px;">● Gemini Key: 未設定 (將無法使用 AI 擴寫)</span>', unsafe_allow_html=True)
         
    # 3. 進階生成設定 (僅在 Cosmos 3 下可用更多微調)
    st.markdown("---")
    st.markdown("### 🛠️ 進階參數微調")
    
    if st.session_state.engine == "cosmos3":
        # 畫面比例
        ratio_options = ["1:1", "16:9", "9:16"]
        ratio_index = ratio_options.index(st.session_state.aspect_ratio) if st.session_state.aspect_ratio in ratio_options else 0
        new_ratio = st.radio("畫面比例 (Aspect Ratio)", ratio_options, index=ratio_index, horizontal=True)
        if new_ratio != st.session_state.aspect_ratio:
            st.session_state.aspect_ratio = new_ratio
            
        # CFG Guidance Scale
        new_cfg = st.slider("提示詞相關度 (CFG Scale)", 1.0, 20.0, st.session_state.guidance_scale, step=0.5)
        if new_cfg != st.session_state.guidance_scale:
            st.session_state.guidance_scale = new_cfg
            
        # Steps
        new_steps = st.slider("去噪步數 (Steps)", 10, 50, st.session_state.inference_steps, step=1)
        if new_steps != st.session_state.inference_steps:
            st.session_state.inference_steps = new_steps
            
        # Seed
        new_seed = st.number_input("隨機種子 (Seed, -1為隨機)", value=st.session_state.seed, step=1)
        if new_seed != st.session_state.seed:
            st.session_state.seed = new_seed
            
        # 重設按鈕
        if st.button("🔄 重設所有參數"):
            st.session_state.aspect_ratio = "1:1"
            st.session_state.guidance_scale = 7.0
            st.session_state.inference_steps = 25
            st.session_state.seed = -1
            st.rerun()
    else:
        st.markdown("*目前引擎使用 Google Imagen 4.0，部分參數將由模型自動調配*")
        st.session_state.aspect_ratio = "1:1" # Imagen 4.0 預設 1:1


# --- 主畫面分頁導覽 ---

tab_generator, tab_architecture, tab_code = st.tabs(["🎨 創意繪圖板", "📐 系統架構圖", "💻 程式碼整合"])

# ==================== 分頁 1: 創意繪圖板 ====================
with tab_generator:
    
    col1, col2 = st.columns([5, 7], gap="large")
    
    # --- 左側：核心輸入面版 ---
    with col1:
        st.markdown("### 📝 1. 輸入繪圖提示詞")
        
        # 提示詞文字框
        prompt_val = st.text_area(
            "提示詞構想 (建議輸入英文)",
            value=st.session_state.prompt,
            placeholder="例如：An advanced industrial robotic arm assembling an electric vehicle... (建議輸入詳細英文描述，或點擊下方 AI 優化按鈕)",
            height=160,
            key="main_prompt_area"
        )
        if prompt_val != st.session_state.prompt:
            st.session_state.prompt = prompt_val
            
        # AI 智慧擴寫按鈕與邏輯
        c_opt, _ = st.columns([1, 1])
        with c_opt:
            disable_opt = not bool(st.session_state.prompt.strip())
            opt_btn = st.button("✨ AI 智慧擴寫 (Gemini)", disabled=disable_opt)
            if opt_btn:
                if not st.session_state.gemini_key.strip():
                    st.error("❌ 請先在左側設定 Gemini API Key！")
                else:
                    with st.spinner("✨ Gemini 正在最佳化提示詞物理描述..."):
                        try:
                            optimized = optimize_prompt(st.session_state.prompt, st.session_state.gemini_key)
                            st.session_state.prompt = optimized
                            st.toast("Prompt 擴寫成功！已套用至輸入框")
                            st.rerun()
                        except Exception as e:
                            st.error(f"擴寫失敗: {str(e)}")
                            
        # 負向提示詞 (僅限 Cosmos 3)
        if st.session_state.engine == "cosmos3":
            neg_val = st.text_input(
                "❌ 不希望出現的特徵 (Negative Prompt)",
                value=st.session_state.negative_prompt
            )
            if neg_val != st.session_state.negative_prompt:
                st.session_state.negative_prompt = neg_val
                
        st.markdown("---")
        
        # 生成影像按鈕
        generate_btn = st.button("🚀 開始生成影像", use_container_width=True)
        if generate_btn:
            if not st.session_state.prompt.strip():
                st.error("❌ 請輸入提示詞！")
            elif st.session_state.engine == "cosmos3" and not st.session_state.hf_token.strip():
                st.error("❌ 請先在左側設定 Hugging Face Access Token！")
            elif st.session_state.engine == "gemini" and not st.session_state.gemini_key.strip():
                st.error("❌ 請先在左側設定 Gemini API Key！")
            else:
                # 執行生成流程
                progress_placeholder = st.empty()
                progress_placeholder.info("⚙️ 正在初始化生成引擎與 GPU 算力集群...")
                
                # 計算實際寬高
                width, height = 1024, 1024
                if st.session_state.aspect_ratio == "16:9":
                    width, height = 1024, 576
                elif st.session_state.aspect_ratio == "9:16":
                    width, height = 576, 1024
                    
                try:
                    if st.session_state.engine == "cosmos3":
                        progress_placeholder.info("⚡ 正在傳送請求至 Hugging Face 雲端推理伺服器 (約需 10-30 秒)...")
                        
                        img_bytes = generate_cosmos3_image(
                            prompt=st.session_state.prompt,
                            negative_prompt=st.session_state.negative_prompt,
                            guidance_scale=st.session_state.guidance_scale,
                            steps=st.session_state.inference_steps,
                            width=width,
                            height=height,
                            seed=st.session_state.seed,
                            token=st.session_state.hf_token
                        )
                        engine_label = "nvidia/Cosmos3-Super-Text2Image"
                        steps_label = str(st.session_state.inference_steps)
                        cfg_label = str(st.session_state.guidance_scale)
                        seed_label = st.session_state.seed
                    else:
                        progress_placeholder.info("⚡ 正在傳送請求至 Google Imagen 4.0 圖像渲染伺服器...")
                        
                        img_bytes = generate_imagen_image(
                            prompt=st.session_state.prompt,
                            api_key=st.session_state.gemini_key
                        )
                        engine_label = "Google Imagen 4.0"
                        steps_label = "Auto"
                        cfg_label = "Auto"
                        seed_label = -1
                        
                    progress_placeholder.empty()
                    
                    # 寫入歷史紀錄
                    new_record = {
                        "id": f"gen-{int(time.time()*1000)}",
                        "prompt": st.session_state.prompt,
                        "engine": engine_label,
                        "aspect_ratio": st.session_state.aspect_ratio,
                        "image_bytes": img_bytes,
                        "timestamp": datetime.datetime.now().strftime("%I:%M:%S %p"),
                        "steps": steps_label,
                        "cfg": cfg_label,
                        "seed": seed_label
                    }
                    
                    st.session_state.history.insert(0, new_record)
                    st.session_state.selected_image_index = 0
                    st.toast("🎨 影像生成成功！")
                    st.rerun()
                    
                except Exception as e:
                    progress_placeholder.empty()
                    st.error(f"❌ 影像生成失敗: {str(e)}")
                    
    # --- 右側：圖像畫布與歷程 ---
    with col2:
        st.markdown("### 🖼️ AI 核心畫布區")
        
        # 取得當前選取的圖片記錄
        active_record = None
        if st.session_state.selected_image_index is not None and len(st.session_state.history) > st.session_state.selected_image_index:
            active_record = st.session_state.history[st.session_state.selected_image_index]
            
        if active_record:
            # 顯示影像畫布
            if "image_url" in active_record:
                # 樣式範例圖片
                st.image(active_record["image_url"], use_container_width=True)
            elif "image_bytes" in active_record:
                # API 生成二進制圖片
                st.image(active_record["image_bytes"], use_container_width=True)
                
            # 工具控制列：下載與提示詞複製
            c_dl, c_copy = st.columns([1, 1])
            with c_dl:
                if "image_url" in active_record:
                    st.markdown(f'<a href="{active_record["image_url"]}" target="_blank" style="text-decoration:none;"><button style="background-color:#1e293b; color:#76b900; font-weight:700; width:100%; border:none; border-radius:8px; padding:10px;">🔗 連結下載大圖</button></a>', unsafe_allow_html=True)
                elif "image_bytes" in active_record:
                    st.download_button(
                        label="💾 下載高畫質大圖",
                        data=active_record["image_bytes"],
                        file_name=f"cosmos3_{active_record['id']}.png",
                        mime="image/png"
                    )
            with c_copy:
                # 使用單擊一鍵複製的輸入欄位
                st.text_input(
                    "單擊下方以選取複製提示詞 (Copy Prompt)",
                    value=active_record["prompt"],
                    key="copy_prompt_input",
                    label_visibility="collapsed"
                )
                
            # 生成細節參數卡
            st.markdown(f"""
            <div class="custom-card">
                <p style="margin:0 0 8px 0; font-size:13px; line-height:1.5;">💡 <b>生成 Prompt:</b> {active_record['prompt']}</p>
                <div style="display:flex; flex-wrap:wrap; gap:12px; font-size:11px; color:#94a3b8; border-top:1px solid #1e293b; padding-top:8px; font-family:monospace;">
                    <span>引擎: <b style="color:#ffffff;">{active_record['engine']}</b></span>
                    <span>去噪步數: <b style="color:#ffffff;">{active_record['steps']}</b></span>
                    <span>引導系數: <b style="color:#ffffff;">{active_record['cfg']}</b></span>
                    <span>比例: <b style="color:#ffffff;">{active_record['aspect_ratio']}</b></span>
                    <span>種子: <b style="color:#ffffff;">{active_record['seed']}</b></span>
                    <span style="margin-left:auto;">{active_record['timestamp']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 空白畫布引導
            st.markdown("""
            <div style="background-color:#05080f; border:1px dashed #1e293b; border-radius:12px; height:360px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:24px;">
                <div style="font-size:48px; margin-bottom:12px; color:#475569;">🖼️</div>
                <h4 style="color:#cbd5e1; margin-bottom:4px;">準備就緒，等候指令</h4>
                <p style="color:#64748b; font-size:12px; max-width:320px;">請在左側輸入提示詞並點擊「開始生成」，或者直接套用下方的學術示範提示詞快速體驗！</p>
            </div>
            """, unsafe_allow_html=True)

    # --- 下方：歷程記錄畫廊與示範庫 ---
    st.markdown("---")
    st.markdown("### 📚 教學範例庫 (點擊直接套用)")
    
    examples = [
        {
            "title": "🤖 未來物理工廠 (Cosmos擅長)",
            "desc": "An advanced industrial robotic arm assembling an electric vehicle battery in a pristine futuristic Gigafactory. Intense physical realism, detailed pneumatic tubes, metallic reflections."
        },
        {
            "title": "🌧️ 台北賽博朋克夜色 (光影反射)",
            "desc": "A cinematic hyper-realistic shot of Taipei City in the year 2099. Cyberpunk skyscrapers with giant holograms, wet street reflecting multi-colored neon signs in Traditional Chinese."
        },
        {
            "title": "🌊 紐西蘭魔戒峽灣 (大自然細節)",
            "desc": "A breathtaking wide-angle shot of Milford Sound, New Zealand. Mirror-like water reflecting massive fjords and waterfalls, golden hour sunlight piercing through storm clouds."
        },
        {
            "title": "🔮 桌上懸浮星系 (折射玻璃)",
            "desc": "A floating glass sphere holding a miniature solar system inside. The glass sphere is sitting on a dark volcanic beach sand, reflecting ocean waves. Macro shot, highly detailed."
        }
    ]
    
    ex_cols = st.columns(4)
    for i, ex in enumerate(examples):
        with ex_cols[i]:
            st.markdown('<div class="example-btn-container">', unsafe_allow_html=True)
            if st.button(f"**{ex['title']}**\n\n{ex['desc']}", key=f"ex_btn_{i}"):
                st.session_state.prompt = ex["desc"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
    # 歷史歷程回顧
    if st.session_state.history:
        st.markdown("---")
        h_col1, h_col2 = st.columns([8, 2])
        with h_col1:
            st.markdown(f"### 🕒 本次繪圖歷程紀錄 ({len(st.session_state.history)})")
        with h_col2:
            if st.button("🗑️ 清空歷史紀錄", use_container_width=True):
                st.session_state.history = []
                st.session_state.selected_image_index = None
                st.rerun()
                
        # 顯示歷史縮圖列表
        hist_cols = st.columns(6)
        for index, item in enumerate(st.session_state.history):
            col_idx = index % 6
            with hist_cols[col_idx]:
                # 設定按鈕外框高亮
                btn_style = "history-btn-selected" if st.session_state.selected_image_index == index else "history-btn"
                st.markdown(f'<div class="{btn_style}">', unsafe_allow_html=True)
                
                # 顯示縮圖預覽
                if "image_url" in item:
                    st.image(item["image_url"], use_container_width=True)
                elif "image_bytes" in item:
                    st.image(item["image_bytes"], use_container_width=True)
                    
                # 檢視按鈕
                if st.button(f"🔍 檢視 #{len(st.session_state.history) - index}", key=f"sel_hist_{item['id']}"):
                    st.session_state.selected_image_index = index
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)


# ==================== 分頁 2: 系統與 API 架構分析 ====================
with tab_architecture:
    st.markdown("## 📐 NVIDIA Cosmos 3 Web App 系統運作架構")
    st.write("幫助學生理解前後端、Hugging Face 雲端算力與 Gemini 智慧擴寫大語言模型之間的「模型鏈 (Model Chaining)」與傳輸機制。")
    
    # 流程架構圖 (Mermaid)
    st.markdown("### 🧬 系統流程圖")
    st.markdown("""
```mermaid
graph TD
    A[1. 前端 UI (Streamlit)] -->|1. 輸入創意提示詞| B(2. Gemini API)
    B -->|2. AI 智慧物理擴寫| A
    A -->|3. POST 傳送參數與密鑰| C{3. 推理路由}
    C -->|Cosmos 3| D[4a. HF Serverless API]
    C -->|Imagen 4.0| E[4b. Google Imagen API]
    D -->|H100 物理去噪| F[5. 圖像還原 (二進制/Base64)]
    E -->|Imagen 矩陣計算| F
    F -->|6. 前端渲染與展示| A
```
""")
    
    # 視覺化步驟小卡
    st.markdown("""
    <div class="arch-container">
        <div class="arch-grid">
            <div class="arch-card">
                <div class="arch-icon">🎛️</div>
                <div class="arch-title">1. 前端 UI 介面</div>
                <div class="arch-desc">學生輸入創意想法，設定 Aspect Ratio、CFG、Steps 與隨機種子。</div>
            </div>
            <div class="arch-card">
                <div class="arch-icon">✨</div>
                <div class="arch-title">2. Gemini 擴寫大師</div>
                <div class="arch-desc">大模型將用戶直覺的字彙擴寫為具備物理細節、光學、鏡頭感的 Cosmos 優化提示詞。</div>
            </div>
            <div class="arch-card">
                <div class="arch-icon">🔐</div>
                <div class="arch-title">3. API 安全請求</div>
                <div class="arch-desc">發送 HTTP POST 請求，將設定參數與 API Bearer Key 安全傳送至雲端。</div>
            </div>
            <div class="arch-card">
                <div class="arch-icon">⚡</div>
                <div class="arch-title">4. 算力集群物理渲染</div>
                <div class="arch-desc">Nvidia Cosmos 3 (64B) / Google Imagen 於多張 GPU 進行降噪與高保真矩陣渲染。</div>
            </div>
            <div class="arch-card">
                <div class="arch-icon">🖼️</div>
                <div class="arch-title">5. 圖像解碼還原</div>
                <div class="arch-desc">前端接收二進制 Blob 數據或 Base64 字串，並在網頁中安全還原與儲存。</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 技術特性介紹與討論
    t_col1, t_col2 = st.columns(2, gap="medium")
    with t_col1:
        st.markdown("""
        ### 🔬 NVIDIA Cosmos 3 Super 技術優勢
        - **物理世界大模型**：Cosmos 3 具備超高解析度的物理真實感，是 NVIDIA 針對世界模擬器推出的新一代生成權重。
        - **640 億參數混合架構**：採用雙塔式 Mixture-of-Transformers (MoT)，結合 Autoregressive 技術與 Diffusion 去噪核心。
        - **時間與空間 mRoPE 技術**：利用 Multidimensional Rotary Position Embedding 保持畫面 3D 空間深度的物理張力。
        - **高擬真折射與流體**：在光學玻璃折射、金屬拉絲材質、流體重力模擬上居於領先地位。
        """)
    with t_col2:
        st.markdown("""
        ### 💡 學生實驗專題思考與討論
        > 🔍 **思考一：為什麼我們不將 Cosmos 3 權重直接下載到本地端部署？**
        > 因其模型參數高達 64B，本地推理至少需要 128GB 以上的顯示記憶體 (VRAM)，這代表需要 2 張以上 NVIDIA H100 GPU。這凸顯了本專案整合「Hugging Face Serverless 推理 API」對一般學生進行研究的輕量便利性。
        
        > 🔍 **思考二：何謂 Prompt Upsampling (提示詞優化)？**
        > Cosmos 3 是高度物理導向的模型，需要非常具體的細節引導。透過 Gemini 擴寫，能幫我們在提示詞中自動添加「金屬拉絲質地、鏡頭焦距、丁達爾效應光影」等描述，使得最終生成畫作更具有物理真實感（Physical Realism）。
        """)


# ==================== 分頁 3: 整合程式碼 ====================
with tab_code:
    st.markdown("## 💻 後端與命令列自動化整合代碼 (API Integration)")
    st.write("以下程式碼是根據您在「創意繪圖板」中目前的 Prompt 及進階參數（CFG、去噪步數、畫面比例等）即時渲染而成。您可以直接複製，在 Jupyter Notebook 或 Linux Terminal 中進行後端程式化生成。")
    
    # 準備程式碼所需的參數
    current_prompt = st.session_state.prompt if st.session_state.prompt else "A majestic medieval castle on a floating island..."
    current_neg = st.session_state.negative_prompt
    current_cfg = st.session_state.guidance_scale
    current_steps = st.session_state.inference_steps
    current_seed = st.session_state.seed
    
    w_px, h_px = 1024, 1024
    if st.session_state.aspect_ratio == "16:9":
        w_px, h_px = 1024, 576
    elif st.session_state.aspect_ratio == "9:16":
        w_px, h_px = 576, 1024
        
    token_str = st.session_state.hf_token if st.session_state.hf_token else "YOUR_HF_TOKEN_HERE"
    
    # 1. Python Code
    python_script = f"""import requests

# 1. 配置 API 端點與 Hugging Face Access Token
API_URL = "https://api-inference.huggingface.co/models/nvidia/Cosmos3-Super-Text2Image"
headers = {{"Authorization": "Bearer {token_str}"}}

def query_cosmos(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"API 錯誤 (HTTP {{response.status_code}}): {{response.text}}")
    return response.content

# 2. 定義 Cosmos 3 生成參數
payload = {{
    "inputs": "{current_prompt.replace('"', '\\"')}",
    "parameters": {{
        "negative_prompt": "{current_neg}",
        "guidance_scale": {current_cfg},
        "num_inference_steps": {current_steps},
        "width": {w_px},
        "height": {h_px},
        "seed": {current_seed if current_seed != -1 else 'random.randint(0, 100000)'}
    }}
}}

print("正在發送請求至 Hugging Face 雲端推理端點...")
try:
    image_bytes = query_cosmos(payload)
    
    # 3. 將二進制圖片儲存至本地端
    with open("cosmos3_output.jpg", "wb") as f:
        f.write(image_bytes)
    print("✨ 圖像生成成功！已儲存為 cosmos3_output.jpg")
except Exception as e:
    print(f"❌ 生成失敗: {{e}}")
"""

    # 2. cURL Command
    curl_prompt = current_prompt.replace("'", "'\\''")
    curl_command = f"""curl https://api-inference.huggingface.co/models/nvidia/Cosmos3-Super-Text2Image \\
  -X POST \\
  -H "Authorization: Bearer {token_str}" \\
  -H "Content-Type: application/json" \\
  -d '{{"inputs": "{curl_prompt}", "parameters": {{"negative_prompt": "{current_neg}", "guidance_scale": {current_cfg}, "num_inference_steps": {current_steps}, "width": {w_px}, "height": {h_px}, "seed": {current_seed}}}}}' \\
  --output cosmos3_image.jpg"""

    lang_py, lang_curl = st.tabs(["🐍 Python Requests 腳本", "🖥️ cURL 終端機指令"])
    
    with lang_py:
        st.write("直接將此 Python 程式碼複製到您的 Jupyter Notebook 或專案檔中：")
        st.code(python_script, language="python")
        
    with lang_curl:
        st.write("直接在 Linux/macOS Terminal 或 Windows PowerShell 中執行此指令：")
        st.code(curl_command, language="bash")
        
    st.markdown("""
    ---
    #### 🎓 學術筆記：如何進行本地部署與微調？
    NVIDIA Cosmos 隨附了專門的輕量化推演容器 `vllm-omni:cosmos3`。對於學校實驗室具備頂規硬體（例如 8x H100 節點）的開發團隊，可以使用該容器在內網啟動與 OpenAI 相容的 API 伺服器，並以此前端網頁更換後端 endpoint，即可實現完全自主控制的校園 AI 圖像生成系統！
    """)

# --- 頁尾 Footer 區塊 ---
st.markdown("""
<div style="border-top: 1px solid #1e293b; padding-top: 20px; margin-top: 50px; text-align: center; font-size: 12px; color: #64748b;">
  <p>© 2026 Cosmos 3 AI 繪圖工坊. 基於開源 AI 科普教學專題專用架構</p>
  <p>
    <a href="https://huggingface.co/nvidia/Cosmos3-Super-Text2Image" target="_blank" style="color:#76b900; text-decoration:none; margin-right:12px;">Hugging Face 模型頁面 🔗</a>
    <a href="https://github.com/nvidia/cosmos" target="_blank" style="color:#76b900; text-decoration:none;">NVIDIA Cosmos GitHub 🔗</a>
  </p>
</div>
""", unsafe_allow_html=True)
