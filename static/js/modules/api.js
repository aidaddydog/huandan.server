export async function apiGet(url){
  const res = await fetch(url);
  if(!res.ok) throw new Error(await res.text());
  return await res.json();
}
export async function apiPost(url, data){
  const res = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data||{})});
  if(!res.ok){
    let txt = ''; try{ txt = await res.text(); }catch(e){}
    throw new Error(txt || '请求失败');
  }
  const ct = res.headers.get('Content-Type') || '';
  if(ct.includes('application/json')) return await res.json();
  return await res.blob();
}
export async function apiUpload(url, formData){
  const res = await fetch(url, {method:'POST', body: formData});
  if(!res.ok){
    let txt = ''; try{ txt = await res.text(); }catch(e){}
    throw new Error(txt || '上传失败');
  }
  return await res.json();
}

