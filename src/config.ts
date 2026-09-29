/**
 * ============================================================
 *  EDIT THIS FILE to change the words, colours and photos.
 *  Everything in the video reads from here.
 * ============================================================
 */

export const brand = {
  name: 'Sparky3dcraft',
  // Leave empty ('') to hide. Example: '@sparky3dcraft' or 'sparky3dcraft.com'
  handle: '',
  website: '',
};

export const copy = {
  // Scene 1 – the hook (first 3 seconds decide if people keep watching)
  hookSmall: 'Wait…',
  hookBig: 'is that YOU?',

  // Scene 2 – the feeling
  memoriesA: 'Your best moments…',
  memoriesB: '…are stuck in your camera roll.',

  // Scene 3 – how it works
  step1: 'Send us one photo',
  step2: 'We sculpt your Mini Me',
  // Only switch this on if you really show customers a 3D preview to approve
  // before printing. It is the single strongest trust-builder for this product.
  showPreviewApproval: false,
  step2b: 'You approve the 3D preview',

  // Scene 4 – visual proof of multi-colour printing
  printTitle: 'Printed in real colour',
  printSub: 'on our Snapmaker U1',
  toolTitle: '4 toolheads. 1 per colour.',
  toolSub: 'crisp colour edges – no muddy mixing',

  // Scene 5 – the reveal
  revealTitle: 'Made from YOUR photo',
  callouts: ['your hairstyle', 'your outfit', 'your smile'],
  revealFoot: 'Colour printed in – not painted on',
  proofTitle: 'Real prints from our workshop',

  // Scene 6 – gifting emotion
  giftTitleA: 'A gift that says',
  giftTitleB: '“I see you.”',
  occasions: ['🎂 Birthdays', '💍 Weddings', '🐶 Pet lovers', '❤️ Anniversaries', '🎓 Graduations', '👨‍👩‍👧 Family'],

  // Scene 7 – call to action
  ctaTitle: 'Turn your photo into a Mini Me',
  ctaButton: 'Send us your photo',
  ctaFoot: 'Multi-colour 3D printed on Snapmaker U1',
};

/**
 * REAL PHOTOS = REAL PROOF.
 * Put photos of your finished miniatures in the /public/photos folder and list
 * the file names here, e.g. ['photos/couple.jpg', 'photos/dog.jpg', 'photos/family.jpg'].
 * Up to 3 are shown. When the list is empty the "real prints" scene is skipped.
 */
export const realPhotos: string[] = [];

/** The 4 filaments loaded in the 4 toolheads (T1–T4). */
export const filaments = {
  t1: {name: 'Charcoal', color: '#2F3142'},
  t2: {name: 'Peach', color: '#F4C39C'},
  t3: {name: 'Sunflower', color: '#FFC83D'},
  t4: {name: 'Coral', color: '#FF6B6B'},
};

export const theme = {
  bgTop: '#1B1446',
  bgBottom: '#0C0A24',
  ink: '#FFFFFF',
  muted: '#C9C3F2',
  spark: '#FFC83D',
  coral: '#FF6B6B',
  teal: '#2EC4B6',
  violet: '#8B6CFF',
  headFont: 'Fredoka',
  bodyFont: 'Nunito',
};
