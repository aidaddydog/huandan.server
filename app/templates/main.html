<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>滑动胶囊导航 · 二级固定视角 · 参数化 · 三级页签 · 面单上传（修复与升级）</title>

  <style>
    /* =========================================================
     * 设计系统（全部可调参数）
     * ========================================================= */
    :root{
      /* ===== 页面壳层 / 布局（全局） ===== */
      --maxw:100%;
      --page-bg:#ffffff;
      --page-px:50px;
      --page-pt:20px;
      --page-pb:2px;
      --text:#0f172a;
      --primary:#111827;

      /* ===== 全局字体 ===== */
      --font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
      --font-size-base:10px;
      --line-height-base:1.6;

      /* ===== 顶部 LOGO / 头像 ===== */
      --logo-w:30px;
      --logo-h:30px;
      --logo-radius:12px;
      --logo-bg:#e7e7e9;
      /* LOGO 左边距参数（保留上一版） */
      --logo-ml:15px;

      --avatar-size:30px;
      --avatar-radius:50%;
      --avatar-bg:#ffffff;
      --avatar-border-width:1px;
      --avatar-border-color:#e7e7e9;
      --avatar-mr:15px;

      /* ===== 顶部行间距 ===== */
      --gap:25px;
      --header-mt:0px;
      --header-mb:0px;

      /* ===== 导航卡片（一级轨道） ===== */
      --nav-w:50.666%;
      --rail-bg:#f6f6f6;
      --rail-border-width:0px;
      --rail-border-color:rgba(0,0,0,.06);
      --rail-radius:999px;
      --rail-shadow:0 0 0 rgba(15,23,42,.06);

      /* ===== 一级菜单文字 ===== */
      --l1-font-size:10px;
      --l1-color:#151515;
      --l1-hover:#0f172a;
      --l1-active:#111827;
      --l1-item-px:20px;
      --l1-gap:1px;
      --l1-height:35px;

      /* ===== 胶囊滑块 ===== */
      --pill-bg:#ffdf5d;
      --pill-border-width:0px;
      --pill-border-color:rgba(0,0,0,.10);
      --pill-shadow:0 0 0 rgba(0,0,0,0);
      --pill-radius:999px;
      --pill-minw:60px;
      --pill-height:20px;

      /* ===== 动画 ===== */
      --anim-speed:.25s;
      --anim-ease:cubic-bezier(.22,.61,.36,1);

      /* ===== 二级导航（文本） ===== */
      --l2-font-size:9px;
      --l2-color:#334155;
      --l2-hover:#ea580c;
      --l2-item-py:6px;
      --l2-item-px:4px;
      --l2-item-radius:8px;
      --l2-gap:14px;
      --l2-item-my:5px;

      /* ===== 二级“固定视角区域”（整行） ===== */
      --sub-top-gap:0px;
      --sub-extra:5px;
      --sub-row-bg:transparent;

      /* ===== 宽容时间窗（防回弹） ===== */
      --sub-grace-ms:220;

      /* ===== 三级页签 & 卡片（Chrome 风格） ===== */
      --tab-w:100%;
      --tab-offset-left:calc(var(--logo-w) + var(--gap));
      --tab-gap:0px;
      --tab-font-size:8px;
      --tab-radius:10px;
      --tab-inactive-bg:transparent;
      --tab-active-bg:#f6f6f6;
      --tab-border:transparent;
      --tab-color:#9f9f9f;
      --tab-color-active:#111827;
      --tab-px:20px; --tab-py:3px;
      --tabcard-radius:25px;
      --tabcard-bg:#f6f6f6;
      --tabcard-shadow:0 0 0 rgba(0,0,0,0);
      --tabcard-p:16px;

      /* ========== 筛选卡片 ========== */
      --filter-card-font-family:var(--font-family);
      --filter-card-font-size:5px;
      --filter-card-line-height:1.6;
      --filter-card-bg:#f6f6f6;
      --filter-card-radius:25px;
      --filter-card-px:14px;
      --filter-card-py:14px;
      --filter-card-mt:0px;
      --filter-card-mb:0px;

      /* ---------- 控件族尺寸（统一入口） ---------- */
      --ctl-h:20px;
      --ctl-minw:50px;
      --ctl-px:12px;
      --ctl-font-size:10px;
      --ctl-radius:999px;
      --ctl-border:#d1d5db;
      --ctl-border-width:1px;
      --ctl-bg:#ffffff;
      --ctl-ink:#111827;
      --ctl-placeholder:#9ca3af;

      /* 按钮（独立覆盖） */
      --btn-h:var(--ctl-h);
      --btn-minw:50px;
      --btn-px:16px;
      --btn-font-size:var(--ctl-font-size);
      --btn-gap:8px;
      --btn-border-width:var(--ctl-border-width);
      --btn-radius:var(--ctl-radius);
      --btn-black-bg:#0a0a0a;
      --btn-black-ink:#ffffff;
      --caret-size:12px;

      /* 输入框（独立覆盖） */
      --input-h:var(--ctl-h);
      --input-minw:60px;
      --input-w:60px;
      --input-search-w:160px;
      --input-datetime-w:80px;
      --input-border-width:var(--ctl-border-width);
      --input-radius:var(--ctl-radius);

      /* 选择框（独立覆盖） */
      --select-h:var(--ctl-h);
      --select-minw:50px;
      --select-w:auto;
      --select-border-width:var(--ctl-border-width);
      --select-radius:var(--ctl-radius);

      /* 下拉弹层（menu） */
      --menu-minw:160px;
      --menu-maxh:280px;
      --menu-radius:12px;
      --menu-item-h:36px;
      --menu-item-px:12px;
      --menu-font-size:12px;
      --menu-shadow:0 10px 30px rgba(0,0,0,.08);
      --menu-border-width:1px;
      --menu-border-color:#e5e7eb;

      /* ========== 表格栏（Table Area）参数 ========== */
      --table-wrap-bg:transparent;
      --table-wrap-radius:8px;
      --table-wrap-mt:12px;
      --table-wrap-mb:60px;
      --table-max-h:100%;

      --table-font-family:var(--font-family);
      --table-font-size:9px;
      --table-ink:#111827;

      /* ✅ 新增：表格行背景参数 */
      --table-row-bg:#ffffff;
      --table-head-ink:#6b7280;
      --table-line:#e5e7eb;
      --table-row-hover:#fafafa;
      --table-row-selected:#fff7d1; /* 浅黄色高亮 */

      /* 表头固定（Sticky） */
      --table-head-sticky-top:0px;
      --table-head-bg:var(--page-bg);
      --table-head-shadow:0 1px 0 var(--table-line);

      /* 列宽参数 */
      --col-w-chk:36px;
      --col-w-order:160px;
      --col-w-waybill:200px;
      --col-w-trans:140px;
      --col-w-ship:110px;
      --col-w-file:160px;
      --col-w-status:110px;
      --col-w-created:160px;
      --col-w-op:140px;

      /* ✅ 新增：滚动条参数（宽/高/颜色） */
      --scrollbar-w:8px;              /* 竖向宽度 */
      --scrollbar-h:8px;              /* 横向高度 */
      --scrollbar-thumb:#cbd5e1;      /* 滑块颜色 */
      --scrollbar-thumb-hover:#94a3b8;/* 滑块悬停色 */
      --scrollbar-track:transparent;  /* 轨道颜色 */
      --scrollbar-radius:999px;

      /* ========== 底部操作栏（Footer Bar）参数 ========== */
      --footer-font-family:var(--font-family);
      --footer-font-size:9px;
      --footer-bg:#f6f6f6;
      --footer-ink:#111827;
      --footer-radius:25px;
      --footer-shadow:0 0 0 rgba(0,0,0,0);
      --footer-px:30px;
      --footer-py:10px;
      --footer-gap:12px;
      --footer-bottom:10px;
      --footer-ctl-h:20px;
      --footer-ctl-border-width:0px;
    }

    /* =========================================================
     * 基础结构样式
     * ========================================================= */
    body{ margin:0; background:var(--page-bg); color:#0f172a;
      font-family:var(--font-family); font-size:var(--font-size-base); line-height:var(--line-height-base); }
    .shell{ max-width:var(--maxw); margin:0 auto; padding:var(--page-pt) var(--page-px) var(--page-pb); }

    html, body { height:100%; overflow:hidden; }
    .header, .subrow, .tabrow { background: var(--page-bg); }

    /* 顶部：LOGO / 导航卡片 / 头像 */
    .header{ display:flex; align-items:center; margin:var(--header-mt) 0 var(--header-mb) }
    .logo{ display:block; width:var(--logo-w); height:var(--logo-h); border-radius:var(--logo-radius); background:var(--logo-bg);
      box-shadow:0 1px 2px rgba(0,0,0,.12); flex:0 0 auto; text-decoration:none; margin-left:var(--logo-ml); }
    .header-gap-left{ width:var(--gap) } .header-gap-right{ flex:1 }
    .avatar{
      width:var(--avatar-size); height:var(--avatar-size);
      border-radius:var(--avatar-radius); background:var(--avatar-bg);
      margin-left:var(--gap); margin-right:var(--avatar-mr);
      flex:0 0 auto; border:var(--avatar-border-width) solid var(--avatar-border-color);
    }

    /* 导航卡片（一级轨道） */
    .nav-rail{ position:relative; flex:0 0 var(--nav-w); width:var(--nav-w); background:var(--rail-bg);
      border:var(--rail-border-width) solid var(--rail-border-color); border-radius:var(--rail-radius); box-shadow:var(--rail-shadow);}
    .track{ position:relative; display:flex; align-items:center; gap:var(--l1-gap); height:var(--l1-height); padding:0 14px; overflow:visible; }

    /* 胶囊滑块 */
    .pill{ position:absolute; top:50%; left:0; transform:translate(0,-50%);
      height:var(--pill-height); border-radius:var(--pill-radius); background:var(--pill-bg);
      border:var(--pill-border-width) solid var(--pill-border-color); box-shadow:var(--pill-shadow);
      transition:transform var(--anim-speed) var(--anim-ease), width var(--anim-speed) var(--anim-ease), opacity .18s ease; opacity:0;}

    /* 一级菜单 */
    .link{ position:relative; z-index:1; padding:0 var(--l1-item-px); height:var(--l1-height);
      display:flex; align-items:center; justify-content:center; font-size:var(--l1-font-size);
      color:#334155; text-decoration:none; white-space:nowrap; border-radius:10px; user-select:none; }
    .link:hover{ color:var(--l1-hover) } .link.active{ color:var(--l1-active); font-weight:600 }

    /* 二级整行（固定视角） */
    .subrow{ position:relative; width:100vw; background:var(--sub-row-bg);
      left:50%; right:50%; margin-left:-50vw; margin-right:-50vw; margin-top:var(--sub-top-gap);}
    .subrow-inner{ max-width:var(--maxw); margin:0 auto; padding:0 var(--page-px); display:flex; align-items:center; }
    .subbar-offset{ width:calc(var(--logo-w) + var(--gap)) }
    .subbar{ flex:0 0 var(--nav-w); width:var(--nav-w) }
    .sub-inner{ display:flex; flex-wrap:wrap; align-items:center; gap:var(--l2-gap) }
    .sub{ font-size:var(--l2-font-size); color:var(--l2-color); text-decoration:none; padding:var(--l2-item-py) var(--l2-item-px); border-radius:var(--l2-item-radius); line-height:1.2; margin-top:var(--l2-item-my); margin-bottom:var(--l2-item-my); }
    .sub:hover,.sub.active{ color:var(--l2-hover) }

    /* 三级页签 + 卡片 */
    .tabrow{ margin-top:12px; }
    .tabrow-inner{ max-width:var(--maxw); margin:0 auto; padding:0 var(--page-px); display:flex; }
    .tab-offset{ width:var(--tab-offset-left) } .tab-wrap{ flex:0 0 var(--tab-w); width:var(--tab-w); }
    .tabs{ display:flex; gap:var(--tab-gap); padding-left:20px; position:relative; z-index:2; }
    .tab{ display:inline-flex; align-items:center; justify-content:center; font-size:var(--tab-font-size); color:var(--tab-color);
      background:var(--tab-inactive-bg); border:1px solid var(--tab-border); border-bottom:none;
      padding:var(--tab-py) var(--tab-px); border-top-left-radius:var(--tab-radius); border-top-right-radius:var(--tab-radius);
      text-decoration:none; white-space:nowrap; height:calc(var(--tab-py) * 2 + 1.2em); }
    .tab:hover{ color:#0f172a; } .tab.active{ background:var(--tab-active-bg); color:var(--tab-color-active); position:relative; z-index:3; }
    .tabcard{ background:var(--tabcard-bg); border:1px solid var(--tab-border); border-radius:var(--tabcard-radius);
      box-shadow:var(--tabcard-shadow); padding:var(--tabcard-p); position:relative; z-index:1; margin-top:-1px; }
    .tabcard.no-tabs{ margin-top:0 }
    .tabpanel{ min-height:60px }

    /* ========== 筛选卡片 ========== */
    .toolbar{
      background:var(--filter-card-bg); border-radius:var(--filter-card-radius);
      padding:var(--filter-card-py) var(--filter-card-px);
      margin:var(--filter-card-mt) 0 var(--filter-card-mb);
      display:flex; flex-wrap:wrap; gap:12px; align-items:center;
      font-family:var(--filter-card-font-family); font-size:var(--filter-card-font-size); line-height:var(--filter-card-line-height);
    }
    .toolbar-left{ display:flex; flex-wrap:wrap; gap:12px; align-items:center; }
    .toolbar-actions{ margin-left:auto; display:flex; align-items:center; gap:12px; }

    /* 按钮 */
    .btn{
      height:var(--btn-h); min-width:var(--btn-minw);
      border-radius:var(--btn-radius); border:var(--btn-border-width) solid var(--ctl-border);
      background:var(--ctl-bg); color:var(--ctl-ink); padding:0 var(--btn-px);
      display:inline-flex; align-items:center; gap:var(--btn-gap);
      cursor:pointer; text-decoration:none; user-select:none; font-size:var(--btn-font-size);
    }
    .btn--black{ background:var(--btn-black-bg); color:var(--btn-black-ink); border-color:var(--btn-black-bg); }
    .btn .caret{ font-size:var(--caret-size); opacity:.8 }

    /* 输入框 */
    .input{
      height:var(--input-h); min-width:var(--input-minw); width:var(--input-w);
      border-radius:var(--input-radius); border:var(--input-border-width) solid var(--ctl-border);
      background:var(--ctl-bg); color:var(--ctl-ink); padding:0 var(--ctl-px); font-size:var(--ctl-font-size);
    }
    .input::placeholder{ color:var(--ctl-placeholder) }
    .input--search{ width:var(--input-search-w); }
    .input--dt{ width:var(--input-datetime-w); cursor:pointer; } /* 鼠标指针样式 */

    /* 选择框（用于视觉触发器） */
    .select{
      height:var(--select-h); min-width:var(--select-minw); width:var(--select-w);
      border-radius:var(--select-radius); border:var(--select-border-width) solid var(--ctl-border);
      background:var(--ctl-bg); color:var(--ctl-ink); padding:0 var(--ctl-px); font-size:var(--ctl-font-size); position:relative; z-index:2;
    }

    /* 下拉弹层（通用） */
    .dropdown{ position:relative; }
    .menu{
      position:absolute; top:calc(100% + 6px); left:0; background:#fff;
      border:var(--menu-border-width) solid var(--menu-border-color);
      border-radius:var(--menu-radius); box-shadow:var(--menu-shadow);
      min-width:var(--menu-minw); max-height:var(--menu-maxh); overflow:auto; display:none; z-index:300;
    }
    .menu::-webkit-scrollbar{ width:var(--scrollbar-w); height:var(--scrollbar-h); background:var(--scrollbar-track) }
    .menu::-webkit-scrollbar-thumb{ background:var(--scrollbar-thumb); border-radius:var(--scrollbar-radius) }
    .menu::-webkit-scrollbar-thumb:hover{ background:var(--scrollbar-thumb-hover) }
    .menu a{
      display:block; height:var(--menu-item-h); line-height:var(--menu-item-h);
      padding:0 var(--menu-item-px); color:#111827; text-decoration:none; font-size:var(--menu-font-size);
    }
    .menu a:hover{ background:#f9fafb }
    .dropdown.open .menu{ display:block; }

    .range{ display:inline-flex; align-items:center; gap:8px }

    /* ========== 表格栏（独立容器） ========== */
    .table-wrap{ margin:var(--table-wrap-mt) 0 var(--table-wrap-mb); background:var(--table-wrap-bg); border-radius:var(--table-wrap-radius); }
    .table-scroll{ max-height:var(--table-max-h); overflow-y:auto; overflow-x:hidden; padding-right:8px; }
    .table-scroll::-webkit-scrollbar{ width:var(--scrollbar-w); height:var(--scrollbar-h); background:transparent; }
    .table-scroll::-webkit-scrollbar-thumb{ background-color:var(--scrollbar-thumb); border-radius:var(--scrollbar-radius); }
    .table-scroll::-webkit-scrollbar-thumb:hover{ background:var(--scrollbar-thumb-hover) }
    .table-scroll::-webkit-scrollbar-track{ background:var(--scrollbar-track) }
    .table-scroll{ scrollbar-width:thin; scrollbar-color:var(--scrollbar-thumb) var(--scrollbar-track); }

    .table{ width:100%; border-collapse:collapse; border-spacing:0; background:transparent; font-family:var(--table-font-family); }
    .table th, .table td{ padding:12px 10px; text-align:left; color:var(--table-ink); font-size:var(--table-font-size); border-bottom:1px solid var(--table-line); background:var(--table-row-bg); transition:background .15s ease; }
    .table thead th{
      color:var(--table-head-ink); font-weight:500; background:var(--table-head-bg);
      position:sticky; top:var(--table-head-sticky-top); z-index:1; box-shadow:var(--table-head-shadow);
      white-space:nowrap;
    }
    .table tr:hover td{ background:var(--table-row-hover) }
    .table tr.selected td{ background:var(--table-row-selected) }

    /* 作废行样式：文本删除线 */
    .table tbody tr.voided td{ text-decoration:line-through; color:#9ca3af; }

    /* 复选框样式 */
    .chk{ appearance:none; min-width:18px; min-height:18px; border-radius:6px; border:1px solid #cbd5e1; background:#fff; vertical-align:middle; cursor:pointer; display:inline-block; }
    .chk:indeterminate{ position:relative; background:#fff; border-color:#111827; }
    .chk:indeterminate::after{ content:""; position:absolute; left:50%; top:50%; width:10px; height:2px; background:#111827; transform:translate(-50%,-50%); border-radius:2px; }
    /* 统一尺寸（后定义覆盖） */
    .chk{ width:10px; height:10px; min-width:10px; min-height:10px; border-radius:4px; border:3px solid #e7e7e9; }
    /* 一般复选框选中为黑色，表格行的勾选框（.rowchk）单独浅黄 */
    .chk:checked{ background:#111827; border-color:#111827; box-shadow: inset 0 0 0 3px #fff; }
    .chk.rowchk:checked{ background:#ffdf5d; border-color:#ffdf5d; box-shadow: inset 0 0 0 3px #fff; }

    .op a{ margin-right:8px; color:#111827; text-decoration:none } .op a:hover{ text-decoration:underline }

    /* 列宽 */
    .table .col-chk{    width:var(--col-w-chk) }
    .table .col-order{  width:var(--col-w-order) }
    .table .col-waybill{width:var(--col-w-waybill) }
    .table .col-trans{  width:var(--col-w-trans) }
    .table .col-ship{   width:var(--col-w-ship) }
    .table .col-file{   width:var(--col-w-file) }
    .table .col-status{ width:var(--col-w-status) }
    .table .col-created{width:var(--col-w-created) }
    .table .col-op{     width:var(--col-w-op) }

    /* ========== 底部操作栏（固定） ========== */
    .footer-bar{
      position:fixed; transform:translateX(-50%); left:50%;
      bottom:var(--footer-bottom);
      width:calc(100% - 150px); max-width:calc(var(--maxw));
      background:var(--footer-bg); color:var(--footer-ink);
      border-radius:var(--footer-radius); box-shadow:var(--footer-shadow);
      padding:var(--footer-py) var(--footer-px); z-index:99;
      font-family:var(--footer-font-family); font-size:var(--footer-font-size);
    }
    .footer-bar .inner{ display:flex; align-items:center; gap:var(--footer-gap); flex-wrap:wrap }
    .footer-bar .size{
      height:var(--footer-ctl-h); border-radius:999px; border:var(--footer-ctl-border-width) solid #d1d5db; background:#fff; padding:0 10px
    }
    .footer-bar .pager a{ margin:0 6px; color:#111827; text-decoration:none } .footer-bar .pager a:hover{ text-decoration:underline }
    .footer-bar input[type="number"]{
      width:70px; height:var(--footer-ctl-h); border-radius:999px; border:var(--footer-ctl-border-width) solid #d1d5db; background:#fff; padding:0 10px
    }

    .flex-1{ flex:1 } .link-top{ text-decoration:none; color:#111827; } .link-top:hover{ text-decoration:underline }

    /* 弹窗（通用） */
    .modal{ position:fixed; inset:0; background:rgba(0,0,0,.35); display:none; align-items:center; justify-content:center; z-index:200 }
    .modal .box{ width:min(400px,90vw); background:#fff; border-radius:16px; padding:16px; border:1px solid #e5e7eb; box-shadow:0 10px 40px rgba(0,0,0,.2) }
    .modal textarea{ width:80%; height:240px; border:1px solid #d1d5db; border-radius:10px; padding:10px; font-family:var(--font-family) }
    .modal .row{ display:flex; justify-content:flex-end; gap:10px; margin-top:12px }
    .hidden{ display:none }

    /* z 层级补丁 */
    .tabcard{ z-index:auto; }
    .table thead th{ z-index:0; position:sticky; }
    .dropdown{ position:relative; }
    .menu{ position:absolute; top:calc(100% + 6px); left:0; z-index:300; } /* 盖过表头 */
    .table tbody td{ background:var(--table-row-bg); }

    /* 页脚选择器尺寸对齐 */
    #pageSize.size {
      height:var(--select-h); min-width:var(--select-minw); width:var(--select-w);
      border-radius:var(--select-radius); border:var(--select-border-width) solid var(--ctl-border);
      background:var(--ctl-bg); color:var(--ctl-ink); padding:0 var(--ctl-px); font-size:var(--ctl-font-size); line-height:1;
    }

    #footerBar a{ color:var(--text); text-decoration:none; cursor:pointer; font-weight:500; }
    #footerBar a:hover{ color:var(--primary); }

    /* 跳转页码输入框 */
    #jumpTo{ width:60px; height:15px; font-size:10px; padding:2px 6px; border:1px solid var(--line); border-radius:var(--radius,6px); outline:none; box-sizing:border-box; }
    #jumpTo:focus{ border-color:var(--primary); box-shadow:0 0 3px var(--primary); }
    #jumpTo::-webkit-outer-spin-button, #jumpTo::-webkit-inner-spin-button{ -webkit-appearance:none; margin:0; }
    #jumpTo{ -moz-appearance:textfield; }

    /* 时间两行样式 */
    .time2{ line-height:1.3; }
    .time2 div{ white-space:nowrap; }

    /* 选择计数样式（紧跟“反选”右侧） */
    .sel-counter{ color:#6b7280; font-weight:500; }

    /* 自定义选择框（仅替换下拉弹层为 .menu 风格） */
    .cselect{ position:relative; display:inline-block; }
    .cselect .cs-toggle{
      height:var(--select-h); min-width:var(--select-minw);
      border-radius:var(--select-radius); border:var(--select-border-width) solid var(--ctl-border);
      background:var(--ctl-bg); color:var(--ctl-ink); padding:0 var(--ctl-px);
      font-size:var(--ctl-font-size); display:inline-flex; align-items:center; gap:8px;
      user-select:none; cursor:pointer;
    }
    .cselect.size-like .cs-toggle{ height:var(--footer-ctl-h); border:var(--footer-ctl-border-width) solid #d1d5db; border-radius:999px; padding:0 10px; font-size:var(--footer-font-size); }
    .cselect .menu{ left:0; }
    .cselect.open .menu{ display:block; }
    .cselect .sr-select{ position:absolute; inset:0; width:0; height:0; opacity:0; pointer-events:none; }

    /* ✅ 页脚“上弹”样式 */
    .cselect.dropup .menu{ top:auto; bottom:calc(100% + 6px); }

    /* ✅ 列头排序按钮（沿用上一版） */
    .sort-btn{ border:0; background:none; cursor:pointer; padding:0 4px; font-size:11px; line-height:1; vertical-align:middle; }
    .sort-btn .ind{ display:inline-block; transform:translateY(-1px); }
    .sort-btn.active{ font-weight:700; }

    /* 响应式 */
    @media (max-width:980px){ .track{ overflow:auto hidden; scroll-snap-type:x mandatory } .link{ scroll-snap-align:center } }
    @media (max-width:600px){ .nav-rail{ flex:1 1 auto; width:auto } .subbar{ flex:1 1 auto; width:auto } .subbar-offset{ width:0 } .tab-offset{ width:0 } .tab-wrap{ flex:1 1 auto; width:auto } .footer-bar{ width:calc(100vw - 24px) } }
  </style>
</head>
<body>
  <div class="shell">
    <!-- 顶部：LOGO / 导航卡片 / 头像 -->
    <div class="header">
      <a class="logo" href="/admin" aria-label="仪表盘"></a>
      <div class="header-gap-left" aria-hidden="true"></div>

      <div class="nav-rail" id="navRail" role="navigation" aria-label="主导航（一级）">
        <div class="track" id="navTrack">
          <div class="pill" id="pill" aria-hidden="true"></div>
          <a class="link" data-path="/orders"    href="/orders">订单</a>
          <a class="link" data-path="/products"  href="/products">商品</a>
          <a class="link" data-path="/logistics" href="/logistics">物流</a>
          <a class="link" data-path="/settings"  href="/settings">设置</a>
        </div>
      </div>

      <div class="header-gap-right" aria-hidden="true"></div>
      <div class="avatar" aria-label="头像"></div>
    </div>
  </div>

  <!-- 二级整行 -->
  <div class="subrow" id="subRow" aria-label="次级导航整行">
    <div class="subrow-inner">
      <div class="subbar-offset" aria-hidden="true"></div>
      <div class="subbar"><div class="sub-inner" id="subInner"></div></div>
    </div>
  </div>

  <!-- 第三行：页签 + 筛选卡片 + 表格栏 -->
  <div class="tabrow" id="tabRow" aria-label="三级页签卡片行">
    <div class="tabrow-inner">
      <div class="tab-offset" aria-hidden="true"></div>
      <div class="tab-wrap">
        <div class="tabs" id="tabs"></div>
        <div class="tabcard" id="tabCard">
          <div class="tabpanel" id="tabPanel">请选择二级菜单。</div>
        </div>

        <!-- 表格栏 -->
        <div class="table-wrap hidden" id="tableWrap">
          <div class="table-scroll">
            <table class="table" id="luTable">
              <thead>
                <tr>
                  <th class="col-chk"><input type="checkbox" class="chk" id="chkAll"></th>
                  <th class="col-order">订单号</th>
                  <th class="col-waybill">运单号</th>
                  <th class="col-trans">转单号</th>
                  <th class="col-ship">运输方式</th>
                  <th class="col-file">面单</th>
                  <th class="col-status">状态
                    <button class="sort-btn" id="sortStatus" title="按状态排序"><span class="ind">⇅</span></button>
                  </th>
                  <th class="col-created">时间
                    <button class="sort-btn" id="sortTime" title="按当前“时间字段”排序"><span class="ind">⇅</span></button>
                  </th>
                  <th class="col-op">操作</th>
                </tr>
              </thead>
              <tbody id="luTbody"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 空白占位 -->
  <div class="shell"><div class="content"><h2> </h2><p> </p></div></div>

  <!-- 固定页底操作栏 -->
  <div class="footer-bar hidden" id="footerBar">
    <div class="inner">
      <!-- ✅ 全选/反选分开，仅当前页有效 -->
      <a href="#" id="selAll">全选</a>
      <a href="#" id="selInvert">反选</a>
      <span id="selCounter" class="sel-counter">已选择 0 条</span>

      <label>每页
        <select id="pageSize" class="size">
          <option value="20">20 条</option>
          <option value="50" selected>50 条</option>
          <option value="100">100 条</option>
        </select>
      </label>

      <span id="pageInfo">共 0 条 0/0 页</span>

      <span class="pager">
        <a href="#" id="firstPage">&laquo;</a>
        <a href="#" id="prevPage">&lsaquo;</a>
        <span id="pageNums"></span>
        <a href="#" id="nextPage">&rsaquo;</a>
        <a href="#" id="lastPage">&raquo;</a>
      </span>

      <span>跳转 <input type="number" id="jumpTo" min="1" value="1"> 页</span>

      <span class="flex-1"></span>
      <!-- ✅ 只作用于表格列表容器 -->
      <a class="link-top" href="#" id="goTop">回到顶部 ↑</a>
    </div>
  </div>

  <!-- 批量单号粘贴弹窗 -->
  <div class="modal" id="bulkModal">
    <div class="box">
      <h3 id="bulkTitle" style="margin:0 0 10px;">粘贴批量单号（空格/换行分隔）</h3>
      <textarea id="bulkText" placeholder="例如：OD202501010001&#10;1ZR0R186919389328&#10;TR000001 ..."></textarea>
      <div class="row">
        <button class="btn" id="bulkCancel">取消</button>
        <button class="btn btn--black" id="bulkApply">应用搜索</button>
      </div>
    </div>
  </div>

  <!-- 通用操作弹窗 -->
  <div class="modal" id="opModal">
    <div class="box">
      <h3 id="opTitle" style="margin:0 0 10px;">操作</h3>
      <div id="opContent" style="min-height:80px;color:#374151;">这里显示对应操作的表单/说明（占位）</div>
      <div class="row">
        <button class="btn" id="opCancel">取消</button>
        <button class="btn btn--black" id="opConfirm">确认</button>
      </div>
    </div>
  </div>

  <script>
    /* ========== 行为 / 状态 / 持久化 ========== */
    const USE_REAL_NAV = false;
    const STORAGE_KEY  = 'NAV_STATE_V10';
    const GRACE_MS = (()=>{ const v=parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sub-grace-ms').trim(),10); return Number.isFinite(v)?v:220; })();

    // DOM 根引用
    const track=document.getElementById('navTrack'), pill=document.getElementById('pill');
    const links=[...track.querySelectorAll('.link')];
    const subRow=document.getElementById('subRow'), subInner=document.getElementById('subInner');
    const tabsEl=document.getElementById('tabs'), tabCard=document.getElementById('tabCard'), tabPanel=document.getElementById('tabPanel');
    const tableWrap=document.getElementById('tableWrap'), tbodyEl=document.getElementById('luTbody');
    const footerBar=document.getElementById('footerBar');

    // 页底栏控件
    const pageSizeSel=document.getElementById('pageSize'), pageInfo=document.getElementById('pageInfo'), pageNums=document.getElementById('pageNums');
    const firstPage=document.getElementById('firstPage'), prevPage=document.getElementById('prevPage'), nextPage=document.getElementById('nextPage'), lastPage=document.getElementById('lastPage');
    const jumpTo=document.getElementById('jumpTo');
    const goTop=document.getElementById('goTop');
    const selAll=document.getElementById('selAll'), selInvert=document.getElementById('selInvert');
    const selCounter=document.getElementById('selCounter');

    // 弹窗
    const bulkModal=document.getElementById('bulkModal'), bulkText=document.getElementById('bulkText');
    const bulkCancel=document.getElementById('bulkCancel'), bulkApply=document.getElementById('bulkApply');
    const opModal=document.getElementById('opModal'), opTitle=document.getElementById('opTitle'), opContent=document.getElementById('opContent');
    const opCancel=document.getElementById('opCancel'), opConfirm=document.getElementById('opConfirm');

    // 状态
    let lockedPath=links[0].dataset.path||'/orders';
    let lockedSubHref='';  // 二级
    let lockedTabHref='';  // 三级
    let hoverPath=lockedPath, inSubRow=false, leaveTimer=null;

    /* ✅ 选择状态（跨分页记忆） */
    let selectedIds = new Set();

    /* ✅ 下拉互斥：统一关闭所有 .dropdown/.cselect */
    function closeAllMenus(exceptEl=null){
      document.querySelectorAll('.dropdown.open').forEach(el=>{
        if(el!==exceptEl) el.classList.remove('open');
      });
      document.querySelectorAll('.cselect.open').forEach(el=>{
        if(el!==exceptEl){
          el.classList.remove('open');
          const btn=el.querySelector('.cs-toggle');
          if(btn) btn.setAttribute('aria-expanded','false');
        }
      });
    }
    document.addEventListener('click',(e)=>{
      if(!e.target.closest('.dropdown') && !e.target.closest('.cselect')) closeAllMenus(null);
    });
    document.addEventListener('keydown',(e)=>{ if(e.key==='Escape') closeAllMenus(null); });
    window.addEventListener('scroll', ()=> closeAllMenus(null), true); // 捕获内部滚动，任何滚动关闭

    /* ✅ 将原生 <select> 升级为自定义 .cselect（下拉用 .menu 风格，视觉为选择框） */
    function upgradeSelectToMenu(selectEl, opts={ sizeLike:false, dropUp:false }){
      if(!selectEl || selectEl.dataset.enhanced === '1') return;

      const wrapper = document.createElement('div');
      wrapper.className = 'cselect' + (opts.sizeLike ? ' size-like' : '') + (opts.dropUp ? ' dropup' : '');

      // 触发器按钮
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'cs-toggle';
      btn.setAttribute('aria-haspopup','listbox');
      btn.setAttribute('aria-expanded','false');

      const txtSpan = document.createElement('span'); txtSpan.className = 'cs-text';
      const curOpt = selectEl.options[selectEl.selectedIndex] || null;
      txtSpan.textContent = curOpt ? curOpt.text : '';
      const caret = document.createElement('span'); caret.className = 'caret'; caret.textContent = '▾';
      btn.appendChild(txtSpan); btn.appendChild(caret);

      // 下拉列表：复用 .menu 样式
      const menu = document.createElement('div'); menu.className = 'menu';
      [...selectEl.options].forEach(opt=>{
        const a = document.createElement('a');
        a.href = '#';
        a.dataset.value = opt.value;
        a.textContent = opt.text;
        a.addEventListener('click', (e)=>{
          e.preventDefault();
          selectEl.value = opt.value;
          txtSpan.textContent = opt.text;
          selectEl.dispatchEvent(new Event('change', { bubbles:true }));
          closeAllMenus(null); // 统一关闭（互斥）
        });
        menu.appendChild(a);
      });

      selectEl.classList.add('sr-select'); selectEl.dataset.enhanced = '1';

      selectEl.parentNode.insertBefore(wrapper, selectEl);
      wrapper.appendChild(selectEl); wrapper.appendChild(btn); wrapper.appendChild(menu);

      // 打开/关闭（互斥）
      btn.addEventListener('click', (e)=>{
        e.stopPropagation();
        const willOpen = !wrapper.classList.contains('open');
        closeAllMenus(willOpen?wrapper:null);
        wrapper.classList.toggle('open', willOpen);
        btn.setAttribute('aria-expanded', willOpen?'true':'false');
      });
    }

    /* ==========  二级菜单数据 ========== */
    const SUBMAP={
      '/orders':[
        {text:'预报',href:'/orders/prealert'},
        {text:'订单列表',href:'/orders/list'},
        {text:'面单上传',href:'/orders/label-upload'},
        {text:'订单轨迹',href:'/orders/track'},
        {text:'订单规则',href:'/orders/rules'},
      ],
      '/products':[
        {text:'商品列表',href:'/products/list'},
        {text:'定制规则',href:'/products/custom-rules'},
      ],
      '/logistics':[
        {text:'物流规则',href:'/logistics/rules'},
        {text:'物流渠道',href:'/logistics/channels'},
        {text:'地址管理',href:'/logistics/address'},
      ],
      '/settings':[
        {text:'仓库设置',href:'/settings/warehouse'},
        {text:'服务商授权',href:'/settings/provider-auth'},
        {text:'店铺授权',href:'/settings/shop-auth'},
        {text:'客户端管理',href:'/settings/client'},
        {text:'系统设置',href:'/settings/system'},
      ],
    };

    /* ========== 三级页签数据（仅“预报”有） ========== */
    const TABMAP={
      '/orders/prealert':[
        {key:'pickup',text:'预约取件',href:'/orders/prealert/pickup'},
        {key:'scan',  text:'扫码发货',href:'/orders/prealert/scan'},
        {key:'list',  text:'预报列表',href:'/orders/prealert/list'},
      ],
    };
    const DEFAULT_TAB_BY_SUB={'/orders/prealert':'/orders/prealert/list'};

    /* ========== 工具函数（导航） ========== */
    function movePillToEl(el){
      if(!el) return;
      const left=el.offsetLeft - track.scrollLeft;
      const width=el.offsetWidth;
      const minw=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--pill-minw'))||60;
      pill.style.width=Math.max(minw,width)+'px';
      pill.style.transform=`translate(${left}px,-50%)`;
      pill.style.opacity=1;
    }
    function renderSub(path){
      const list=SUBMAP[path]||[];
      subInner.innerHTML=list.map(i=>`<a class="sub" data-owner="${path}" href="${i.href}">${i.text}</a>`).join('');
      if(lockedSubHref){
        const t=[...subInner.querySelectorAll('.sub')].find(a=>a.getAttribute('href')===lockedSubHref);
        if(t) t.classList.add('active');
      }
      updateSubRowMinHeight();

      if(TABMAP[lockedSubHref]){
        renderTabs(lockedSubHref);
        tabCard.classList.remove('no-tabs');
        tableWrap.classList.add('hidden');
        footerBar.classList.add('hidden');
      }else{
        tabsEl.innerHTML='';
        tabCard.classList.add('no-tabs');
        renderSingleCardAndTable(lockedSubHref);
      }
    }
    function highlightActive(){ links.forEach(a=>a.classList.toggle('active',a.dataset.path===lockedPath)); }
    function saveState(){ try{ localStorage.setItem(STORAGE_KEY, JSON.stringify({lockedPath,lockedSubHref,lockedTabHref,ts:Date.now()})); }catch(e){} }
    function loadState(){
      try{
        const raw=localStorage.getItem(STORAGE_KEY); if(!raw) return;
        const obj=JSON.parse(raw);
        if(obj&&obj.lockedPath&&SUBMAP[obj.lockedPath]){
          lockedPath=obj.lockedPath;
          const okSub=Object.values(SUBMAP).flat().some(s=>s.href===obj.lockedSubHref);
          lockedSubHref=okSub?obj.lockedSubHref:'';
          if(lockedSubHref&&TABMAP[lockedSubHref]){
            const okTab=(TABMAP[lockedSubHref]||[]).some(t=>t.href===obj.lockedTabHref);
            lockedTabHref=okTab?obj.lockedTabHref:(DEFAULT_TAB_BY_SUB[lockedSubHref]||'');
          }else lockedTabHref='';
        }
      }catch(e){}
    }
    function updateSubRowMinHeight(){
      const textH=subInner.getBoundingClientRect().height||0;
      const extra=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--sub-extra'))||5;
      subRow.style.minHeight=(textH+extra)+'px';
    }

    /* ========== 三级页签渲染（仅预报） ========== */
    function renderTabs(subHref){
      const tabsData=TABMAP[subHref]||[];
      if(!tabsData.length){ tabsEl.innerHTML=''; tabPanel.innerHTML=''; return; }
      if(!lockedTabHref || !tabsData.some(t=>t.href===lockedTabHref)){
        lockedTabHref=DEFAULT_TAB_BY_SUB[subHref]||tabsData[0].href;
      }
      tabsEl.innerHTML=tabsData.map(t=>`<a class="tab ${t.href===lockedTabHref?'active':''}" data-sub="${subHref}" href="${t.href}">${t.text}</a>`).join('');
      const activeTab=tabsData.find(t=>t.href===lockedTabHref);
      tabPanel.innerHTML=`
        <div>当前：<strong>${(SUBMAP[lockedPath]||[]).find(s=>s.href===subHref)?.text||''}</strong>
        &nbsp;&rsaquo;&nbsp;<strong>${activeTab?.text||''}</strong></div>
        <div style="margin-top:12px;color:#64748b;">（此处为 <em>${activeTab?.text||''}</em> 的内容占位）</div>
      `;
    }

    /* =========================================
     * 面单上传：筛选卡片 + 表格栏
     * subHref === '/orders/label-upload'
     * ========================================= */
    let masterRows=[], viewRows=[], pageSize=50, pageIndex=1;

    /* ✅ 排序状态：默认按状态（待换单优先） */
    let sortKey='status';            // 'status' | 'time'
    let sortDir='asc';               // 'asc' | 'desc'
    // 新增 '已预报' 为排序项，'已作废' 不作为主状态（作废以 voided 标识）
    const STATUS_ORDER = { '已预报':0, '待换单':1, '待导入面单':2, '待映射订单号':3, '已换单':4 };

    function renderSingleCardAndTable(subHref){
      if(subHref!=='/orders/label-upload'){
        tabPanel.innerHTML='该二级暂无页签内容。';
        tableWrap.classList.add('hidden');
        footerBar.classList.add('hidden');
        return;
      }

      /* --- 筛选卡片（右侧为搜索+批量操作） --- */
      tabPanel.innerHTML=`
        <div class="toolbar" id="luToolbar">
          <div class="toolbar-left">
            <div class="range">
              <select class="select" id="timeField">
                <option value="created">创建时间</option>
                <option value="printed">打印时间</option>
              </select>

              <!-- ✅ 时间框：点击即弹原生选择器（分别独立），禁止键盘输入 -->
              <input type="datetime-local" class="input input--dt" id="startTime">
              <span>—</span>
              <input type="datetime-local" class="input input--dt" id="endTime">

              <div class="dropdown" id="quickDrop">
                <button class="btn" id="quickBtn">快捷时间 <span class="caret">▾</span></button>
                <div class="menu">
                  <a href="#" data-days="1">近 1 天</a>
                  <a href="#" data-days="3">近 3 天</a>
                  <a href="#" data-days="7">近 7 天</a>
                  <a href="#" data-days="15">近 15 天</a>
                  <a href="#" data-days="30">近 30 天</a>
                </div>
              </div>
            </div>

            <select class="select" id="statusSel">
              <option value="">面单状态</option>
              <option>已预报</option>
              <option>待映射订单号</option>
              <option>待导入面单</option>
              <option>待换单</option>
              <option>已换单</option>
              <option>已作废</option>
            </select>
            <select class="select" id="shipSel">
              <option value="">运输方式</option>
              <option>USPS</option>
              <option>JC</option>
            </select>

            <!-- ✅ 新增：重置按钮（外观与“选择框”一致） -->
            <button type="button" id="resetBtn" class="select" title="重置筛选">重置</button>
          </div>

          <div class="toolbar-actions">
            <input class="input input--search" id="kw" placeholder="单号搜索 / 双击批量搜索">
            <button class="btn btn--black" id="searchBtn">搜索</button>

            <div class="dropdown" id="bulkDrop">
              <button class="btn btn--black" id="bulkBtn">批量操作 <span class="caret">▾</span></button>
              <div class="menu">
                <a href="#" data-act="import-label">导入面单</a>
                <a href="#" data-act="import-map">导入单号映射</a>
                <a href="#" data-act="delete">批量删除</a>
                <a href="#" data-act="export-orders">订单导出</a>
                <a href="#" data-act="copy-waybill">批量复制单号</a>
                <!-- 新增三项 -->
                <a href="#" data-act="batch-print">批量打印</a>
                <a href="#" data-act="batch-activate">批量激活</a>
                <a href="#" data-act="batch-void">批量作废</a>
              </div>
            </div>
          </div>
        </div>
      `;

      tableWrap.classList.remove('hidden');
      footerBar.classList.remove('hidden');

      if(!masterRows.length){ masterRows = genDemoRows(120); }
      pageSize=parseInt(pageSizeSel.value,10)||50;
      pageIndex=1;

      bindLabelUploadEvents();
      applyFilters();
      fitTableHeight();
      updateSortBtnsUI();
    }

    // 生成示例数据（增加 '已预报' 状态可能性，voided 默认 false）
    function genDemoRows(n=100){
      const statuses=['已预报','待映射订单号','待导入面单','待换单','已换单'];
      const ships=['USPS','JC',''];
      const now=Date.now(); const rows=[];
      for(let i=1;i<=n;i++){
        const created=new Date(now - Math.floor(Math.random()*60)*86400000 - Math.floor(Math.random()*86400000));
        const printed=Math.random()<0.6 ? new Date(created.getTime()+Math.floor(Math.random()*3)*86400000 + Math.floor(Math.random()*86400000)) : null;
        const pad=(x,len)=>String(x).padStart(len,'0');
        rows.push({
          id:i,
          orderNo:`OD${created.getFullYear()}${pad(created.getMonth()+1,2)}${pad(created.getDate(),2)}${pad(i,4)}`,
          waybill:`1Z${Math.random().toString(36).slice(2,10).toUpperCase()}${Math.floor(Math.random()*1e6)}`,
          transNo:`TR${pad(i,6)}`,
          ship:ships[Math.floor(Math.random()*ships.length)],
          file:`label_${pad(i,4)}.pdf`,
          status:statuses[Math.floor(Math.random()*statuses.length)],
          createdAt:created,
          printedAt:printed,
          voided:false
        });
      }
      return rows;
    }

    // 输入控件用（datetime-local）
    function toLocal(d){
      const p=n=>String(n).padStart(2,'0');
      return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
    }
    function formatDateTime(d){
      if(!(d instanceof Date) || isNaN(d)) return '-';
      const p=n=>String(n).padStart(2,'0');
      return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
    }

    /* 只让表格栏滚动的自适应高度计算 */
    function fitTableHeight(){
      const wrap = document.getElementById('tableWrap');
      if(!wrap || wrap.classList.contains('hidden')) return;
      const scroller = wrap.querySelector('.table-scroll');
      if(!scroller) return;
      const top = scroller.getBoundingClientRect().top;
      const footerTop = footerBar.classList.contains('hidden') ? window.innerHeight : footerBar.getBoundingClientRect().top;
      const h = Math.max(120, Math.floor(footerTop - top - 12));
      scroller.style.maxHeight = h + 'px';
      scroller.style.height    = h + 'px';
    }

    function getCurrentPageRows(){
      const start=(pageIndex-1)*pageSize;
      return viewRows.slice(start, start+pageSize);
    }
    function getSelectedRows(){
      return masterRows.filter(r=>selectedIds.has(r.id));
    }

    async function copyToClipboard(text){
      try{ await navigator.clipboard.writeText(text); return true; }
      catch(e){
        try{
          const ta=document.createElement('textarea'); ta.value=text; document.body.appendChild(ta);
          ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
          return true;
        }catch(e2){ return false; }
      }
    }

    function updateSelCounter(){
      if(selCounter) selCounter.textContent = `已选择 ${selectedIds.size} 条`;
    }

    // 排序
    function sortRows(){
      const tf = document.getElementById('timeField')?.value || 'created'; // 'created' | 'printed'
      viewRows.sort((a,b)=>{
        if(sortKey==='status'){
          const av = STATUS_ORDER.hasOwnProperty(a.status)? STATUS_ORDER[a.status] : 99;
          const bv = STATUS_ORDER.hasOwnProperty(b.status)? STATUS_ORDER[b.status] : 99;
          return (av - bv) * (sortDir==='asc'?1:-1);
        }else if(sortKey==='time'){
          const va = tf==='printed' ? a.printedAt : a.createdAt;
          const vb = tf==='printed' ? b.printedAt : b.createdAt;
          const na = va instanceof Date && !isNaN(va) ? +va : (sortDir==='asc' ? Infinity : -Infinity);
          const nb = vb instanceof Date && !isNaN(vb) ? +vb : (sortDir==='asc' ? Infinity : -Infinity);
          return (na - nb) * (sortDir==='asc'?1:-1);
        }
        return 0;
      });
    }
    function updateSortBtnsUI(){
      const bs=document.getElementById('sortStatus'), bt=document.getElementById('sortTime');
      if(!bs || !bt) return;
      bs.classList.toggle('active', sortKey==='status');
      bt.classList.toggle('active', sortKey==='time');
      bs.querySelector('.ind').textContent = sortKey==='status' ? (sortDir==='asc'?'↑':'↓') : '⇅';
      bt.querySelector('.ind').textContent = sortKey==='time'   ? (sortDir==='asc'?'↑':'↓') : '⇅';
    }

    // 绑定筛选卡片/表格栏事件
    function bindLabelUploadEvents(){
      const bulkDrop=document.getElementById('bulkDrop'), bulkBtn=document.getElementById('bulkBtn');
      const startTime=document.getElementById('startTime'), endTime=document.getElementById('endTime');
      const statusSel=document.getElementById('statusSel'), shipSel=document.getElementById('shipSel');
      const kw=document.getElementById('kw'), searchBtn=document.getElementById('searchBtn');
      const quickDrop=document.getElementById('quickDrop'), quickBtn=document.getElementById('quickBtn');
      const chkAll=document.getElementById('chkAll');
      const timeField=document.getElementById('timeField');
      const sortStatusBtn=document.getElementById('sortStatus'), sortTimeBtn=document.getElementById('sortTime');
      const resetBtn=document.getElementById('resetBtn');

      /* ✅ 升级筛选区域内的 select 为“选择框触发 + .menu 下拉”，互斥打开 */
      upgradeSelectToMenu(timeField);
      upgradeSelectToMenu(statusSel);
      upgradeSelectToMenu(shipSel);

      // ✅ 页脚“每页”选择器也升级为 .menu，下拉向上弹
      upgradeSelectToMenu(pageSizeSel, { sizeLike:true, dropUp:true });

      // ✅ 时间输入：点击即弹原生选择器；禁止键盘输入
      [startTime,endTime].forEach(inp=>{
        inp.addEventListener('click', (e)=>{ if (typeof inp.showPicker === 'function'){ e.preventDefault(); inp.showPicker(); } });
        inp.addEventListener('keydown', e=> e.preventDefault());
      });

      // 批量操作（互斥）
      bulkBtn.addEventListener('click',(e)=>{
        e.stopPropagation();
        const willOpen = !bulkDrop.classList.contains('open');
        closeAllMenus(willOpen?bulkDrop:null);
        bulkDrop.classList.toggle('open', willOpen);
      });
      bulkDrop.querySelectorAll('.menu a').forEach(a=>{
        a.addEventListener('click',(e)=>{
          e.preventDefault();
          openOpModal(a.dataset.act || '');
          closeAllMenus(null);
        });
      });

      // 快捷时间（互斥）
      quickBtn.addEventListener('click',(e)=>{
        e.stopPropagation();
        const willOpen = !quickDrop.classList.contains('open');
        closeAllMenus(willOpen?quickDrop:null);
        quickDrop.classList.toggle('open', willOpen);
      });
      quickDrop.querySelectorAll('.menu a').forEach(a=>{
        a.addEventListener('click',(e)=>{
          e.preventDefault();
          const days=parseInt(a.dataset.days||'',10);
          if(a.dataset.clear){ startTime.value=''; endTime.value=''; }
          else if(Number.isFinite(days)){
            const to=new Date(); const from=new Date(to.getTime()-days*86400000);
            startTime.value=toLocal(from); endTime.value=toLocal(to);
          }
          closeAllMenus(null); applyFilters();
        });
      });

      // 搜索：按钮 / 回车；双击打开批量粘贴
      searchBtn.addEventListener('click',()=>{ applyFilters(); fitTableHeight(); });
      kw.addEventListener('keydown',(e)=>{ if(e.key==='Enter'){ applyFilters(); fitTableHeight(); } });
      kw.addEventListener('dblclick', ()=>{ bulkText.value=''; bulkModal.style.display='flex'; bulkText.focus(); });

      // 批量粘贴弹窗
      bulkCancel.addEventListener('click', ()=> bulkModal.style.display='none');
      bulkApply.addEventListener('click', ()=>{
        const ids = bulkText.value.split(/\s+/).map(s=>s.trim()).filter(Boolean);
        if(ids.length){ kw.value = ids.join(' '); applyFilters(); fitTableHeight(); }
        bulkModal.style.display='none';
      });

      // 表头复选框：全选/全不选（仅当前页）
      chkAll.addEventListener('change',()=>{
        const slice=getCurrentPageRows();
        if(chkAll.checked){ slice.forEach(r=>selectedIds.add(r.id)); }
        else{ slice.forEach(r=>selectedIds.delete(r.id)); }
        renderTable();
      });

      // 表体行“点任意位置即勾选/取消”
      tbodyEl.addEventListener('click', (e)=>{
        // 优先处理 op 操作（作废/激活）
        const voidBtn = e.target.closest('a.toggle-void');
        if(voidBtn){
          e.preventDefault();
          const id = Number(voidBtn.dataset.id);
          if(!Number.isFinite(id)) return;
          const row = masterRows.find(r=>r.id===id);
          if(!row) return;
          row.voided = !row.voided;
          // 如果作废时，也确保 statusSel 的 "已作废" 过滤与显示一致（显示逻辑在 renderTable）
          renderTable();
          return;
        }

        const tr = e.target.closest('tr'); if(!tr) return;
        // 避免在可交互元素上误触
        if(e.target.closest('a,button,input,select,textarea,.menu,.cselect,.dropdown')) return;
        const id = Number(tr.getAttribute('data-id')); if(!Number.isFinite(id)) return;
        if(selectedIds.has(id)) selectedIds.delete(id); else selectedIds.add(id);
        renderTable();
      });

      // 单独变更复选框
      tbodyEl.addEventListener('change', (e)=>{
        if(e.target && e.target.matches('input.rowchk')){
          const id = +e.target.getAttribute('data-id');
          if(e.target.checked) selectedIds.add(id); else selectedIds.delete(id);
          syncHeaderCheckbox(); updateSelCounter();
          // 只更新行样式
          const tr=e.target.closest('tr'); if(tr) tr.classList.toggle('selected', e.target.checked);
        }
      });

      // 页底栏事件
      pageSizeSel.addEventListener('change',()=>{ pageSize=parseInt(pageSizeSel.value,10)||50; pageIndex=1; renderTable(); fitTableHeight(); });
      firstPage.addEventListener('click',(e)=>{ e.preventDefault(); pageIndex=1; renderTable(); fitTableHeight(); });
      prevPage .addEventListener('click',(e)=>{ e.preventDefault(); pageIndex=Math.max(1,pageIndex-1); renderTable(); fitTableHeight(); });
      nextPage .addEventListener('click',(e)=>{ e.preventDefault(); pageIndex=Math.min(totalPages(),pageIndex+1); renderTable(); fitTableHeight(); });
      lastPage .addEventListener('click',(e)=>{ e.preventDefault(); pageIndex=totalPages(); renderTable(); fitTableHeight(); });
      jumpTo   .addEventListener('change',()=>{ const p=+jumpTo.value||1; pageIndex=Math.min(Math.max(1,p),totalPages()); renderTable(); fitTableHeight(); });

      // ✅ 全选 / 反选（仅当前页）
      selAll.addEventListener('click',(e)=>{ e.preventDefault(); const slice=getCurrentPageRows(); slice.forEach(r=>selectedIds.add(r.id)); renderTable(); });
      selInvert.addEventListener('click',(e)=>{ e.preventDefault(); const slice=getCurrentPageRows(); slice.forEach(r=>{ if(selectedIds.has(r.id)) selectedIds.delete(r.id); else selectedIds.add(r.id); }); renderTable(); });

      // ✅ 回到顶部：仅滚动表格列表容器
      goTop.addEventListener('click',(e)=>{
        e.preventDefault();
        const sc=document.querySelector('#tableWrap .table-scroll');
        if(sc) sc.scrollTo({top:0, behavior:'smooth'});
      });

      // ✅ 时间字段变更 → 重新排序/渲染（若当前按时间排序）
      timeField.addEventListener('change', ()=>{ applyFilters(); });

      // ✅ 列头排序按钮
      sortStatusBtn.addEventListener('click', ()=>{
        if(sortKey==='status'){ sortDir = (sortDir==='asc'?'desc':'asc'); } else { sortKey='status'; sortDir='asc'; }
        sortRows(); pageIndex=1; renderTable(); updateSortBtnsUI();
      });
      sortTimeBtn.addEventListener('click', ()=>{
        if(sortKey==='time'){ sortDir = (sortDir==='asc'?'desc':'asc'); } else { sortKey='time'; sortDir='desc'; }
        sortRows(); pageIndex=1; renderTable(); updateSortBtnsUI();
      });

      // ✅ 重置按钮：清空所有筛选项 + 搜索框
      resetBtn.addEventListener('click', ()=>{
        // 清空输入
        document.getElementById('startTime').value='';
        document.getElementById('endTime').value='';
        document.getElementById('kw').value='';
        // 选择框恢复默认
        timeField.value='created';
        statusSel.value='';
        shipSel.value='';
        // 同步自定义选择框文字
        [timeField,statusSel,shipSel].forEach(sel=>{
          const wrap=sel.closest('.cselect'); if(!wrap) return;
          const txt=wrap.querySelector('.cs-text'); const cur=sel.options[sel.selectedIndex]||null;
          if(txt) txt.textContent = cur ? cur.text : '';
        });
        applyFilters();
      });
    }

    function syncHeaderCheckbox(){
      const head=document.getElementById('chkAll');
      const slice=getCurrentPageRows();
      const total=slice.length;
      const sel = slice.filter(r=>selectedIds.has(r.id)).length;
      head.indeterminate = sel>0 && sel<total;
      head.checked = total>0 && sel===total;
    }

    let currentAction = '';
    function openOpModal(act){
      currentAction = act;
      const count = getSelectedRows().length;

      if(act==='import-label'){
        opTitle.textContent = '导入面单';
        opContent.innerHTML = `<div>导入面单文件：</div>
          <div style="margin-top:8px"><input type="file" multiple accept=".pdf,.png,.jpg,.jpeg"></div>`;
      }else if(act==='import-map'){
        opTitle.textContent = '导入单号映射';
        opContent.innerHTML = `<div>导入单号映射文件：</div>
          <div style="margin-top:8px"><input type="file" accept=".csv,.xlsx"></div>`;
      }else if(act==='delete'){
        opTitle.textContent = '批量删除';
        opContent.innerHTML = `<div>将删除已选 <strong>${count}</strong> 条记录。此操作不可恢复，请确认。</div>`;
      }else if(act==='export-orders'){
        opTitle.textContent = '订单导出';
        opContent.innerHTML = `<div>将导出当前筛选结果（或已选 <strong>${count}</strong> 条）。此为占位弹窗。</div>`;
      }else if(act==='copy-waybill'){
        const rows = getSelectedRows();
        const txt = rows.map(r=>r.waybill).filter(Boolean).join('\n');
        opTitle.textContent = '批量复制单号';
        opContent.innerHTML = rows.length
          ? `<div style="color:#374151; margin-bottom:8px;">将复制 <strong>${rows.length}</strong> 个运单号到剪贴板。</div>
             <textarea readonly>${txt}</textarea>
             <div style="margin-top:8px;color:#64748b;">（预览，可直接确认复制）</div>`
          : `<div style="color:#ef4444;">当前未选择任何记录，请先勾选需要复制的行。</div>`;
      }else if(act==='batch-print'){
        opTitle.textContent = '批量打印';
        opContent.innerHTML = `<div>将对已选 <strong>${count}</strong> 条记录执行批量打印（模拟）。确认开始打印？</div>`;
      }else if(act==='batch-activate'){
        opTitle.textContent = '批量激活';
        opContent.innerHTML = `<div>将把已选 <strong>${count}</strong> 条记录标记为激活（取消作废）。确认执行？</div>`;
      }else if(act==='batch-void'){
        opTitle.textContent = '批量作废';
        opContent.innerHTML = `<div>将把已选 <strong>${count}</strong> 条记录标记为作废（显示删除线）。确认执行？</div>`;
      }else{
        opTitle.textContent = '操作';
        opContent.textContent = '占位内容';
      }
      opModal.style.display = 'flex';
    }
    opCancel.addEventListener('click', ()=> opModal.style.display='none');
    opConfirm.addEventListener('click', async ()=>{
      // 处理新增批量操作的实际逻辑（模拟）
      if(currentAction==='copy-waybill'){
        const rows = getSelectedRows();
        const txt = rows.map(r=>r.waybill).filter(Boolean).join('\n');
        if(!txt){ alert('没有可复制的运单号。'); return; }
        const ok = await copyToClipboard(txt);
        opModal.style.display='none';
        alert(ok ? `已复制 ${rows.length} 个运单号到剪贴板。` : '复制失败，请手动选择文本复制。');
        return;
      }

      if(currentAction==='batch-print'){
        // 模拟批量打印
        const rows = getSelectedRows();
        opModal.style.display='none';
        alert(`已模拟将 ${rows.length} 条记录发送至打印队列。`);
        return;
      }

      if(currentAction==='batch-activate'){
        const rows = getSelectedRows();
        if(rows.length){
          rows.forEach(r=>{ r.voided = false; });
          renderTable();
        }
        opModal.style.display='none';
        alert(`已将 ${rows.length} 条记录标记为激活。`);
        return;
      }

      if(currentAction==='batch-void'){
        const rows = getSelectedRows();
        if(rows.length){
          rows.forEach(r=>{ r.voided = true; });
          renderTable();
        }
        opModal.style.display='none';
        alert(`已将 ${rows.length} 条记录标记为作废。`);
        return;
      }

      // 原有操作的简单模拟处理（导入/删除/导出等）
      if(currentAction==='delete'){
        // 模拟删除：从 masterRows 中移除已选择
        const sel = Array.from(selectedIds);
        if(sel.length){
          masterRows = masterRows.filter(r => !selectedIds.has(r.id));
          selectedIds.clear();
          applyFilters();
        }
        opModal.style.display='none';
        alert('已模拟批量删除（已从演示数据中移除选中项）。');
        return;
      }

      opModal.style.display='none';
      alert('已模拟执行操作（占位）');
    });

    function applyFilters(){
      const timeField=document.getElementById('timeField')?.value||'created';
      const startTime=document.getElementById('startTime').value, endTime=document.getElementById('endTime').value;
      const statusSel=document.getElementById('statusSel').value.trim(), shipSel=document.getElementById('shipSel').value.trim();
      const kw=document.getElementById('kw').value.trim(); const picks=kw?kw.split(/\s+/).filter(Boolean):[];
      const getDate=r=> timeField==='printed'? r.printedAt : r.createdAt;

      viewRows=masterRows.filter(r=>{
        const d=getDate(r);
        if(startTime){ if(!d || d<new Date(startTime)) return false; }
        if(endTime){   if(!d || d>new Date(endTime))   return false; }
        // 如果选择 "已作废"，以 voided 标识过滤
        if(statusSel){
          if(statusSel === '已作废'){
            if(!r.voided) return false;
          }else{
            if(r.status !== statusSel) return false;
          }
        }
        if(shipSel   && r.ship!==shipSel)     return false;
        if(picks.length){
          const hay=`${r.orderNo} ${r.waybill} ${r.transNo}`.toLowerCase();
          if(!picks.some(p=>hay.includes(p.toLowerCase()))) return false;
        }
        return true;
      });

      // 应用排序
      sortRows();

      pageIndex=1; renderTable();
    }
    function totalPages(){ return Math.max(1, Math.ceil(viewRows.length/pageSize)); }

    function renderTable(){
      const start=(pageIndex-1)*pageSize, slice=viewRows.slice(start,start+pageSize);
      tbodyEl.innerHTML=slice.map(r=>{
        const checked = selectedIds.has(r.id) ? 'checked' : '';
        const selCls  = selectedIds.has(r.id) ? 'selected' : '';
        const voidCls = r.voided ? 'voided' : '';
        // 状态显示：当作废时追加 "｜已作废"
        const shownStatus = `${r.status}${r.voided ? '｜已作废' : ''}`;
        return `
        <tr data-id="${r.id}" class="${selCls} ${voidCls}">
          <td class="col-chk"><input type="checkbox" class="chk rowchk" data-id="${r.id}" ${checked}></td>
          <td class="col-order">${r.orderNo}</td>
          <td class="col-waybill">${r.waybill}</td>
          <td class="col-trans">${r.transNo}</td>
          <td class="col-ship">${r.ship||'-'}</td>
          <td class="col-file">${r.file}</td>
          <td class="col-status">${shownStatus}</td>
          <td class="col-created">
            <div class="time2">
              <div>创建时间：${formatDateTime(r.createdAt)}</div>
              <div>打印时间：${formatDateTime(r.printedAt)}</div>
            </div>
          </td>
          <td class="col-op op"><a href="#" data-op="预览">预览</a><a href="#" class="toggle-void" data-id="${r.id}">${r.voided ? '激活' : '作废'}</a></td>
        </tr>
      `}).join('');

      pageInfo.textContent=`共 ${viewRows.length} 条 ${pageIndex}/${totalPages()} 页`;
      jumpTo.value=pageIndex;

      const pages=totalPages(); const nums=[];
      const s=Math.max(1,pageIndex-2), e=Math.min(pages,pageIndex+2);
      for(let i=s;i<=e;i++){ nums.push(`<a href="#" data-p="${i}" style="${i===pageIndex?'font-weight:700;text-decoration:underline':''}">${i}</a>`); }
      pageNums.innerHTML=nums.join('');
      pageNums.querySelectorAll('a').forEach(a=>a.addEventListener('click',(e)=>{ e.preventDefault(); pageIndex=+a.dataset.p; renderTable(); fitTableHeight(); }));

      syncHeaderCheckbox();
      fitTableHeight();
      updateSelCounter();
    }

    /* ========== 初始化（导航） ========== */
    (function init(){
      loadState();
      if(!lockedSubHref){ const firstSub=(SUBMAP[lockedPath]||[])[0]; lockedSubHref=firstSub?firstSub.href:''; }
      hoverPath=lockedPath;
      movePillToEl(links.find(a=>a.dataset.path===lockedPath)||links[0]);
      renderSub(lockedPath);
      highlightActive();

      const ro=new ResizeObserver(()=>{ updateSubRowMinHeight(); fitTableHeight(); });
      ro.observe(subInner); updateSubRowMinHeight();

      window.addEventListener('resize', fitTableHeight);
    })();

    /* ========== 顶部导航交互（含防回弹） ========== */
    links.forEach(a=>{
      a.addEventListener('pointerenter',()=>{ if(inSubRow) return; hoverPath=a.dataset.path; movePillToEl(a); renderSubPreview(hoverPath); });
    });
    function renderSubPreview(path){
      const list=SUBMAP[path]||[];
      subInner.innerHTML=list.map(i=>`<a class="sub" data-owner="${path}" href="${i.href}">${i.text}</a>`).join('');
    }
    track.addEventListener('pointerleave',()=>{
      clearTimeout(leaveTimer);
      leaveTimer=setTimeout(()=>{ if(!inSubRow){ hoverPath=lockedPath; movePillToEl(links.find(x=>x.dataset.path===lockedPath)||links[0]); renderSub(lockedPath); fitTableHeight(); } }, GRACE_MS);
    });
    subRow.addEventListener('pointerenter',()=>{ inSubRow=true; clearTimeout(leaveTimer); });
    subRow.addEventListener('pointerleave',()=>{ inSubRow=false; hoverPath=lockedPath; movePillToEl(links.find(x=>x.dataset.path===lockedPath)||links[0]); renderSub(lockedPath); fitTableHeight(); });
    subInner.addEventListener('pointerover',(e)=>{ const s=e.target.closest('a.sub'); if(!s) return; const ownerEl=links.find(a=>a.dataset.path===s.getAttribute('data-owner')); if(ownerEl) movePillToEl(ownerEl); });
    links.forEach(a=>{
      a.addEventListener('click',(e)=>{
        if(!USE_REAL_NAV) e.preventDefault();
        lockedPath=a.dataset.path;
        const firstSub=(SUBMAP[lockedPath]||[])[0];
        lockedSubHref=firstSub?firstSub.href:'';
        lockedTabHref=TABMAP[lockedSubHref] ? (DEFAULT_TAB_BY_SUB[lockedSubHref]||'') : '';
        saveState(); hoverPath=lockedPath; highlightActive(); renderSub(lockedPath);
        if(USE_REAL_NAV && lockedSubHref) window.location.href=lockedSubHref;
        fitTableHeight();
      });
    });
    subInner.addEventListener('click',(e)=>{
      const a=e.target.closest('a.sub'); if(!a) return;
      if(!USE_REAL_NAV) e.preventDefault();
      lockedPath=a.getAttribute('data-owner'); lockedSubHref=a.getAttribute('href')||'';
      if(TABMAP[lockedSubHref]){
        if(!lockedTabHref || !TABMAP[lockedSubHref].some(t=>t.href===lockedTabHref)) lockedTabHref=DEFAULT_TAB_BY_SUB[lockedSubHref]||TABMAP[lockedSubHref][0].href;
      }else lockedTabHref='';
      saveState(); hoverPath=lockedPath; highlightActive();
      subInner.querySelectorAll('.sub').forEach(s=>s.classList.remove('active')); a.classList.add('active');
      renderSub(lockedPath);
      if(USE_REAL_NAV && lockedSubHref) window.location.href=lockedSubHref;
      fitTableHeight();
    });
    function currentVisualPath(){ return inSubRow?hoverPath:(hoverPath||lockedPath); }
    window.addEventListener('resize',()=>{ movePillToEl(links.find(x=>x.dataset.path===currentVisualPath())||links[0]); updateSubRowMinHeight(); });
    track.addEventListener('scroll',()=>{ movePillToEl(links.find(x=>x.dataset.path===currentVisualPath())||links[0]); });
  </script>
</body>
</html>
