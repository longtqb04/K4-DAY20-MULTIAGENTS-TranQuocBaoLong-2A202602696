# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên |
|---|---|
| Tràn Quốc Bảo Long | 2A202602696 |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: LAB_MODEL=openai:gpt-4o-mini, LAB_TEMPERATURE=0,
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: chạy trực tiếp
- Số lần chạy tác vụ đã dùng / ngân sách:
- Commit của tag `freeze`: c8fd20ce68fa696a3857c1e3099fb167e46c6c2f

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): Dự đoán `subagents` cải thiện nhẹ điểm đánh giá nhờ chuyên môn hóa; mức tăng có thể hạn chế nếu agent không giao việc hoặc không kiểm tra kết quả subagent.
- H2 (skills-auto so với baseline): Dự đoán `skills-auto` không cải thiện đáng kể điểm đánh giá; skill tự sinh có thể mã hóa quy trình hữu ích nhưng dễ lệch khỏi tác vụ mới hoặc quá khớp với tác vụ học (GUIDE, SkillsBench và SkillEvolBench).
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán điểm tác vụ học cao hơn điểm đánh giá vì quy trình/skill được rút ra từ tác vụ học có thể không khái quát sang yêu cầu mới; SkillEvolBench cũng ghi nhận nguy cơ lợi ích không chuyển giao.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Các công cụ được cung cấp cho mô hình gồm: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute` và `task`. Trong đó, `execute` cho phép chạy lệnh shell.
2. Mô hình có thể gọi công cụ `task` để khởi chạy một subagent tạm thời, phù hợp với công việc phức tạp gồm nhiều bước. Agent type được nêu trong kết quả là `general-purpose`.
3. Theo mô tả công cụ, subagent `general-purpose` có quyền truy cập tất cả công cụ như agent chính. Mỗi lần gọi mặc định là stateless; mô hình cần đưa đủ chi tiết vào prompt cho subagent. Kết quả của subagent được trả về dưới dạng một báo cáo cuối cùng.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| code-learn | `visible_suite_passes` | B | `pytest workspace/tests/` dừng khi thu thập test: `ModuleNotFoundError: No module named 'inventory'`; vết cho thấy tác tử thử lại nhưng vẫn kết thúc với lỗi. |
| code-learn | `tests_not_modified` | G | Check báo: `the original files in tests/ must not be modified`; tác tử đã vi phạm ràng buộc này. |
| code-learn | `parse_price_all_formats` | D | `wrong for: ['(12.00)']`; thiếu xử lý định dạng số âm kiểu kế toán trong docstring. |
| code-learn | `other_caller_fixed` | G | `SyntaxError: unterminated string literal` tại `export.py`, dòng 12; thay đổi tạo cú pháp không hợp lệ. |
| code-learn | `csv_quoting_follows_docstring` | G | Cùng lỗi `SyntaxError` ở `export.py:12`, khiến hàm CSV không thể được kiểm tra. |
| code-learn | `rule_type_hints` | E | Tên check bắt đầu bằng `rule_`; chi tiết lỗi là `SyntaxError` khi kiểm tra type hints. |
| code-learn | `rule_regression_tests` | E | Check `rule_`; bot yêu cầu `tests/test_regressions.py` có ít nhất 3 test hồi quy. |
| code-learn | `rule_changelog` | E | Check `rule_`; bot yêu cầu ghi ít nhất 3 bullet dưới `## Unreleased` trong `CHANGELOG.md`. |
| data-learn | `north_q1_revenue` | G | Không có `workspace/answer.json` (`FileNotFoundError`); run kết thúc với `GraphRecursionError` ở giới hạn 60 bước. |
| data-learn | `north_q1_orders` | G | Không có `workspace/answer.json` (`FileNotFoundError`); run kết thúc với `GraphRecursionError`. |
| data-learn | `top_region` | G | Không có `workspace/answer.json` (`FileNotFoundError`); run kết thúc với `GraphRecursionError`. |
| data-learn | `missing_amount_orders` | G | Không có `workspace/answer.json` (`FileNotFoundError`); run kết thúc với `GraphRecursionError`. |
| data-learn | `duplicate_rows_removed` | G | Không có `workspace/answer.json` (`FileNotFoundError`); run kết thúc với `GraphRecursionError`. |
| data-learn | `rule_money_in_cents` | E | Check `rule_`; do `answer.json` không tồn tại nên checker không thể xác minh quy ước tiền tính bằng cents. |
| data-learn | `rule_meta_block` | E | Check `rule_`; do `answer.json` không tồn tại nên checker không thể xác minh metadata block. |
| data-learn | `rule_clean_csv` | E | Check `rule_`; bot yêu cầu tạo `workspace/clean.csv` với header, định dạng UTC, region chuẩn hóa và amount dạng cents. |
| logs-learn | `valid_structure` | G | Không có `workspace/errors.json` (`FileNotFoundError`); vết chỉ cho thấy đọc `app.log`, không có lần ghi file đầu ra. |
| logs-learn | `entry_count` | G | Không có `workspace/errors.json` (`FileNotFoundError`), nên không thể đếm entry lỗi. |
| logs-learn | `timestamps_utc` | G | Không có `workspace/errors.json` (`FileNotFoundError`), nên timestamp không được kiểm tra. |
| logs-learn | `exception_fields` | G | Không có `workspace/errors.json` (`FileNotFoundError`), nên trường exception không được kiểm tra. |
| logs-learn | `repeat_counts` | G | Không có `workspace/errors.json` (`FileNotFoundError`), nên số lần lặp không được kiểm tra. |
| logs-learn | `counts_by_service` | G | Không có `workspace/errors.json` (`FileNotFoundError`), nên tổng theo service không được kiểm tra. |
| logs-learn | `rule_service_names` | E | Check `rule_`; checker không thể xác minh quy ước tên service vì thiếu `errors.json`. |
| logs-learn | `rule_sorted_errors` | E | Check `rule_`; checker không thể xác minh thứ tự lỗi vì thiếu `errors.json`. |
| logs-learn | `rule_schema_header` | E | Check `rule_`; checker không thể xác minh schema/header vì thiếu `errors.json`. |

Nhận xét: Nhóm G chiếm đa số (14/25 check thất bại), chủ yếu do tác vụ không tạo được artifact đầu ra (`answer.json`/`errors.json`) và lỗi cú pháp trong `export.py`. Nhóm E có 9 check, nhóm B và D mỗi nhóm có 1 check. Một skill quy trình có thể nhắc tác tử tạo đúng file đầu ra sớm, kiểm tra file tồn tại, chạy checker/test và chỉ báo hoàn thành sau khi xác minh; điều này có thể giảm lỗi thiếu artifact và lỗi kiểm chứng, nhưng không đảm bảo tránh được `GraphRecursionError` hoặc lỗi triển khai cụ thể.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent được định nghĩa trong `get_subagents()`:
  - `explorer`: đọc và báo cáo thông tin về tệp/thư mục; phù hợp cho bước khảo sát trước khi sửa.
  - `implementer`: thực hiện tác vụ lập trình/phát triển; phù hợp để giao phần triển khai.
  - `reviewer`: kiểm tra độc lập kết quả; nhằm phát hiện lỗi sau khi triển khai.
  Các vai trò tách việc khảo sát, thực hiện và rà soát.

| Tác vụ | `subagent_calls` | Subagent được gọi | Token baseline | Token subagents | Chênh lệch |
|---|---:|---|---:|---:|---:|
| code-learn | 0 | — | 59.476 | 72.070 | +12.594 (+21,2%) |
| data-learn | 1 | `implementer` | 368.860 | 89.560 | −279.300 (−75,7%) |
| logs-learn | 0 | — | 29.140 | 20.149 | −8.991 (−30,9%) |

- Các trường hợp `subagent_calls = 0` là kết quả hợp lệ: trong trace của `code-learn` và `logs-learn` không có lệnh gọi `task`, nên tác tử chính tự xử lý. Trong `data-learn`, tác tử chính giao một lần việc xử lý dữ liệu cho `implementer`.
- Lời giao việc cho `implementer` nêu mục tiêu xử lý CSV, chuẩn hóa, khử trùng lặp và các phép tính. Tuy nhiên, nó không truyền đủ đặc tả đầu ra: thiếu tên file và schema JSON chính xác, thiếu yêu cầu giá trị `-999` không được cộng vào doanh thu, và mô tả chuẩn hóa vùng thành chữ hoa thay vì dạng chuẩn `North/South/East/West`. Nó cũng yêu cầu đổi ngày thành `YYYY-MM-DD`, không nói rõ cần quy đổi timestamp có offset sang UTC để áp dụng mốc Q1.
- Trace cho thấy subagent trả về pseudocode và nói không chạy được Python. Tác tử chính sau đó tự ghi `answer.json`, nhưng không có bước đọc lại/đối chiếu kết quả với báo cáo của subagent trước khi hoàn tất. Kết quả chấm chỉ đạt `1/8`, nên việc kiểm chứng không đủ.
- Trung bình token trên ba tác vụ là 152.492 ở baseline và 60.593 ở điều kiện `subagents` (−60,3%). Mức giảm chủ yếu trùng với việc baseline `data-learn` tiêu tốn 368.860 token rồi gặp `GraphRecursionError`; chỉ một trong ba tác vụ thực sự gọi subagent, nên số liệu này chưa chứng minh bản thân việc phân công làm giảm token. `code-learn` còn tăng 21,2% token dù không gọi subagent.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator: 3

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `check-module-imports` | Khá tổng quát cho dự án Python có chạy test; không nhắc tên tác vụ hay file dữ liệu riêng. | Hướng dẫn hợp lý: xác nhận dependency và đường dẫn import, chạy test import sớm. “Check that the module exists” hơi lặp với kiểm tra import nhưng không gây hại. | 10 dòng tổng, 5 dòng body. `description` bắt đầu bằng “Use this skill” và nêu kiểm tra import/module trước test hoặc chạy code. `skills_read`: chưa có dữ liệu vì chưa tồn tại `results/skills-auto/`. |
| `follow-test-protocols` | Khá tổng quát cho tác vụ lập trình; hướng đến giữ nguyên test gốc, regression tests và changelog. | Phù hợp với các lỗi code-learn về sửa test gốc, thiếu regression tests và changelog. Quy tắc “mọi hàm/phương thức đều cần test” khá rộng, có thể tốn công không cần thiết. `description` chưa mở đầu bằng “Use when” và chưa nêu rõ tình huống kích hoạt. | 10 dòng tổng, 5 dòng body. `description` nói chung về quy trình kiểm thử và tuân thủ yêu cầu. `skills_read`: chưa có dữ liệu vì chưa tồn tại `results/skills-auto/`. |
| `verify-code-syntax` | Tổng quát cho tác vụ sửa hoặc chạy mã nguồn. | Các bước kiểm tra cú pháp, dùng `py_compile`, chú ý escape chuỗi và chia nhỏ biểu thức đều phù hợp; sát lỗi `SyntaxError` trong code-learn. Gợi ý chèn print/log để dò lỗi có thể tạo nhiễu nếu lạm dụng. | 10 dòng tổng, 5 dòng body. `description` nêu tình huống kiểm tra cú pháp trước khi chạy mã. `skills_read`: chưa có dữ liệu vì chưa tồn tại `results/skills-auto/`. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 2/10 | 4/10 | 3/10 |
| data-learn | 0/8 | 1/8 | 0/8 |
| logs-learn | 0/9 | 1/9 | 0/9 |
| code-eval | 0/11 | 1/11 | 0/11 |
| data-eval | 1/9 | 4/9 | 0/9 |
| logs-eval | 2/10 | 1/10 | 1/10 |
| **Mean score - learning tasks** | 0.07 | 0.21 | 0.10 |
| **Mean score - evaluation tasks** | 0.10 | 0.21 | 0.03 |
| **Mean tokens per run** | 87,966 | 107,933 | 29,296 |
| **Runs that read a skill** | 0/6 | 0/6 | 0/6 |

condition     role    technical  house rules  mean tokens  read a skill
baseline      learn     2/18         0/9          152,492      0/3     
subagents     learn     6/18         0/9           60,593      0/3  
```

Các run có `error` và cách xử lý:

- `baseline/data-learn` và `subagents/data-eval` kết thúc bằng `GraphRecursionError` ở `recursion_limit=60`. `subagents/data-eval` vẫn được chấm `4/9` trên workspace dở dang; `calls=0` là giới hạn ghi trace khi `invoke` ném lỗi, không có nghĩa là agent không chạy. Theo GUIDE, cần chạy lại riêng tác vụ lỗi; nếu lỗi lặp lại, ghi nhận kết quả là không hoàn tất và không xem điểm một phần là lần chạy thành công. Tăng recursion limit chỉ nên làm có chủ đích vì có thể tăng token và làm giảm tính so sánh.
- `skills-auto/code-learn` lần đầu timeout, lần chạy lại báo `OpenAIConnectionError` và vẫn có `error`; điểm `3/10` cùng token của lần này là kết quả một phần, chưa phải lần chạy hoàn tất. Kiểm tra kết nối mạng, endpoint và trạng thái API bằng một yêu cầu nhỏ; sau khi kết nối ổn định, chạy lại riêng task này. Lần chạy lại các task `skills-auto` khác đã hết lỗi: `code-eval`, `data-learn`, `logs-eval` và `logs-learn`.
- `skills-auto/data-eval` không có lỗi runtime nhưng đạt `0/9`; đây là kết quả điểm thấp, không phải lỗi kết nối. Tất cả run `skills-auto` có `skills_read=0`, vì vậy chưa có bằng chứng agent đã đọc và áp dụng skill.
- Không run nào có `skills_modified=true`; không cần xử lý skill bị sửa trong lúc chạy.

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
> `subagents` cao hơn `baseline` ở học (0,21 so với 0,07) và đánh giá (0,21 so với 0,10). `skills-auto` cao hơn nhẹ ở học (0,10 so với 0,07) nhưng thấp hơn ở đánh giá (0,03 so với 0,10), có thể gợi ý quá khớp. Tuy nhiên, không run `skills-auto` nào đọc skill (`skills_read=0/6`), nên chênh lệch này không chứng minh hiệu quả hay tác hại của skill; thêm vào đó, `subagents/data-eval` lỗi recursion và điểm 4/9 chỉ là trạng thái một phần.
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
> Theo `check_breakdown.py`, số check kỹ thuật đạt là baseline 2/18 học, 2/18 đánh giá; subagents 6/18 ở cả hai vai trò; skills-auto 3/18 học và 1/18 đánh giá. Check quy ước đạt lần lượt là 0/9 và 1/12 ở baseline, 0/9 và 0/12 ở subagents, 0/9 và 0/12 ở skills-auto. Vì không run nào đọc skill, chưa có bằng chứng skill giúp nhóm check nào. Các quy ước mới ở tác vụ đánh giá cũng không được skills-auto đạt; nguyên nhân có thể thấy trực tiếp là skill chưa được đọc (`skills_read=0`), không thể kết luận nội dung skill đã được áp dụng nhưng thất bại. 
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
> Không thể nêu check nào được skill giúp đạt vì cả sáu run skills-auto đều `skills_read=0`. Ví dụ, `rule_type_hints` vẫn fail ở `skills-auto/code-eval` và `rule_changelog` fail ở `skills-auto/code-learn`; các run không đọc `follow-test-protocols` hoặc `verify-code-syntax`. Đây là trường hợp skill chưa được đọc, không phải bằng chứng skill được đọc nhưng làm theo sai.
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
> Token trung bình mỗi run là 87.966 baseline, 107.933 subagents và 29.296 skills-auto. Tỷ lệ thô số check đạt trên một triệu token lần lượt khoảng 9,47; 18,53; 22,76, nên skills-auto có tỷ lệ thô cao nhất nhưng điểm tuyệt đối thấp và gồm run lỗi; mọi tỷ lệ đều bị ảnh hưởng bởi `baseline/data-learn` (368.860 token, GraphRecursionError), `subagents/data-eval` (407.461 token, GraphRecursionError) và `skills-auto/code-learn` (lỗi kết nối). Chỉ một trong sáu run subagents gọi subagent (data-learn); mean token cao hơn baseline khoảng 22,7%, nên thí nghiệm này chưa cho thấy đa tác tử đáng chi phí một cách ổn định.
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
> Ba skill hiện có mô tả quy trình chung cho import, kiểm thử và cú pháp, không thấy tên file/dữ liệu riêng của eval; curator chỉ lấy run `learn` và validator loại marker của eval. `verify_freeze.py` không báo skill thay đổi, hash run lệch, run trước freeze hay `skills_modified=true`, nhưng báo thiếu commit `hypotheses` trước tag, nên quy trình đóng băng chưa được xác minh hoàn toàn. `skills-auto` cao hơn baseline ở học nhưng thấp hơn ở eval có vẻ giống quá khớp, song vì skills không được đọc nên chưa thể quy kết cho skill.
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?
> Không có run/trace học `skills-auto` được lưu riêng trước khi chạy chính thức; vì thế không tính được chênh lệch điểm cùng bộ skill trước/sau freeze. Không thể dùng số hiện tại thay cho snapshot 3.4; thiếu bản đối chiếu làm giảm độ tin cậy của kết luận về nhiễu và hiệu quả học.

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1. Chỉ có ba tác vụ học và ba tác vụ đánh giá, mỗi cấu hình chạy một lần; chênh lệch có thể do đặc điểm từng task hoặc ngẫu nhiên của mô hình, chưa đại diện cho hiệu quả ổn định.
2. Có run lỗi recursion/kết nối nhưng vẫn được chấm trên workspace một phần và được tính vào bảng; các điểm trung bình và tỷ lệ điểm/token vì vậy không hoàn toàn so sánh được.
3. Không lưu snapshot Phần 3.4 và toàn bộ `skills_read` bằng 0; không kiểm nghiệm được liệu skill có được chọn đọc, làm theo, hay ảnh hưởng đến điểm.

## 10. Kết luận

> Trong các run hiện có, `subagents` đạt điểm trung bình cao hơn baseline ở cả học (0.21 so với 0.07) và đánh giá (0.21 so với 0.10), nhưng một run đánh giá bị `GraphRecursionError`. `skills-auto` đạt 0.10 ở học và 0.03 ở đánh giá, nhưng không run nào đọc skill nên chưa thể kết luận về tác dụng của skill. Các lỗi API và recursion cùng số lượng tác vụ nhỏ làm giảm độ tin cậy của so sánh. Thí nghiệm tiếp theo nên lưu snapshot Phần 3.4, bảo đảm commit giả thuyết trước tag freeze, ổn định kết nối và lặp mỗi cấu hình nhiều lần.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
