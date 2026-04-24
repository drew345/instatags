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
    if (result.forced_tag) {
      const forced = document.createElement("div");
      forced.className = "meta-pill";
      forced.textContent = `Forced: ${result.forced_tag}`;
      meta.appendChild(forced);
    }
    card.appendChild(meta);

    const tagList = document.createElement("div");
    tagList.className = "tag-list";
    result.selected_tags.forEach((tag) => {
      const item = document.createElement("div");
      item.className = "pill tag";
      item.textContent = tag;
      tagList.appendChild(item);
    });
    card.appendChild(tagList);

    const detailGrid = document.createElement("div");
    detailGrid.className = "detail-grid";
    result.selected_details.forEach((detail) => {
      const row = document.createElement("div");
      row.className = "detail-row";
      const headline = document.createElement("strong");
      headline.textContent = detail.tag;
      row.appendChild(headline);
      const line = document.createElement("div");
      const parts = [];
      if (detail.rank) parts.push(`rank ${detail.rank}`);
      if (detail.base_score !== null && detail.base_score !== undefined) parts.push(`base ${detail.base_score}`);
      if (detail.effective_score !== null && detail.effective_score !== undefined) parts.push(`effective ${detail.effective_score}`);
      if (detail.categories && detail.categories.length) parts.push(detail.categories.join(" / "));
      line.className = "muted";
      line.textContent = parts.join(" · ");
      row.appendChild(line);
      detailGrid.appendChild(row);
    });
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
  renderSelections([data]);
  renderQueue(data.queue_head);
  document.getElementById("statusLine").textContent = `Saved queue is currently at iteration ${data.iteration} with ${data.active_deck_size} active tags.`;
}

async function resetQueue() {
  const data = await fetchJson("/api/reset", { method: "POST" });
  renderQueue(data.queue_head);
  document.getElementById("results").innerHTML = "";
  document.getElementById("statusLine").textContent = `Saved queue reset to iteration ${data.iteration} with ${data.active_deck_size} active tags.`;
}

document.getElementById("previewBtn").addEventListener("click", previewIterations);
document.getElementById("nextBtn").addEventListener("click", useNext);
document.getElementById("resetBtn").addEventListener("click", resetQueue);

loadStatus();
