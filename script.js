/* script.js — Improved neon visuals + full functionality
   - BFS, DFS, Dijkstra, Bipartite check, SCC
   - Adjacency list / matrix / edge list
   - Add vertex, drag, add-edge mode, pan, zoom
   - Enhanced neon pink/aqua gradients & glow effects
*/

(() => {
  // DOM refs
  const canvas = document.getElementById('graphCanvas');
  const logArea = document.getElementById('logArea');
  const btnAddEdgeMode = document.getElementById('btnModeAddEdge');
  const btnLoadExample = document.getElementById('btnLoadExample');
  const btnDijkstra = document.getElementById('btnDijkstra');
  const btnBFS = document.getElementById('btnBFS');
  const btnDFS = document.getElementById('btnDFS');
  const btnBipartite = document.getElementById('btnBipartite');
  const btnSCC = document.getElementById('btnSCC');
  const btnAdjMat = document.getElementById('btnAdjMatrix');
  const btnAdjList = document.getElementById('btnAdjList');
  const btnEdgeList = document.getElementById('btnEdgeList');
  const btnClearLog = document.getElementById('btnClearLog');
  const btnExport = document.getElementById('btnExport');
  const infoVertices = document.getElementById('infoVertices');
  const infoEdges = document.getElementById('infoEdges');
  const infoMode = document.getElementById('infoMode');
  
  // THÊM DÒNG NÀY - DOM ref cho nút toggle đồ thị
  const btnToggleDirected = document.getElementById('btnToggleDirected');

  // Canvas setup
  let dpr = window.devicePixelRatio || 1;
  const ctx = canvas.getContext('2d');

  function fitCanvas(){
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.floor(rect.width * dpr);
    canvas.height = Math.floor(rect.height * dpr);
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }

  // Camera
  let scale = 1.0;
  let panX = 0;
  let panY = 0;

  // Graph
  const graph = {
    vertices: [],  // {id,x,y,label,sccColor}
    edges: [],     // {from,to,weight,directed,isPath,sccColor,hover}
    isDirected: false
  };
  let nextId = 1;

  // State
  let draggingVertex = null;
  let draggingOffset = {x:0,y:0};
  let isPanning = false;
  let lastPan = {x:0,y:0};
  let hoveredVertex = null;

  let addEdgeMode = false;
  let edgeFromSelection = null;

  const V_RADIUS = 20;
  const neonPink = "#ff4ecb";
  const neonAqua = "#2ee7d6";
  const vertexFill = "#071217";
  
  // Animation
  let pulseTime = 0;
  const pulseSpeed = 0.05;

  // Helpers
  function toWorld(x,y){ return {x:(x-panX)/scale, y:(y-panY)/scale}; }
  function toScreen(x,y){ return {x:x*scale+panX, y:y*scale+panY}; }

  function log(txt){
    const t = new Date().toLocaleTimeString();
    logArea.textContent += `[${t}] ${txt}\n`;
    logArea.scrollTop = logArea.scrollHeight;
  }
  
  btnClearLog.addEventListener("click",()=> logArea.textContent="");

  function addVertexAt(x,y){
    const id = nextId++;
    graph.vertices.push({id,x,y,label:String(id)});
    updateInfo(); 
    draw();
    return id;
  }

  function findVertexAtWorld(x,y){
    for (let i=graph.vertices.length-1;i>=0;i--){
      const v = graph.vertices[i];
      const dx=v.x-x, dy=v.y-y;
      if (Math.hypot(dx,dy)<=V_RADIUS+2) return v;
    }
    return null;
  }

  function addEdge(a,b,weight=1){
    if (a===b) return;
    if (graph.edges.find(e=>e.from===a&&e.to===b&&e.weight===weight)) return;
    graph.edges.push({from:a,to:b,weight,directed:graph.isDirected,isPath:false});
    updateInfo(); 
    draw();
  }

  function updateInfo(){
    infoVertices.textContent = graph.vertices.length;
    infoEdges.textContent = graph.edges.length;
    infoMode.textContent = addEdgeMode? "AddEdge":"Normal";
  }

  // Drawing with enhanced glow effects
  function clearCanvas(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = "#071018";
    ctx.fillRect(0,0,canvas.width,canvas.height);
  }

  // Helper function to lighten colors
  function lightenColor(color, percent) {
    if (color.startsWith("#")) {
      let r = parseInt(color.slice(1, 3), 16);
      let g = parseInt(color.slice(3, 5), 16);
      let b = parseInt(color.slice(5, 7), 16);
      
      r = Math.min(255, r + percent);
      g = Math.min(255, g + percent);
      b = Math.min(255, b + percent);
      
      return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    }
    return color;
  }

  function drawArrowWithGlow(x1, y1, x2, y2, edge) {
    const t = 0.82;
    const sx = x1 + (x2 - x1) * t;
    const sy = y1 + (y2 - y1) * t;
    const ang = Math.atan2(y2 - y1, x2 - x1);
    const size = 10 / scale;
    
    // Draw arrow glow
    if (edge.isPath || edge.sccColor) {
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(sx, sy);
      ctx.lineTo(
        sx - size * Math.cos(ang - Math.PI/6),
        sy - size * Math.sin(ang - Math.PI/6)
      );
      ctx.lineTo(
        sx - size * Math.cos(ang + Math.PI/6),
        sy - size * Math.sin(ang + Math.PI/6)
      );
      ctx.closePath();
      ctx.fillStyle = edge.sccColor || neonAqua;
      ctx.shadowColor = edge.sccColor || neonAqua;
      ctx.shadowBlur = 15;
      ctx.fill();
      ctx.restore();
    }
    
    // Main arrow
    ctx.beginPath();
    ctx.moveTo(sx, sy);
    ctx.lineTo(
      sx - size * Math.cos(ang - Math.PI/6),
      sy - size * Math.sin(ang - Math.PI/6)
    );
    ctx.lineTo(
      sx - size * Math.cos(ang + Math.PI/6),
      sy - size * Math.sin(ang + Math.PI/6)
    );
    ctx.closePath();
    ctx.fillStyle = edge.sccColor ? 
      lightenColor(edge.sccColor, 20) : 
      (edge.isPath ? neonAqua : "rgba(0,0,0,0.7)");
    ctx.fill();
  }

  function draw(){
    clearCanvas();
    ctx.save();
    ctx.translate(panX, panY);
    ctx.scale(scale, scale);

    // Calculate pulse factor for animated glow
    const pulseFactor = 0.8 + 0.2 * Math.sin(pulseTime);

    // ==================== DRAW EDGES WITH GLOW ====================
    graph.edges.forEach(e => {
      const a = graph.vertices.find(v => v.id === e.from);
      const b = graph.vertices.find(v => v.id === e.to);
      if(!a || !b) return;

      // Enhanced glow settings
      let glowIntensity = 0;
      let glowColor = "";
      let lineWidth = 3.2 / scale;
      let mainColor = "";
      let isHighlighted = false;
      
      if (e.sccColor) {
        // SCC edges - strongest glow
        glowIntensity = 35 * pulseFactor;
        glowColor = e.sccColor + "CC";
        lineWidth = 6 / scale;
        mainColor = e.sccColor;
        isHighlighted = true;
      } else if (e.isPath) {
        // Algorithm path edges - strong pulsing glow
        glowIntensity = 25 * pulseFactor;
        glowColor = "rgba(255, 78, 203, 0.8)";
        lineWidth = 5 / scale;
        mainColor = neonPink;
        isHighlighted = true;
      } else if (e.hover) {
        // Hovered edges - medium glow
        glowIntensity = 15;
        glowColor = "rgba(46, 231, 214, 0.6)";
        lineWidth = 4 / scale;
        mainColor = neonAqua;
      } else {
        // Normal edges - subtle glow
        glowIntensity = 8;
        glowColor = "rgba(255, 78, 203, 0.25)";
        lineWidth = 3.2 / scale;
        mainColor = "rgba(255, 78, 203, 0.6)";
      }

      // Draw outer glow layer
      if (glowIntensity > 0) {
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        
        // Create glowing gradient
        const glowGradient = ctx.createLinearGradient(a.x, a.y, b.x, b.y);
        if (e.sccColor) {
          // Multi-color gradient for SCC
          glowGradient.addColorStop(0, e.sccColor + "99");
          glowGradient.addColorStop(0.5, "#ffffff");
          glowGradient.addColorStop(1, e.sccColor + "99");
        } else if (e.isPath) {
          // Neon pink to aqua gradient
          glowGradient.addColorStop(0, "rgba(255, 78, 203, 0.9)");
          glowGradient.addColorStop(0.5, "rgba(255, 255, 255, 1)");
          glowGradient.addColorStop(1, "rgba(46, 231, 214, 0.9)");
        } else {
          // Single color gradient
          glowGradient.addColorStop(0, glowColor);
          glowGradient.addColorStop(1, glowColor);
        }
        
        ctx.strokeStyle = glowGradient;
        ctx.lineWidth = lineWidth + glowIntensity / scale;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        
        // Apply shadow for glow effect
        ctx.shadowColor = e.sccColor || neonPink;
        ctx.shadowBlur = glowIntensity;
        ctx.globalAlpha = 0.8;
        ctx.stroke();
        ctx.restore();
      }

      // Draw main edge line
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      
      // Create main gradient
      const mainGradient = ctx.createLinearGradient(a.x, a.y, b.x, b.y);
      if (e.sccColor) {
        mainGradient.addColorStop(0, e.sccColor);
        mainGradient.addColorStop(0.5, lightenColor(e.sccColor, 50));
        mainGradient.addColorStop(1, e.sccColor);
      } else if (e.isPath) {
        mainGradient.addColorStop(0, neonPink);
        mainGradient.addColorStop(0.5, "#ffffff");
        mainGradient.addColorStop(1, neonAqua);
      } else {
        mainGradient.addColorStop(0, "rgba(255, 78, 203, 0.9)");
        mainGradient.addColorStop(1, "rgba(46, 231, 214, 0.9)");
      }
      
      ctx.strokeStyle = mainGradient;
      ctx.lineWidth = lineWidth;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      // Add subtle shadow to main line
      if (isHighlighted) {
        ctx.shadowColor = e.sccColor || neonPink;
        ctx.shadowBlur = 10;
      }
      
      ctx.stroke();
      ctx.restore();

      // Draw arrow if directed
      if(graph.isDirected || e.directed){
        drawArrowWithGlow(a.x, a.y, b.x, b.y, e);
      }

      // Draw weight with glow background
      const mx = (a.x + b.x) / 2;
      const my = (a.y + b.y) / 2;
      
      // Background for weight text
      ctx.save();
      ctx.fillStyle = "rgba(8, 10, 12, 0.95)";
      if (isHighlighted) {
        ctx.shadowColor = e.sccColor || neonAqua;
        ctx.shadowBlur = 8;
      }
      const textPadding = 6;
      const textWidth = ctx.measureText(String(e.weight)).width;
      ctx.fillRect(
        mx - textWidth/2 - textPadding, 
        my - 9, 
        textWidth + textPadding*2, 
        18
      );
      ctx.restore();
      
      // Weight text
      ctx.fillStyle = e.sccColor ? "#ffffff" : (e.isPath ? "#ffffff" : "#e6eef6");
      ctx.font = `${12/scale}px "Space Grotesk"`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(String(e.weight), mx, my);
    });

    // ==================== DRAW VERTICES WITH GLOW ====================
    graph.vertices.forEach(v => {
      const x = v.x;
      const y = v.y;

      // Background glow for vertices
      if (v.sccColor || hoveredVertex?.id === v.id) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(x, y, V_RADIUS + 18, 0, Math.PI * 2);
        const glowColor = v.sccColor || neonPink;
        const gradient = ctx.createRadialGradient(
          x, y, V_RADIUS, 
          x, y, V_RADIUS + 18
        );
        gradient.addColorStop(0, glowColor + "88");
        gradient.addColorStop(1, glowColor + "00");
        ctx.fillStyle = gradient;
        ctx.globalAlpha = 0.7;
        ctx.fill();
        ctx.restore();
      }

      // Outer glow ring
      ctx.beginPath();
      ctx.arc(x, y, V_RADIUS + 8, 0, Math.PI * 2);
      const outerGradient = ctx.createRadialGradient(
        x - 6, y - 6, 4,
        x, y, V_RADIUS + 8
      );
      outerGradient.addColorStop(0, "rgba(255,78,203,0.2)");
      outerGradient.addColorStop(1, "rgba(255,78,203,0.02)");
      ctx.fillStyle = outerGradient;
      ctx.fill();

      // Main vertex gradient
      const g = ctx.createRadialGradient(x - 4, y - 4, 4, x, y, V_RADIUS);
      g.addColorStop(0, v.sccColor || neonPink);
      g.addColorStop(0.45, v.sccColor || neonAqua);
      g.addColorStop(1, vertexFill);

      // Draw main vertex with glow
      ctx.beginPath();
      ctx.arc(x, y, V_RADIUS, 0, Math.PI * 2);
      ctx.save();
      
      // Enhanced glow for vertices
      if (v.sccColor) {
        ctx.shadowColor = v.sccColor;
        ctx.shadowBlur = 30 * pulseFactor;
      } else {
        ctx.shadowColor = "rgba(255,78,203,0.4)";
        ctx.shadowBlur = 22;
      }
      
      ctx.fillStyle = g;
      ctx.fill();
      ctx.restore();

      // Vertex border
      ctx.lineWidth = 2 / scale;
      ctx.strokeStyle = v.sccColor ? 
        lightenColor(v.sccColor, 40) + "EE" : 
        "rgba(255,255,255,0.1)";
      ctx.stroke();

      // Vertex label
      ctx.fillStyle = vertexFill;
      ctx.font = `${14/scale}px "Space Grotesk"`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(v.label, x, y);

      // Hover effect with enhanced glow
      if (hoveredVertex && hoveredVertex.id === v.id) {
        ctx.beginPath();
        ctx.arc(x, y, V_RADIUS + 10, 0, Math.PI * 2);
        ctx.lineWidth = 3 / scale;
        ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
        ctx.shadowColor = neonPink;
        ctx.shadowBlur = 25;
        ctx.stroke();
      }
    });

    ctx.restore();
  }

  // Animation loop for pulsing effects
  function animate() {
    pulseTime += pulseSpeed;
    draw();
    requestAnimationFrame(animate);
  }

  // Start animation
  animate();

  // Original drawArrow function (kept for compatibility)
  function drawArrow(x1,y1,x2,y2,highlight){
    const t=0.82;
    const sx=x1+(x2-x1)*t, sy=y1+(y2-y1)*t;
    const ang=Math.atan2(y2-y1,x2-x1);
    const size=highlight?10/scale:7/scale;

    ctx.beginPath();
    ctx.fillStyle=highlight?neonAqua:"rgba(0,0,0,0.6)";
    ctx.moveTo(sx,sy);
    ctx.lineTo(
      sx-size*Math.cos(ang-Math.PI/6),
      sy-size*Math.sin(ang-Math.PI/6)
    );
    ctx.lineTo(
      sx-size*Math.cos(ang+Math.PI/6),
      sy-size*Math.sin(ang+Math.PI/6)
    );
    ctx.closePath();
    ctx.fill();
  }

  // Interaction
  let isMouseDown=false;

  function resizeCanvas(){
    const rect=canvas.getBoundingClientRect();
    if(rect.width===0){
      canvas.style.width="100%";
      canvas.style.height="100%";
    }
    fitCanvas();
    draw();
  }
  window.addEventListener("resize",resizeCanvas);

  function initSize(){
    const wrap=canvas.parentElement;
    if(wrap){
      canvas.style.width="100%";
      canvas.style.height="100%";
    } else {
      canvas.style.width="800px";
      canvas.style.height="480px";
    }
    fitCanvas();
  }
  initSize();

  function clientToWorld(ev){
    const r=canvas.getBoundingClientRect();
    return toWorld(ev.clientX-r.left, ev.clientY-r.top);
  }

  canvas.addEventListener("pointerdown",ev=>{
    ev.preventDefault();
    canvas.setPointerCapture(ev.pointerId);
    isMouseDown=true;

    const world=clientToWorld(ev);
    const v=findVertexAtWorld(world.x,world.y);

    if(ev.button===2){
      isPanning=true;
      lastPan={x:ev.clientX,y:ev.clientY};
      return;
    }

    if(v){
      draggingVertex=v;
      draggingOffset={x:world.x-v.x,y:world.y-v.y};

      if(addEdgeMode){
        if(!edgeFromSelection){
          edgeFromSelection=v;
          log(`Selected source vertex ${v.id}`);
          btnAddEdgeMode.classList.add("active");
          btnAddEdgeMode.textContent=`Add Edge Mode: SELECTING ${v.id}`;
        }
        else if(edgeFromSelection.id===v.id){
          edgeFromSelection=null;
          log(`Deselected.`);
          btnAddEdgeMode.textContent="Add Edge Mode: ON";
        }
        else {
          addEdge(edgeFromSelection.id,v.id,1);
          log(`Added edge: ${edgeFromSelection.id} → ${v.id}`);
          edgeFromSelection=null;
          btnAddEdgeMode.textContent="Add Edge Mode: ON";
        }
      }
    }
    else {
      if(!addEdgeMode){
        const id=addVertexAt(world.x,world.y);
        log("Vertex "+id+" added");
      }
    }

    draw();
  });

  canvas.addEventListener("pointermove",ev=>{
    const world=clientToWorld(ev);
    
    // Check vertex hover
    const v=findVertexAtWorld(world.x,world.y);
    if(v!==hoveredVertex){ 
      hoveredVertex=v; 
    }
    
    // Check edge hover
    let foundEdgeHover = false;
    graph.edges.forEach(e => {
      const a = graph.vertices.find(v => v.id === e.from);
      const b = graph.vertices.find(v => v.id === e.to);
      if (!a || !b) {
        e.hover = false;
        return;
      }
      
      // Skip if hovering a vertex
      if (hoveredVertex) {
        e.hover = false;
        return;
      }
      
      // Calculate distance from point to line segment
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const length = Math.hypot(dx, dy);
      
      if (length === 0) {
        e.hover = false;
        return;
      }
      
      const t = Math.max(0, Math.min(1, 
        ((world.x - a.x) * dx + (world.y - a.y) * dy) / (length * length)
      ));
      
      const projX = a.x + t * dx;
      const projY = a.y + t * dy;
      const dist = Math.hypot(world.x - projX, world.y - projY);
      
      // Hover threshold (increased for better UX)
      const hoverThreshold = 14 / scale;
      e.hover = dist < hoverThreshold;
      
      if (e.hover) foundEdgeHover = true;
    });

    if(isPanning){
      const dx=ev.clientX-lastPan.x;
      const dy=ev.clientY-lastPan.y;
      panX+=dx; panY+=dy;
      lastPan={x:ev.clientX,y:ev.clientY};
      draw();
      return;
    }

    if(draggingVertex){
      draggingVertex.x = world.x - draggingOffset.x;
      draggingVertex.y = world.y - draggingOffset.y;
      draw();
    } else if (hoveredVertex || foundEdgeHover) {
      // Redraw for hover effects
      draw();
    }
  });

  canvas.addEventListener("pointerup",ev=>{
    isMouseDown=false;
    draggingVertex=null;
    isPanning=false;
    canvas.releasePointerCapture(ev.pointerId);
  });

  canvas.addEventListener("contextmenu",ev=>ev.preventDefault());

  canvas.addEventListener("wheel",ev=>{
    ev.preventDefault();
    const delta=-ev.deltaY;
    const zoom=delta>0?1.08:0.92;

    const r=canvas.getBoundingClientRect();
    const mx=ev.clientX-r.left, my=ev.clientY-r.top;

    const before=toWorld(mx,my);
    scale*=zoom;
    scale=Math.min(Math.max(scale,0.35),3.5);
    const after=toWorld(mx,my);
    panX+=(after.x-before.x)*scale;
    panY+=(after.y-before.y)*scale;

    draw();
  },{passive:false});

  // Buttons
  btnAddEdgeMode.addEventListener("click",()=>{
    addEdgeMode=!addEdgeMode;
    if(!addEdgeMode){
      edgeFromSelection=null;
      btnAddEdgeMode.classList.remove("active");
      btnAddEdgeMode.textContent="Add Edge Mode: OFF";
    } else {
      btnAddEdgeMode.classList.add("active");
      btnAddEdgeMode.textContent="Add Edge Mode: ON";
    }
    updateInfo();
  });

  btnLoadExample.addEventListener("click",loadExample);
  
  // Example graph
  function loadExample(){
    graph.vertices.length=0;
    graph.edges.length=0;
    nextId=1;
    
    // THÊM DÒNG NÀY - Reset về đồ thị vô hướng khi load example
    graph.isDirected = false;
    if (btnToggleDirected) {
      btnToggleDirected.textContent = "Đồ thị: Vô hướng";
      btnToggleDirected.classList.remove("active");
    }

    const layout=[
      {x:120,y:120},
      {x:300,y:90},
      {x:480,y:120},
      {x:180,y:300},
      {x:360,y:300},
      {x:560,y:240}
    ];
    layout.forEach(p=>addVertexAt(p.x,p.y));
    addEdge(1,2,2);
    addEdge(1,4,1);
    addEdge(2,3,3);
    addEdge(2,5,2);
    addEdge(3,6,1);
    addEdge(4,5,4);
    addEdge(5,3,1);
    addEdge(5,6,5);
    addEdge(2,4,2);
    log("Example graph loaded");
    draw();
  }

  // Graph representation functions
  function getAdjList(){
    const adj={};
    graph.vertices.forEach(v=>adj[v.id]=[]);
    graph.edges.forEach(e=>{
      adj[e.from].push({to:e.to,w:e.weight});
      if(!graph.isDirected && !e.directed)
        adj[e.to].push({to:e.from,w:e.weight});
    });
    return adj;
  }

  function getAdjListText(){
    const adj=getAdjList();
    const keys=Object.keys(adj).map(Number).sort((a,b)=>a-b);
    let out="";
    keys.forEach(k=>{
      out+=`${k}: [${adj[k].map(o=>`${o.to}(${o.w})`).join(", ")}]\n`;
    });
    return out;
  }

  function getAdjMatrixText(){
    const ids=graph.vertices.map(v=>v.id);
    if(ids.length===0) return "Empty";
    const n=Math.max(...ids);
    const mat=Array.from({length:n+1},()=>Array(n+1).fill(0));

    graph.edges.forEach(e=>{
      mat[e.from][e.to]=e.weight;
      if(!graph.isDirected) mat[e.to][e.from]=e.weight;
    });

    let out="    ";
    for(let i=1;i<=n;i++) out+=i.toString().padStart(4);
    out+="\n";
    for(let i=1;i<=n;i++){
      out+=i.toString().padStart(3)+" ";
      for(let j=1;j<=n;j++) out+=String(mat[i][j]).padStart(4);
      out+="\n";
    }
    return out;
  }

  function getEdgeListText(){
    if(graph.edges.length===0) return "Empty";
    return graph.edges.map(e=>`${e.from} -> ${e.to} (w=${e.weight})`).join("\n");
  }

  // Algorithm implementations
  function runDijkstraUI(){
    if(!graph.vertices.length){ log("No vertices"); return; }
    graph.edges.forEach(e=>{
      e.isPath=false;
      delete e.sccColor;
    });
    graph.vertices.forEach(v=>delete v.sccColor);

    const ids=graph.vertices.map(v=>v.id).sort((a,b)=>a-b);
    const start=ids[0], target=ids[ids.length-1];

    const adj={};
    ids.forEach(id=>adj[id]=[]);
    graph.edges.forEach(e=>{
      adj[e.from].push({to:e.to,w:e.weight});
      if(!graph.isDirected)
        adj[e.to].push({to:e.from,w:e.weight});
    });

    const n=Math.max(...ids);
    const dist=Array(n+1).fill(Infinity);
    const prev=Array(n+1).fill(-1);
    const vis=Array(n+1).fill(false);

    dist[start]=0;

    for(let _=0;_<ids.length;_++){
      let u=-1,best=Infinity;
      ids.forEach(v=>{
        if(!vis[v] && dist[v]<best){best=dist[v]; u=v;}
      });
      if(u===-1) break;
      vis[u]=true;
      adj[u].forEach(nb=>{
        if(!vis[nb.to] && dist[u]+nb.w<dist[nb.to]){
          dist[nb.to]=dist[u]+nb.w;
          prev[nb.to]=u;
        }
      });
    }

    if(dist[target]===Infinity){
      log(`No path ${start}→${target}`);
    } else {
      const path=[];
      let cur=target;
      while(cur!==-1){ path.unshift(cur); cur=prev[cur]; }

      for(let i=0;i<path.length-1;i++){
        const a=path[i], b=path[i+1];
        const e=graph.edges.find(ed=>
          (ed.from===a&&ed.to===b) || (!graph.isDirected && ed.from===b&&ed.to===a)
        );
        if(e) e.isPath=true;
      }

      log(`Dijkstra ${start}→${target}: ${path.join(" → ")} (cost=${dist[target]})`);
    }
    draw();
  }

  function runBFSUI(){
    if(!graph.vertices.length){ log("No vertices"); return; }
    graph.edges.forEach(e=>{
      e.isPath=false;
      delete e.sccColor;
    });
    graph.vertices.forEach(v=>delete v.sccColor);

    const adj=getAdjList();
    const ids=graph.vertices.map(v=>v.id).sort((a,b)=>a-b);
    const start=ids[0];

    const vis={};
    const q=[start];
    vis[start]=true;

    const order=[];
    while(q.length){
      const u=q.shift();
      order.push(u);
      adj[u].forEach(nb=>{
        if(!vis[nb.to]){
          vis[nb.to]=true;
          q.push(nb.to);
        }
      });
    }

    for(let i=0;i<order.length-1;i++){
      const a=order[i], b=order[i+1];
      const e=graph.edges.find(ed=>
        (ed.from===a&&ed.to===b) || (!graph.isDirected && ed.from===b&&ed.to===a)
      );
      if(e) e.isPath=true;
    }

    log(`BFS order: ${order.join(" → ")}`);
    draw();
  }

  function runDFSUI(){
    if(!graph.vertices.length){ log("No vertices"); return; }
    graph.edges.forEach(e=>{
      e.isPath=false;
      delete e.sccColor;
    });
    graph.vertices.forEach(v=>delete v.sccColor);

    const adj=getAdjList();
    const ids=graph.vertices.map(v=>v.id).sort((a,b)=>a-b);
    const start=ids[0];

    const vis={};
    const stack=[start];
    const order=[];

    while(stack.length){
      const u=stack.pop();
      if(vis[u]) continue;
      vis[u]=true;
      order.push(u);

      adj[u]
        .slice()
        .sort((a,b)=>b.to-a.to)
        .forEach(nb=>{
          if(!vis[nb.to]) stack.push(nb.to);
        });
    }

    for(let i=0;i<order.length-1;i++){
      const a=order[i], b=order[i+1];
      const e=graph.edges.find(ed=>
        (ed.from===a&&ed.to===b) || (!graph.isDirected && ed.from===b&&ed.to===a)
      );
      if(e) e.isPath=true;
    }

    log(`DFS order: ${order.join(" → ")}`);
    draw();
  }

  function runBipartiteUI() {
    if (!graph.vertices.length) {
      log("No vertices");
      return;
    }
    
    graph.edges.forEach(e => {
      e.isPath = false;
      delete e.sccColor;
    });
    graph.vertices.forEach(v => delete v.sccColor);

    const adj = getAdjList();
    const ids = graph.vertices.map(v => v.id).sort((a, b) => a - b);
    const color = {};
    let isBip = true;

    const g0 = new Set();
    const g1 = new Set();

    for (const s of ids) {
      if (color[s] !== undefined) continue;
      
      color[s] = 0;
      g0.add(s);

      const q = [s];
      while (q.length && isBip) {
        const u = q.shift();
        
        if (!adj[u]) continue;
        
        adj[u].forEach(nb => {
          const v = nb.to;
          if (color[v] === undefined) {
            color[v] = 1 - color[u];
            if (color[v] === 0) {
              g0.add(v);
            } else {
              g1.add(v);
            }
            q.push(v);
          } else if (color[v] === color[u]) {
            isBip = false;
          }
        });
      }
      if (!isBip) break;
    }

    if (!isBip) {
      log("Không phải đồ thị 2 phía.");
      
      graph.edges.forEach(e => {
        if (color[e.from] === color[e.to]) {
          e.isPath = true;
        }
      });
      
    } else {
      log("Đồ thị 2 phía.");
      log("Nhóm 0: " + [...g0].join(", "));
      log("Nhóm 1: " + [...g1].join(", "));

      graph.edges.forEach(e => {
        if (color[e.from] !== color[e.to]) {
          e.isPath = true;
        }
      });
    }

    draw();
  }

  // SCC implementation (Kosaraju's algorithm)
  function runSCC() {
    if (!graph.vertices.length) {
      log("Không có đỉnh nào!");
      return;
    }

    graph.edges.forEach(e => {
      e.isPath = false;
      delete e.sccColor;
    });
    graph.vertices.forEach(v => delete v.sccColor);

    log("🔍 Đang tìm SCC (Kosaraju)...");

    const originalDirected = graph.isDirected;
    if (!graph.isDirected) {
      log("⚠️ SCC chỉ áp dụng cho đồ thị CÓ HƯỚNG");
      log("Tạm thời chuyển sang chế độ có hướng...");
      graph.isDirected = true;
    }

    const adj = {};
    const revAdj = {};
    graph.vertices.forEach(v => {
      adj[v.id] = [];
      revAdj[v.id] = [];
    });

    graph.edges.forEach(e => {
      adj[e.from].push(e.to);
      revAdj[e.to].push(e.from);
    });

    const ids = graph.vertices.map(v => v.id);
    
    const visited = {};
    const order = [];

    function dfs1(v) {
      if (visited[v]) return;
      visited[v] = true;
      
      const neighbors = adj[v] || [];
      for (const w of neighbors) {
        if (!visited[w]) dfs1(w);
      }
      
      order.push(v);
    }

    ids.forEach(v => {
      if (!visited[v]) dfs1(v);
    });

    const visited2 = {};
    const components = [];

    function dfs2(v, component) {
      if (visited2[v]) return;
      visited2[v] = true;
      component.push(v);
      
      const neighbors = revAdj[v] || [];
      for (const w of neighbors) {
        if (!visited2[w]) dfs2(w, component);
      }
    }

    while (order.length > 0) {
      const v = order.pop();
      if (!visited2[v]) {
        const component = [];
        dfs2(v, component);
        components.push(component);
      }
    }

    if (!originalDirected) {
      graph.isDirected = false;
    }

    log(`✅ Tìm thấy ${components.length} SCC:`);
    
    const colors = [neonPink, neonAqua, "#ffcc33", "#9d4edd", "#4dff91"];
    
    components.forEach((comp, idx) => {
      comp.sort((a, b) => a - b);
      const color = colors[idx % colors.length];
      log(`📦 SCC ${idx + 1} (${comp.length} đỉnh): ${comp.join(", ")}`);
      
      comp.forEach(vId => {
        const vertex = graph.vertices.find(v => v.id === vId);
        if (vertex) vertex.sccColor = color;
      });
      
      graph.edges.forEach(e => {
        if (comp.includes(e.from) && comp.includes(e.to)) {
          e.isPath = true;
          e.sccColor = color;
        }
      });
    });

    if (components.length === 1 && components[0].length === graph.vertices.length) {
      log("💪 Đồ thị LIÊN THÔNG MẠNH!");
    } else if (components.length === graph.vertices.length) {
      log("📌 Mỗi đỉnh là 1 SCC riêng biệt");
    }

    draw();
    log("SCC hoàn tất!");
  }
  
  // Ford–Fulkerson (có highlight)
  function runFordFulkersonUI(){
    if (!graph.vertices.length) { 
      log("No vertices"); 
      return;
    }

    // Reset hiển thị
    graph.edges.forEach(e => { e.isPath = false; delete e.sccColor; });
    graph.vertices.forEach(v => delete v.sccColor);

    // Build capacity graph
    const adj = {};
    graph.vertices.forEach(v => { adj[v.id] = []; });
    graph.edges.forEach(e => {
      adj[e.from].push([e.to, e.weight]);
      if (!graph.isDirected) adj[e.to].push([e.from, e.weight]);
    });

    const ids = graph.vertices.map(v => v.id).sort((a,b)=>a-b);
    const s = ids[0];
    const t = ids[ids.length-1];

    const capacity = {};
    for (let u in adj) {
      capacity[u] = {};
      adj[u].forEach(([v, w]) => {
        capacity[u][v] = w;
        if (!capacity[v]) capacity[v] = {};
        if (!capacity[v][u]) capacity[v][u] = 0;
      });
    }
    // BFS tìm đường tăng luồng
    function bfsFindPath() {
      const parent = {};
      const visited = new Set([s]);
      const q = [s];

      while (q.length) {
        const u = q.shift();
        for (let v in capacity[u]) {
          if (!visited.has(v) && capacity[u][v] > 0) {
            visited.add(v);
            parent[v] = u;
            if (v == t) return parent;
            q.push(v);
          }
        }
      }
      return null;
    }
    let maxFlow = 0;
     
    // main FF loop
    while (true) {
      const parent = bfsFindPath();
      if (!parent) break;
      
      // Tìm lượng tăng
      let flow = Infinity;
      let v = t;
      while (v != s) {
        let u = parent[v];
        flow = Math.min(flow, capacity[u][v]);
        v = u;
      }

      maxFlow += flow;

      // Cập nhật residual graph
      v = t;
      while (v != s) {
        let u = parent[v];
        capacity[u][v] -= flow;
        capacity[v][u] += flow;
        v = u;
      }
      // Highlight đường tăng
      v = t;
      while (v != s) {
        let u = parent[v];

        const e = graph.edges.find(ed =>
          (ed.from == u && ed.to == v) ||
          (!graph.isDirected && (ed.from == v && ed.to == u))
        );

        if (e) e.isPath = true;

        v = u;
      }

      draw();
      log(`Tìm được augmenting path (tăng thêm ${flow})`);
    }

    log(`Ford–Fulkerson max flow từ ${s} → ${t} = ${maxFlow}`);
    draw();
  } 
  // Hierholzer
  function runHierholzerUI() {
    if (!graph.vertices.length) {
      log("No vertices");
      return;
    }

    graph.edges.forEach(e => { e.isPath = false; delete e.sccColor; });
    graph.vertices.forEach(v => delete v.sccColor);

    const adj = {};
    graph.vertices.forEach(v => adj[v.id] = []);
    graph.edges.forEach(e => {
      adj[e.from].push(e.to);
      if (!graph.isDirected) adj[e.to].push(e.from);
    });

    const ids = graph.vertices.map(v => v.id).sort((a, b) => a - b);
    const start = ids[0];

    const stack = [start];
    const circuit = [];

    const graphCopy = {};
    for (let u in adj) graphCopy[u] = [...adj[u]];

    while (stack.length) {
      let u = stack[stack.length - 1];
      
      if (graphCopy[u].length === 0) {
        stack.pop();
        if (stack.length) circuit.push([stack[stack.length - 1], u]);
      } else {
        const v = graphCopy[u].pop();
        graphCopy[v] = graphCopy[v].filter(x => x !== u);
        stack.push(v);
      }
    }

    circuit.reverse();

    circuit.forEach(([a, b]) => {
      const e = graph.edges.find(ed =>
        (ed.from == a && ed.to == b) ||
        (!graph.isDirected && ed.from == b && ed.to == a)
      );
      if (e) e.isPath = true;
    });

    log("Hierholzer Euler path: " + circuit.map(p => p.join("→")).join(", "));
    draw();
  }
  
  // Fleury
  function runFleuryUI() {
    if (!graph.vertices.length) {
      log("No vertices");
      return;
    }

    if (graph.isDirected) {
      log("Fleury chỉ chạy với đồ thị vô hướng.");
      return;
    }

    graph.edges.forEach(e => { 
      e.isPath = false;
      e.active = false;
    });
    graph.vertices.forEach(v => delete v.sccColor);

    // Build adj list
    const adj = {};
    graph.vertices.forEach(v => adj[v.id] = []);
    graph.edges.forEach(e => {
      adj[e.from].push(e.to);
      adj[e.to].push(e.from);
    });

    // Degree
    function degree(u) { return adj[u].length; }

    // DFS count
    function dfsCount(u, visited) {
      visited[u] = true;
      adj[u].forEach(v => {
        if (!visited[v]) dfsCount(v, visited);
      });
    }

    // Remove exactly ONE edge u-v
    function removeOne(u, v) {
      let idxU = adj[u].indexOf(v);
      if (idxU !== -1) adj[u].splice(idxU, 1);

      let idxV = adj[v].indexOf(u);
      if (idxV !== -1) adj[v].splice(idxV, 1);
    }

    // Check bridge
    function isBridge(u, v) {
      let visited1 = {};
      dfsCount(u, visited1);

      removeOne(u, v);

      let visited2 = {};
      dfsCount(u, visited2);

      // restore
      adj[u].push(v);
      adj[v].push(u);

      return Object.keys(visited1).length > Object.keys(visited2).length;
    }

    // Pick start vertex
    const ids = graph.vertices.map(v => v.id).sort((a, b) => a - b);
    let curr = ids[0];

    // Euler path rule: start at odd-degree vertex if exists
    let odd = ids.filter(u => degree(u) % 2 === 1);
    if (odd.length === 2) curr = odd[0];
    else if (odd.length > 2) {
      log("Đồ thị không có Euler Path.");
      return;
    }

    const path = [];

    while (degree(curr) > 0) {
      let neighbors = [...adj[curr]];
      let chosen = null;

      for (let v of neighbors) {
        // If only 1 edge left OR not bridge
        if (degree(curr) === 1 || !isBridge(curr, v)) {
          chosen = v;
          break;
        }
      }

      path.push([curr, chosen]);
      removeOne(curr, chosen);
      curr = chosen;
    }

    // Highlight edges in graph
    path.forEach(([a, b]) => {
      let e = graph.edges.find(ed =>
        (ed.from == a && ed.to == b) ||
        (ed.from == b && ed.to == a)
      );
      if (e) {
        e.isPath = true;
        e.active = true;
      }
    });

    log("Fleury Euler path: " + path.map(p => p.join("→")).join(", "));
    draw();
  }

  // Additional features
  window.addEventListener("keydown", e => {
    if (e.key.toLowerCase() === "l") {
      log("🔄 Auto Layout đang chạy...");

      const iterations = 150;
      const repulsionForce = 1800;
      const springLength = 140;
      const springStrength = 0.01;

      for (let iter = 0; iter < iterations; iter++) {
        graph.vertices.forEach(a => {
          graph.vertices.forEach(b => {
            if (a === b) return;
            let dx = a.x - b.x;
            let dy = a.y - b.y;
            let dist = Math.hypot(dx, dy) + 0.1;

            let force = repulsionForce / (dist * dist);
            a.x += (dx / dist) * force;
            a.y += (dy / dist) * force;
          });
        });

        graph.edges.forEach(e => {
          const a = graph.vertices.find(v => v.id === e.from);
          const b = graph.vertices.find(v => v.id === e.to);
          let dx = b.x - a.x;
          let dy = b.y - a.y;
          let dist = Math.hypot(dx, dy) + 0.1;

          let force = (dist - springLength) * springStrength;

          a.x += dx / dist * force;
          a.y += dy / dist * force;
          b.x -= dx / dist * force;
          b.y -= dy / dist * force;
        });
      }

      draw();
      log("✅ Auto Layout hoàn tất!");
    }
  });

  canvas.addEventListener("dblclick", ev => {
    const w = clientToWorld(ev);
    const v = findVertexAtWorld(w.x, w.y);
    if (!v) return;
    const name = prompt("Tên mới của đỉnh:", v.label);
    if (name) v.label = name;
    draw();
  });

  // Button event listeners
  btnBFS.addEventListener("click", runBFSUI);
  btnDFS.addEventListener("click", runDFSUI);
  btnBipartite.addEventListener("click", runBipartiteUI);
  btnDijkstra.addEventListener("click", runDijkstraUI);
  btnAdjMat.addEventListener("click",()=> log("--- Adjacency Matrix ---\n"+getAdjMatrixText()));
  btnAdjList.addEventListener("click",()=> log("--- Adjacency List ---\n"+getAdjListText()));
  btnEdgeList.addEventListener("click",()=> log("--- Edge List ---\n"+getEdgeListText()));
  btnExport.addEventListener("click",()=>{
    const data=JSON.stringify(graph,null,2);
    const blob = new Blob([data],{type:"application/json"});
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url; a.download="graph.json"; a.click();
    URL.revokeObjectURL(url);
    log("Exported graph JSON");
  });
  // Ford-Fulkerson
  document.querySelectorAll("button").forEach(btn => {
    if (btn.textContent.includes("Ford-Fulkerson")) {
      btn.addEventListener("click", runFordFulkersonUI);
      btn.classList.remove("unimplemented");
    }
  });
  // Hierholzer
  document.querySelectorAll("button").forEach(btn => {
    if (btn.textContent.includes("Hierholzer")) {
      btn.addEventListener("click", runHierholzerUI);
      btn.classList.remove("unimplemented");
    }
  });
  // Fleury
  document.querySelectorAll("button").forEach(btn => {
    if (btn.textContent.trim() === "Fleury") {
      btn.addEventListener("click", () => {
        if (graph.isDirected) {
          log("Fleury chỉ chạy với đồ thị vô hướng.");
          return;
        }
        runFleuryUI();
      });
      btn.classList.remove("unimplemented");
    }
  });
  
  // THÊM ĐOẠN CODE NÀY - TOGGLE ĐỒ THỊ CÓ HƯỚNG/VÔ HƯỚNG
  btnToggleDirected.addEventListener("click", () => {
    graph.isDirected = !graph.isDirected;
    btnToggleDirected.textContent = `Đồ thị: ${graph.isDirected ? "Có hướng" : "Vô hướng"}`;
    btnToggleDirected.classList.toggle("active", graph.isDirected);
    log(`✅ Chuyển sang đồ thị ${graph.isDirected ? "CÓ HƯỚNG" : "VÔ HƯỚNG"}`);
    
    // Cập nhật tất cả cạnh hiện có
    graph.edges.forEach(edge => {
      edge.directed = graph.isDirected;
    });
    
    draw();
  });
  
  // Initialize SCC button
  if (btnSCC) {
    btnSCC.addEventListener("click", runSCC);
  }

  // Remove unimplemented class from SCC button
  if (btnSCC && btnSCC.classList.contains("unimplemented")) {
    btnSCC.classList.remove("unimplemented");
  }

  // Initialize
  log("⚡ Graph Visualizer Ready!");
  log("Click canvas để thêm đỉnh • Right-drag để pan • Wheel để zoom");
  updateInfo();
  draw();
  setTimeout(resizeCanvas, 50);
/* ============================================================
     PHẦN BỔ SUNG: THUẬT TOÁN PRIM & KRUSKAL (Do bạn thêm vào)
     ============================================================ */

  // 1. Hàm thuật toán Prim
  function runPrimUI(){
    if(!graph.vertices.length){ log("Chưa có đỉnh nào!"); return; }
    
    // Reset trạng thái hiển thị (xóa màu cũ nếu có)
    graph.edges.forEach(e => {
      e.isPath = false;
      delete e.sccColor;
    });
    graph.vertices.forEach(v => delete v.sccColor);

    const ids = graph.vertices.map(v => v.id).sort((a,b)=>a-b);
    const start = ids[0]; 
    const n = Math.max(...ids);

    const dist = Array(n+1).fill(Infinity);
    const parent = Array(n+1).fill(-1);
    const vis = Array(n+1).fill(false);
    
    // Lấy danh sách kề
    const adj = getAdjList(); 

    dist[start] = 0;
    let totalWeight = 0;
    const mstEdges = [];

    // Vòng lặp chính Prim
    for(let i = 0; i < ids.length; i++){
      let u = -1, minVal = Infinity;
      ids.forEach(v => {
        if(!vis[v] && dist[v] < minVal){
          minVal = dist[v];
          u = v;
        }
      });

      if(u === -1) break; // Đồ thị không liên thông
      vis[u] = true;

      if(parent[u] !== -1){
        totalWeight += minVal;
        mstEdges.push({u: parent[u], v: u});
      }

      if(adj[u]){
        adj[u].forEach(nb => {
          if(!vis[nb.to] && nb.w < dist[nb.to]){
            dist[nb.to] = nb.w;
            parent[nb.to] = u;
          }
        });
      }
    }

    // Highlight các cạnh kết quả
    mstEdges.forEach(pair => {
      const e = graph.edges.find(ed => 
        (ed.from === pair.u && ed.to === pair.v) || 
        (!graph.isDirected && ed.from === pair.v && ed.to === pair.u)
      );
      if(e) e.isPath = true;
    });

    log(`🌲 Prim MST: Tổng trọng số = ${totalWeight}`);
    draw();
  }

  // 2. Hàm thuật toán Kruskal
  function runKruskalUI(){
    if(!graph.vertices.length){ log("Chưa có đỉnh nào!"); return; }
    
    // Reset trạng thái
    graph.edges.forEach(e => {
      e.isPath = false;
      delete e.sccColor;
    });
    graph.vertices.forEach(v => delete v.sccColor);

    // Sắp xếp tất cả cạnh tăng dần theo trọng số
    const sortedEdges = [...graph.edges].sort((a,b) => a.weight - b.weight);

    // Cấu trúc Union-Find (DSU)
    const parent = {};
    graph.vertices.forEach(v => parent[v.id] = v.id);

    function find(i) {
      if (parent[i] === i) return i;
      return parent[i] = find(parent[i]);
    }

    function union(i, j) {
      const rootI = find(i);
      const rootJ = find(j);
      if (rootI !== rootJ) {
        parent[rootI] = rootJ;
        return true;
      }
      return false;
    }

    let totalWeight = 0;
    let edgeCount = 0;

    sortedEdges.forEach(e => {
      if(union(e.from, e.to)){
        e.isPath = true; // Đánh dấu cạnh thuộc MST
        totalWeight += e.weight;
        edgeCount++;
      }
    });

    log(`🌲 Kruskal MST: Tổng trọng số = ${totalWeight} (Gồm ${edgeCount} cạnh)`);
    draw();
  }

  // 3. Tự động tìm nút và gán sự kiện (Không cần sửa HTML)
  // Đoạn này sẽ tìm các nút có chữ "Prim" hoặc "Kruskal" để kích hoạt
  setTimeout(() => {
    document.querySelectorAll("button").forEach(btn => {
      const txt = btn.textContent.trim();
      
      // Kích hoạt nút Prim
      if (txt.includes("Prim")) {
        btn.onclick = runPrimUI; // Gán hàm xử lý
        btn.classList.remove("unimplemented"); // Xóa class làm mờ
        btn.classList.add("control"); // Đảm bảo style đẹp
        // console.log("Đã kích hoạt Prim");
      }
      
      // Kích hoạt nút Kruskal
      if (txt.includes("Kruskal")) {
        btn.onclick = runKruskalUI;
        btn.classList.remove("unimplemented");
        btn.classList.add("control");
        // console.log("Đã kích hoạt Kruskal");
      }
    });
  }, 100); // Đợi 100ms để đảm bảo giao diện đã tải xong
  // Make graph accessible from console for debugging
  window._gv = {graph, addVertexAt, addEdge, draw, log};
})();