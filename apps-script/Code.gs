const SPREADSHEET_ID = '1xoEg3HIEAsMlGvIeAGs09ZzcNB32RssaaMc4Vrozs28';
const RANKED_SHEET = 'ranked_tags';
const CURRENT_DECK_SHEET = 'current_deck';
const STATE_SHEET = 'state';
const HISTORY_SHEET = 'history';
const SELECTION_COUNT = 5;
const REFERENCE_DECK_SIZE = 67;
const REFERENCE_SCORE_MIDPOINT = 30;
const REFERENCE_SCORE_SPREAD = 10;

const RANKED_TAGS = [{"rank":1,"tag":"#외국인남자모델","categories":[]},{"rank":2,"tag":"#외국인중년모델","categories":["senior"]},{"rank":3,"tag":"#외국인남자배우","categories":["acting"]},{"rank":4,"tag":"#외국인시니어모델","categories":["senior"]},{"rank":5,"tag":"#외국인모델","categories":[]},{"rank":6,"tag":"#외국인캐스팅","categories":["acting"]},{"rank":7,"tag":"#短剧","categories":["chinese","drama","acting","shortform"]},{"rank":8,"tag":"#외국인중년배우","categories":["acting","drama","senior"]},{"rank":9,"tag":"#외국인배우","categories":["acting","drama"]},{"rank":10,"tag":"#광고모델","categories":["commercial"]},{"rank":11,"tag":"#중년모델","categories":["senior"]},{"rank":12,"tag":"#시니어모델","categories":["senior"]},{"rank":13,"tag":"#중년외국인모델","categories":["senior"]},{"rank":14,"tag":"#외국인모델섭외","categories":[]},{"rank":15,"tag":"#외국인시니어모델섭외","categories":["senior"]},{"rank":16,"tag":"#微短剧","categories":["chinese","drama","acting","shortform"]},{"rank":17,"tag":"#외국인모델에이전시","categories":[]},{"rank":18,"tag":"#촬영문의","categories":["commercial"]},{"rank":19,"tag":"#모델프로필","categories":["commercial"]},{"rank":20,"tag":"#배우프로필","categories":["acting","drama"]},{"rank":21,"tag":"#외국인연기자","categories":["acting","drama"]},{"rank":22,"tag":"#시니어배우","categories":["acting","drama","senior"]},{"rank":23,"tag":"#modelinkorea","categories":[]},{"rank":24,"tag":"#actorinkorea","categories":["acting","drama"]},{"rank":25,"tag":"#竖屏短剧","categories":["chinese","drama","acting","shortform"]},{"rank":26,"tag":"#외국모델","categories":[]},{"rank":27,"tag":"#미국인모델","categories":[]},{"rank":28,"tag":"#남자모델","categories":[]},{"rank":29,"tag":"#남자배우","categories":["acting","drama"]},{"rank":30,"tag":"#외국남자모델","categories":[]},{"rank":31,"tag":"#남자외국인모델","categories":[]},{"rank":32,"tag":"#패션모델","categories":["commercial","lookbook"]},{"rank":33,"tag":"#룩북모델","categories":["commercial","lookbook"]},{"rank":34,"tag":"#外籍演员","categories":["chinese","acting"]},{"rank":35,"tag":"#외국인패션모델","categories":["commercial","lookbook"]},{"rank":36,"tag":"#외국인피팅모델","categories":["commercial","lookbook"]},{"rank":37,"tag":"#룩북촬영","categories":["commercial","lookbook"]},{"rank":38,"tag":"#광고촬영","categories":["commercial"]},{"rank":39,"tag":"#모델촬영","categories":["commercial"]},{"rank":40,"tag":"#외국인모델촬영","categories":["commercial"]},{"rank":41,"tag":"#외국인광고","categories":["commercial"]},{"rank":42,"tag":"#foreignmodel","categories":[]},{"rank":43,"tag":"#外国演员","categories":["chinese","acting"]},{"rank":44,"tag":"#seniormodel","categories":["senior"]},{"rank":45,"tag":"#Seoulmodel","categories":[]},{"rank":46,"tag":"#프리랜서모델","categories":["commercial"]},{"rank":47,"tag":"#freelancemodel","categories":["commercial"]},{"rank":48,"tag":"#외국인실버모델","categories":["senior"]},{"rank":49,"tag":"#시니어외국인모델","categories":["senior"]},{"rank":50,"tag":"#실버모델","categories":["senior"]},{"rank":51,"tag":"#silvermodel","categories":["senior"]},{"rank":52,"tag":"#外国资深演员","categories":["chinese","acting","senior"]},{"rank":53,"tag":"#중년배우","categories":["acting","drama","senior"]},{"rank":54,"tag":"#중년연기자","categories":["acting","drama","senior"]},{"rank":55,"tag":"#드라마","categories":["acting","drama"]},{"rank":56,"tag":"#외국인남자","categories":[]},{"rank":57,"tag":"#외국남자","categories":[]},{"rank":58,"tag":"#남자외국모델","categories":[]},{"rank":59,"tag":"#미국남자","categories":[]},{"rank":60,"tag":"#竖屏剧","categories":["chinese","drama","shortform"]},{"rank":61,"tag":"#외국인중년남자","categories":["senior"]},{"rank":62,"tag":"#외국인할아버지","categories":["senior"]},{"rank":63,"tag":"#할아버지모델","categories":["senior"]},{"rank":64,"tag":"#실버외국인","categories":["senior"]},{"rank":65,"tag":"#시니어모델섭외","categories":["senior"]},{"rank":66,"tag":"#서울모델","categories":[]}];
const BAKED_QUEUE = ["#외국인시니어모델","#短剧","#竖屏剧","#외국인남자모델","#외국인캐스팅","#竖屏短剧","#외국인모델","#外国资深演员","#외국인모델에이전시","#modelinkorea","#외국인연기자","#외국인중년배우","#외국인남자배우","#외국인배우","#광고모델","#외국인중년남자","#외국인중년모델","#외국인모델섭외","#시니어모델","#외국인패션모델","#미국남자","#배우프로필","#외국인남자","#중년외국인모델","#微短剧","#외국인피팅모델","#모델프로필","#촬영문의","#중년연기자","#외국남자모델","#중년모델","#시니어배우","#룩북촬영","#外国演员","#패션모델","#외국인시니어모델섭외","#룩북모델","#남자외국모델","#silvermodel","#시니어외국인모델","#미국인모델","#외국모델","#남자배우","#actorinkorea","#외국남자","#남자외국인모델","#프리랜서모델","#seniormodel","#드라마","#외국인할아버지","#남자모델","#foreignmodel","#실버모델","#할아버지모델","#외국인실버모델","#실버외국인","#外籍演员","#외국인모델촬영","#중년배우","#광고촬영","#시니어모델섭외","#서울모델","#freelancemodel","#외국인광고","#Seoulmodel","#모델촬영"];

function doGet() {
  ensureInitialized();
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('instatags')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function setupSpreadsheet() {
  const ss = getSpreadsheet();
  writeRankedTags(ss);
  writeState(ss, { iteration: 100, queue: BAKED_QUEUE.slice() });
  setupHistory(ss);
  removeBlankDefaultSheet(ss);
  return getStatus();
}

function getStatus() {
  ensureInitialized();
  const state = readState();
  return {
    iteration: state.iteration,
    activeDeckSize: RANKED_TAGS.length,
    queueHead: state.queue.slice(0, 12)
  };
}

function generateNext(categoriesText, forcedTag) {
  ensureInitialized();
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const state = readState();
    const iteration = state.iteration + 1;
    const result = selectTags(state.queue, parseCategories(categoriesText), normalizeForcedTag(forcedTag));
    const newQueue = applyCooldown(state.queue, result.selectedTags);
    writeState(getSpreadsheet(), { iteration: iteration, queue: newQueue });
    appendHistory(iteration, result.selectedTags);
    return {
      iteration: iteration,
      selectedTags: result.selectedTags,
      selectedDetails: result.selectedDetails,
      queueHead: newQueue.slice(0, 12),
      activeDeckSize: RANKED_TAGS.length
    };
  } finally {
    lock.releaseLock();
  }
}

function previewNext(iterations, categoriesText, forcedTag) {
  ensureInitialized();
  const count = Math.max(1, Math.min(Number(iterations) || 6, 12));
  const categories = parseCategories(categoriesText);
  const normalizedForcedTag = normalizeForcedTag(forcedTag);
  const state = readState();
  let queue = state.queue.slice();
  let iteration = state.iteration;
  const results = [];
  for (let i = 0; i < count; i += 1) {
    iteration += 1;
    const result = selectTags(queue, categories, normalizedForcedTag);
    queue = applyCooldown(queue, result.selectedTags);
    results.push({
      iteration: iteration,
      selectedTags: result.selectedTags,
      selectedDetails: result.selectedDetails,
      queueHead: queue.slice(0, 12),
      activeDeckSize: RANKED_TAGS.length
    });
  }
  return results;
}

function resetBakedState() {
  setupSpreadsheet();
  return getStatus();
}

function ensureInitialized() {
  const ss = getSpreadsheet();
  getOrCreateSheet(ss, RANKED_SHEET);
  getOrCreateSheet(ss, CURRENT_DECK_SHEET);
  const stateSheet = getOrCreateSheet(ss, STATE_SHEET);
  setupHistory(ss);
  writeRankedTags(ss);
  if (stateSheet.getLastRow() < 2) {
    writeState(ss, { iteration: 100, queue: BAKED_QUEUE.slice() });
  }
  writeCurrentDeck(ss, readState().queue);
  removeBlankDefaultSheet(ss);
}

function getSpreadsheet() {
  return SpreadsheetApp.openById(SPREADSHEET_ID);
}

function getOrCreateSheet(ss, name) {
  return ss.getSheetByName(name) || ss.insertSheet(name);
}

function writeRankedTags(ss) {
  const sheet = getOrCreateSheet(ss, RANKED_SHEET);
  sheet.clearContents();
  const rows = [['rank', 'tag', 'categories']].concat(
    RANKED_TAGS.map(record => [record.rank, record.tag, record.categories.join('|')])
  );
  sheet.getRange(1, 1, rows.length, rows[0].length).setValues(rows);
  sheet.setFrozenRows(1);
}

function setupHistory(ss) {
  const sheet = getOrCreateSheet(ss, HISTORY_SHEET);
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, 4).setValues([['timestamp', 'iteration', 'selected_tags', 'selected_json']]);
    sheet.setFrozenRows(1);
  }
}

function writeState(ss, state) {
  const sheet = getOrCreateSheet(ss, STATE_SHEET);
  sheet.clearContents();
  sheet.getRange(1, 1, 1, 2).setValues([['key', 'value']]);
  sheet.getRange(2, 1, 2, 2).setValues([
    ['iteration', state.iteration],
    ['queue_json', JSON.stringify(normalizeQueue(state.queue))]
  ]);
  sheet.setFrozenRows(1);
  writeCurrentDeck(ss, state.queue);
}

function writeCurrentDeck(ss, queue) {
  const sheet = getOrCreateSheet(ss, CURRENT_DECK_SHEET);
  sheet.clearContents();
  const rows = [['position', 'tag', 'rank', 'categories']].concat(
    normalizeQueue(queue).map((tag, index) => {
      const record = recordByTag(tag);
      return [
        index + 1,
        tag,
        record ? record.rank : '',
        record ? record.categories.join('|') : ''
      ];
    })
  );
  sheet.getRange(1, 1, rows.length, rows[0].length).setValues(rows);
  sheet.setFrozenRows(1);
}

function removeBlankDefaultSheet(ss) {
  const sheet = ss.getSheetByName('Sheet1');
  if (!sheet || ss.getSheets().length <= 1) {
    return;
  }
  if (sheet.getLastRow() === 0 && sheet.getLastColumn() === 0) {
    ss.deleteSheet(sheet);
  }
}

function readState() {
  const sheet = getOrCreateSheet(getSpreadsheet(), STATE_SHEET);
  const values = sheet.getDataRange().getValues();
  const state = { iteration: 100, queue: BAKED_QUEUE.slice() };
  values.slice(1).forEach(row => {
    if (row[0] === 'iteration') {
      state.iteration = Number(row[1]) || 100;
    }
    if (row[0] === 'queue_json' && row[1]) {
      state.queue = JSON.parse(row[1]);
    }
  });
  state.queue = normalizeQueue(state.queue);
  return state;
}

function normalizeQueue(queue) {
  const known = {};
  RANKED_TAGS.forEach(record => known[record.tag] = true);
  const seen = {};
  const normalized = [];
  (Array.isArray(queue) ? queue : []).forEach(tag => {
    if (typeof tag === 'string' && known[tag] && !seen[tag]) {
      normalized.push(tag);
      seen[tag] = true;
    }
  });
  RANKED_TAGS.forEach(record => {
    if (!seen[record.tag]) {
      normalized.push(record.tag);
      seen[record.tag] = true;
    }
  });
  return normalized;
}

function appendHistory(iteration, selectedTags) {
  const sheet = getOrCreateSheet(getSpreadsheet(), HISTORY_SHEET);
  sheet.appendRow([new Date(), iteration, selectedTags.join(' '), JSON.stringify(selectedTags)]);
}

function selectTags(queue, categories, forcedTag) {
  const scoredQueue = scoreQueue(queue, categories);
  const selected = [];
  const selectedDetails = [];
  if (forcedTag) {
    selected.push(forcedTag);
    selectedDetails.push({
      tag: forcedTag,
      source: 'forced',
      categories: [],
      rank: null
    });
  }
  scoredQueue.some(detail => {
    if (selected.length >= SELECTION_COUNT) {
      return true;
    }
    if (selected.indexOf(detail.tag) !== -1 || isTooSimilar(detail.tag, selected)) {
      return false;
    }
    selected.push(detail.tag);
    selectedDetails.push(detail);
    return false;
  });
  return sortSelectionByRank(selected.slice(0, SELECTION_COUNT), selectedDetails.slice(0, SELECTION_COUNT));
}

function scoreQueue(queue, categories) {
  const categorySet = {};
  categories.forEach(category => categorySet[category] = true);
  const scored = [];
  queue.forEach((tag, queueIndex) => {
    const record = recordByTag(tag);
    if (!record) {
      return;
    }
    const categoryMatches = record.categories.filter(category => categorySet[category]).length;
    const categoryShift = categoryMatches * 3;
    const priorityPosition = queueIndex - categoryShift;
    const effectiveScore = scoreForRank(record.rank) + (categoryMatches * 0.08);
    scored.push({
      tag: record.tag,
      rank: record.rank,
      source: 'ranked',
      categories: record.categories.slice(),
      priorityPosition: priorityPosition,
      baseScore: round3(scoreForRank(record.rank)),
      effectiveScore: round3(effectiveScore)
    });
  });
  scored.sort((a, b) => {
    if (a.priorityPosition !== b.priorityPosition) {
      return a.priorityPosition - b.priorityPosition;
    }
    if (a.effectiveScore !== b.effectiveScore) {
      return b.effectiveScore - a.effectiveScore;
    }
    return b.baseScore - a.baseScore;
  });
  return scored;
}

function sortSelectionByRank(selectedTags, selectedDetails) {
  const detailsByTag = {};
  selectedDetails.forEach(detail => detailsByTag[detail.tag] = detail);
  const sortedTags = selectedTags.slice().sort((a, b) => rankForTag(a) - rankForTag(b));
  return {
    selectedTags: sortedTags,
    selectedDetails: sortedTags.filter(tag => detailsByTag[tag]).map(tag => detailsByTag[tag])
  };
}

function applyCooldown(queue, selectedTags) {
  const selectedSet = {};
  selectedTags.forEach(tag => selectedSet[tag] = true);
  const remaining = queue.filter(tag => !selectedSet[tag]);
  const cooldowns = selectedTags
    .filter(tag => recordByTag(tag))
    .map((tag, index) => ({ tag: tag, index: index, position: cooldownPosition(tag) }))
    .sort((a, b) => (a.position - b.position) || (a.index - b.index));
  cooldowns.forEach(item => {
    const insertIndex = Math.min(item.position - 1, remaining.length);
    remaining.splice(insertIndex, 0, item.tag);
  });
  return remaining;
}

function cooldownPosition(tag) {
  const range = cooldownRange(tag);
  return range.minimum + Math.floor(Math.random() * (range.maximum - range.minimum + 1));
}

function cooldownRange(tag) {
  const record = recordByTag(tag);
  const score = Math.max(0, Math.min(scoreForRank(record.rank), 1));
  const deckSize = RANKED_TAGS.length;
  const minimum = deckSize * (0.5 - 0.375 * score);
  const maximumUncapped = deckSize * (1.5 - (7 / 6) * score);
  const maximum = Math.min(maximumUncapped, deckSize);
  const minimumPosition = clampCooldownPosition(Math.ceil(minimum));
  let maximumPosition = clampCooldownPosition(Math.floor(maximum));
  if (maximumPosition < minimumPosition) {
    maximumPosition = minimumPosition;
  }
  return { minimum: minimumPosition, maximum: maximumPosition };
}

function clampCooldownPosition(position) {
  return Math.max(1, Math.min(position, RANKED_TAGS.length));
}

function scoreForRank(rank) {
  const scale = RANKED_TAGS.length / REFERENCE_DECK_SIZE;
  const midpoint = REFERENCE_SCORE_MIDPOINT * scale;
  const spread = REFERENCE_SCORE_SPREAD * scale;
  return 1 / (1 + Math.exp((rank - midpoint) / spread));
}

function recordByTag(tag) {
  return RANKED_TAGS.find(record => record.tag === tag) || null;
}

function rankForTag(tag) {
  const record = recordByTag(tag);
  return record ? record.rank : RANKED_TAGS.length + 1;
}

function isTooSimilar(candidateTag, selectedTags) {
  const candidateRecord = recordByTag(candidateTag);
  const candidateCategories = candidateRecord ? candidateRecord.categories : [];
  return selectedTags.some(selected => {
    if (candidateTag === selected) {
      return true;
    }
    const selectedRecord = recordByTag(selected);
    if (!selectedRecord) {
      return normalizeTag(candidateTag) === normalizeTag(selected);
    }
    const overlap = candidateCategories.filter(category => selectedRecord.categories.indexOf(category) !== -1);
    return overlap.length >= 4 || normalizeTag(candidateTag) === normalizeTag(selected);
  });
}

function normalizeTag(tag) {
  return String(tag || '').replace(/^#/, '').toLowerCase();
}

function parseCategories(categoriesText) {
  return String(categoriesText || '')
    .split(',')
    .map(category => category.trim().toLowerCase())
    .filter(Boolean);
}

function normalizeForcedTag(forcedTag) {
  const cleaned = String(forcedTag || '').trim();
  if (!cleaned) {
    return null;
  }
  return cleaned.charAt(0) === '#' ? cleaned : '#' + cleaned;
}

function round3(value) {
  return Math.round(value * 1000) / 1000;
}
