// Direction for the typo skit test (skit_test.py): per line, [emotion, pose] for each character.
export const DIR = {
  s1: {dev: ["annoyed", "point"], claude: ["watch", "idle"], codex: ["hidden"]},
  s2: {dev: ["tired", "rest"], claude: ["eager", "salute"], codex: ["hidden"]},
  s3: {dev: ["tired", "rest"], claude: ["proud", "cheer"], codex: ["hidden"]},
  s4: {dev: ["shocked", "lean"], claude: ["proud", "cheer"], codex: ["hidden"]},
  s5: {dev: ["shocked", "rest"], claude: ["sheepish", "headscratch"], codex: ["hidden"]},
  s6: {dev: ["hopeful", "rest"], claude: ["oops", "idle"], codex: ["eager", "popup"]},
  s7: {dev: ["hopeful", "pray"], claude: ["watch", "idle"], codex: ["eager", "bounce"]},
  s8: {dev: ["tired", "rest"], claude: ["watch", "idle"], codex: ["proud", "bounce"]},
  s9: {dev: ["done", "facepalm"], claude: ["oops", "idle"], codex: ["oops", "idle"]},
};
