# 鐢靛伐鏉疄娴嬪垎甯?(SEED v0.1)

> **姝ょ洰褰曟暟鎹负绉嶅瓙鐗堟湰 (seed_v0.1), 鏈仛鐪?PDF 鐑樼剻銆?*
> 闃堝€煎彇鑷巻骞寸數宸ユ澂棰樼洰棰橀噺鍒嗘瀽 + 鍏紑璇勫鏍囧噯浼扮畻 + 鍥借禌 D 棰橀儴鍒嗙被姣斻€?
> 鍚庣画鑻ユ彁浜?30+ 绡囩數宸ユ澂涓€绛夊 PDF, 鍙敤 `scripts/dev/ingest_papers.py` 閲嶆柊鐑樼剻瑕嗙洊銆?

## 鏁版嵁缂哄彛鎻愮ず

`empirical.json` 涓墍鏈?`min` / `max` / `mean` 瀛楁濉殑鏄及绠楀€笺€?In `v1.2-alpha`, treat them as optional background context for per-question review and final quality checks, and mark them clearly as seed-level evidence when cited.

## 闃堝€煎嚭澶?

| 闃堝€?| 鏉ユ簮 |
|------|------|
| 鎽樿 600-1000 瀛?| 宸ョ▼绫绘憳瑕佸父瑙佸尯闂? 姣斿浗璧?5 娈靛紡鐣ョ煭 |
| 璁烘枃 25-30 椤?| 鍘嗗勾鑾峰璁烘枃鐩祴 |
| 瀛愰棶鏁?6-8 | 鍘嗗勾棰樼洰缁撴瀯绋冲畾 |
| 鍥?12-25 | 宸ョ▼绫诲浘琛ㄥ, 鍚瓑楂樼嚎 / 鏃跺簭鏇茬嚎 / 鍗曠嚎鍥?|
| 鍏紡 18-50 | 涓瓑瀵嗗害 |
| 寮曠敤 10-22 | 鐢靛姏 / 鑳芥簮绫绘湡鍒婁负涓?|

## 涓?cumcm 鐨勫樊寮?

鐢靛伐鏉殑"宸ョ▼瀹炵敤鎬?缁村害鍥借禌娌℃湁鏄惧紡瀵瑰簲銆傛湰 overlay 鍔犱簡 3 涓伐绋嬪寲缁村害 (engineering_practicality / physical_meaning / data_completeness), 鐩存帴杩?stage 8銆?

鐢靛伐鏉殑瀛愰棶鏁颁腑浣嶆暟 7, 姣斿浗璧?4 澶氳繎涓€鍊? 杩欐剰鍛崇潃 stage 5 鍦?standard 妯″紡涓嬪彲鑳借窇涓嶅畬銆傚缓璁绠楀垎閰?
- planning and setup: about 8h
- per-question build loop: about 18-24h
- final integration, paper, and review: about 12-18h



