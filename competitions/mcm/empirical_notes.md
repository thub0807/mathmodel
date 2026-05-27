# MCM/ICM 瀹炴祴鍒嗗竷 (SEED v0.1)

> **姝ょ洰褰曟暟鎹负绉嶅瓙鐗堟湰 (seed_v0.1), 鏈仛鐪?PDF 鐑樼剻銆?*
> 闃堝€煎彇鑷?COMAP 鍏紑 scoring rubric + 宸插彂琛?MCM 澶囪禌鏁欐潗鍏辫瘑銆?
> 鍚庣画鑻ユ彁浜?30+ 绡?Outstanding Winner PDF, 鍙敤 `scripts/dev/ingest_papers.py` 閲嶆柊鐑樼剻瑕嗙洊銆?

## 鏁版嵁缂哄彛鎻愮ず

`empirical.json` contains estimated `min` / `max` / `mean` values rather than measured sample statistics. In `v1.2-alpha`, treat them as optional background context for per-question review and final quality checks, and mark them clearly as seed-level evidence when cited.

## 闃堝€煎嚭澶?

| 闃堝€?| 鏉ユ簮 | 澶囨敞 |
|------|------|------|
| Summary 250-350 璇?| COMAP scoring sheet "1-page summary" | 鍘嗗勾瑙勫垯涓€鑷?|
| 璁烘枃椤垫暟 25-35 椤?| Outstanding 璇勫璁茶В | 瓒?50 椤垫墸鍒?|
| Figure 8-22 | 缁忛獙浼扮畻 | Outstanding 鏅亶鍥惧 |
| Reference 12-25 | 缁忛獙浼扮畻 | IEEE 寮曠敤 |
| Letter 350-700 璇?| F 棰樺巻骞?Memo 闀垮害 | 1-2 椤垫甯?|

## 涓?cumcm/ 鐨勫樊寮?

鍥借禌 91 绡?PDF 鐑樼剻浜?11 涓淮搴︾殑 p25/p50/p75銆傛湰鐩綍鍙墜濉?8 涓淮搴︾殑浼板€笺€侻CM 缂烘暟鎹細
- Outstanding Winner PDF 涓嶅叕寮€涓嬭浇
- COMAP 鍙彂甯冩瘡骞?outstanding 璁烘枃鐨?~30 瀛楁憳瑕佹弿杩? 鏃犲叏鏂?
- GitHub 涓婇浂鏁?MCM 璁烘枃鐗堟潈鐘舵€佷笉涓€

## 鎺ㄨ崘浣跨敤鏂瑰紡

1. **浼樺厛浣跨敤妯″紡瀹氭€?*: `winning_patterns.md` 鍒楃殑 Outstanding 鍏辨€ф槸鏇村彲闈犵殑 anchor
2. **鏁板€奸槇鍊间粎浣滃弬鑰?*: L1 critic 瑙佸埌 `seed` 鏍囪鍚庡急鍖栨暟鍊艰瘎鍒? 寮哄寲妯″紡鍖归厤
3. **鑻ョ敤鎴疯兘鎻愪緵鍘嗗勾 Outstanding 璁烘枃**: 璺?`scripts/dev/ingest_papers.py --competition mcm`, 瑕嗙洊鏈?JSON
