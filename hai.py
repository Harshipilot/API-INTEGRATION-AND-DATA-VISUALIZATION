""" Streamlit app: "Friendship Surprise" How to run:

1. pip install streamlit


2. streamlit run app.py



This single-file app embeds an interactive HTML/JS experience that reacts to clicks/touches and reveals heartfelt messages about friendship, love, closeness and achievements. Customize the MESSAGES list to change the texts. """

import streamlit as st 
import random from textwrap
 import dedent

st.set_page_config(page_title="Friendship Surprise", page_icon="💖", layout="wide")

--- Configuration: edit these messages to personalize ---

MESSAGES = [ {"title": "You & Me", "text": "From silly inside jokes to late-night study sessions — you make every moment brighter.", "tag": "closeness"}, {"title": "My Biggest Fan", "text": "You cheered for my tiny wins and my big leaps. Your belief in me changed everything.", "tag": "achievement"}, {"title": "Secret Keeper", "text": "Thank you for listening, for holding my secrets, and for never judging — only supporting.", "tag": "trust"}, {"title": "Giggle Partner", "text": "Our random laughter is proof that the best therapy is just being together.", "tag": "joy"}, {"title": "Brave Together", "text": "We celebrate the wins and face the fears — together. Here's to more adventures ahead.", "tag": "future"}, {"title": "You Are Loved", "text": "If I had to sum it up: you are loved deeply, admired truly, and forever appreciated.", "tag": "love"} ]

--- Sidebar controls ---

with st.sidebar: st.header("Customize") name = st.text_input("Name to display", "Friend") accent = st.color_picker("Accent color", "#ff4da6") show_confetti = st.checkbox("Enable confetti on reveal", value=True) play_sound = st.checkbox("Play chime on reveal (browser)", value=False)

Build HTML/JS content

html_content = dedent(f""" <!doctype html>

<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root{{--accent:{accent};}}
    html,body{{height:100%;margin:0;font-family:Inter, Roboto, -apple-system, 'Segoe UI', 'Helvetica Neue', Arial;}}
    .wrap{{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;gap:18px;}}
    .card{{width:100%;max-width:900px;background:linear-gradient(135deg, rgba(255,255,255,0.85), rgba(255,255,255,0.7));backdrop-filter: blur(6px);border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,0.12);padding:26px;}}
    .title{{font-size:28px;font-weight:700;color:var(--accent);display:flex;gap:12px;align-items:center}}
    .subtitle{{color:#333;margin-top:6px}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:18px}}
    .tile{{background:linear-gradient(180deg, #fff, #fff);border-radius:12px;padding:16px;cursor:pointer;transition:transform .18s ease, box-shadow .18s ease;box-shadow:0 6px 18px rgba(13,13,13,0.06);min-height:120px;display:flex;flex-direction:column;justify-content:space-between}}
    .tile:hover{{transform:translateY(-6px);box-shadow:0 14px 34px rgba(13,13,13,0.12)}}
    .tile .head{{font-weight:700;font-size:16px;color:#111}}
    .tile .emoji{{font-size:28px}}
    .reveal{{margin-top:18px;min-height:86px;border-radius:12px;padding:18px;background:linear-gradient(90deg, rgba(255,255,255,0.9), rgba(255,255,255,0.85));box-shadow:inset 0 1px 0 rgba(255,255,255,0.4);}}
    .msg-title{{font-size:20px;font-weight:700;color:var(--accent)}}
    .msg-body{{margin-top:8px;color:#222;line-height:1.5;font-size:15px}}
    .heart{{width:56px;height:56px;border-radius:14px;display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--accent),#ff7ab5);box-shadow:0 8px 24px rgba(255,77,166,0.18);color:white;font-weight:700}}
    .foot{{display:flex;justify-content:space-between;align-items:center;margin-top:18px;gap:12px}}
    .btn{{padding:10px 14px;border-radius:10px;border:none;cursor:pointer;background:var(--accent);color:white;font-weight:600}}
    /* small responsive tweaks */
    @media (max-width:520px){{.title{{font-size:20px}}}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;">
        <div>
          <div class="title">💖 Surprise for {name}</div>
          <div class="subtitle">Tap any tile, or touch the heart to reveal something special about your friendship.</div>
        </div>
        <div style="display:flex;gap:12px;align-items:center">
          <div class="heart" id="bigHeart">💗</div>
        </div>
      </div><div class="grid" id="grid"></div>

  <div class="reveal" id="reveal">
    <div class="msg-title">Touch a tile to begin...</div>
    <div class="msg-body">Each message celebrates love, closeness, and the things you've achieved together.</div>
  </div>

  <div class="foot">
    <div style="font-size:14px;color:#666">Made with ♥ for a special friendship.</div>
    <div style="display:flex;gap:8px">
      <button class="btn" id="randomBtn">Surprise me</button>
      <button class="btn" id="resetBtn" style="background:#888">Reset</button>
    </div>
  </div>
</div>

  </div><canvas id="confettiCanvas" style="position:fixed;left:0;top:0;pointer-events:none;width:100%;height:100%;z-index:9999;display:none"></canvas>

<audio id="chime" src="data:audio/wav;base64,//uQZAAAAAAAAAAAAAAAAAAAAAA..." preload="auto"></audio>

  <script>
    // Messages passed from Python
    const MESSAGES = {MESSAGES};
    const grid = document.getElementById('grid');
    const reveal = document.getElementById('reveal');
    const bigHeart = document.getElementById('bigHeart');
    const randomBtn = document.getElementById('randomBtn');
    const resetBtn = document.getElementById('resetBtn');
    const confettiCanvas = document.getElementById('confettiCanvas');
    const chime = document.getElementById('chime');

    // Helper to create tiles
    function buildTiles(){
      grid.innerHTML = '';
      MESSAGES.forEach((m, idx) => {
        const tile = document.createElement('div');
        tile.className = 'tile';
        tile.dataset.idx = idx;
        tile.innerHTML = `<div style=\"display:flex;justify-content:space-between;align-items:flex-start;gap:10px\"><div><div class=\"head\">${m.title}</div><div style=\"color:#666;margin-top:6px;font-size:13px\">${m.tag}</div></div><div class=\"emoji\">${randomEmoji()}</div></div><div style=\"font-size:13px;color:#444;margin-top:10px\">Tap to reveal</div>`;
        tile.addEventListener('click', () => revealMessage(idx));
        grid.appendChild(tile);
      });
    }

    function randomEmoji(){
      const arr = ['🌟','✨','🎉','💫','🌈','🔥','💖','😊'];
      return arr[Math.floor(Math.random()*arr.length)];
    }

    function revealMessage(idx){
      const m = MESSAGES[idx];
      reveal.innerHTML = `<div class=\"msg-title\">${m.title}</div><div class=\"msg-body\">${m.text}</div>`;
      triggerCelebrate();
    }

    function triggerCelebrate(){
      // Play chime if allowed by Python flag
      if ({"true" if play_sound else "false"} === "true"){
        try{ chime.play(); }catch(e){}
      }
      if ({"true" if show_confetti else "false"} === "true") fireConfetti();
    }

    randomBtn.addEventListener('click', ()=>{
      const i = Math.floor(Math.random()*MESSAGES.length);
      revealMessage(i);
    });
    resetBtn.addEventListener('click', ()=>{
      reveal.innerHTML = `<div class=\"msg-title\">Touch a tile to begin...</div><div class=\"msg-body\">Each message celebrates love, closeness, and the things you've achieved together.</div>`;
    });
    bigHeart.addEventListener('click', ()=>{
      const i = Math.floor(Math.random()*MESSAGES.length);
      revealMessage(i);
      // heart pop animation
      bigHeart.animate([{transform:'scale(1)'},{transform:'scale(1.25)'},{transform:'scale(1)'}],{duration:420,easing:'ease-out'});
    });

    // --- simple confetti ---
    function fireConfetti(){
      confettiCanvas.style.display='block';
      const ctx = confettiCanvas.getContext('2d');
      confettiCanvas.width = window.innerWidth;
      confettiCanvas.height = window.innerHeight;
      const particles = [];
      const count = 80;
      for(let i=0;i<count;i++){
        particles.push({x:Math.random()*confettiCanvas.width, y:Math.random()*-confettiCanvas.height, r: 6+Math.random()*8, s:Math.random()*3+2, vx:(Math.random()-0.5)*6, vy:Math.random()*6+2, c:`hsl(${Math.random()*60+320},80%,60%)`});
      }
      let t=0;
      function step(){
        t+=1;
        ctx.clearRect(0,0,confettiCanvas.width,confettiCanvas.height);
        particles.forEach(p=>{
          p.x += p.vx;
          p.y += p.vy + Math.sin((t + p.x)/50)*0.5;
          p.vy *= 0.995;
          ctx.beginPath();
          ctx.fillStyle = p.c;
          ctx.fillRect(p.x, p.y, p.r, p.r*0.6);
        });
        if(t<240) requestAnimationFrame(step); else { confettiCanvas.style.display='none'; ctx.clearRect(0,0,confettiCanvas.width,confettiCanvas.height); }
      }
      step();
    }

    // instantiate tiles
    buildTiles();

    // allow keyboard shortcuts - press space/random
    document.addEventListener('keydown',(e)=>{ if(e.key === ' '){ e.preventDefault(); randomBtn.click(); } });
  </script></body>
</html>
""".replace('{MESSAGES}', str(MESSAGES).replace("'", "\'") ))Use st.components.v1.html to render

st.markdown("""

<style>
.css-1v3fvcr {padding:0}
</style>""", unsafe_allow_html=True)

st.components.v1.html(html_content, height=720, scrolling=True)

st.markdown("---") col1, col2 = st.columns([1,3]) with col1: st.image("https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=60", caption="Moments together", use_column_width=True) with col2: st.header("How to personalize") st.write("- Edit the MESSAGES list at the top of this file: change title, text, or tag.") st.write("- Use the sidebar to change the displayed name and accent color.") st.write("- Want to play a sound on reveal? Toggle 'Play chime' in the sidebar (browser may ask permission).")

st.success("Open the app in your browser and tap tiles or the heart to reveal your messages. Want a downloadable version or more personalization? Tell me what to change — fonts, colors, or special messages.")

