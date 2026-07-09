<!DOCTYPE html>
<html>
<head>
<style>
  html, body {
    margin:0; padding:0; background: transparent;
    width:1080px; height:1920px; overflow:hidden;
    font-family: 'Segoe UI', Arial, sans-serif;
  }
  .stage { position:relative; width:1080px; height:1920px; }

  .heading {
    position:absolute; top:60px; left:50%; transform:translateX(-50%) scale(0.8); opacity:0;
    font-size:38px; font-weight:800; color:#fff;
    background: linear-gradient(135deg, #1e1e3f, #3d1e6d);
    padding:16px 32px; border-radius:14px;
    transition: transform 1.2s cubic-bezier(.22,.68,0,1.01), opacity 1.2s ease;
  }
  .heading.show { transform:translateX(-50%) scale(1); opacity:1; }

  .timeline { position:absolute; top:220px; left:50%; transform:translateX(-50%); width:900px; height:100px; }
  .track { position:absolute; top:38px; left:0; width:900px; height:6px; background:rgba(255,255,255,0.25); border-radius:3px; }
  .fill { position:absolute; top:38px; left:0; width:0%; height:6px; background:linear-gradient(90deg,#ffd60a,#ff8a00); border-radius:3px; transition: width linear; }

  .dot { position:absolute; top:0; width:60px; text-align:center; transform:translateX(-30px); }
  .dot-circle {
    width:36px; height:36px; border-radius:50%; background:#444;
    display:block; margin:0 auto; transition: all 0.5s ease;
  }
  .dot.active .dot-circle {
    background: linear-gradient(135deg,#ffd60a,#ff8a00);
    transform:scale(1.3);
    box-shadow:0 0 20px rgba(255,138,0,0.6);
  }
  .dot-label { display:block; margin-top:10px; font-size:20px; color:#ccc; transition: color 0.5s ease; }
  .dot.active .dot-label { color:#ffd60a; font-weight:700; }

  .counter {
    position:absolute; top:360px; left:50%; transform:translateX(-50%) translateY(20px); opacity:0;
    font-size:32px; color:#fff; font-weight:700;
    background:rgba(20,20,20,0.6); padding:14px 28px; border-radius:12px;
    transition: opacity 0.8s ease, transform 0.8s ease;
  }
  .counter.show { opacity:1; transform:translateX(-50%) translateY(0); }

  .deadlineBadge {
    position:absolute; top:460px; left:50%;
    transform:translateX(-50%) scale(0); opacity:0;
    background: #d90000;
    color:white; padding:20px 40px; border-radius:16px;
    font-size:40px; font-weight:800;
    transition: transform 0.9s cubic-bezier(.17,.89,.32,1.49), opacity 0.5s ease;
  }
  .deadlineBadge.show {
    opacity:1; transform:translateX(-50%) scale(1);
    animation: pulse 1.6s ease-in-out 0.9s infinite;
  }
  @keyframes pulse {
    0%,100%{ box-shadow:0 0 0 0 rgba(217,0,0,0.6); }
    50%{ box-shadow:0 0 0 24px rgba(217,0,0,0); }
  }

  .penalty {
    position:absolute; top:640px; left:50%;
    transform:translateX(-50%) translateY(20px); opacity:0; text-align:center;
    font-size:30px; font-weight:700;
    background: linear-gradient(90deg, #ffd60a, #ff8a00);
    -webkit-background-clip:text; background-clip:text; color:transparent;
    transition: opacity 1s ease, transform 1s ease;
  }
  .penalty.show { opacity:1; transform:translateX(-50%) translateY(0); }
</style>
</head>
<body>
  <div class="stage">
    <div class="heading" id="heading">CIT FILING COUNTDOWN</div>

    <div class="timeline">
      <div class="track"></div>
      <div class="fill" id="fill"></div>
      <div class="dot" data-i="0" style="left:0px"><span class="dot-circle"></span><span class="dot-label">Year End</span></div>
      <div class="dot" data-i="1" style="left:150px"><span class="dot-circle"></span><span class="dot-label">Jan</span></div>
      <div class="dot" data-i="2" style="left:300px"><span class="dot-circle"></span><span class="dot-label">Feb</span></div>
      <div class="dot" data-i="3" style="left:450px"><span class="dot-circle"></span><span class="dot-label">Mar</span></div>
      <div class="dot" data-i="4" style="left:600px"><span class="dot-circle"></span><span class="dot-label">Apr</span></div>
      <div class="dot" data-i="5" style="left:750px"><span class="dot-circle"></span><span class="dot-label">May</span></div>
      <div class="dot" data-i="6" style="left:900px"><span class="dot-circle"></span><span class="dot-label">Jun</span></div>
    </div>

    <div class="counter" id="counter">0 of 6 months used</div>
    <div class="deadlineBadge" id="deadlineBadge">⚠ DEADLINE REACHED</div>
    <div class="penalty" id="penalty">Penalties: 100,000s of Naira</div>
  </div>

<script>
  // ---- TOTAL_DURATION_MS controls the pacing of the whole sequence. ----
  // Set this to match how long the spoken passage actually takes, in milliseconds.
  // Everything below scales itself to fit inside this window automatically.
  const TOTAL_DURATION_MS = 16000;   // placeholder - we'll set this from your real timestamps

  const heading = document.getElementById('heading');
  const dots = document.querySelectorAll('.dot');
  const fill = document.getElementById('fill');
  const counter = document.getElementById('counter');
  const deadlineBadge = document.getElementById('deadlineBadge');
  const penalty = document.getElementById('penalty');

  // Reserve time at the end so the finished state holds still and is readable,
  // instead of finishing right as the video cuts away.
  const holdTime = 3000;
  const activeWindow = TOTAL_DURATION_MS - holdTime;

  const headingShowAt = 200;
  const timelineStartAt = 1200;
  const stepTime = (activeWindow - timelineStartAt - 1800) / 6; // spread 6 months across remaining time
  const deadlineAt = timelineStartAt + 6 * stepTime + 400;
  const penaltyAt = deadlineAt + 900;

  fill.style.transitionDuration = (stepTime * 6) + 'ms';

  setTimeout(() => { heading.classList.add('show'); }, headingShowAt);
  setTimeout(() => { fill.style.width = '100%'; }, timelineStartAt);

  dots.forEach((dot, i) => {
    setTimeout(() => {
      dot.classList.add('active');
      counter.classList.add('show');
      if (i > 0) counter.textContent = i + ' of 6 months used';
    }, timelineStartAt + i * stepTime);
  });

  setTimeout(() => { deadlineBadge.classList.add('show'); }, deadlineAt);
  setTimeout(() => { penalty.classList.add('show'); }, penaltyAt);
</script>
</body>
</html>