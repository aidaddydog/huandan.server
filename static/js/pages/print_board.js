import { apiGet, apiUpload } from '../modules/api.js';

const formImportOrders = document.querySelector('#formImportOrders');
const formImportPdfs = document.querySelector('#formImportPdfs');
const resOrders = document.querySelector('#importOrdersResult');
const resPdfs = document.querySelector('#importPdfsResult');
const btnScan = document.querySelector('#btnScan');
const btnFix = document.querySelector('#btnFix');
const alignResult = document.querySelector('#alignResult');
const btnBuild = document.querySelector('#btnBuild');
const btnList = document.querySelector('#btnList');
const packList = document.querySelector('#packList');
const rollbackVer = document.querySelector('#rollbackVer');
const btnRollback = document.querySelector('#btnRollback');

formImportOrders?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const fd = new FormData(formImportOrders);
  const j = await apiUpload('/api/v1/import/orders', fd);
  resOrders.textContent = JSON.stringify(j, null, 2);
});

formImportPdfs?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const fd = new FormData(formImportPdfs);
  const j = await apiUpload('/api/v1/import/pdfs_zip', fd);
  resPdfs.textContent = JSON.stringify(j, null, 2);
});

btnScan?.addEventListener('click', async ()=>{
  const j = await apiGet('/api/v1/align/scan');
  alignResult.textContent = JSON.stringify(j, null, 2);
});

btnFix?.addEventListener('click', async ()=>{
  const j = await apiUpload('/api/v1/align/fix', new FormData());
  alignResult.textContent = JSON.stringify(j, null, 2);
});

btnBuild?.addEventListener('click', async ()=>{
  const j = await apiUpload('/api/v1/version/build', new FormData());
  alert('已生成版本包：' + (j.version || ''));
});

async function refreshPacks(){
  const j = await apiGet('/api/v1/version/list');
  packList.innerHTML = (j.packs||[]).map(p => `<li>${p.version} — ${p.size} Bytes — <a href="${p.url}" target="_blank">下载</a></li>`).join('');
}
btnList?.addEventListener('click', refreshPacks);
refreshPacks().catch(()=>{});

btnRollback?.addEventListener('click', async ()=>{
  const v = rollbackVer.value.trim();
  if(!v) return alert('请输入版本号，如 20250919-01');
  const fd = new FormData(); fd.append('version', v);
  const res = await fetch('/api/v1/version/rollback?version=' + encodeURIComponent(v), {method:'POST'});
  const j = await res.json();
  alert(JSON.stringify(j));
});

