# Đánh giá LLM Judge Phase B

Nhóm: Nhóm K4 Track 3A

Người phụ trách: Bui Hoang Anh - 2A202602697

Nguồn: `artifacts/judge_results.json`; run timestamp: 2026-10-12T11:11:24+00:00.
Models generation/judge: generation là `gemini-3.1-flash-lite`; judge là
`cx/gpt-6-luna` (qua 9router).

## Năm cặp A/B và hai lượt

Nguồn cố định: A từ artifacts/answers_50q.json:answer; B từ
fixtures/human_labels_10q.json:model_answer; reference từ fixtures/test_set_50q.json:ground_truth.
Ids: 1, 5, 12, 21, 41. Không đổi nguồn sau khi xem kết quả judge.

| id | Tóm tắt câu hỏi | pass1 | pass2 | final | consistent |
|---|---|---|---|---|---|
| 1 | Nghỉ bao nhiêu ngày khi kết hôn? | B | B | B | true |
| 5 | Mua thiết bị 55 triệu cần ai duyệt? | A | A | A | true |
| 12 | Thưởng Tết tối thiểu từ 6 tháng? | A | A | A | true |
| 21 | Senior 9 năm: phép và lương? | B | B | B | true |
| 41 | Nghỉ bao nhiêu ngày phép năm? | A | A | A | true |

Cả năm cặp đều có `position_consistent = true`; không có case hoán đổi thứ tự mà
winner đổi.

Position bias count/rate: 0 / 0.0.
Verbosity win rate: 0.6; decisive cases: 5.

Verbosity chỉ là dấu hiệu thống kê trên 5 cặp: winner dài hơn candidate kia trong
3/5 case (A dài hơn thắng 2 lần, B dài hơn thắng 1 lần). Số mẫu quá nhỏ và các
winner đều có nội dung đầy đủ hơn theo reasoning, nên không kết luận nguyên nhân
là bias độ dài.

## Calibration đúng model_answer

Helper đánh giá đúng question/model_answer đang có trong fixtures/human_labels_10q.json;
không lấy answer mới của pipeline. Prompt chỉ nhận question, answer, reference.
Không gửi human_label, human_note hoặc phân bố nhãn human vào prompt.

Mười nhãn binary (ids 1, 5, 12, 21, 23, 29, 33, 41, 46, 50) giữ đúng thứ tự JSON.
Nhãn judge so với human: `[1,0,1,1,1,0,1,0,0,0]` so với `[1,0,1,1,1,0,1,0,1,0]`.
Lệch đúng 1 vị trí (id 46): human=1 còn judge=0.

Cohen’s κ: 0.8.
Observed agreement là 9/10 = 0.9; chance agreement tính từ tỷ lệ nhãn 1/0 là 0.5,
nên κ = (0.9 - 0.5) / (1 - 0.5) = 0.8.

κ = 0.8 là substantial, nhưng chỉ trên 10 nhãn nên độ tin cậy của ước lượng còn hẹp.

## Giới hạn và cách dùng judge

Model judge là một LLM proxy duy nhất (`cx/gpt-6-luna`) với prompt cố định, nhiệt độ
bằng 0. Chỉ có 5 cặp và 10 nhãn, nên các con số bias/κ chưa thể kết luận ổn định dài
hạn. Không xem judge là đáp án tuyệt đối; nên dùng swap-and-average với mọi kết quả
pairwise và đối chiếu bằng human sample mỗi lần thay prompt/model.
