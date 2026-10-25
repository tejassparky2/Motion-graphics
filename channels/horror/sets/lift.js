// "Floor 13": an elevator car (x -0.85..0.85, z -0.75..0.75) whose doors open (z = 0.75) onto a dark hallway
// (z 0.78..8). You stand in the car; "Mrs. Gray" stands in the hallway. She lives on layer 1, so the mirror on the
// back wall never shows her. Her feet face backwards (the hidden detail). The drop raises the hallway by 0.5 m.
export async function build(c) {
  const {THREE, scene, mat, basic, glowMat, mesh, box, add, canvasTex, seg, lin, lerp, clamp, noise, person, pose, POSES,
         mixPose, poseFace, EMO, mixEmo, B, word, envAt, beatAt, onLayer, Reflector, rnd} = c;
  scene.fog = new THREE.FogExp2(0x000000, .12);
  const car = new THREE.Group(); scene.add(car);
  const steel = mat(0x8a9098, {metalness: .85, roughness: .32}), steelDark = mat(0x40444a, {metalness: .8, roughness: .4});
  // brushed-steel look: a faint vertical streak texture
  const brushed = canvasTex(256, 256, g => { g.fillStyle = "#9aa0a8"; g.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 400; i++) { g.fillStyle = `rgba(${rnd() < .5 ? 255 : 0},${rnd() < .5 ? 255 : 0},255,${.03 + rnd() * .05})`; g.fillRect(rnd() * 256, 0, 1, 256); } });
  brushed.wrapS = brushed.wrapT = THREE.RepeatWrapping;
  const wallM = new THREE.MeshStandardMaterial({map: brushed, metalness: .75, roughness: .38, color: 0xb0b6be});
  const floorM = mat(0x2a2624, {roughness: .55});
  const floor = mesh(new THREE.PlaneGeometry(1.7, 1.5), floorM); floor.rotation.x = -Math.PI / 2; add(floor, 0, 0, 0, car);
  for (let i = 0; i < 5; i++) add(mesh(new THREE.BoxGeometry(1.7, .004, .02), steelDark, false), 0, .002, -.6 + i * .3, car);
  const ceil = mesh(new THREE.PlaneGeometry(1.7, 1.5), mat(0x30333a)); ceil.rotation.x = Math.PI / 2; add(ceil, 0, 2.4, 0, car);
  const L = mesh(new THREE.PlaneGeometry(1.5, 2.4), wallM); L.rotation.y = Math.PI / 2; add(L, -.85, 1.2, 0, car);
  const R = mesh(new THREE.PlaneGeometry(1.5, 2.4), wallM); R.rotation.y = -Math.PI / 2; add(R, .85, 1.2, 0, car);
  const back = mesh(new THREE.PlaneGeometry(1.7, 2.4), wallM); add(back, 0, 1.2, -.75, car);
  for (const x of [-.6, .6]) add(mesh(new THREE.CylinderGeometry(.018, .018, 1.3, 10), steel), x, .95, -.7, car).rotation.z = Math.PI / 2;
  const rail = add(mesh(new THREE.CylinderGeometry(.018, .018, 1.4, 10), steel), 0, .95, -.7, car); rail.rotation.z = Math.PI / 2;
  // the mirror on the back wall (Reflector: renders the scene again, only while a mirror shot needs it)
  const mirror = new Reflector(new THREE.PlaneGeometry(1.3, 1.0), {textureWidth: 512, textureHeight: 512, color: 0x9aa2a8, clipBias: .003});
  add(mirror, 0, 1.62, -.744, car);
  const mframe = mesh(box(1.36, 1.06, .02, .1), steelDark); add(mframe, 0, 1.62, -.758, car);   // behind the glass
  // front wall with the door opening (x -0.45..0.45, up to 2.1 m)
  for (const s of [-1, 1]) add(mesh(new THREE.BoxGeometry(.4, 2.4, .05), wallM), s * .65, 1.2, .75, car);
  add(mesh(new THREE.BoxGeometry(.9, .3, .05), wallM), 0, 2.25, .75, car);
  const doors = [-1, 1].map(s => { const d = mesh(new THREE.BoxGeometry(.46, 2.1, .03), mat(0x9aa0a8, {metalness: .85, roughness: .28})); add(d, s * .225, 1.05, .72, car); d.userData.s = s; return d; });
  // floor display above the doors (inside), the button panel and the sign
  const disp = canvasTex(256, 128, g => { g.fillStyle = "#050202"; g.fillRect(0, 0, 256, 128); g.fillStyle = "#ff2a1a"; g.shadowColor = "#ff2a1a"; g.shadowBlur = 18;
    g.font = "bold 92px monospace"; g.textAlign = "center"; g.fillText("13", 128, 100); });
  const display = new THREE.Mesh(new THREE.PlaneGeometry(.26, .13), new THREE.MeshBasicMaterial({map: disp, toneMapped: false, color: 0xffffff}));
  display.rotation.y = Math.PI; add(display, 0, 2.24, .72, car);
  const panel = new THREE.Group(); add(panel, .845, 1.2, .45, car); panel.rotation.y = -Math.PI / 2;
  panel.add(mesh(box(.28, .62, .02, .2), steel));
  const btnTex = n => canvasTex(64, 64, g => { g.fillStyle = "#c8ccd2"; g.beginPath(); g.arc(32, 32, 30, 0, 7); g.fill(); g.fillStyle = "#22262c"; g.font = "bold 30px sans-serif"; g.textAlign = "center"; g.fillText(n, 32, 43); });
  const floors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, "B", "G"];
  floors.forEach((n, i) => { const b = new THREE.Mesh(new THREE.CircleGeometry(.028, 20), new THREE.MeshStandardMaterial({map: btnTex(n), metalness: .3, roughness: .4}));
    b.position.set(-.08 + (i % 3) * .08, .24 - Math.floor(i / 3) * .085, .012); panel.add(b); });
  const lit = new THREE.Mesh(new THREE.RingGeometry(.029, .035, 24), glowMat(0xffa040, 2)); lit.position.set(-.08 + 0 * .08, .24 - 4 * .085, .013); panel.add(lit); // nothing to press for 13
  const signTex = canvasTex(512, 300, g => { g.fillStyle = "#e9e3d0"; g.fillRect(0, 0, 512, 300); g.strokeStyle = "#8a1a14"; g.lineWidth = 10; g.strokeRect(8, 8, 496, 284);
    g.fillStyle = "#1a0d0a"; g.textAlign = "center"; g.font = "bold 30px sans-serif"; g.fillText("IF THE DOORS OPEN ON", 256, 70); g.fillText("A FLOOR THAT ISN'T THERE:", 256, 110);
    g.fillStyle = "#a01810"; g.font = "bold 40px sans-serif"; g.fillText("DO NOT STEP OUT.", 256, 180); g.fillText("DO NOT ANSWER.", 256, 235); });
  const sign = new THREE.Mesh(new THREE.PlaneGeometry(.34, .2), new THREE.MeshStandardMaterial({map: signTex, roughness: .7}));
  sign.rotation.y = -Math.PI / 2; add(sign, .846, 1.68, .45, car);
  // lights: a fluorescent panel (dies at f5), a red emergency lamp (on from f5), the phone screen
  const tube = mesh(new THREE.BoxGeometry(1.0, .02, .5), glowMat(0xdfeaff, .9), false); add(tube, 0, 2.39, 0, car);
  const ceilLight = new THREE.PointLight(0xdfe8ff, 4.5, 6, 1.6); add(ceilLight, 0, 2.25, .05, car);
  const emLamp = mesh(new THREE.BoxGeometry(.14, .05, .08), glowMat(0xff2a10, 0), false); add(emLamp, -.6, 2.37, .62, car);
  const em = new THREE.SpotLight(0xff3a1c, 0, 7, .95, .6, 1.4); add(em, -.6, 2.33, .6, car); em.target.position.set(.15, .7, -.2); car.add(em.target);
  em.castShadow = true; em.shadow.mapSize.set(1024, 1024); em.shadow.bias = -.002;
  const em2 = new THREE.PointLight(0xff4a28, 0, 3, 1.6); add(em2, .3, 2.2, -.6, car);         // second lamp at the back (faces the mirror)
  const emLamp2 = mesh(new THREE.BoxGeometry(.14, .05, .08), glowMat(0xff2a10, 0), false); add(emLamp2, .3, 2.37, -.68, car);
  // cold light from the hallway's far window: the second colour against the red
  const moon = new THREE.SpotLight(0x5a78ff, 0, 12, .5, .8, 1.2); add(moon, -.6, 2.3, 7.6, scene); moon.target.position.set(0, 1.2, -.3); scene.add(moon.target);
  const hallWin = new THREE.Mesh(new THREE.PlaneGeometry(.7, 1.0), glowMat(0x4a64c8, .5)); hallWin.rotation.y = Math.PI / 2; add(hallWin, -1.09, 1.5, 7.4, scene);
  // the roof, the cables and the dark shaft above (for the "cable" shot)
  add(mesh(new THREE.BoxGeometry(1.75, .06, 1.55), steelDark), 0, 2.45, 0, car);
  const cables = [-.08, 0, .08].map(x => add(mesh(new THREE.CylinderGeometry(.008, .008, 12, 8), mat(0x6a6a6a, {metalness: .9, roughness: .3})), x, 8.45, 0, car));
  add(mesh(box(.3, .12, .2, .2), steelDark), 0, 2.52, 0, car);
  for (const [x, z, ry] of [[-1.3, 0, Math.PI / 2], [1.3, 0, -Math.PI / 2], [0, -1.2, 0]]) { const w = mesh(new THREE.PlaneGeometry(3, 14), mat(0x15151a, {roughness: 1})); w.rotation.y = ry; add(w, x, 6, z, scene); }
  const shaftLight = new THREE.PointLight(0xffb070, 0, 3, 1.5); add(shaftLight, .5, 3.2, .5, car);
  const fill = new THREE.HemisphereLight(0x5a6a90, 0x100808, .12); scene.add(fill);
  // the hallway (moves up 0.5 m when the car drops)
  const hall = new THREE.Group(); scene.add(hall);
  const hfloorTex = canvasTex(256, 1024, g => { g.fillStyle = "#3a352e"; g.fillRect(0, 0, 256, 1024); for (let y = 0; y < 1024; y += 64) for (let x = 0; x < 256; x += 64) { g.fillStyle = `rgba(0,0,0,${.1 + rnd() * .15})`; g.fillRect(x + 1, y + 1, 62, 62); } });
  const hfloor = mesh(new THREE.PlaneGeometry(2.2, 7.4), new THREE.MeshStandardMaterial({map: hfloorTex, roughness: .5, metalness: .1})); hfloor.rotation.x = -Math.PI / 2; add(hfloor, 0, 0, 4.5, hall);
  const hwall = mat(0x4a463e, {roughness: .9});
  for (const s of [-1, 1]) { const w = mesh(new THREE.PlaneGeometry(7.4, 2.7), hwall); w.rotation.y = -s * Math.PI / 2; add(w, s * 1.1, 1.35, 4.5, hall); }
  const hc = mesh(new THREE.PlaneGeometry(2.2, 7.4), mat(0x22201c)); hc.rotation.x = Math.PI / 2; add(hc, 0, 2.7, 4.5, hall);
  const endW = mesh(new THREE.PlaneGeometry(2.2, 2.7), hwall); endW.rotation.y = Math.PI; add(endW, 0, 1.35, 8.2, hall);
  for (const s of [-1, 1]) add(mesh(new THREE.BoxGeometry(.4, 2.7, .1), hwall), s * .9, 1.35, .8, hall);   // the frame around the shaft door
  add(mesh(new THREE.BoxGeometry(2.2, .6, .1), hwall), 0, 2.4, .8, hall);
  add(mesh(new THREE.BoxGeometry(2.2, 3, .1), mat(0x0a0a0a)), 0, -1.5, .8, hall);   // the shaft wall under the hallway floor (seen after the drop)
  for (const [z, s] of [[2.6, -1], [4.8, 1], [6.6, -1]]) { const d = mesh(box(.06, 2.0, .9, .1), mat(0x3a2a20)); add(d, s * 1.07, 1.0, z, hall);
    const n = new THREE.Mesh(new THREE.PlaneGeometry(.16, .08), new THREE.MeshBasicMaterial({map: canvasTex(64, 32, g => { g.fillStyle = "#b8a878"; g.fillRect(0, 0, 64, 32); g.fillStyle = "#222"; g.font = "bold 20px sans-serif"; g.fillText("13" + String.fromCharCode(48 + Math.round(z)), 6, 24); })}));
    n.rotation.y = -s * Math.PI / 2; add(n, s * 1.03, 1.65, z, hall); }
  const exitTex = canvasTex(128, 48, g => { g.fillStyle = "#300"; g.fillRect(0, 0, 128, 48); g.fillStyle = "#ff3020"; g.font = "bold 34px sans-serif"; g.fillText("EXIT", 24, 37); });
  const exit = new THREE.Mesh(new THREE.PlaneGeometry(.36, .14), new THREE.MeshBasicMaterial({map: exitTex, toneMapped: false})); exit.rotation.y = Math.PI; add(exit, 0, 2.35, 8.1, hall);
  const exitLight = new THREE.PointLight(0xff2010, 1.2, 5, 1.3); add(exitLight, 0, 2.2, 7.8, hall);
  // wet footprints coming up the hallway to the doors
  const wet = new THREE.MeshStandardMaterial({color: 0x0c0a08, roughness: .05, metalness: .5, transparent: true, opacity: .85});
  for (let i = 0; i < 12; i++) { const fp = mesh(new THREE.CircleGeometry(.055, 16), wet, false); fp.scale.set(.75, 1.6, 1); fp.rotation.x = -Math.PI / 2;
    add(fp, (i % 2 ? .12 : -.12) + .03 * Math.sin(i), .003, 7.4 - i * .55, hall); }
  // you
  const you = person({skin: 0xc68a5e, top: 0x2f4a55, legs: 0x26324a, hair: 0x1a120c, style: "short", hood: true, iris: 0x3a2414});
  add(you.root, -.18, 0, -.15, car);
  const phone = new THREE.Group(); you.armR.end.add(phone); phone.position.set(0, -.02, .04); phone.rotation.set(-1.2, 0, 0);
  phone.add(mesh(box(.075, .15, .01, .2), mat(0x111111)));
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(.066, .135), glowMat(0x9fc4ff, 1.2)); screen.position.z = .006; phone.add(screen);
  const phoneLight = new THREE.PointLight(0x9fbfff, 0, 1.2, 2); phoneLight.position.set(0, 0, .12); phone.add(phoneLight);
  // "Mrs. Gray": the thing in the hallway (layer 1: invisible to the mirror)
  const gray = person({skin: 0xd8c0aa, top: 0x5a4a5a, legs: 0x2a2430, hair: 0xb8b8b4, style: "bun", shawl: 0x6a5a6a, skirt: true, glasses: true,
                       backwardFeet: true, iris: 0x2a2a2a, h: .95, brow: 0x9a9a98, lip: 0x8a5a5a});
  const cane = mesh(new THREE.CylinderGeometry(.012, .012, .85, 8), mat(0x3a2414)); gray.armR.end.add(cane); cane.position.y = -.4;
  const shine = [-1, 1].map(s => { const e = new THREE.Mesh(new THREE.CircleGeometry(.008, 10), glowMat(0xfff0c0, 3)); e.position.set(s * .038, .018, .112); gray.head.add(e); return e; });
  add(gray.root, 0, 0, 4.6, hall); gray.root.rotation.y = Math.PI;
  onLayer(gray.root, 1);

  // per line: you [emotion, pose, facing], gray [emotion, pose, place]
  const DIR = {
    f1:  {you: ["worried", "stand", 0]},
    f2:  {you: ["worried", "stand", 0]},
    f3:  {you: ["worried", "stand", .5]},
    f4:  {you: ["scared", "stand", .5]},
    f5:  {you: ["scared", "stand", 0]},
    f6:  {you: ["scared", "back", 0], gray: ["neutral", "cane", "far"]},
    f7:  {you: ["scared", "back", 0], gray: ["neutral", "cane", "far"]},
    f8:  {you: ["scared", "back", 0], gray: ["pleading", "cane", "mid"]},
    f9:  {you: ["terror", "back", 0], gray: ["pleading", "cane", "mid"]},
    f10: {you: ["scared", "phone", 0]}, f11: {you: ["scared", "phone", 0]}, f12: {you: ["terror", "phone", 0]},
    f13: {you: ["scared", "phone", 0]}, f14: {you: ["terror", "phone", 0]},
    f15: {you: ["terror", "back", 0], gray: ["neutral", "stand", "gone"]},   // the hallway is suddenly empty
    f16: {you: ["terror", "cower", Math.PI], gray: ["creepy", "stand", "door"]},
    f17: {you: ["terror", "back", 0], gray: ["creepy", "stand", "door"]},
    f18: {you: ["terror", "cower", 0], gray: ["creepy", "lean", "door"]},
    f19: {you: ["terror", "cower", 0], gray: ["creepy", "reachBoth", "door"]},
    f20: {you: ["terror", "cower", 0], gray: ["creepy", "reach", "door"]},
    f20b: {you: ["terror", "cower", 0], gray: ["creepy", "reach", "door"]},
    f20c: {you: ["terror", "cower", 0], gray: ["creepy", "reach", "door"]},
    f21: {you: ["terror", "cower", 0], gray: ["creepy", "reach", "door"]},
    f22: {you: ["terror", "cower", 0], gray: ["creepy", "reach", "door"]},
  };
  const PLACE = {far: 4.6, mid: 3.0, door: 1.02, gone: 1.02};
  const get = (id, who) => (DIR[id] && DIR[id][who]) || null;
  function last(who, t) { let d = null; for (const b of c.beats) { if (b.start - .12 > t) break; if (get(b.id, who)) d = get(b.id, who); } return d; }

  const SHOTS = {
    you_close: c.track(you, {dist: .62, side: .12, fov: 38}),
    doors:     {pos: [.4, 1.66, -.6], look: [-.05, 1.2, 2.6], fov: 50, push: .25},
    panel:     {pos: [.3, 1.6, .1], look: [.84, 1.5, .5], fov: 48, push: .06},
    you_over:  {pos: [.55, 1.72, .62], look: [-.2, 1.6, -.28], fov: 48, push: .1},
    hall_dark: {pos: [-.1, 1.76, .12], look: [0, 1.4, 4.5], fov: 38, push: .45},
    phone:     {pos: [.26, 1.95, .46], look: [-.15, 1.56, -.12], fov: 46, push: .06},
    mirror:    {pos: [.32, 1.88, .72], look: [-.14, 1.72, -1.5], fov: 34, push: .12},
    reveal:    {pos: [.5, 1.62, -.66], look: [0, 1.5, 1.1], fov: 48, push: .2},
    drop:      {pos: [.5, 1.4, -.66], look: [0, 1.75, 1.1], fov: 50, push: 0},
    reveal_close: {pos: [.15, 1.3, -.25], look: [0, 2.0, 1.0], fov: 42, push: .12},
    cable:     {pos: [.75, 3.7, .95], look: [0, 2.45, 0], fov: 55, push: .15},
    choice:    {pos: [.6, 1.85, -.68], look: [-.05, 1.4, 1.0], fov: 54, push: .15},
  };
  const tDie = word("f5", 2) + .25;   // "The lights die."
  const tTurn = B.f17.start, tDrop = B.f18.start + .1;

  function update(t, cur, prev) {
    // ----- lights: fluorescent with a nervous flicker, then dead; the red emergency lamp takes over
    const flick = t < tDie ? (noise(t * 9, 3) > .72 ? .35 : 1) * (1 - .8 * seg(t, tDie - .4, tDie)) : 0;
    ceilLight.intensity = 4.5 * flick; tube.material.color.setHex(0xdfeaff).multiplyScalar(.9 * flick + .02);
    const emOn = t > tDie + .35 ? (1 - .5 * lin(t, B.f19.start, B.f22.end)) * (noise(t * 13, 9) > .85 ? .6 : 1) : 0;
    em.intensity = 5 * emOn; em2.intensity = 1.6 * emOn; emLamp2.material.color.setHex(0xff2a10).multiplyScalar(2.5 * emOn + .05);
    c.camFill.color.setHex(t < tDie ? 0xdfe6ff : 0xff6a50); c.camFill.intensity = t < tDie ? .9 * flick + .1 : .35;
    moon.intensity = t > tDie ? 6 : 1.5; shaftLight.intensity = cur.scene === "cable" ? 4 : 0; if (cur.scene === "choice") moon.intensity = 3; emLamp.material.color.setHex(0xff2a10).multiplyScalar(2.5 * emOn + .05);
    const ph = ["f10", "f11", "f12", "f13", "f14"].includes(cur.id);
    phoneLight.intensity = ph ? .5 : 0; screen.visible = ph || t < tDie; phone.visible = ph;
    // ----- doors open at f2 (and stay open)
    const op = seg(t, B.f2.start + .1, B.f2.start + 1.6);
    doors.forEach(d => d.position.x = d.userData.s * (.225 + .44 * op));
    // ----- the drop
    const dk = t < tDrop ? 0 : Math.min(1, (t - tDrop) / .18);
    hall.position.y = .5 * dk * dk;
    c.dropShake = t >= tDrop ? Math.max(0, 1 - (t - tDrop) / 1.2) : 0;
    // ----- you
    const yd = last("you", t) || ["worried", "stand", 0], yp = last("you", prev.start) || yd;
    const u = seg(t, cur.start - .15, cur.start + .35);
    pose(you, mixPose(POSES[yp[1]], POSES[yd[1]], u));
    let face = lerp(yp[2], yd[2], u);
    if (cur.id === "f17") face = Math.PI * (1 - seg(t, tTurn, tTurn + .5));    // you turn around
    you.root.rotation.y = face;
    you.root.position.z = yd[1] === "back" || yd[1] === "cower" ? -.3 : -.15;
    if (cur.id === "f16") you.root.position.z = .05;
    const ye = mixEmo(EMO[yp[0]], EMO[yd[0]], u);
    if (ph) ye.look = [0, -.6];
    if (["f6", "f7", "f8", "f15"].includes(cur.id)) ye.look = [.1 * Math.sin(t * .8), .1];
    poseFace(you.face, ye, t, .3);
    const tremble = ["scared", "terror"].includes(yd[0]) ? .004 : 0;
    you.chest.rotation.z += tremble * Math.sin(t * 37); you.neck.rotation.y += .015 * noise(t, 2);
    you.chest.rotation.x += .012 * Math.sin(t * 2.2 * (yd[0] === "terror" ? 2 : 1));       // breathing, faster when terrified
    // ----- Mrs. Gray
    const gd = last("gray", t);
    gray.root.visible = !!gd && gd[2] !== "gone";
    if (gd) {
      const gp = last("gray", prev.start) || gd;
      const placeA = PLACE[gp[2]], placeB = PLACE[gd[2]];
      gray.root.position.z = lerp(placeA, placeB, seg(t, cur.start, cur.start + 1.2));
      pose(gray, mixPose(POSES[gp[1]] || POSES.stand, POSES[gd[1]] || POSES.stand, u));
      if (gd[1] === "lean" || gd[1] === "reach" || gd[1] === "reachBoth") { gray.chest.rotation.x += .25 + .25 * hall.position.y; gray.neck.rotation.x += .35 * hall.position.y / .5; }
      gray.neck.rotation.z = .25 * seg(t, B.f16.start, B.f17.start + .4) + .03 * Math.sin(t * .7);   // the head tilts
      const ge = mixEmo(EMO[gp[0]], EMO[gd[0]], u);
      ge.talk = Math.max(envAt("gray", t), envAt("gray", t - 1 / 30) * .6);
      ge.look = [0, -.2];
      poseFace(gray.face, ge, t + 7, 1.7);
      cane.visible = gd[1] === "cane" || gd[1] === "stand";
      shine.forEach(s => s.visible = t > tDie);
    }
    mirror.visible = cur.scene === "mirror";
  }
  c.dropShake = 0;
  return {SHOTS, update, shake: t => c.dropShake * .9};
}
