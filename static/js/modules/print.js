import { apiPost } from './api.js';

export async function mergeAndPrint(trackingNos){
  if(!trackingNos || !trackingNos.length){ alert('请先勾选需要打印的订单'); return; }
  const blob = await apiPost('/api/v1/print/merge', { tracking_nos: trackingNos });
  const url = URL.createObjectURL(blob);
  const iframe = document.createElement('iframe');
  iframe.style.position='fixed'; iframe.style.right='-9999px'; iframe.style.bottom='-9999px';
  iframe.src = url; document.body.appendChild(iframe);
  iframe.onload = ()=>{ try{ iframe.contentWindow.focus(); iframe.contentWindow.print(); }catch(e){} setTimeout(()=>{ URL.revokeObjectURL(url); iframe.remove(); }, 60000); };
}

