import { apiGet } from '../modules/api.js';
import { mergeAndPrint } from '../modules/print.js';
const tbody = document.querySelector('#orderTbody');
const checkAll = document.querySelector('#checkAll');
const selInfo = document.querySelector('#selInfo');
const bulkAction = document.querySelector('#bulkAction');
const doAction = document.querySelector('#doAction');
const totalInfo = document.querySelector('#totalInfo');
function selectedTrackingNos(){
  const rows = [...tbody.querySelectorAll('tr')];
  return rows.filter(r => r.querySelector('.rowCheck')?.checked).map(r => r.dataset.tracking).filter(Boolean);
}
function refreshSelInfo(){ if(selInfo) selInfo.textContent = `已选 ${selectedTrackingNos().length} 条`; }
async function load(page=1,size=50){
  const j = await apiGet(`/api/v1/orders?page=${page}&size=${size}`);
  const {rows,total} = j.data;
  tbody.innerHTML = rows.map(r => `
    <tr data-order-id="${r.order_id||''}" data-tracking="${r.tracking_no||''}">
      <td><input type="checkbox" class="rowCheck"></td>
      <td><div class="cell-primary">${(r.platform||'').toUpperCase()}</div><div class="cell-sub">${r.shop_name||''}</div></td>
      <td><div class="cell-primary">${r.order_id||''}</div><div class="cell-sub">${r.sku_summary||''}</div></td>
      <td><div class="cell-primary">${r.buyer_id||''}</div><div class="cell-sub">${r.country||''} ${(r.postal_code||'')}</div></td>
      <td><div class="cell-primary">${r.tracking_no||''}${r.transfer_no?(' / '+r.transfer_no):''}</div><div class="cell-sub">${r.channel_name||''}</div></td>
      <td><div class="cell-primary">创建：${r.updated_at||''}</div><div class="cell-sub">打印：${r.printed_at||'—'}</div><div class="cell-sub">发货：${r.shipped_at||'—'}</div></td>
      <td><button class="btn btn--plain btnPrintOne">打印</button></td>
    </tr>
  `).join('');
  totalInfo && (totalInfo.textContent = `共 ${total} 条`);
  refreshSelInfo();
}
checkAll?.addEventListener('change', ()=>{
  tbody.querySelectorAll('.rowCheck').forEach(cb => cb.checked = checkAll.checked);
  refreshSelInfo();
});
tbody?.addEventListener('change', e=>{
  if(e.target.classList.contains('rowCheck')) refreshSelInfo();
});
tbody?.addEventListener('click', e=>{
  if(e.target.classList.contains('btnPrintOne')){
    const tr = e.target.closest('tr'); const no = tr?.dataset.tracking;
    if(no) mergeAndPrint([no]);
  }
});
doAction?.addEventListener('click', ()=>{
  const action = bulkAction.value;
  if(action==='print'){ mergeAndPrint(selectedTrackingNos()); }
  else if(action==='copy'){ const arr = selectedTrackingNos(); if(!arr.length) return alert('请选择'); navigator.clipboard.writeText(arr.join('\n')); alert('已复制运单号'); }
  else alert('TODO：稍后实现');
});
load().catch(console.error);

