# notes.db corruption — 56 lost inline comments (2026-07-26)

On **2026-07-26** `db/notes.db` became *"database disk image is malformed"* — a torn/lost write left a contiguous run of zero-filled leaf pages in the `pdf_inline_comments` B-tree (`btreeInitPage` error 11). 118 of 174 rows were salvaged via `.recover`; the **56 rows below were physically destroyed** (their pages were zeroed and they were created *after* the 2026-07-19 auto-commit, so absent from git / snapshots / WAL).

**Only the row `id`, `source`, and `file_id` survive** — recovered from the two intact indexes (`idx_pic_file_id`, `idx_pic_source_file`). The comment **text (`body`), page number, and highlighted quote are unrecoverable.** This manifest exists so the annotations can be re-created; the affected PDFs are linked below.

> ⚠️ Caveat: a corrupt index can retain entries for already-deleted rows, so the true loss may be somewhat under 56.

## Summary — 56 lost comments across 8 PDFs

| Lost | Broker | PDF | file_id |
|---:|---|---|---|
| 24 | — | [世界模型：物理世界的重塑，AGI的终极拼图.pdf](http://xs-macbook-air.local:5001/zsxq/pdf/814515488555252/%E4%B8%96%E7%95%8C%E6%A8%A1%E5%9E%8B%EF%BC%9A%E7%89%A9%E7%90%86%E4%B8%96%E7%95%8C%E7%9A%84%E9%87%8D%E5%A1%91%EF%BC%8CAGI%E7%9A%84%E7%BB%88%E6%9E%81%E6%8B%BC%E5%9B%BE.pdf) | `814515488555252` |
| 17 | Deutsche Bank | [Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf](http://xs-macbook-air.local:5001/zsxq/pdf/584282511152254/Deutsche%20Bank-SpaceX%EF%BC%88SPCX.OQ%EF%BC%89Data%20Centers%20in%20Space%20Part%204-260714.pdf) | `584282511152254` |
| 6 | Bernstein | [Bernstein-Space Exploration Technologies Corporation（SPCX.US）SpaceX： Starship launch 13 scrubbed ~ Replacing two engines； targeting early next week-260717.pdf](http://xs-macbook-air.local:5001/zsxq/pdf/412414245188158/Bernstein-Space%20Exploration%20Technologies%20Corporation%EF%BC%88SPCX.US%EF%BC%89SpaceX%EF%BC%9A%20Starship%20launch%2013%20scrubbed%20~%20Replacing%20two%20engines%EF%BC%9B%20targeting%20early%20next%20week-260717.pdf) | `412414245188158` |
| 4 | Morgan Stanley | [Morgan Stanley-Space Exploration Technologies Corp.（SPCX.US）A 'Heavenly' Hedge to DC NIMBYism？-260716.pdf](http://xs-macbook-air.local:5001/zsxq/pdf/412414241484548/Morgan%20Stanley-Space%20Exploration%20Technologies%20Corp.%EF%BC%88SPCX.US%EF%BC%89A%20%27Heavenly%27%20Hedge%20to%20DC%20NIMBYism%EF%BC%9F-260716.pdf) | `412414241484548` |
| 2 | Goldman Sachs | [Goldman Sachs-Montage （688008）：Rising memory interface IC with Gen~3  Gen~4 ramp up； 2Q26 NI guidance beat； Buy-260718.pdf](http://xs-macbook-air.local:5001/zsxq/pdf/584282851148884/Goldman%20Sachs-Montage%20%EF%BC%88688008%EF%BC%89%EF%BC%9ARising%20memory%20interface%20IC%20with%20Gen~3%20%20Gen~4%20ramp%20up%EF%BC%9B%202Q26%20NI%20guidance%20beat%EF%BC%9B%20Buy-260718.pdf) | `584282851148884` |
| 1 | J.P. Morgan | [J.P. Morgan-Korea Battery：LGES wins 2.9GWh Google ESS project； SK On wins 13% of Korea AI ESS tender-260717.pdf](http://xs-macbook-air.local:5001/zsxq/pdf/412414158814458/J.P.%20Morgan-Korea%20Battery%EF%BC%9ALGES%20wins%202.9GWh%20Google%20ESS%20project%EF%BC%9B%20SK%20On%20wins%2013%25%20of%20Korea%20AI%20ESS%20tender-260717.pdf) | `412414158814458` |
| 1 | Goldman Sachs | [Goldman Sachs-JCET （600584）： New advanced packaging capacity announced； 2Q26 NI guidance beat-260717.pdf](http://xs-macbook-air.local:5001/zsxq/pdf/181282154414812/Goldman%20Sachs-JCET%20%EF%BC%88600584%EF%BC%89%EF%BC%9A%20New%20advanced%20packaging%20capacity%20announced%EF%BC%9B%202Q26%20NI%20guidance%20beat-260717.pdf) | `181282154414812` |
| 1 | — | [机械行业机汇：人形机器人，国内外量产稳步推进.pdf](http://xs-macbook-air.local:5001/zsxq/pdf/214515488555551/%E6%9C%BA%E6%A2%B0%E8%A1%8C%E4%B8%9A%E6%9C%BA%E6%B1%87%EF%BC%9A%E4%BA%BA%E5%BD%A2%E6%9C%BA%E5%99%A8%E4%BA%BA%EF%BC%8C%E5%9B%BD%E5%86%85%E5%A4%96%E9%87%8F%E4%BA%A7%E7%A8%B3%E6%AD%A5%E6%8E%A8%E8%BF%9B.pdf) | `214515488555551` |

## Full row list

| id | source | file_id | PDF |
|---:|---|---|---|
| 148 | zsxq | `412414241484548` | Morgan Stanley-Space Exploration Technologies Corp.（SPCX.US）A 'Heavenly' Hedge to DC NIMBYism？-260716.pdf |
| 149 | zsxq | `412414241484548` | Morgan Stanley-Space Exploration Technologies Corp.（SPCX.US）A 'Heavenly' Hedge to DC NIMBYism？-260716.pdf |
| 150 | zsxq | `412414241484548` | Morgan Stanley-Space Exploration Technologies Corp.（SPCX.US）A 'Heavenly' Hedge to DC NIMBYism？-260716.pdf |
| 151 | zsxq | `412414241484548` | Morgan Stanley-Space Exploration Technologies Corp.（SPCX.US）A 'Heavenly' Hedge to DC NIMBYism？-260716.pdf |
| 152 | zsxq | `412414245188158` | Bernstein-Space Exploration Technologies Corporation（SPCX.US）SpaceX： Starship launch 13 scrubbed ~ Replacing two engines； targeting early next week-260717.pdf |
| 153 | zsxq | `412414245188158` | Bernstein-Space Exploration Technologies Corporation（SPCX.US）SpaceX： Starship launch 13 scrubbed ~ Replacing two engines； targeting early next week-260717.pdf |
| 154 | zsxq | `412414245188158` | Bernstein-Space Exploration Technologies Corporation（SPCX.US）SpaceX： Starship launch 13 scrubbed ~ Replacing two engines； targeting early next week-260717.pdf |
| 156 | zsxq | `412414245188158` | Bernstein-Space Exploration Technologies Corporation（SPCX.US）SpaceX： Starship launch 13 scrubbed ~ Replacing two engines； targeting early next week-260717.pdf |
| 157 | zsxq | `412414245188158` | Bernstein-Space Exploration Technologies Corporation（SPCX.US）SpaceX： Starship launch 13 scrubbed ~ Replacing two engines； targeting early next week-260717.pdf |
| 158 | zsxq | `412414245188158` | Bernstein-Space Exploration Technologies Corporation（SPCX.US）SpaceX： Starship launch 13 scrubbed ~ Replacing two engines； targeting early next week-260717.pdf |
| 159 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 161 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 162 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 163 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 164 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 165 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 166 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 167 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 168 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 169 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 170 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 171 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 172 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 174 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 175 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 176 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 177 | zsxq | `584282511152254` | Deutsche Bank-SpaceX（SPCX.OQ）Data Centers in Space Part 4-260714.pdf |
| 178 | zsxq | `412414158814458` | J.P. Morgan-Korea Battery：LGES wins 2.9GWh Google ESS project； SK On wins 13% of Korea AI ESS tender-260717.pdf |
| 181 | zsxq | `584282851148884` | Goldman Sachs-Montage （688008）：Rising memory interface IC with Gen~3  Gen~4 ramp up； 2Q26 NI guidance beat； Buy-260718.pdf |
| 182 | zsxq | `584282851148884` | Goldman Sachs-Montage （688008）：Rising memory interface IC with Gen~3  Gen~4 ramp up； 2Q26 NI guidance beat； Buy-260718.pdf |
| 183 | zsxq | `181282154414812` | Goldman Sachs-JCET （600584）： New advanced packaging capacity announced； 2Q26 NI guidance beat-260717.pdf |
| 184 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 185 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 186 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 187 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 188 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 189 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 190 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 191 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 192 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 193 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 194 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 195 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 196 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 197 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 198 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 199 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 200 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 201 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 202 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 203 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 204 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 206 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 207 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 208 | zsxq | `814515488555252` | 世界模型：物理世界的重塑，AGI的终极拼图.pdf |
| 209 | zsxq | `214515488555551` | 机械行业机汇：人形机器人，国内外量产稳步推进.pdf |

---

*Root cause & fix: see commit `ede6712` — WAL + `synchronous=FULL` hardening, rotating backups (`db_paths.backup_db`), and a startup `quick_check` now guard notes.db against this failure mode. Corrupt original preserved locally as `db/notes.db.corrupt-2026-07-26` (untracked).*
