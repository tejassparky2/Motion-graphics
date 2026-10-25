// "Tower 9": a fire-watch cabin 30 m above a forest at night, in the rain. The cabin floor is y = 0 (x, z within
// +-1.8); the forest floor is y = -30. A hatch in the floor (at x = z = 1.0) opens onto the ladder. Torches circle
// the tower below; lightning shows the figures holding them (one wears your orange jacket: the hidden detail).
export async function build(c) {
  const {THREE, scene, mat, basic, glowMat, mesh, box, add, canvasTex, seg, lin, lerp, clamp, noise, person, pose, POSES,
         mixPose, poseFace, EMO, mixEmo, B, word, envAt, rnd, T} = c;
  scene.background = new THREE.Color(0x03050a);
  scene.fog = new THREE.FogExp2(0x05070c, .03);
  const wood = mat(0x6a4a30, {roughness: .85}), woodDark = mat(0x3a2818, {roughness: .9}), metal = mat(0x6a6e70, {metalness: .3, roughness: .5});
  const planks = canvasTex(512, 512, g => { g.fillStyle = "#6a4a30"; g.fillRect(0, 0, 512, 512);
    for (let y = 0; y < 512; y += 42) { g.fillStyle = `rgba(0,0,0,${.15 + rnd() * .15})`; g.fillRect(0, y, 512, 3); for (let i = 0; i < 30; i++) { g.fillStyle = `rgba(40,20,10,${rnd() * .12})`; g.fillRect(rnd() * 512, y + rnd() * 40, 40 + rnd() * 80, 2); } } });
  planks.wrapS = planks.wrapT = THREE.RepeatWrapping;
  const floorM = new THREE.MeshStandardMaterial({map: planks, roughness: .8});
  // cabin: floor with the hatch hole, walls below and above the windows, corner posts, roof
  const S = 1.8;
  const floorShape = new THREE.Shape([[-S, -S], [S, -S], [S, S], [-S, S]].map(([x, y]) => new THREE.Vector2(x, y)));
  const hole = new THREE.Path([[.6, .6], [1.4, .6], [1.4, 1.4], [.6, 1.4]].map(([x, y]) => new THREE.Vector2(x, y))); floorShape.holes.push(hole);
  const fl = mesh(new THREE.ShapeGeometry(floorShape), floorM); fl.rotation.x = Math.PI / 2; add(fl, 0, 0, 0);
  fl.material.side = THREE.DoubleSide;
  for (const [x, z, ry] of [[0, -S, 0], [0, S, Math.PI], [-S, 0, Math.PI / 2], [S, 0, -Math.PI / 2]]) {
    const lo = mesh(new THREE.PlaneGeometry(2 * S, .9), wood); lo.rotation.y = ry; add(lo, x, .45, z); lo.material.side = THREE.DoubleSide;
    const hi = mesh(new THREE.PlaneGeometry(2 * S, .25), wood); hi.rotation.y = ry; add(hi, x, 2.12, z);
    const sill = mesh(new THREE.BoxGeometry(2 * S, .05, .14), woodDark); sill.rotation.y = ry; add(sill, x * .98, .92, z * .98);
    for (const k of [-.6, .6]) { const mull = mesh(new THREE.BoxGeometry(.06, 1.1, .06), woodDark); add(mull, x === 0 ? k * S : x * .99, 1.5, z === 0 ? k * S : z * .99); }
  }
  for (const [x, z] of [[-S, -S], [S, -S], [-S, S], [S, S]]) add(mesh(new THREE.BoxGeometry(.14, 2.3, .14), woodDark), x, 1.15, z);
  const roof = mesh(new THREE.ConeGeometry(2.9, 1.0, 4, 1, true), woodDark); roof.rotation.y = Math.PI / 4; add(roof, 0, 2.75, 0); roof.material.side = THREE.DoubleSide;
  const ceil = mesh(new THREE.PlaneGeometry(2 * S, 2 * S), mat(0x4a3424)); ceil.rotation.x = Math.PI / 2; add(ceil, 0, 2.25, 0);
  const glass = new THREE.MeshStandardMaterial({color: 0x101820, roughness: .05, metalness: .9, transparent: true, opacity: .18});
  for (const [x, z, ry] of [[0, -S, 0], [0, S, Math.PI], [-S, 0, Math.PI / 2], [S, 0, -Math.PI / 2]]) { const g = new THREE.Mesh(new THREE.PlaneGeometry(2 * S, 1.1), glass); g.rotation.y = ry; add(g, x * 1.005, 1.5, z * 1.005); }
  // the hatch (a trapdoor that jolts on the knocks; light from torches below leaks through its gaps)
  const hatch = new THREE.Group(); add(hatch, 1.0, 0, 1.0);
  const lid = mesh(box(.78, .05, .78, .1), new THREE.MeshStandardMaterial({map: planks, roughness: .8, color: 0x8a6a50})); lid.position.y = .02; hatch.add(lid);
  for (const z of [-.25, .25]) hatch.add(add(mesh(new THREE.BoxGeometry(.7, .015, .06), metal), 0, .052, z, hatch));
  const ringH = mesh(new THREE.TorusGeometry(.05, .01, 8, 16), metal); ringH.rotation.x = Math.PI / 2; ringH.position.set(.25, .055, 0); hatch.add(ringH);
  const latch = mesh(new THREE.BoxGeometry(.18, .03, .05), metal); latch.position.set(-.4, .05, 0); hatch.add(latch);
  const leak = new THREE.Mesh(new THREE.PlaneGeometry(.84, .84), glowMat(0xff8a2a, 0)); leak.rotation.x = -Math.PI / 2; leak.position.y = .003; hatch.add(leak);
  const hatchGlow = new THREE.PointLight(0xff8a30, 0, 1.8, 1.6); hatchGlow.position.set(0, .15, 0); hatch.add(hatchGlow);
  // desk with the radio, logbook, mug; chair; map table; clock; fuel gauge; hanging bulb
  add(mesh(box(1.6, .05, .6, .1), wood), 0, .75, -1.48); add(mesh(new THREE.BoxGeometry(1.5, .7, .04), woodDark), 0, .38, -1.75);
  const radio = new THREE.Group(); add(radio, -.35, .78, -1.55);
  radio.add(add(mesh(box(.42, .2, .26, .1), mat(0x2a3020, {roughness: .6})), 0, .1, 0, radio));
  const dialTex = canvasTex(128, 48, g => { g.fillStyle = "#1a1008"; g.fillRect(0, 0, 128, 48); g.fillStyle = "#ffb040"; g.font = "bold 22px monospace"; g.fillText("CH 9  158.2", 6, 32); });
  const dial = new THREE.Mesh(new THREE.PlaneGeometry(.2, .075), new THREE.MeshBasicMaterial({map: dialTex, toneMapped: false})); dial.position.set(-.06, .13, .131); radio.add(dial);
  const led = new THREE.Mesh(new THREE.SphereGeometry(.012, 10, 8), glowMat(0xff2010, 1)); led.position.set(.14, .15, .13); radio.add(led);
  const ledLight = new THREE.PointLight(0xff2a10, 0, 1.2, 1.6); ledLight.position.set(.14, .18, .25); radio.add(ledLight);
  for (const x of [.08, .16]) { const k = mesh(new THREE.CylinderGeometry(.022, .022, .02, 14), metal); k.rotation.x = Math.PI / 2; k.position.set(x, .06, .135); radio.add(k); }
  const ant = mesh(new THREE.CylinderGeometry(.004, .004, .45, 6), metal); ant.position.set(.18, .42, -.05); radio.add(ant);
  const mic = mesh(box(.06, .1, .04, .3), mat(0x151515)); mic.position.set(.3, .05, .08); radio.add(mic);
  const bookTex = canvasTex(512, 340, g => { g.fillStyle = "#e8dcc0"; g.fillRect(0, 0, 512, 340); g.fillStyle = "rgba(0,0,0,.15)"; g.fillRect(253, 0, 6, 340);
    g.fillStyle = "#2a1a10"; g.font = "italic 22px serif"; ["Oct 3 - clear", "Oct 4 - smoke, NE", "Oct 9 - nothing", "Oct 12 - radio??"].forEach((l, i) => g.fillText(l, 20, 50 + i * 40));
    g.fillStyle = "#8a1a10"; g.font = "bold 28px serif"; g.fillText("1. Never answer the", 270, 70); g.fillText("radio after 3 AM.", 270, 110); g.fillText("2. Never open", 270, 170); g.fillText("the hatch.", 270, 210);
    g.font = "italic 20px serif"; g.fillStyle = "#2a1a10"; g.fillText("Whatever it sounds like.", 272, 270); });
  const book = new THREE.Mesh(new THREE.PlaneGeometry(.42, .28), new THREE.MeshStandardMaterial({map: bookTex, roughness: .9})); book.rotation.x = -Math.PI / 2; book.rotation.z = .1; add(book, .35, .78, -1.42);
  const mug = mesh(new THREE.CylinderGeometry(.04, .035, .09, 14), mat(0x8a2a1a)); add(mug, .68, .82, -1.55);
  const chair = new THREE.Group(); add(chair, 0, 0, -.82);
  chair.add(add(mesh(box(.44, .05, .44, .2), wood), 0, .46, 0, chair)); chair.add(add(mesh(box(.44, .5, .05, .2), wood), 0, .72, .22, chair));
  for (const [x, z] of [[-.19, -.19], [.19, -.19], [-.19, .19], [.19, .19]]) chair.add(add(mesh(new THREE.CylinderGeometry(.02, .02, .45, 6), woodDark), x, .22, z, chair));
  const mapT = new THREE.Group(); add(mapT, -.6, 0, .55);
  mapT.add(add(mesh(new THREE.CylinderGeometry(.06, .08, .95, 10), woodDark), 0, .47, 0, mapT));
  const mapTex = canvasTex(256, 256, g => { g.fillStyle = "#c8c09a"; g.beginPath(); g.arc(128, 128, 126, 0, 7); g.fill(); g.strokeStyle = "rgba(60,90,50,.6)"; g.lineWidth = 2;
    for (let r = 20; r < 126; r += 14) { g.beginPath(); g.arc(128 + Math.sin(r) * 8, 128 + Math.cos(r) * 6, r, 0, 7); g.stroke(); } g.strokeStyle = "#8a1a10"; g.beginPath(); g.moveTo(128, 0); g.lineTo(128, 256); g.moveTo(0, 128); g.lineTo(256, 128); g.stroke(); });
  const mapTop = mesh(new THREE.CylinderGeometry(.45, .45, .04, 32), [mat(0x3a2818), new THREE.MeshStandardMaterial({map: mapTex}), mat(0x3a2818)]); add(mapTop, 0, .96, 0, mapT);
  const clockTex = canvasTex(128, 128, g => { g.fillStyle = "#f0ead8"; g.beginPath(); g.arc(64, 64, 60, 0, 7); g.fill(); g.strokeStyle = "#222"; g.lineWidth = 4; g.stroke();
    for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; g.fillStyle = "#222"; g.fillRect(64 + Math.sin(a) * 50 - 2, 64 - Math.cos(a) * 50 - 2, 4, 4); }
    g.lineCap = "round"; g.lineWidth = 6; g.beginPath(); g.moveTo(64, 64); g.lineTo(64 + Math.sin(3.23 / 12 * Math.PI * 2) * 30, 64 - Math.cos(3.23 / 12 * Math.PI * 2) * 30); g.stroke();
    g.lineWidth = 4; g.beginPath(); g.moveTo(64, 64); g.lineTo(64 + Math.sin(14 / 60 * Math.PI * 2) * 46, 64 - Math.cos(14 / 60 * Math.PI * 2) * 46); g.stroke(); });
  const clock = new THREE.Mesh(new THREE.CircleGeometry(.14, 32), new THREE.MeshStandardMaterial({map: clockTex})); clock.rotation.y = -Math.PI / 2; add(clock, S - .02, 2.0 - .15, -1.0);
  const gaugeTex = canvasTex(256, 256, g => { g.fillStyle = "#e8e0c8"; g.beginPath(); g.arc(128, 140, 110, 0, 7); g.fill(); g.lineWidth = 16;
    g.strokeStyle = "#c02010"; g.beginPath(); g.arc(128, 140, 90, Math.PI * 1.05, Math.PI * 1.3); g.stroke(); g.strokeStyle = "#2a8a3a"; g.beginPath(); g.arc(128, 140, 90, Math.PI * 1.6, Math.PI * 1.95); g.stroke();
    g.fillStyle = "#222"; g.font = "bold 26px sans-serif"; g.fillText("E", 40, 150); g.fillText("F", 200, 150); g.font = "bold 22px sans-serif"; g.fillText("GEN FUEL", 70, 210); });
  const gauge = new THREE.Group(); add(gauge, S - .02, 1.45, -.2); gauge.rotation.y = -Math.PI / 2;
  gauge.add(mesh(new THREE.CircleGeometry(.14, 32), new THREE.MeshStandardMaterial({map: gaugeTex})));
  const needle = mesh(new THREE.BoxGeometry(.008, .1, .004), mat(0x101010)); needle.geometry.translate(0, .05, 0); needle.position.set(0, -.01, .005); gauge.add(needle);
  const cord = mesh(new THREE.CylinderGeometry(.004, .004, .25, 6), mat(0x111111)); add(cord, .2, 2.13, .3);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(.045, 16, 12), glowMat(0xffc070, 2)); add(bulb, .2, 2.0, .3);
  const bulbLight = new THREE.PointLight(0xffb060, 3.2, 7, 1.5); add(bulbLight, .2, 1.96, .3);
  bulbLight.castShadow = true; bulbLight.shadow.mapSize.set(512, 512); bulbLight.shadow.bias = -.004;
  const hemi = new THREE.HemisphereLight(0x405080, 0x0a0806, .12); scene.add(hemi);
  const sky = new THREE.DirectionalLight(0xb8c8ff, 0); sky.position.set(-20, 40, 30); scene.add(sky);
  // the tower legs, bracing and ladder below the hatch
  for (const [x, z] of [[-1.5, -1.5], [1.5, -1.5], [-1.5, 1.5], [1.5, 1.5]]) add(mesh(new THREE.BoxGeometry(.18, 30, .18), woodDark), x * (1 + .0), -15, z);
  for (let y = -27; y < 0; y += 4) for (const [x, z, ry] of [[0, -1.5, 0], [0, 1.5, 0], [-1.5, 0, Math.PI / 2], [1.5, 0, Math.PI / 2]]) {
    const br = mesh(new THREE.BoxGeometry(4.3, .1, .08), woodDark); br.rotation.set(0, ry, .75); add(br, x, y, z); }
  const ladder = new THREE.Group(); add(ladder, 1.0, 0, 1.38);
  const rungM = mat(0xa8a8a0, {roughness: .5});
  for (const x of [-.22, .22]) ladder.add(add(mesh(new THREE.BoxGeometry(.05, 30, .05), rungM), x, -15, 0, ladder));
  for (let y = -.3; y > -30; y -= .32) add(mesh(new THREE.CylinderGeometry(.015, .015, .44, 6), rungM), 0, y, 0, ladder).rotation.z = Math.PI / 2;
  // the thing on the ladder: a pale hand and arm reaching up out of the dark
  const climber = new THREE.Group(); ladder.add(climber);
  const pale = mat(0xb8b0a0, {roughness: .7});
  const handGeo = new THREE.SphereGeometry(.05, 12, 10);
  for (const s of [-1, 1]) { const arm = mesh(new THREE.CapsuleGeometry(.04, .9, 4, 10), pale); arm.position.set(s * .14, -.55, .1); arm.rotation.x = .25; climber.add(arm);
    const h = mesh(handGeo, pale); h.position.set(s * .14, -.05, .02); h.scale.set(1.1, .7, 1); climber.add(h);
    for (let f = 0; f < 4; f++) { const fi = mesh(new THREE.CapsuleGeometry(.01, .06, 3, 6), pale); fi.position.set(s * .14 + (f - 1.5) * .022, .02, -.03); fi.rotation.x = 1.3; climber.add(fi); } }
  const headC = mesh(new THREE.SphereGeometry(.13, 16, 12), mat(0x151515)); headC.position.set(0, -.75, .25); climber.add(headC);
  const climbGlow = new THREE.PointLight(0xff8a30, 8, 9, 1.2); climbGlow.position.set(.3, -2.5, .8); climber.add(climbGlow);
  // the forest below, the torches and the figures holding them
  const ground = mesh(new THREE.CircleGeometry(80, 40), mat(0x0a0d08, {roughness: 1})); ground.rotation.x = -Math.PI / 2; add(ground, 0, -30, 0);
  const NT = 420, trees = new THREE.InstancedMesh(new THREE.ConeGeometry(1.6, 9, 7), mat(0x0e1a12, {roughness: 1}), NT);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion();
  for (let i = 0; i < NT; i++) { const a = rnd() * Math.PI * 2, r = 5 + Math.pow(rnd(), .7) * 60, s = .8 + rnd() * .8;
    m4.compose(new THREE.Vector3(Math.cos(a) * r, -30 + 4.5 * s, Math.sin(a) * r), q, new THREE.Vector3(s, s, s)); trees.setMatrixAt(i, m4); }
  scene.add(trees);
  const torches = [], figs = [];
  for (let i = 0; i < 23; i++) {
    const a0 = rnd() * Math.PI * 2, r = 4 + rnd() * 9, sp = (.08 + rnd() * .06) * (rnd() < .5 ? 1 : -1);
    const fig = person({skin: 0x8a8a84, top: i === 6 ? 0xd8641c : 0x0c0c0c, legs: 0x0c0c0c, hair: 0x050505, beanie: i === 6 ? 0x2a3a2a : undefined, glowEyes: 0xffe8c0});
    pose(fig, POSES.radio); fig.root.scale.setScalar(1.0); scene.add(fig.root);
    const flame = new THREE.Mesh(new THREE.SphereGeometry(.4, 10, 8), glowMat(0xffa040, 4)); scene.add(flame);   // big enough to read from 30 m up
    torches.push({a0, r, sp, flame, fig, ph: rnd() * 6});
  }
  const torchLights = [0, 1, 2, 3, 4, 5].map(() => { const l = new THREE.PointLight(0xff8a30, 0, 18, 1.1); scene.add(l); return l; });
  const moon = new THREE.DirectionalLight(0x5a70b0, .35); moon.position.set(30, 40, -20); scene.add(moon);   // the forest is never pure black
  // rain: falling streaks around the cabin
  const NR = 1600, rainGeo = new THREE.BufferGeometry(), rp = new Float32Array(NR * 6), r0 = [];
  for (let i = 0; i < NR; i++) { const a = rnd() * Math.PI * 2, r = 2.0 + rnd() * 12; r0.push([Math.cos(a) * r, rnd() * 40 - 30, Math.sin(a) * r]); }
  rainGeo.setAttribute("position", new THREE.BufferAttribute(rp, 3));
  const rain = new THREE.LineSegments(rainGeo, new THREE.LineBasicMaterial({color: 0x8090b0, transparent: true, opacity: .35})); scene.add(rain);
  // ----- you, the ranger (orange jacket)
  const you = person({skin: 0xc89a72, top: 0xd8641c, legs: 0x3a3a2a, hair: 0x3a2414, beanie: 0x2a3a2a, iris: 0x3a5a6a, collar: 0xb8501a});
  scene.add(you.root);

  const DIR = {   // you: [emotion, pose, place]
    t1: {you: ["worried", "sitRadio", "desk"]}, t2: {you: ["scared", "sitRadio", "desk"]}, t3: {you: ["scared", "sitTense", "desk"]},
    t4: {you: ["scared", "sitTense", "desk"]}, t5: {you: ["scared", "sitTense", "desk"]}, t6: {you: ["worried", "stand", "mid"]},
    t7: {you: ["worried", "stand", "mid"]}, t8: {you: ["scared", "stand", "window"]}, t9: {you: ["scared", "stand", "window"]},
    t10: {you: ["scared", "radio", "deskStand"]}, t11: {you: ["terror", "stand", "mid"]}, t12: {you: ["terror", "back", "mid"]},
    t13: {you: ["scared", "radio", "deskStand"]}, t14: {you: ["scared", "radio", "deskStand"]}, t15: {you: ["terror", "stand", "deskStand"]},
    t16: {you: ["terror", "kneel", "hatch"]}, t17: {you: ["terror", "kneel", "hatch"]}, t17b: {you: ["terror", "kneel", "hatch"]},
    t17c: {you: ["terror", "stand", "mid"]}, t18: {you: ["terror", "stand", "mid"]}, t19: {you: ["terror", "stand", "mid"]},
  };
  const PLACE = {desk: [0, -.82, Math.PI], deskStand: [-.1, -.95, Math.PI], mid: [-.45, .1, .7], window: [-1.25, -.5, -1.4], hatch: [.35, .4, .78]};
  const get = (id) => (DIR[id] && DIR[id].you) || null;
  function last(t) { let d = null; for (const b of c.beats) { if (b.start - .12 > t) break; if (get(b.id)) d = get(b.id); } return d || ["worried", "sitRadio", "desk"]; }

  const under = new THREE.PointLight(0x5a6a90, 1.2, 6, 1.4); add(under, 1.2, -1.2, 1.6);   // cold light under the cabin (the ladder shot)
  const knockAt = B.t12.start - 1.25;                 // the knocks come in the silence before "Three knocks on the hatch."
  const SHOTS = {
    radio_close: {pos: [-.85, 1.2, -1.02], look: [-.35, .88, -1.55], fov: 44, push: .12},     // from the side: you never block it
    you_close:   c.track(you, {dist: .6, side: .1, fov: 40}),
    logbook:     {pos: [.52, 1.3, -1.08], look: [.47, .78, -1.43], fov: 40, push: .08},    // the rules page, readable in 3D
    cabin:       {pos: [1.45, 1.85, 1.5], look: [-.3, 1.1, -1.0], fov: 56, push: .25},
    generator:   {pos: [.95, 1.55, .2], look: [1.78, 1.45, -.25], fov: 44, push: .12},
    trees:       {pos: [-3.4, 2.6, 2.8], look: [-1.5, -30, 1.5], fov: 62, push: .6},
    ladder:      t => t < knockAt - .1 ? {pos: [1.05, -.35, 1.95], look: [1.0, -6, 1.38], fov: 52, push: .25}
                                       : {pos: [1.5, 1.45, 1.62], look: [.95, 0, .95], fov: 48, push: .15},   // cut to the hatch for the knocks
    hatch:       {pos: [1.5, 1.45, 1.62], look: [.95, 0, .95], fov: 48, push: .15},
    hatch_close: c.track(you, {dist: .7, side: -.15, up: -.1, fov: 42, lookUp: -.05}),
    choice:      {pos: [1.0, 1.9, -1.2], look: [-.45, 1.0, .2], fov: 56, push: .25},
  };
  const flashes = [B.t9.start + .4, knockAt, B.t16.start + .2, B.t1.start + 1.6, B.t5.start + .8, B.t15.start + .6];
  const knocks = [0, .32, .64].map(k => knockAt + k);
  const fuelAt = t => .34 - .24 * lin(t, word("t7", 3), B.t19.end);

  function update(t, cur, prev) {
    // lightning: a double flash; the sky light lights the forest and the figures
    let fl = 0; for (const f of flashes) { const d = t - f; if (d >= 0 && d < .5) fl = Math.max(fl, d < .08 ? 1 : d < .16 ? .2 : d < .24 ? .8 : Math.max(0, 1 - (d - .24) / .26) * .5); }
    sky.intensity = 4.5 * fl; scene.background.setHex(fl > .3 ? 0x2a3450 : 0x03050a); hemi.intensity = .12 + .5 * fl;
    // the bulb: steady, then flickering more as the fuel runs out
    const fuel = fuelAt(t), weak = clamp((.25 - fuel) / .15);
    const flick = (noise(t * 10, 4) > .8 - .35 * weak ? .25 : 1) * (1 - .25 * weak);
    bulbLight.intensity = 3.2 * flick; bulb.material.color.setHex(0xffc070).multiplyScalar(2 * flick);
    bulb.position.x = .2 + .02 * Math.sin(t * .9); bulbLight.position.x = bulb.position.x;
    needle.rotation.z = lerp(1.25, -1.25, fuel / .34 * .5 + .0);
    // radio LED pulses with whoever is talking through it
    const talk = Math.max(envAt("radio", t), envAt("base", t));
    led.material.color.setHex(0xff2010).multiplyScalar(.6 + 3 * talk); ledLight.intensity = .05 + .5 * talk;
    // torches: how many are lit follows the count in the HUD
    const lit = t < word("t8", 5) ? 0 : t < word("t9", 0) ? 2 : t < word("t9", 2) ? 5 : t < word("t9", 4) ? 9 : 23;
    torches.forEach((tc, i) => { const a = tc.a0 + tc.sp * t, x = Math.cos(a) * tc.r, z = Math.sin(a) * tc.r;
      tc.flame.visible = i < lit; tc.flame.position.set(x, -28.1 + .05 * Math.sin(t * 9 + tc.ph), z);
      tc.flame.scale.setScalar(1 + .15 * noise(t * 8, tc.ph));
      tc.fig.root.visible = i < lit || fl > .3; tc.fig.root.position.set(x + .35 * Math.cos(a + 1.6), -30, z + .35 * Math.sin(a + 1.6));
      tc.fig.root.rotation.y = Math.atan2(-x, -z); poseFace(tc.fig.face, {...EMO.neutral, look: [0, .6]}, t, i); });
    torchLights.forEach((l, k) => { const tc = torches[k * 3]; l.intensity = k * 3 < lit ? 30 : 0; l.position.copy(tc.flame.position).y += .8; });
    // rain
    for (let i = 0; i < NR; i++) { const [x, y0, z] = r0[i]; const y = ((y0 - t * 9) % 40 + 40) % 40 - 30; rp.set([x, y, z, x + .05, y + .5, z], i * 6); }
    rainGeo.attributes.position.needsUpdate = true;
    // the hatch: three knocks make it jump; torchlight leaks through when something is under it
    let kick = 0; for (const k of knocks) { const d = t - k; if (d >= 0 && d < .25) kick = Math.max(kick, Math.sin(d / .25 * Math.PI)); }
    if (cur.id === "t17" || cur.id === "t16") kick = .15 * Math.max(0, Math.sin(t * 7)) * (noise(t, 3) > .3 ? 1 : 0);
    hatch.position.y = .025 * kick; hatch.rotation.z = .02 * kick;
    const under = t > knockAt ? 1 : 0;
    leak.material.color.setHex(0xff8a2a).multiplyScalar(under * (.25 + .25 * noise(t * 6, 2))); hatchGlow.intensity = under * (.8 + .4 * noise(t * 7, 1));
    // the climber comes up the ladder during t11; under the hatch from t12
    const ck = seg(t, B.t11.start, B.t11.end + .3);
    climber.position.y = lerp(-9, -1.2, ck) + .08 * Math.sin(t * 5); climber.visible = t > B.t11.start - .3 && t < B.t12.start + 2;
    // ----- you
    const yd = last(cur.start), yp = last(prev.start);
    const u = seg(t, cur.start - .15, cur.start + .45);
    pose(you, mixPose(POSES[yp[1]], POSES[yd[1]], u));
    const P0 = PLACE[yp[2]], P1 = PLACE[yd[2]];
    you.root.position.set(lerp(P0[0], P1[0], u), 0, lerp(P0[1], P1[1], u)); you.root.rotation.y = lerp(P0[2], P1[2], u);
    chair.position.z = yd[2] === "desk" ? -.82 : -.55; chair.rotation.y = yd[2] === "desk" ? 0 : .5;
    const ye = mixEmo(EMO[yp[0]], EMO[yd[0]], u);
    if (cur.id === "t6") ye.look = [.6, .4];
    if (["t12", "t16", "t17", "t17b"].includes(cur.id)) ye.look = [0, -.7];
    poseFace(you.face, ye, t, .9);
    you.chest.rotation.x += .014 * Math.sin(t * (yd[0] === "terror" ? 4.6 : 2.3));
    you.chest.rotation.z += yd[0] === "terror" ? .004 * Math.sin(t * 37) : 0;
    if (cur.id === "t6") you.neck.rotation.set(-.25, .5, 0);
    c.camFill.color.setHex(0xffc890); c.camFill.intensity = cur.scene === "trees" || cur.scene === "ladder" ? 0 : .3;
  }
  return {SHOTS, update, shake: t => 0};
}
