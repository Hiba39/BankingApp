// ---------- DATA (illustrative sample) ----------
const DISTRICTS = {
    "District A": { regs: 403, txn: 6290, pen: 68.7, vol: 327.2, branches: ["Bole Branch", "Piassa Branch", "Kazanchis Branch"], share: [0.417, 0.273, 0.310] },
    "District B": { regs: 362, txn: 5480, pen: 65.2, vol: 284.5, branches: ["Mercato Branch", "Arat Kilo Branch", "Other Branches B"], share: [0.400, 0.309, 0.291] },
    "District C": { regs: 300, txn: 4920, pen: 61.8, vol: 241.1, branches: ["Bahir Dar Main", "Gondar City", "Other Branches C"], share: [0.517, 0.317, 0.166] }
};
const BRANCH_SHARE = [0.40, 0.35, 0.25];
const BRANCH_PEN = [2.1, -0.8, -1.3];
const TOTAL_REGS = 1065;

const PERIOD = { "MTD": [1, 12.4], "Today": [0.05, 3.1], "This Week": [0.25, 6.8], "This Month": [1.2, 9.7], "Quarterly": [3, 15.2], "YTD": [9.5, 18.2], "Custom": [1.5, 8.4] };
const SECTOR = { "All Sectors": 1, "Government": 0.15, "NGO": 0.05, "Private Company": 0.60, "SME": 0.12, "Cooperative": 0.05, "Others": 0.03 };
const BANK = { "Conventional": 882 / TOTAL_REGS, "IFB": 183 / TOTAL_REGS };
const MIX = { Retail: 815, Business: 223, Both: 27 };
const SEG_TX = { Retail: 0.45, Business: 0.45, Both: 0.10 };

const TOP = [
    { name: "Sample Business A", type: "Conv.", count: 846, vol: 72.5 },
    { name: "Sample Business B", type: "IFB", count: 633, vol: 61.2 },
    { name: "Sample Business C", type: "Conv.", count: 1120, vol: 55.8 },
    { name: "Sample Business D", type: "Conv.", count: 512, vol: 48.7 },
    { name: "Sample Business E", type: "IFB", count: 475, vol: 42.1 }
];

// ---------- HELPERS ----------
const $ = id => document.getElementById(id);
const fmt = n => Math.round(n).toLocaleString("en-US");
const etb = v => "ETB " + v.toFixed(1) + "M";
const selects = ["period", "district", "branch", "segment", "bank", "sector"];

// ---------- BRANCH DROPDOWN (depends on district) ----------
function fillBranches() {
    const d = $("district").value;
    const list = d === "All Districts" ? [] : DISTRICTS[d].branches;
    $("branch").innerHTML = "";
    ["All Branches", ...list].forEach(name => {
        const o = document.createElement("option");
        o.textContent = name;
        $("branch").appendChild(o);
    });
}

// ---------- MAIN RENDER ----------
function render() {
    const s = {};
    selects.forEach(id => s[id] = $(id).value);

    const [pf, growth] = PERIOD[s.period];
    const sector = SECTOR[s.sector];
    const bank = s.bank === "All" ? 1 : BANK[s.bank];
    const segReg = s.segment === "All Segments" ? 1 : MIX[s.segment] / TOTAL_REGS;
    const segTx = s.segment === "All Segments" ? 1 : SEG_TX[s.segment];

    // share of the bank covered by the chosen district / branch
    let share = 1, pen = 68.7;
    if (s.district !== "All Districts") {
        const d = DISTRICTS[s.district];
        share = d.regs / TOTAL_REGS;
        pen = d.pen;
        if (s.branch !== "All Branches") {
            const i = d.branches.indexOf(s.branch);
            share *= d.share[i];
            pen += BRANCH_PEN[i];
        }
    }
    const tf = share * pf * bank * sector * segTx;     // transaction scale

    // --- registration mix ---
    const ms = share * pf * sector * (s.bank === "All" ? 1 : BANK[s.bank]);
    const mix = {};
    let mixTotal = 0;
    for (const k in MIX) { mix[k] = MIX[k] * ms; mixTotal += mix[k]; }
    const conv = s.bank === "All" ? 882 * share * pf * sector : (s.bank === "Conventional" ? mixTotal : 0);
    const ifb = s.bank === "All" ? 183 * share * pf * sector : (s.bank === "IFB" ? mixTotal : 0);

    // --- KPI cards ---
    const regCount = s.segment === "All Segments" ? mixTotal : mix[s.segment];
    $("kReg").textContent = fmt(regCount);
    $("kRegSub").textContent = "+" + growth + "% vs prior period";
    $("kVol").textContent = etb(327.2 * tf);
    $("kCnt").textContent = fmt(6290 * tf);
    $("kActive").textContent = fmt(277 * tf);
    $("kActiveSub").textContent = pen.toFixed(1) + "% transaction penetration";

    // --- registration bars ---
    for (const k in MIX) {
        $("n" + k).textContent = fmt(mix[k]);
        $("b" + k).style.width = (mixTotal > 0 ? (mix[k] / mixTotal) * 100 : 0) + "%";
    }
    $("nConv").textContent = fmt(conv);
    $("nIfb").textContent = fmt(ifb);

    // --- transaction mix ---
    $("a2aVol").textContent = etb(189.9 * tf);
    $("a2aTx").textContent = fmt(4150 * tf) + " txns";
    $("otherVol").textContent = etb(137.3 * tf);
    $("otherTx").textContent = fmt(2140 * tf) + " txns";
    $("avgVal").textContent = "ETB " + fmt((327.2 * 1e6) / 6290);

    // --- top customers (filtered by banking type) ---
    // (top customers are drawn in renderExtra below)

    // --- district / branch table ---
    const scaleReg = pf * bank * sector * segReg;
    const scaleTx = pf * bank * sector * segTx;
    let units = [];
    if (s.district === "All Districts") {
        units = Object.entries(DISTRICTS).map(([name, d]) => ({ name, regs: d.regs, txn: d.txn, vol: d.vol, pen: d.pen }));
    } else {
        const d = DISTRICTS[s.district];
        d.branches.forEach((b, i) => {
            if (s.branch === "All Branches" || s.branch === b)
                units.push({ name: b, regs: d.regs * d.share[i], txn: d.txn * d.share[i], vol: d.vol * d.share[i], pen: d.pen + BRANCH_PEN[i] });
        });
    }
    $("perfBody").innerHTML = units.map(u => `
        <tr><td>${u.name}</td><td class="r">${fmt(u.regs * scaleReg)}</td>
        <td class="r">${fmt(u.txn * scaleTx)}</td><td class="r">${etb(u.vol * scaleTx)}</td>
        <td class="r">${u.pen.toFixed(1)}%</td></tr>`).join("");
}

// ---------- EVENTS ----------
$("district").addEventListener("change", fillBranches);
selects.forEach(id => $(id).addEventListener("change", render));

$("resetBtn").addEventListener("click", function () {
    selects.forEach(id => $(id).selectedIndex = 0);
    fillBranches();
    render();
});

fillBranches();
render();

// =====================================================
// TABS
// =====================================================
document.querySelectorAll(".tab").forEach(btn => {
    btn.addEventListener("click", function () {
        document.querySelectorAll(".tab").forEach(t => t.classList.toggle("active", t === btn));
        ["viewDash", "viewWeekly"].forEach(id => $(id).hidden = (id !== btn.dataset.view));
    });
});

// =====================================================
// WEEKLY REPORT: date filter + data from the server (database) or data.js
// =====================================================
const SERVICES = ["Bank Transfer", "Other Bank Transfer", "Birr Transfer", "Top-up"];
const DAY = 86400000, START = Date.UTC(2026, 0, 1), MAX_IDX = 190;     // sample data: Jan 01 - Jul 10, 2026
const ix = (y, m, d) => Math.round((Date.UTC(y, m, d) - START) / DAY); // day number (m = 0..11)
const isoIx = s => { const [y, m, d] = s.split("-").map(Number); return ix(y, m - 1, d); };
const dateOf = i => new Date(START + i * DAY);
const dayLabel = i => dateOf(i).toLocaleDateString("en-US", { month: "short", day: "2-digit", timeZone: "UTC" });
const rangeLabel = ([a, b]) => a === b ? dayLabel(a) : dayLabel(a) + " – " + dayLabel(b);

const wInt = v => Math.round(v).toLocaleString("en-US");
const wMoney = v => v.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const wPct = v => (v > 0 ? "+" : "") + v.toFixed(1) + "%";
function compact(v, prefix) {
    const f = (x, s) => prefix + (+x.toFixed(1)) + s;
    if (v >= 1e9) return f(v / 1e9, "B");
    if (v >= 1e6) return f(v / 1e6, "M");
    if (v >= 1e3) return f(v / 1e3, "K");
    return prefix + Math.round(v);
}

function currentFilters() {
    return { district: $("district").value, branch: $("branch").value, segment: $("segment").value,
             bank: $("bank").value, sector: $("sector").value };
}
function selectedUnits() {
    const f = currentFilters(), ok = new Set();
    UNITS.forEach((u, i) => {
        if (f.district !== "All Districts" && u.district !== f.district) return;
        if (f.branch !== "All Branches" && u.branch !== f.branch) return;
        if ((f.segment === "Retail" || f.segment === "Business") && u.segment !== f.segment) return;   // "Both" = all
        if (f.bank !== "All" && u.bank !== f.bank) return;
        if (f.sector !== "All Sectors" && u.sector !== f.sector) return;
        ok.add(i);
    });
    return ok;
}

// ---- date filter: returns 4 ranges [from, to] in day numbers: selected, previous, MTD, YTD ----
function getRanges() {
    const mode = $("dMode").value, y = +$("dYear").value;
    let from, to, pFrom;
    if (mode === "day" && $("dDay").value) { from = to = isoIx($("dDay").value); }
    else if (mode === "month" && $("dMonth").value) {
        const [yy, mm] = $("dMonth").value.split("-").map(Number);
        from = ix(yy, mm - 1, 1); to = ix(yy, mm, 0); pFrom = ix(yy, mm - 2, 1);
    } else if (mode === "quarter") {
        const q = +$("dQuarter").value;
        from = ix(y, (q - 1) * 3, 1); to = ix(y, q * 3, 0); pFrom = ix(y, (q - 2) * 3, 1);
    } else if (mode === "year") {
        from = ix(y, 0, 1); to = ix(y, 12, 0); pFrom = ix(y - 1, 0, 1);
    } else if (mode === "custom" && $("dFrom").value && $("dTo").value) {
        from = isoIx($("dFrom").value); to = isoIx($("dTo").value);
        if (from > to) [from, to] = [to, from];
    } else { to = MAX_IDX; from = to - 6; }                     // "This Week" (also the fallback)
    to = Math.min(to, MAX_IDX);
    if (pFrom === undefined) pFrom = from - (to - from + 1);    // same length, right before
    const e = dateOf(to);
    return [[from, to], [pFrom, from - 1],
            [ix(e.getUTCFullYear(), e.getUTCMonth(), 1), to],   // month to date
            [ix(e.getUTCFullYear(), 0, 1), to]];                // year to date
}

// ---- data: ask the server (database) first, fall back to data.js ----
function weeklyFromLocal(ranges) {
    const ok = selectedUnits(), services = {};
    SERVICES.forEach(n => { if (RECORDS.some(r => r.s === n)) services[n] = ranges.map(() => [0, 0]); });
    RECORDS.forEach(r => {
        if (!ok.has(r.u)) return;
        ranges.forEach(([lo, hi], k) => {
            if (r.d >= lo && r.d <= hi) { services[r.s][k][0] += r.t; services[r.s][k][1] += r.a; }
        });
    });
    let business = 0, retail = 0;
    const cards = { Conventional: [0, 0], IFB: [0, 0] };
    ok.forEach(i => {
        const u = UNITS[i];
        if (u.segment === "Business") business += u.customers; else retail += u.customers;
        cards[u.bank][0] += u.cardAmt; cards[u.bank][1] += u.cardTrans;
    });
    return { services, customers: { business, retail }, cards };
}
async function getWeeklyModel(ranges) {
    try {
        const q = new URLSearchParams({ ...currentFilters(), ranges: ranges.map(r => r.join(":")).join(",") });
        const res = await fetch("/api/weekly?" + q);
        if (!res.ok) throw new Error("API error " + res.status);
        return await res.json();
    } catch (err) {
        console.warn("Using local sample data:", err.message);
        return weeklyFromLocal(ranges);
    }
}

// ---- draw ----
function paintWeekly(m, ranges) {
    $("hd0").textContent = rangeLabel(ranges[0]);
    $("hd1").textContent = "Previous Period (" + rangeLabel(ranges[1]) + ")";
    $("hd2").textContent = "MTD (" + rangeLabel(ranges[2]) + ")";
    $("hd3").textContent = "YTD (" + rangeLabel(ranges[3]) + ")";
    $("wkRange").textContent = rangeLabel(ranges[0]) + ", " + dateOf(ranges[0][1]).getUTCFullYear();
    $("dInfo").textContent = "Showing " + rangeLabel(ranges[0]) + " compared with " + rangeLabel(ranges[1]) +
        ". Sample data covers Jan 01 – Jul 10, 2026.";

    const tot = ranges.map(() => [0, 0]);
    let html = "";
    SERVICES.forEach(name => {
        const row = m.services[name];
        if (!row) { html += `<tr><td>${name}</td><td class="none" colspan="8">No data</td></tr>`; return; }
        html += `<tr><td>${name}</td>` + row.map(([t, a], i) => {
            tot[i][0] += t; tot[i][1] += a;
            return `<td>${wInt(t)}</td><td>${wMoney(a)}</td>`;
        }).join("") + `</tr>`;
    });
    html += `<tr class="total"><td>Total</td>` + tot.map(([t, a]) => `<td>${wInt(t)}</td><td>${wMoney(a)}</td>`).join("") + `</tr>`;
    const varCell = (cur, prev) => prev === 0 ? `<td class="none">–</td>`
        : `<td class="${cur < prev ? "neg" : "pos"}">${wPct((cur - prev) / prev * 100)}</td>`;
    html += `<tr><td>Variance</td>${varCell(tot[0][0], tot[1][0])}${varCell(tot[0][1], tot[1][1])}<td colspan="6"></td></tr>`;
    $("wkBody").innerHTML = html;

    const days = ranges[2][1] - ranges[2][0] + 1;                // days of the month so far
    $("avOn").textContent = "No data";
    $("avVol").textContent = "ETB " + (tot[2][1] / days / 1e6).toFixed(1) + "M";
    $("avCnt").textContent = wInt(tot[2][0] / days);

    $("cTotal").textContent = wInt(m.customers.business + m.customers.retail);
    $("cBiz").textContent = wInt(m.customers.business);
    $("cRet").textContent = wInt(m.customers.retail);
    $("mConvAmt").textContent = compact(m.cards.Conventional[0], "ETB ");
    $("mAlhAmt").textContent = compact(m.cards.IFB[0], "ETB ");
    $("mConvTx").textContent = compact(m.cards.Conventional[1], "");
    $("mAlhTx").textContent = compact(m.cards.IFB[1], "");
}
async function renderWeekly() {
    const ranges = getRanges();
    paintWeekly(await getWeeklyModel(ranges), ranges);
    renderTrend(ranges[0][1]);
}

// ---- events ----
function syncDateControls() {
    const mode = $("dMode").value;
    document.querySelectorAll(".d-opt").forEach(el => el.hidden = !el.dataset.mode.split(" ").includes(mode));
}
["dDay", "dFrom", "dTo"].forEach(id => { $(id).min = "2026-01-01"; $(id).max = "2026-07-10"; });
$("dMonth").min = "2026-01"; $("dMonth").max = "2026-07";
$("dDay").value = $("dTo").value = "2026-07-10"; $("dFrom").value = "2026-07-04"; $("dMonth").value = "2026-07";

$("dMode").addEventListener("change", () => { syncDateControls(); renderWeekly(); });
["dDay", "dMonth", "dQuarter", "dYear", "dFrom", "dTo"].forEach(id => $(id).addEventListener("change", renderWeekly));
selects.forEach(id => $(id).addEventListener("change", renderWeekly));
$("resetBtn").addEventListener("click", () => { $("dMode").selectedIndex = 0; syncDateControls(); renderWeekly(); });
document.querySelectorAll(".tab").forEach(btn => btn.addEventListener("click", () =>
    document.querySelector(".slide").classList.toggle("weekly-on", btn.dataset.view === "viewWeekly")));
renderWeekly();


// =====================================================
// PLAN vs ACTUAL, HIGH ACTIVITY, CUSTOMER DETAIL (sample data)
// =====================================================
const PLAN_DISTRICTS = {
    "District A": { tc: 400, ac: 403, tv: 310.0, av: 327.2 },
    "District B": { tc: 380, ac: 362, tv: 290.0, av: 284.5 },
    "District C": { tc: 320, ac: 300, tv: 250.0, av: 241.1 }
};
// name, district, target customers, actual customers, target volume, actual volume
const PLAN_BRANCHES = [
    ["Bole Branch", "District A", 150, 168, 120.0, 142.5], ["Piassa Branch", "District A", 120, 110, 90.0, 88.2],
    ["Kazanchis Branch", "District A", 130, 125, 100.0, 96.5], ["Mercato Branch", "District B", 160, 145, 140.0, 132.0],
    ["Arat Kilo Branch", "District B", 110, 112, 85.0, 91.4], ["Bahir Dar Main", "District C", 140, 155, 110.0, 124.8],
    ["Gondar City", "District C", 120, 95, 80.0, 68.3]
];
// id, name, contract, sector, district, branch, banking type, access, txn count, volume (M), A2A volume (M)
const CUSTOMERS = [
    ["C000123", "Sample Business A (MOHAD PLC)", "CTR-8801", "Private Company", "District A", "Bole Branch", "Conventional", "Full Access", 846, 72.5, 42.0],
    ["C000482", "Sample Business B (AL-HUDA IMPORT)", "CTR-4412", "SME", "District B", "Mercato Branch", "IFB", "Full Access", 633, 61.2, 35.0],
    ["C000219", "Sample Business C (ETHIO FED GOV)", "CTR-9011", "Government", "District A", "Kazanchis Branch", "Conventional", "View Only", 1120, 55.8, 38.8],
    ["C000774", "Sample Business D (RED CROSS NGO)", "CTR-1102", "NGO", "District C", "Bahir Dar Main", "Conventional", "View Only", 512, 48.7, 28.0],
    ["C000884", "Sample Business E (UNION COOP)", "CTR-3091", "Cooperative", "District B", "Arat Kilo Branch", "IFB", "Full Access", 475, 42.1, 25.1],
    ["C000912", "Sample Business F (NILE FARMS)", "CTR-5521", "Private Company", "District C", "Gondar City", "Conventional", "Full Access", 390, 32.4, 20.0],
    ["C001044", "Sample Business G (PIASSA TRADING)", "CTR-7710", "SME", "District A", "Piassa Branch", "Conventional", "View Only", 280, 28.0, 18.0]
].map(([id, name, contract, sector, district, branch, bank, access, count, vol, a2a]) =>
    ({ id, name, contract, sector, district, branch, bank, access, count, vol, a2a }));

let openDist = "District A";
const statusOf = p => p >= 100 ? ["Plan Achieved", "b-ok"] : p >= 90 ? ["On Track", "b-mid"] : ["Below Target", "b-low"];

function filteredCustomers() {
    const v = id => $(id).value, q = v("search").trim().toLowerCase();
    return CUSTOMERS.filter(c =>
        (v("district") === "All Districts" || c.district === v("district")) &&
        (v("branch") === "All Branches" || c.branch === v("branch")) &&
        (v("sector") === "All Sectors" || c.sector === v("sector")) &&
        (v("bank") === "All" || c.bank === v("bank")) &&
        (v("access") === "All Access Types" || c.access === v("access")) &&
        v("segment") !== "Retail" &&                     // these are all Business customers
        (!q || [c.name, c.id, c.contract].some(t => t.toLowerCase().includes(q))));
}

function planRow(cls, label, r, attr) {
    const p = r.tc ? r.ac / r.tc * 100 : 0, [txt, badge] = statusOf(p);
    const col = p >= 100 ? "#10a66e" : p >= 90 ? "#f59e0b" : "#e11d48";
    return `<tr class="${cls}" ${attr || ""}><td>${label}</td><td class="r">${r.tc}</td><td class="r">${r.ac}</td>
        <td class="r">${p.toFixed(1)}%<span class="bar"><i style="width:${Math.min(p, 100)}%;background:${col}"></i></span></td>
        <td class="r">${r.tv.toFixed(1)}M</td><td class="r">${r.av.toFixed(1)}M</td><td><span class="badge ${badge}">${txt}</span></td></tr>`;
}

function renderPlan() {
    const dSel = $("district").value, bSel = $("branch").value;
    let html = "";
    Object.entries(PLAN_DISTRICTS).forEach(([name, p]) => {
        if (dSel !== "All Districts" && dSel !== name) return;
        const rows = PLAN_BRANCHES.filter(r => r[1] === name).map(([n, , tc, ac, tv, av]) => ({ n, tc, ac, tv, av }));
        // listed branches do not add up to the district total, so the difference is shown as "Other Branches"
        const sum = k => rows.reduce((t, r) => t + r[k], 0);
        const rest = { n: "Other Branches " + name.slice(-1), tc: p.tc - sum("tc"), ac: p.ac - sum("ac"),
                       tv: +(p.tv - sum("tv")).toFixed(1), av: +(p.av - sum("av")).toFixed(1) };
        if (rest.tc > 0) rows.push(rest);
        const open = openDist === name || bSel !== "All Branches";
        html += planRow("dist", (open ? "▾ " : "▸ ") + name, p, `data-d="${name}"`);
        if (open) rows.filter(r => bSel === "All Branches" || r.n === bSel).forEach(r => { html += planRow("br", r.n, r); });
    });
    $("planBody").innerHTML = html;
}

function renderExtra() {
    renderPlan();
    const hv = +$("hvT").value, hc = +$("hcT").value, list = filteredCustomers();

    $("custBody").innerHTML = list.map(c => `<tr><td><b>${c.id}</b></td><td>${c.name}<small>Contract: ${c.contract}</small></td>
        <td>${c.sector}</td><td>${c.district}<small>${c.branch}</small></td>
        <td class="${c.bank === "IFB" ? "ifb" : "conv"}">${c.bank}</td><td>${c.access}</td>
        <td class="r">${fmt(c.count)}</td><td class="r"><b>${c.vol.toFixed(1)}M</b></td><td class="r">${c.a2a.toFixed(1)}M</td>
        <td>${c.vol >= hv ? '<span class="flag f-hv">HV</span>' : ""}${c.count >= hc ? '<span class="flag f-hc">HC</span>' : ""}</td></tr>`).join("")
        || `<tr><td colspan="10">No business customers match the selected filters.</td></tr>`;
    $("custCount").textContent = `Showing ${list.length} of ${CUSTOMERS.length} records`;
    $("hvN").textContent = list.filter(c => c.vol >= hv).length;
    $("hcN").textContent = list.filter(c => c.count >= hc).length;
    $("faN").textContent = list.filter(c => c.access === "Full Access").length;
    $("voN").textContent = list.filter(c => c.access === "View Only").length;

    // top business customers (same filters, scaled by the chosen period)
    const pf = PERIOD[$("period").value][0];
    $("topBody").innerHTML = [...list].sort((a, b) => b.vol - a.vol).slice(0, 5).map((c, i) =>
        `<tr><td>${i + 1}</td><td>${c.name}</td><td class="${c.bank === "IFB" ? "ifb" : "conv"}">${c.bank === "IFB" ? "IFB" : "Conv."}</td>
        <td class="r">${fmt(c.count * pf)}</td><td class="r">${(c.vol * pf).toFixed(1)}M</td></tr>`).join("")
        || `<tr><td colspan="5">No customers match</td></tr>`;
}

$("planBody").addEventListener("click", e => {
    const tr = e.target.closest("tr.dist");
    if (tr) { openDist = openDist === tr.dataset.d ? null : tr.dataset.d; renderPlan(); }
});
selects.forEach(id => $(id).addEventListener("change", renderExtra));
["access"].forEach(id => $(id).addEventListener("change", renderExtra));
["search", "hvT", "hcT"].forEach(id => $(id).addEventListener("input", renderExtra));
$("resetBtn").addEventListener("click", () => { $("access").selectedIndex = 0; $("search").value = ""; renderExtra(); });

$("csvBtn").addEventListener("click", () => {
    const hv = +$("hvT").value, hc = +$("hcT").value;
    const head = ["Customer ID", "Customer Name", "Contract ID", "Sector", "District", "Branch", "Banking Type", "Access Type",
                  "Txn Count", "Txn Volume (ETB M)", "A2A Vol (ETB M)", "Other Bank Vol (ETB M)", "High Vol", "High Count"];
    const rows = filteredCustomers().map(c => [c.id, c.name, c.contract, c.sector, c.district, c.branch, c.bank, c.access,
        c.count, c.vol, c.a2a, (c.vol - c.a2a).toFixed(1), c.vol >= hv ? "Yes" : "No", c.count >= hc ? "Yes" : "No"]);
    const csv = [head, ...rows].map(r => r.map(v => '"' + String(v).replace(/"/g, '""') + '"').join(",")).join("\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
    a.download = "CoopApp_Business_Customers_" + new Date().toISOString().slice(0, 10) + ".csv";
    a.click();
});
$("printBtn").addEventListener("click", () => window.print());

renderExtra();


// =====================================================
// WEEKLY TREND CHART (drawn with SVG, no library)
// =====================================================
function renderTrend(to) {
    const WEEKS = 6, ok = selectedUnits();
    const a2a = Array(WEEKS).fill(0), other = Array(WEEKS).fill(0);

    // put every record into a 7-day bucket; the last bucket ends on the selected end date
    RECORDS.forEach(r => {
        if (!ok.has(r.u)) return;
        const k = WEEKS - 1 - Math.floor((to - r.d) / 7);
        if (k < 0 || k >= WEEKS) return;
        (r.s === "Bank Transfer" ? a2a : other)[k] += r.a / 1e6;
    });

    const W = 640, H = 260, L = 50, R = 16, T = 16, B = 36;
    const top = Math.max(10, Math.ceil(Math.max(...a2a, ...other) / 10) * 10);
    const x = i => L + i * (W - L - R) / (WEEKS - 1);
    const y = v => T + (H - T - B) * (1 - v / top);

    let svg = "";
    for (let g = 0; g <= 4; g++) {                       // grid lines + y labels
        const v = top * g / 4;
        svg += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="#e6ebf1"/>
                <text x="${L - 8}" y="${y(v) + 4}" text-anchor="end" font-size="11" fill="#6b7686">${v.toFixed(0)}</text>`;
    }
    for (let i = 0; i < WEEKS; i++)                      // x labels = last day of each week
        svg += `<text x="${x(i)}" y="${H - 12}" text-anchor="middle" font-size="11" fill="#6b7686">${dayLabel(to - 7 * (WEEKS - 1 - i))}</text>`;
    [[a2a, "#10a66e"], [other, "#7c3aed"]].forEach(([vals, color]) => {
        svg += `<polyline fill="none" stroke="${color}" stroke-width="2.5" points="${vals.map((v, i) => x(i) + "," + y(v)).join(" ")}"/>`;
        vals.forEach((v, i) => { svg += `<circle cx="${x(i)}" cy="${y(v)}" r="4" fill="${color}"><title>${v.toFixed(1)} M ETB</title></circle>`; });
    });
    $("trendSvg").innerHTML = svg;
}
renderTrend(MAX_IDX);