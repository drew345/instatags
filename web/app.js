let latestTags = [];

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function getControls() {
  const categories = document.getElementById("categories").value.trim();
  const forcedTag = document.getElementById("forcedTag").value.trim();
  return { categories, forcedTag };
}

function buildQuery({ categories, forcedTag, iterations }) {
  const params = new URLSearchParams();
  if (categories) params.set("categories", categories);
  if (forcedTag) params.set("forced_tag", forcedTag);
  if (iterations) params.set("iterations", String(iterations));
  const query = params.toString();
  return query ? `?${query}` : "";
}

function renderQueue(queueHead) {
  const container = document.getElementById("queueHead");
  container.innerHTML = "";
  queueHead.forEach((tag) => {
    const pill = document.createElement("div");
    pill.className = "queue-pill";
    pill.textContent = tag;
    container.appendChild(pill);
  });
}

function renderTagPills(container, tags) {
  container.innerHTML = "";
  tags.forEach((tag) => {
    const item = document.createElement("div");
    item.className = "pill tag";
    item.textContent = tag;
    container.appendChild(item);
  });
}

function renderDetails(container, details) {
  container.innerHTML = "";
  details.forEach((detail) => {
    const row = document.createElement("div");
    row.className = "detail-row";
    const headline = document.createElement("strong");
    headline.textContent = detail.tag;
    row.appendChild(headline);
    const line = document.createElement("div");
    const parts = [];
    if (detail.source === "forced") parts.push("forced");
    if (detail.rank) parts.push(`rank ${detail.rank}`);
    if (detail.categories && detail.categories.length) parts.push(detail.categories.join(" / "));
    line.className = "muted";
    line.textContent = parts.join(" · ");
    row.appendChild(line);
    container.appendChild(row);
  });
}

function renderCurrentSelection(result) {
  latestTags = result.selected_tags || [];
  renderTagPills(document.getElementById("currentTags"), latestTags);
  renderDetails(document.getElementById("currentDetails"), result.selected_details || []);
  document.getElementById("outputStatus").textContent = `Iteration ${result.iteration}`;
  document.getElementById("copyBtn").disabled = latestTags.length === 0;
}

function renderSelections(results) {
  const container = document.getElementById("results");
  container.innerHTML = "";
  results.forEach((result) => {
    const card = document.createElement("article");
    card.className = "result-card";

    const title = document.createElement("h3");
    title.textContent = `Iteration ${result.iteration}`;
    card.appendChild(title);

    const meta = document.createElement("div");
    meta.className = "meta-list";
    const categories = document.createElement("div");
    categories.className = "meta-pill";
    categories.textContent = `Focus: ${(result.categories || []).join(", ") || "none"}`;
    meta.appendChild(categories);
    if (result.forced_tags && result.forced_tags.length) {
      const forced = document.createElement("div");
      forced.className = "meta-pill";
      forced.textContent = `Forced: ${result.forced_tags.join(" ")}`;
      meta.appendChild(forced);
    }
    card.appendChild(meta);

    const tagList = document.createElement("div");
    tagList.className = "tag-list";
    renderTagPills(tagList, result.selected_tags || []);
    card.appendChild(tagList);

    const detailGrid = document.createElement("div");
    detailGrid.className = "detail-grid";
    renderDetails(detailGrid, result.selected_details || []);
    card.appendChild(detailGrid);

    container.appendChild(card);
  });
}

async function loadStatus() {
  const status = await fetchJson("/api/status");
  document.getElementById("statusLine").textContent = `Saved queue is currently at iteration ${status.iteration} with ${status.active_deck_size} active tags.`;
  renderQueue(status.queue_head);
}

async function previewIterations() {
  const controls = getControls();
  const data = await fetchJson(`/api/preview${buildQuery({ ...controls, iterations: 6 })}`);
  renderSelections(data.results);
}

async function useNext() {
  const controls = getControls();
  const data = await fetchJson(`/api/next${buildQuery(controls)}`, { method: "POST" });
  renderCurrentSelection(data);
  renderQueue(data.queue_head);
  document.getElementById("results").innerHTML = "";
  document.getElementById("statusLine").textContent = `Saved queue is currently at iteration ${data.iteration} with ${data.active_deck_size} active tags.`;
}

async function resetQueue() {
  const data = await fetchJson("/api/reset", { method: "POST" });
  latestTags = [];
  document.getElementById("currentTags").innerHTML = "";
  document.getElementById("currentDetails").innerHTML = "";
  document.getElementById("copyBtn").disabled = true;
  document.getElementById("outputStatus").textContent = "No hashtags generated yet.";
  renderQueue(data.queue_head);
  document.getElementById("results").innerHTML = "";
  document.getElementById("statusLine").textContent = `Saved queue reset to iteration ${data.iteration} with ${data.active_deck_size} active tags.`;
}

async function copyTags() {
  if (!latestTags.length) return;
  const text = latestTags.join(" ");
  await navigator.clipboard.writeText(text);
  const button = document.getElementById("copyBtn");
  button.textContent = "Copied";
  window.setTimeout(() => {
    button.textContent = "Copy";
  }, 1200);
}

document.getElementById("previewBtn").addEventListener("click", previewIterations);
document.getElementById("nextBtn").addEventListener("click", useNext);
document.getElementById("resetBtn").addEventListener("click", resetQueue);
document.getElementById("copyBtn").addEventListener("click", copyTags);

loadStatus();
