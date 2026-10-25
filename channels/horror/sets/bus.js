// "Last Stop": the last night bus. The bus stands still at the origin (forward = -z, floor y = 0, road y = -0.5) and
// the world slides past: streetlamps in town, then forest. The front half of the cabin is lit, the back half is
// dark. Things in the back seats live on layer 2: only the window's reflection sees them (the old man is among them,
// the hidden detail), until the last two lines.
export async function build(c) {
  const {THREE, scene, mat, basic, glowMat, mesh, box, add, canvasTex, seg, lin, lerp, clamp, noise, person, pose, POSES,
         mixPose, poseFace, EMO, mixEmo, B, word, envAt, onLayer, Reflector, rnd, T} = c;
  scene.fog = new THREE.FogExp2(0x02030a, .045);
  scene.background = new THREE.Color(0x02030a);
  const bus = new THREE.Group(); scene.add(bus);
  const paint = mat(0xcfd6d0, {roughness: .6, side: THREE.DoubleSide}), dark = mat(0x22262c, {roughness: .7});
  const seatM = mat(0x2a4a7a, {roughness: .9}), poleM = mat(0xe0b020, {metalness: .6, roughness: .35});
  const BW = 1.2, ZF = -5.6, ZB = 5.6;
  const floorTex = canvasTex(256, 1024, g => { g.fillStyle = "#3a3e40"; g.fillRect(0, 0, 256, 1024); for (let i = 0; i < 2600; i++) { g.fillStyle = `rgba(255,255,255,${rnd() * .05})`; g.fillRect(rnd() * 256, rnd() * 1024, 2, 2); } });
  const fl = mesh(new THREE.PlaneGeometry(2 * BW, ZB - ZF), new THREE.MeshStandardMaterial({map: floorTex, roughness: .7})); fl.rotation.x = -Math.PI / 2; add(fl, 0, 0, 0, bus);
  const roof = mesh(new THREE.PlaneGeometry(2 * BW, ZB - ZF), mat(0xb8beb8, {side: THREE.DoubleSide})); roof.rotation.x = Math.PI / 2; add(roof, 0, 2.3, 0, bus);
  // side walls with window openings (windows between y 1.0 and 1.9, posts every 1.1 m)
  for (const s of [-1, 1]) {
    const low = mesh(new THREE.PlaneGeometry(ZB - ZF, 1.0), paint); low.rotation.y = -s * Math.PI / 2; add(low, s * BW, .5, 0, bus);
    const up = mesh(new THREE.PlaneGeometry(ZB - ZF, .4), paint); up.rotation.y = -s * Math.PI / 2; add(up, s * BW, 2.1, 0, bus);
    for (let z = ZF; z <= ZB + .01; z += 1.1) add(mesh(new THREE.BoxGeometry(.06, .9, .1), paint), s * BW, 1.45, z, bus);
  }
  const backW = mesh(new THREE.PlaneGeometry(2 * BW, 2.3), paint); backW.rotation.y = Math.PI; add(backW, 0, 1.15, ZB, bus);
  // front: dashboard, windshield frame, the driver's seat and wheel, the door on the right
  add(mesh(box(2.3, .9, .5, .1), dark), 0, .45, ZF + .1, bus);
  add(mesh(new THREE.BoxGeometry(2.4, .15, .1), paint), 0, 2.22, ZF, bus);
  const dashTex = canvasTex(256, 64, g => { g.fillStyle = "#050a08"; g.fillRect(0, 0, 256, 64); g.fillStyle = "#3aff8a"; g.font = "bold 22px monospace"; g.fillText("ROUTE 9  23:58", 20, 40); });
  const dash = new THREE.Mesh(new THREE.PlaneGeometry(.5, .12), new THREE.MeshBasicMaterial({map: dashTex, toneMapped: false})); dash.rotation.x = -.6; add(dash, -.75, .93, ZF + .32, bus);
  const dashLight = new THREE.PointLight(0x40ff90, .5, 1.6, 1.5); add(dashLight, -.75, 1.0, ZF + .5, bus);
  const sign = canvasTex(512, 64, g => { g.fillStyle = "#000"; g.fillRect(0, 0, 512, 64); g.fillStyle = "#ffa020"; g.font = "bold 40px monospace"; g.fillText("9  LAST SERVICE", 40, 48); });
  const routeSign = new THREE.Mesh(new THREE.PlaneGeometry(1.0, .13), new THREE.MeshBasicMaterial({map: sign, toneMapped: false})); routeSign.rotation.y = Math.PI; add(routeSign, 0, 2.14, ZF + .05, bus);
  const wheel = mesh(new THREE.TorusGeometry(.2, .025, 8, 24), dark); wheel.rotation.x = -1.0; add(wheel, -.75, 1.0, ZF + .75, bus);
  const doors = [0, 1].map(k => { const d = mesh(new THREE.BoxGeometry(.04, 2.0, .45), mat(0x8a9a90, {metalness: .3, roughness: .4})); add(d, BW, 1.0, ZF + .55 + k * .45, bus); return d; });
  const doorLight = new THREE.PointLight(0xffc070, 0, 4, 1.5); add(doorLight, BW - .2, 2.1, ZF + .8, bus);
  // seats: pairs on both sides, rows facing forward; poles
  const seats = [];
  for (let z = -3.6; z <= 4.4; z += .9) for (const x of [-.85, -.45, .45, .85]) {
    const sg = new THREE.Group(); add(sg, x, 0, z, bus);
    sg.add(add(mesh(box(.38, .12, .42, .3), seatM), 0, .45, 0, sg));
    sg.add(add(mesh(box(.38, .55, .1, .3), seatM), 0, .75, .2, sg));
    sg.add(add(mesh(new THREE.CylinderGeometry(.02, .02, .4, 8), dark), 0, .2, 0, sg));
    seats.push(sg);
  }
  add(mesh(box(2.2, .12, .5, .2), seatM), 0, .45, ZB - .35, bus); add(mesh(box(2.2, .6, .1, .2), seatM), 0, .8, ZB - .1, bus);
  for (const z of [-2.7, -.9, .9, 2.7]) add(mesh(new THREE.CylinderGeometry(.02, .02, 2.3, 8), poleM), .3, 1.15, z, bus);
  // ceiling lights: front half on (cold green-white), back half dead
  const strips = [];
  for (let z = -4.6; z <= 4.6; z += 1.15) { const st = mesh(new THREE.BoxGeometry(.25, .03, .9), glowMat(0xd8ffe8, z < 1.2 ? 1.1 : .03), false); add(st, 0, 2.28, z, bus); strips.push(st); }
  const cab = [-4.4, -2.2, -.2].map(z => add(new THREE.PointLight(0xc8f0dc, 1.6, 4.5, 1.6), 0, 2.1, z, bus));
  const hemi = new THREE.HemisphereLight(0x405060, 0x080808, .25); scene.add(hemi);
  // the bus outside (seen in the forest stop): body shell, wheels, headlights
  const shell = mat(0x2a6a6a, {roughness: .5});
  add(mesh(new THREE.BoxGeometry(2.5, .6, 11.3), shell), 0, -.25, 0, bus);
  add(mesh(new THREE.BoxGeometry(2.5, .1, 11.3), shell), 0, 2.36, 0, bus);
  for (const [x, z] of [[-1.25, -3.8], [1.25, -3.8], [-1.25, 3.6], [1.25, 3.6]]) { const w = mesh(new THREE.CylinderGeometry(.45, .45, .3, 20), mat(0x111111)); w.rotation.z = Math.PI / 2; add(w, x, -.1, z, bus); }
  for (const x of [-.8, .8]) { add(new THREE.Mesh(new THREE.CircleGeometry(.12, 16), glowMat(0xfff4d0, 2.5)), x, -.05, ZF - .01, bus).rotation.y = Math.PI;
    const hl = new THREE.SpotLight(0xfff0d0, 25, 30, .45, .5, 1.2); add(hl, x, 0, ZF - .1, bus); hl.target.position.set(x * 1.5, -.5, ZF - 15); bus.add(hl.target); }
  // lit windows seen from outside (the forest stop) and a cold moon over the forest
  for (const s of [-1, 1]) for (let z = ZF + .55; z < ZB; z += 1.1) { const w = new THREE.Mesh(new THREE.PlaneGeometry(1.0, .85), glowMat(z < 1.2 ? 0x9fd8b8 : 0x101810, .55));
    w.rotation.y = s * Math.PI / 2; add(w, s * (BW + .03), 1.45, z, bus); w.material.side = THREE.FrontSide; }
  const moon = new THREE.DirectionalLight(0x6a80c0, .6); moon.position.set(8, 12, -4); scene.add(moon);
  // windshield glass + side glass (faint)
  const glass = new THREE.MeshStandardMaterial({color: 0x0a1018, roughness: .05, metalness: .8, transparent: true, opacity: .25});
  for (const s of [-1, 1]) { const g = new THREE.Mesh(new THREE.PlaneGeometry(ZB - ZF, .9), glass); g.rotation.y = -s * Math.PI / 2; add(g, s * (BW + .01), 1.45, 0, bus); }
  // the world: road, ground, streetlamps (town), trees (forest), a bus shelter at the first stop
  const world = new THREE.Group(); scene.add(world);
  const ground = mesh(new THREE.PlaneGeometry(80, 400), mat(0x06080a, {roughness: 1})); ground.rotation.x = -Math.PI / 2; add(ground, 0, -.52, 0, scene);
  const road = mesh(new THREE.PlaneGeometry(7, 400), mat(0x15171a, {roughness: .4, metalness: .2})); road.rotation.x = -Math.PI / 2; add(road, 0, -.51, 0, scene);
  const treeGeo = new THREE.ConeGeometry(1.4, 7, 7), trunkGeo = new THREE.CylinderGeometry(.15, .2, 2, 6);
  const NT = 260, trees = new THREE.InstancedMesh(treeGeo, mat(0x0a1410, {roughness: 1}), NT), trunks = new THREE.InstancedMesh(trunkGeo, mat(0x120c08), NT);
  const tpos = Array.from({length: NT}, () => { const s = rnd() < .5 ? -1 : 1; return [s * (5.5 + rnd() * 22), rnd() * 200 - 100, .8 + rnd() * .7]; });
  scene.add(trees, trunks);
  const lampGeo = new THREE.CylinderGeometry(.06, .08, 6, 8), headGeo = new THREE.BoxGeometry(.5, .12, .25);
  const lamps = Array.from({length: 8}, (_, i) => { const g = new THREE.Group(); g.add(add(mesh(lampGeo, dark), 0, 2.5, 0, g)); g.add(add(new THREE.Mesh(headGeo, glowMat(0xffb050, 2.2)), -.25, 5.5, 0, g)); scene.add(g); return g; });
  const passL = new THREE.PointLight(0xffa040, 0, 9, 1.4), passR = new THREE.PointLight(0xffa040, 0, 9, 1.4); scene.add(passL, passR);
  const shelter = new THREE.Group(); scene.add(shelter);
  shelter.add(add(mesh(new THREE.BoxGeometry(2.6, .08, 1.2), dark), 0, 2.2, 0, shelter));
  for (const z of [-1.2, 1.2]) shelter.add(add(mesh(new THREE.BoxGeometry(.08, 2.2, .08), dark), .5, 1.1, z, shelter));
  shelter.add(add(mesh(new THREE.BoxGeometry(.05, 1.6, 2.4), new THREE.MeshStandardMaterial({color: 0x99aabb, transparent: true, opacity: .2})), .55, 1.2, 0, shelter));
  const shelterLamp = new THREE.PointLight(0xe8f0ff, 0, 6, 1.4); add(shelterLamp, 0, 2.0, 0, shelter);
  const shelterTube = add(new THREE.Mesh(new THREE.BoxGeometry(.06, .04, 1.4), glowMat(0xe8f0ff, 1.5)), 0, 2.14, 0, shelter);
  // ----- people
  const you = person({skin: 0x9a6a48, top: 0x6a2a2a, legs: 0x22283a, hair: 0x120c08, style: "short", hood: true, iris: 0x2a1a10});
  add(you.root, -.45, 0, .5, bus); you.root.rotation.y = Math.PI;
  const phone = new THREE.Group(); you.armR.end.add(phone); phone.position.set(0, -.02, .04); phone.rotation.set(-1.2, 0, 0);
  phone.add(mesh(box(.075, .15, .01, .2), mat(0x111111)));
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(.066, .135), glowMat(0x9fc4ff, 1.2)); screen.position.z = .006; phone.add(screen);
  const phoneLight = new THREE.PointLight(0x9fbfff, 0, 1.2, 2); phoneLight.position.set(0, 0, .12); phone.add(phoneLight);
  const old = person({skin: 0xb08060, top: 0x4a3a2a, legs: 0x2a2620, hair: 0x8a8a86, style: "short", beard: 0xc8c4bc, glasses: true, h: .95, brow: 0xd0d0c8, iris: 0x3a3a3a});
  add(old.root, .85, 0, -.4, bus); old.root.rotation.y = Math.PI;
  const driver = person({skin: 0x7a5034, top: 0x23324e, legs: 0x1a2030, cap: 0x1a2a44, style: "short", iris: 0x1a1a1a, beard: 0x1a1410});
  add(driver.root, -.75, 0, ZF + 1.05, bus); driver.root.rotation.y = Math.PI;
  // the back seats: pale shapes with shining eyes (layer 2 until the end); one of them is the old man again
  const ghosts = [];
  for (const [x, z, k] of [[-.85, 1.4, 0], [.45, 1.4, 1], [-.45, 2.3, 2], [.85, 2.3, 3], [-.85, 3.2, 4], [.45, 4.1, 5], [-.45, 4.4, 6], [0, 5.25, 7], [.85, 5.25, 8]]) {
    const g = k === 1 ? person({skin: 0xb08060, top: 0x4a3a2a, legs: 0x2a2620, hair: 0x8a8a86, beard: 0xc8c4bc, glasses: true, h: .95, brow: 0xd0d0c8, glowEyes: 0xfff0c0})
                      : person({skin: 0x9a9890, top: 0x101012, legs: 0x101012, hair: 0x050505, style: k % 3 ? "short" : "long", glowEyes: 0xfff0c0, h: 1.05});
    add(g.root, x, 0, z, bus); g.root.rotation.y = Math.PI; pose(g, POSES.sit); g.k = k; ghosts.push(g);
    onLayer(g.root, 2);
  }
  const winRefl = new Reflector(new THREE.PlaneGeometry(2.0, .9), {textureWidth: 512, textureHeight: 256, color: 0x6a7480, clipBias: .003});
  winRefl.rotation.y = Math.PI / 2; add(winRefl, -BW + .02, 1.45, 1.0, bus); winRefl.camera.layers.enable(2);
  const puff = canvasTex(128, 128, g => { const gr = g.createRadialGradient(64, 64, 4, 64, 64, 64); gr.addColorStop(0, "rgba(220,230,255,.9)"); gr.addColorStop(1, "rgba(220,230,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); });
  const breath = new THREE.Sprite(new THREE.SpriteMaterial({map: puff, transparent: true, opacity: 0, depthWrite: false})); breath.scale.setScalar(.12);
  add(breath, -.45, 1.33, .82, bus);

  // ----- direction: you [emotion, pose], old man [emotion, pose], driver [emotion]
  const DIR = {
    b1: {you: ["worried", "sitTense"], old: ["sleep", "sitSleep"], drv: ["stern"]},
    b2: {you: ["worried", "sit"]},
    b3: {you: ["worried", "sit"]},
    b4: {you: ["worried", "sitTense"]},
    b5: {you: ["scared", "sitTense"]},
    b6: {you: ["scared", "sitTense"]},
    b7: {you: ["terror", "sitTense"], drv: ["stern"]},
    b8: {you: ["terror", "sitTense"]},
    b9: {you: ["scared", "sitPhone"]}, b10: {you: ["scared", "sitPhone"]}, b11: {you: ["terror", "sitPhone"]},
    b12: {you: ["terror", "sitTense"], old: ["urgent", "sit"]},
    b13: {you: ["terror", "sitTense"], old: ["urgent", "lean"]},
    b14: {you: ["terror", "sitTense"], old: ["urgent", "sit"]},
    b15: {you: ["terror", "sitTense"]},
    b16: {you: ["terror", "sitTense"], drv: ["stern"]},
    b17: {you: ["terror", "sitTense"], old: ["pleading", "reach"]},
  };
  const get = (id, who) => (DIR[id] && DIR[id][who]) || null;
  function last(who, t, dflt) { let d = null; for (const b of c.beats) { if (b.start - .12 > t) break; if (get(b.id, who)) d = get(b.id, who); } return d || dflt; }

  const SHOTS = {
    you_close:     c.track(you, {dist: .62, side: .14, up: .06, fov: 40}),
    bus_wide:      {pos: [.25, 1.8, -4.3], look: [-.1, 1.0, 3], fov: 52, push: .4},
    you_over:      {pos: [-.75, 1.62, 1.35], look: [-.2, 1.1, -3], fov: 50, push: .2},
    stop_doors:    {pos: [0, 1.55, -2.5], look: [1.2, 1.0, -4.8], fov: 52, push: .2},
    bus_dip:       {pos: [-.15, 1.45, -1.3], look: [-.4, 1.15, 2.5], fov: 48, push: .1},
    driver_mirror: {pos: [-.45, 1.45, ZF + .25], look: [-.75, 1.32, ZF + 1.05], fov: 40, push: .05},
    window:        {pos: [-.55, 1.42, -.3], look: [-1.2, 1.38, .95], fov: 46, push: .06},
    phone:         {pos: [-.3, 1.6, .05], look: [-.45, 1.0, .65], fov: 46, push: .05},
    oldman:        {pos: [-.2, 1.42, .4], look: [.8, 1.3, -.4], fov: 44, push: .1},
    oldman_close:  c.track(old, {dist: .85, side: .12, up: .02, fov: 40}),
    neck:          {pos: [-.2, 1.5, 1.55], look: [-.45, 1.3, .5], fov: 42, push: .25},
    forest_stop:   {pos: [3.2, 1.7, -12.5], look: [0, .9, -3], fov: 46, push: .6},
    oldman_out:    {pos: [.5, 1.6, -3.7], look: [2.4, .3, -5.1], fov: 50, push: .15},
    back_seats:    {pos: [0, 1.45, -.9], look: [0, 1.0, 5], fov: 46, push: .3},
    choice:        {pos: [.35, 1.95, -4.2], look: [-.1, 1.0, 3], fov: 50, push: .3},
  };
  // travel: distance driven by time t (stops at the first stop and in the forest)
  const stopA = [B.b4.start - 1.2, B.b5.end + .8], stopB = [B.b15.start - 1.5, 1e9];
  const speed = t => { const v = 11; let k = 1;
    k *= 1 - seg(t, stopA[0], stopA[0] + 1.2) + seg(t, stopA[1], stopA[1] + 1.5);
    k *= 1 - seg(t, stopB[0], stopB[0] + 1.5); return v * clamp(k); };
  const dist = [0]; for (let i = 1; i <= Math.ceil(T.total * 30) + 2; i++) dist.push(dist[i - 1] + speed(i / 30) / 30);
  const D = t => dist[clamp(Math.round(t * 30), 0, dist.length - 1)];
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sv = new THREE.Vector3(), pv = new THREE.Vector3();

  function update(t, cur, prev) {
    const d = D(t), moving = speed(t) / 11, forest = t > B.b9.start;
    // trees and lamps slide past (+z as the bus drives toward -z)
    for (let i = 0; i < NT; i++) { const [x, z0, s] = tpos[i]; const z = ((z0 + d) % 200 + 200) % 200 - 100;
      const show = forest || Math.abs(x) > 14 ? 1 : .001;
      m4.compose(pv.set(x, 3.0 - .52, z), q, sv.set(s * show, s * show, s * show)); trees.setMatrixAt(i, m4);
      m4.compose(pv.set(x, .5 - .52, z), q, sv.set(show, show, show)); trunks.setMatrixAt(i, m4); }
    trees.instanceMatrix.needsUpdate = trunks.instanceMatrix.needsUpdate = true;
    let nearL = 1e9, nearR = 1e9;
    lamps.forEach((g, i) => { const s = i % 2 ? 1 : -1; const z = (((i * 12.5 + d) % 100) + 100) % 100 - 50;
      g.position.set(s * 4.2, -.52, z); g.rotation.y = s > 0 ? Math.PI : 0; g.visible = !forest;
      if (!forest) { if (s < 0 && Math.abs(z) < Math.abs(nearL)) nearL = z; if (s > 0 && Math.abs(z) < Math.abs(nearR)) nearR = z; } });
    passL.position.set(-3.6, 4.5, nearL); passR.position.set(3.6, 4.5, nearR);
    passL.intensity = forest ? 0 : 10; passR.intensity = forest ? 0 : 10;
    const zs = (stopA[0] + 1.2 <= t && t < stopA[1] + 4) ? D(t) - D(stopA[0] + 1.2) : null;
    shelter.visible = zs !== null && t < B.b6.end; if (shelter.visible) shelter.position.set(3.0, -.52, ZF + 1.2 + zs);
    shelterLamp.intensity = noise(t * 8, 5) > .6 ? .4 : 3; shelterTube.material.color.setHex(0xe8f0ff).multiplyScalar(shelterLamp.intensity / 2);
    // the cabin: engine judder, the dip at b5, flicker of the last working strip
    const dip = seg(t, B.b5.start + .1, B.b5.start + .35) * (1 - seg(t, B.b5.start + .5, B.b5.start + 1.6));
    bus.rotation.x = -.035 * dip + .002 * Math.sin(t * 23) * moving; bus.position.y = -.05 * dip + .003 * Math.sin(t * 17) * moving;
    const fl = noise(t * 11, 2) > .78 ? .25 : 1;
    cab[2].intensity = 1.6 * fl * (1 - .6 * lin(t, B.b14.start, B.b19.end)); strips[4].material.color.setHex(0xd8ffe8).multiplyScalar(1.1 * fl);
    // doors: open at the first stop and at the forest stop
    const open = Math.max(seg(t, B.b4.start, B.b4.start + .7) * (1 - seg(t, B.b5.end + .3, B.b5.end + 1.0)), seg(t, B.b17.start - .3, B.b17.start + .4));
    doors.forEach((dd, k) => { dd.rotation.y = (k ? -1 : 1) * 1.3 * open; dd.position.x = BW + .15 * open; });
    doorLight.intensity = 2.5 * open;
    // ----- you
    const u = seg(t, cur.start - .15, cur.start + .35);
    const yd = last("you", cur.start, ["worried", "sit"]), yp = last("you", prev.start, yd);
    pose(you, mixPose(POSES[yp[1]], POSES[yd[1]], u));
    const ye = mixEmo(EMO[yp[0]], EMO[yd[0]], u);
    const ph = ["b9", "b10", "b11"].includes(cur.id);
    if (ph) ye.look = [0, -.6];
    if (cur.id === "b8") ye.look = [-.8, 0];
    if (["b12", "b13"].includes(cur.id)) ye.look = [.7, -.1];
    poseFace(you.face, ye, t, .2);
    you.neck.rotation.y += cur.id === "b8" ? -.5 * u : ["b12", "b13"].includes(cur.id) ? .55 * u : .02 * noise(t, 1);
    you.chest.rotation.x += .012 * Math.sin(t * (yd[0] === "terror" ? 4.4 : 2.2));
    phone.visible = ph; phoneLight.intensity = ph ? .5 : 0;
    // ----- the old man (gone from his seat once he has stepped out)
    const out = t >= B.b17.start - .3;
    const od = last("old", cur.start, ["sleep", "sitSleep"]), op = last("old", prev.start, od);
    if (!out) { add(old.root, .85, 0, -.4, bus); old.root.rotation.y = Math.PI; pose(old, mixPose(POSES[op[1]], POSES[od[1]], u)); }
    else { old.root.position.set(2.2, -.5, ZF + .8); old.root.rotation.y = -Math.PI / 2 - .3; pose(old, POSES.reach); }
    if (!out && ["b12", "b13", "b14"].includes(cur.id)) {        // he turns round in his seat to face you
      const k = seg(t, B.b12.start + .2, B.b12.start + 1.0);
      old.root.rotation.y = lerp(Math.PI, 2 * Math.PI - .96, k); old.root.position.z = -.4 + .12 * k;
      if (od[1] === "lean") { old.chest.rotation.x = .3 * seg(t, B.b13.start - .2, B.b13.start + .4); old.neck.rotation.x = .1; }
    }
    const oe = mixEmo(EMO[op[0]], EMO[od[0]], u);
    oe.talk = Math.max(envAt("oldman", t), envAt("oldman", t - 1 / 30) * .6);
    if (["b12", "b13", "b14"].includes(cur.id)) oe.look = [-.8, 0];
    poseFace(old.face, oe, t, 1.1);
    // ----- the driver
    pose(driver, POSES.drive);
    const de = {...EMO.stern, look: [cur.scene === "driver_mirror" ? .5 : 0, 0]};
    de.talk = Math.max(envAt("driver", t), envAt("driver", t - 1 / 30) * .6);
    poseFace(driver.face, de, t, 2.3);
    driver.neck.rotation.y = cur.scene === "driver_mirror" ? .35 : 0;
    // ----- the back seats: only in the reflection, until the end; their eyes drift
    const shown = t >= B.b17c.start - .2;
    ghosts.forEach(g => { onLayer(g.root, shown ? 0 : 2); g.root.visible = g.k !== 1 || !out || cur.scene === "window";
      g.neck.rotation.y = .15 * noise(t * .3, g.k); g.neck.rotation.z = .2 * Math.sin(g.k * 1.7);
      poseFace(g.face, {...EMO.neutral, wide: 1.1, look: [0, 0]}, t, g.k); });
    winRefl.visible = cur.scene === "window";
    // breath on your neck
    breath.material.opacity = cur.id === "b14" ? .1 * Math.max(0, Math.sin((t - B.b14.start) * 3.2)) : 0;
    breath.scale.setScalar(.05 + .08 * ((t * 1.6) % 1));
    c.camFill.color.setHex(0xa0c8ff); c.camFill.intensity = ["forest_stop"].includes(cur.scene) ? 0 : .35;
  }
  return {SHOTS, update, shake: t => .15};
}
