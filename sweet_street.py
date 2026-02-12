import math
import random
import time
from datetime import timedelta
import streamlit as st

CAKE_TIME_LIMIT_SECONDS = 45

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Sweet Street", page_icon="🍰", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #FFF8E7; }
    [data-testid="stSidebar"] {
        background-color: #FFB7B2;
        border-left: 2px solid #E27D60;
    }
    [data-testid="stSidebar"] h1 { font-size: 2.25rem; font-weight: bold; }
    [data-testid="stSidebar"] .stMarkdown { color: #5D4037; }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #5D4037; }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] { color: #5D4037; }
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background-color: #E3F2FD;
        border: 1px solid #BBDEFB;
        color: #5D4037;
    }
    [data-testid="stAlert"] {
        background-color: #E3F2FD !important;
        border: 1px solid #BBDEFB !important;
        color: #5D4037 !important;
    }
    [data-testid="stAlert"] div,
    [data-testid="stAlert"] section {
        background-color: #E3F2FD !important;
    }
    div.stButton > button {
        background-color: #FFB7B2; color: white; border-radius: 20px;
        border: 2px solid #E27D60; font-weight: bold; width: 100%;
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #E27D60; }
    h1, h2, h3 { font-family: 'Comic Sans MS', sans-serif; color: #5D4037; }
    .poetic-text {
        font-style: italic; color: #555; font-size: 1.3rem; background: #fff;
        padding: 20px; border-left: 6px solid #FFB7B2; margin: 20px 0; border-radius: 5px;
    }
    [data-testid="stSelectbox"], [data-testid="stRadio"], [data-testid="stMultiSelect"],
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #E3F2FD;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    [data-testid="stExpander"] {
        background-color: #E3F2FD;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- GAME DATA ---
GAME_DATA = {
    "bases": {
        "Vanilla Sponge": {"color": "#F3E5AB", "tags": ["Comfort", "Classic"], "dark_color": "#D4C58B"},
        "Chocolate Sponge": {"color": "#5D4037", "tags": ["Rich", "Dark"], "dark_color": "#3E2723"},
        "Strawberry Sponge": {"color": "#FFB7B2", "tags": ["Sweet", "Fruity"], "dark_color": "#E27D60"},
        "Lemon Sponge": {"color": "#F9F0C7", "tags": ["Zesty", "Bright"], "dark_color": "#E6D96A"},
        "Coconut Sponge": {"color": "#F5F5DC", "tags": ["Smooth", "Light"], "dark_color": "#E0E0C8"},
        "Red Velvet": {"color": "#722F37", "tags": ["Rich", "Decadent"], "dark_color": "#4A1C22"},
        "Confetti Sponge": {"color": "#FFF0F5", "tags": ["Sweet", "Comfort"], "dark_color": "#F0D0E0"},
    },
    "fillings": {
        "Vanilla Cream": {"color": "#FFFDD0", "tags": ["Smooth", "Light"]},
        "Dark Ganache": {"color": "#3E2723", "tags": ["Decadent", "Heavy"]},
        "Lemon Curd": {"color": "#FFF176", "tags": ["Zesty", "Bright"]},
        "Cherry Compote": {"color": "#C62828", "tags": ["Tart", "Deep"]},
    },
    "frostings": {
        "Cherry Red": {"color": "#D32F2F", "vibe": "Romantic", "stroke": "#B71C1C"},
        "Tangerine": {"color": "#FF9800", "vibe": "Energetic", "stroke": "#E65100"},
        "Sunshine Yellow": {"color": "#FFF176", "vibe": "Energetic", "stroke": "#FBC02D"},
        "Forest Green": {"color": "#66BB6A", "vibe": "Natural", "stroke": "#388E3C"},
        "Midnight Blue": {"color": "#1A237E", "vibe": "Melancholy", "stroke": "#0D47A1"},
        "Royal Purple": {"color": "#7B1FA2", "vibe": "Whimsical", "stroke": "#4A148C"},
        "Blush Pink": {"color": "#FF8A80", "vibe": "Romantic", "stroke": "#D32F2F"},
        "Cloud White": {"color": "#FFFFFF", "vibe": "Clean", "stroke": "#E0E0E0"},
        "Warm Brown": {"color": "#795548", "vibe": "Natural", "stroke": "#5D4037"},
    },
    "decorations": {
        "🍒 Cherries": {"icon": "🍒", "vibe": "Romantic"},
        "🌹 Rose Petal": {"icon": "🌹", "vibe": "Romantic"},
        "🍓 Strawberry": {"icon": "🍓", "vibe": "Natural"},
        "🌸 Cherry Blossom": {"icon": "🌸", "vibe": "Romantic"},
        "🍋 Lemon Slice": {"icon": "🍋", "vibe": "Energetic"},
        "⭐ Star": {"icon": "⭐", "vibe": "Whimsical"},
        "🌿 Mint Leaf": {"icon": "🌿", "vibe": "Natural"},
        "🫐 Blueberries": {"icon": "🫐", "vibe": "Melancholy"},
        "🍇 Grapes": {"icon": "🍇", "vibe": "Melancholy"},
        "✨ Stardust": {"icon": "✨", "vibe": "Whimsical"},
        "❄️ Snowflake": {"icon": "❄️", "vibe": "Whimsical"},
        "🍬 Gummy Worm": {"icon": "🍬", "vibe": "Chaotic"},
        "🍫 Chocolate Drizzle": {"icon": "🍫", "vibe": "Chaotic"},
    }
}

# Characters (rotate through these); order is chosen randomly each time
CHARACTERS = [
    {"customer": "Ella", "avatar": "👩🏻"},
    {"customer": "Rafael", "avatar": "🧑🏾"},
    {"customer": "Pepper", "avatar": "👱🏻‍♀️"},
    {"customer": "Claire", "avatar": "👩🏻‍🦰"},
    {"customer": "Jack", "avatar": "🧑🏻"},
]

# 23 possible orders — each level picks one at random (req_* must match GAME_DATA)
ORDERS = [
    {"quote": "The sky is crying, but I feel safe inside. Make me a taste of that gray comfort.", "req_flavor": ["Comfort", "Classic"], "req_color": "#1A237E", "req_vibe": "Melancholy"},
    {"quote": "My heart burns! It is a volcano of passion! I need intensity!", "req_flavor": ["Rich", "Decadent"], "req_color": "#FF8A80", "req_vibe": "Romantic"},
    {"quote": "ZOOM! I need rocket fuel! Something bright that pops in my mouth!", "req_flavor": ["Zesty", "Bright"], "req_color": "#FFF176", "req_vibe": "Energetic"},
    {"quote": "Something pure and simple. Clean lines, clean taste. No fuss.", "req_flavor": ["Smooth", "Light"], "req_color": "#FFFFFF", "req_vibe": "Natural"},
    {"quote": "I'm in a deep mood. Give me something dark and serious.", "req_flavor": ["Tart", "Deep"], "req_color": "#1A237E", "req_vibe": "Melancholy"},
    {"quote": "Indulge me. I want rich, heavy, and unforgettable.", "req_flavor": ["Decadent", "Heavy"], "req_color": "#1A237E", "req_vibe": "Melancholy"},
    {"quote": "Sweet like summer fruit, and pretty as a sunset.", "req_flavor": ["Sweet", "Fruity"], "req_color": "#FF8A80", "req_vibe": "Romantic"},
    {"quote": "I need calm. Earth tones, natural vibes, nothing fake.", "req_flavor": ["Comfort", "Classic"], "req_color": "#66BB6A", "req_vibe": "Natural"},
    {"quote": "Dark chocolate energy. Moody and intense.", "req_flavor": ["Rich", "Dark"], "req_color": "#1A237E", "req_vibe": "Melancholy"},
    {"quote": "Zing! Fresh, green, and full of life!", "req_flavor": ["Zesty", "Bright"], "req_color": "#66BB6A", "req_vibe": "Natural"},
    {"quote": "Bright and sunny — I need a boost!", "req_flavor": ["Smooth", "Light"], "req_color": "#FFF176", "req_vibe": "Energetic"},
    {"quote": "Surprise me. Something a little magical and unexpected.", "req_flavor": ["Tart", "Deep"], "req_color": "#FF8A80", "req_vibe": "Whimsical"},
    {"quote": "Go wild. I don't care if it makes sense — just go for it!", "req_flavor": ["Decadent", "Heavy"], "req_color": "#FFF176", "req_vibe": "Chaotic"},
    {"quote": "Like a cozy blanket and a rainy afternoon. Soft and familiar.", "req_flavor": ["Comfort", "Classic"], "req_color": "#FFFFFF", "req_vibe": "Natural"},
    {"quote": "Bold. In your face. I want to taste the drama.", "req_flavor": ["Rich", "Dark"], "req_color": "#795548", "req_vibe": "Chaotic"},
    {"quote": "Tart and moody. Think autumn leaves and red wine.", "req_flavor": ["Tart", "Deep"], "req_color": "#D32F2F", "req_vibe": "Romantic"},
    {"quote": "Light as a cloud, bright as morning. Wake me up!", "req_flavor": ["Smooth", "Light"], "req_color": "#FFF176", "req_vibe": "Energetic"},
    {"quote": "A little magic, a little mystery. Purple dreams.", "req_flavor": ["Sweet", "Fruity"], "req_color": "#7B1FA2", "req_vibe": "Whimsical"},
    {"quote": "Heavy and luxurious. I want to sink into it.", "req_flavor": ["Decadent", "Heavy"], "req_color": "#795548", "req_vibe": "Melancholy"},
    {"quote": "Fresh citrus burst! No holding back.", "req_flavor": ["Zesty", "Bright"], "req_color": "#FF9800", "req_vibe": "Energetic"},
    {"quote": "Romantic and dreamy. Pink skies and sugar.", "req_flavor": ["Sweet", "Fruity"], "req_color": "#FF8A80", "req_vibe": "Romantic"},
    {"quote": "Green and growing. Earthy and real.", "req_flavor": ["Comfort", "Classic"], "req_color": "#66BB6A", "req_vibe": "Natural"},
    {"quote": "Wild and weird. Break the rules.", "req_flavor": ["Decadent", "Heavy"], "req_color": "#7B1FA2", "req_vibe": "Chaotic"},
    {"quote": "Deep blue feelings. Quiet and thoughtful.", "req_flavor": ["Tart", "Deep"], "req_color": "#1A237E", "req_vibe": "Melancholy"},
]

# --- SVG ENGINE (3D-style round cake: layers, gloss, sparkles) ---
def render_cake_svg(base, filling, frosting, decorations):
    svg = []
    svg.append('<defs>')
    svg.append('<linearGradient id="plateGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" style="stop-color:#F5F5F5"/><stop offset="100%" style="stop-color:#E8E8E8"/></linearGradient>')
    svg.append('<filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    svg.append('<filter id="sparkleGlow"><feGaussianBlur stdDeviation="1.5" result="blur"/><feFlood flood-color="#FFF9C4" flood-opacity="0.9"/><feComposite in2="blur" operator="in"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    svg.append('</defs>')
    # 1. Plate (soft gradient, slight 3D)
    svg.append('<ellipse cx="200" cy="318" rx="155" ry="55" fill="url(#plateGrad)" stroke="#E0E0E0" stroke-width="1.5"/>')
    svg.append('<ellipse cx="200" cy="312" rx="125" ry="45" fill="#FAFAFA" stroke="#EEEEEE" stroke-width="1"/>')

    def add_gradient(name, base_hex, dark_hex=None):
        dark_hex = dark_hex or base_hex
        svg.append(f'<linearGradient id="{name}" x1="0%" y1="100%" x2="0%" y2="0%">')
        svg.append(f'<stop offset="0%" style="stop-color:{dark_hex};stop-opacity:1"/>')
        svg.append(f'<stop offset="50%" style="stop-color:{base_hex};stop-opacity:1"/>')
        svg.append(f'<stop offset="100%" style="stop-color:{base_hex};stop-opacity:1"/>')
        svg.append('</linearGradient>')

    # 2. Base layer (round cake body with gradient for gloss)
    if base and base in GAME_DATA["bases"]:
        b_data = GAME_DATA["bases"][base]
        add_gradient("baseGrad", b_data["color"], b_data["dark_color"])
        # Side of cake (curved band)
        svg.append(f'<path d="M75,252 L75,298 A125,45 0 0,0 325,298 L325,252" fill="url(#baseGrad)" stroke="{b_data["dark_color"]}" stroke-width="1.5" opacity="0.95"/>')
        # Top ellipse of base (visible “layer”)
        svg.append(f'<ellipse cx="200" cy="252" rx="125" ry="45" fill="{b_data["color"]}" stroke="{b_data["dark_color"]}" stroke-width="1"/>')

    # 3. Filling layer (distinct band)
    if filling and filling in GAME_DATA["fillings"] and base:
        f_col = GAME_DATA["fillings"][filling]["color"]
        svg.append(f'<path d="M75,265 A125,45 0 0,0 325,265 L325,278 A125,45 0 0,1 75,278 Z" fill="{f_col}" stroke="{f_col}" stroke-width="0.5" opacity="0.98"/>')

    # 4. Frosting (smooth top + soft drip, gradient for glossy look)
    if frosting and frosting in GAME_DATA["frostings"]:
        fr_data = GAME_DATA["frostings"][frosting]
        c = fr_data["color"]
        s = fr_data["stroke"]
        svg.append(f'<linearGradient id="frostGrad" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" style="stop-color:{s}"/><stop offset="100%" style="stop-color:{c}"/></linearGradient>')
        # Gentle drips
        drips = "M75,252 Q105,278 140,255 T200,268 T260,252 T325,252"
        svg.append(f'<path d="{drips} L325,232 A125,45 0 0,0 75,232 Z" fill="url(#frostGrad)" stroke="{s}" stroke-width="1.5"/>')
        svg.append(f'<ellipse cx="200" cy="232" rx="125" ry="45" fill="{c}" stroke="{s}" stroke-width="1"/>')

    # 5. Sparkles (golden glow above cake, like reference)
    sparkle_pts = [(120, 175), (200, 155), (280, 178), (165, 195), (235, 192)]
    for sx, sy in sparkle_pts:
        svg.append(f'<circle cx="{sx}" cy="{sy}" r="4" fill="#FFF9C4" filter="url(#sparkleGlow)" opacity="0.85"/>')
        svg.append(f'<circle cx="{sx}" cy="{sy}" r="1.5" fill="#FFFDE7"/>')

    # 6. Decorations — 4 per topping, slightly inward from the rim so they sit on the cake; slots interleaved so toppings don't overlap
    # 12 positions on an inner ellipse (cx=200, cy=232), ~80% of rim radius so still on the frosting
    rim_slots = []
    rx_inner, ry_inner = 100, 36
    for i in range(12):
        ang = i * (2 * math.pi / 12)
        rim_slots.append((round(200 + rx_inner * math.cos(ang)), round(232 + ry_inner * math.sin(ang))))
    # Assign interleaved: topping 1 → slots 0,3,6,9; topping 2 → 1,4,7,10; topping 3 → 2,5,8,11
    for i, deco_name in enumerate(decorations):
        if i < 3 and deco_name in GAME_DATA["decorations"]:
            icon = GAME_DATA["decorations"][deco_name]["icon"]
            for j in range(4):
                x, y = rim_slots[i + j * 3]
                svg.append(f'<g filter="url(#softGlow)"><text x="{x}" y="{y}" font-size="26" text-anchor="middle" style="filter: drop-shadow(0 1px 2px rgba(255,255,255,0.8)) drop-shadow(1px 2px 3px rgba(0,0,0,0.15));">{icon}</text></g>')

    return f'<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">{"".join(svg)}</svg>'

# --- STATE MANAGEMENT (THE FIX) ---
if "level_idx" not in st.session_state:
    st.session_state.level_idx = 0
    st.session_state.score = 0
    st.session_state.phase = "ORDER"
    st.session_state.current_order = random.choice(ORDERS)
    
    # PERMANENT MEMORY FOR THE CAKE
    st.session_state.final_cake = {
        "base": list(GAME_DATA["bases"].keys())[0],
        "filling": list(GAME_DATA["fillings"].keys())[0],
        "frosting": list(GAME_DATA["frostings"].keys())[0],
        "decorations": []
    }

def save_baking_choice(base, filling):
    """Force save the choices before moving to next screen"""
    st.session_state.final_cake["base"] = base
    st.session_state.final_cake["filling"] = filling

def save_decor_choice(frosting, decos):
    """Force save decorations"""
    st.session_state.final_cake["frosting"] = frosting
    st.session_state.final_cake["decorations"] = decos

def get_player_level():
    """Level 1 at 0–9 stars, level 2 at 10–19, etc."""
    return (st.session_state.score // 10) + 1

def get_available_bases():
    """Bases unlocked for current level: 3 at level 1, +1 per level after."""
    level = get_player_level()
    all_bases = list(GAME_DATA["bases"].keys())
    return all_bases[: min(2 + level, len(all_bases))]

def next_level():
    st.session_state.level_idx = (st.session_state.level_idx + 1) % len(CHARACTERS)
    st.session_state.current_order = random.choice(ORDERS)
    available = get_available_bases()
    st.session_state.final_cake = {
        "base": available[0],
        "filling": list(GAME_DATA["fillings"].keys())[0],
        "frosting": list(GAME_DATA["frostings"].keys())[0],
        "decorations": []
    }
    st.session_state.phase = "ORDER"

# --- MAIN RENDER LOOP ---
current_character = CHARACTERS[st.session_state.level_idx]
current_order = st.session_state.current_order

@st.fragment(run_every=timedelta(seconds=1))
def cake_timer():
    """Runs every second when in BAKE or DECORATE; shows countdown and auto-submits when time is up."""
    if st.session_state.get("phase") not in ("BAKE", "DECORATE"):
        return
    start = st.session_state.get("order_start_time")
    if start is None:
        st.session_state.order_start_time = time.time()
        start = st.session_state.order_start_time
    elapsed = time.time() - start
    remaining = max(0, CAKE_TIME_LIMIT_SECONDS - elapsed)
    mins, secs = int(remaining // 60), int(remaining % 60)
    st.metric("Time left", f"{mins}:{secs:02d}")
    if remaining <= 0:
        st.session_state.phase = "RESULT"
        st.rerun()

# Sidebar
current_level = get_player_level()
with st.sidebar:
    st.title("Sweet Street")
    st.metric("Level", current_level)
    st.metric("Total Score", f"{st.session_state.score} Stars")
    next_at = current_level * 10
    st.caption(f"New cake flavor at {next_at} stars")
    if st.session_state.get("phase") in ("BAKE", "DECORATE"):
        cake_timer()
    st.info("💡 Hint: Read the customer's quote carefully. Colors and feelings matter more than recipes!")

# PHASE 1: ORDER
if st.session_state.phase == "ORDER":
    st.markdown(f"## Customer: {current_character['customer']}")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<div style='font-size:120px; text-align:center;'>{current_character['avatar']}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='poetic-text'>“{current_order['quote']}”</div>", unsafe_allow_html=True)
        if st.button("Start Baking"):
            st.session_state.phase = "BAKE"
            st.session_state.order_start_time = time.time()
            st.rerun()

# PHASE 2: BAKING
elif st.session_state.phase == "BAKE":
    st.title("The Kitchen")
    
    vis_col, ctrl_col = st.columns([1, 1])
    
    # CONTROLS
    with ctrl_col:
        st.subheader("Mix Ingredients")
        st.info(f"Order: \"{current_order['quote']}\"")
        
        # We use local variables for the widget; only show bases unlocked for current level
        available_bases = get_available_bases()
        current_base = st.session_state.final_cake["base"]
        if current_base not in available_bases:
            current_base = available_bases[0]
            st.session_state.final_cake["base"] = current_base
        selected_base = st.selectbox(
            "Choose Base", 
            available_bases, 
            index=available_bases.index(current_base)
        )
        
        selected_filling = st.selectbox(
            "Choose Filling", 
            list(GAME_DATA["fillings"].keys()),
            index=list(GAME_DATA["fillings"].keys()).index(st.session_state.final_cake["filling"])
        )
        
        # Update the visual preview immediately in memory so the left col sees it
        st.session_state.final_cake["base"] = selected_base
        st.session_state.final_cake["filling"] = selected_filling
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Put in Oven"):
            # Explicitly Save before moving on
            save_baking_choice(selected_base, selected_filling)
            with st.spinner("Baking..."):
                time.sleep(0.5)
            st.session_state.phase = "DECORATE"
            st.rerun()

    # VISUALS (Reads from Permanent Memory)
    with vis_col:
        st.markdown(render_cake_svg(
            st.session_state.final_cake["base"],
            st.session_state.final_cake["filling"],
            None, 
            []
        ), unsafe_allow_html=True)

# PHASE 3: DECORATING
elif st.session_state.phase == "DECORATE":
    st.title("Decorating Station")
    
    vis_col, ctrl_col = st.columns([1, 1])
    
    with ctrl_col:
        st.subheader("Apply Toppings")
        st.info(f"Order: \"{current_order['quote']}\"")
        
        # Frosting
        selected_frosting = st.radio(
            "Select Frosting", 
            list(GAME_DATA["frostings"].keys()),
            index=list(GAME_DATA["frostings"].keys()).index(st.session_state.final_cake["frosting"])
        )
        
        # Decorations (up to 3 toppings)
        selected_decos = st.multiselect(
            "Add Toppings (Max 3)", 
            list(GAME_DATA["decorations"].keys()),
            default=st.session_state.final_cake["decorations"],
            max_selections=3,
            key=f"toppings_{st.session_state.level_idx}"
        )

        # Update memory for preview
        st.session_state.final_cake["frosting"] = selected_frosting
        st.session_state.final_cake["decorations"] = selected_decos
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Serve Order! 🛎️"):
            save_decor_choice(selected_frosting, selected_decos)
            st.session_state.phase = "RESULT"
            st.rerun()

    with vis_col:
        # Renders using the permanent memory variables
        st.markdown(render_cake_svg(
            st.session_state.final_cake["base"],
            st.session_state.final_cake["filling"],
            st.session_state.final_cake["frosting"],
            st.session_state.final_cake["decorations"]
        ), unsafe_allow_html=True)

# PHASE 4: RESULT
elif st.session_state.phase == "RESULT":
    st.title("The Verdict")
    
    # Calculate Score using Permanent Memory
    cake = st.session_state.final_cake
    score = 0
    feedback = []
    
    # 1. Flavor Check
    b_tags = GAME_DATA["bases"][cake["base"]]["tags"]
    f_tags = GAME_DATA["fillings"][cake["filling"]]["tags"]
    if any(t in current_order["req_flavor"] for t in b_tags + f_tags):
        score += 1; feedback.append("✅ Flavor: Tasted like the memory.")
    else:
        feedback.append("❌ Flavor: The taste didn't match.")

    # 2. Color Check
    p_color = GAME_DATA["frostings"][cake["frosting"]]["color"]
    if p_color == current_order["req_color"]:
        score += 1; feedback.append("✅ Visuals: Perfect color match.")
    else:
        feedback.append("❌ Visuals: The color felt wrong.")

    # 3. Vibe Check
    vibe_matches = 0
    for d in cake["decorations"]:
        if GAME_DATA["decorations"][d]["vibe"] == current_order["req_vibe"]:
            vibe_matches += 1
    if vibe_matches >= 1:
        score += 1; feedback.append("✅ Vibe: You captured the feeling.")
    else:
        feedback.append("❌ Vibe: The decorations clashed.")

    # Render Final Result
    st.markdown(render_cake_svg(
        cake["base"], cake["filling"],
        cake["frosting"], cake["decorations"]
    ), unsafe_allow_html=True)

    if score == 3:
        st.success(f"Perfect Score! 3/3 Stars!")
        st.balloons()
    elif score > 0:
        st.warning(f"Decent Job! {score}/3 Stars.")
    else:
        st.error("Oh no! 0/3 Stars.")
        
    for f in feedback: st.write(f)
    
    if st.button("Next Customer"):
        st.session_state.score += score
        next_level()
        st.rerun()