# Phân tích lỗi Phase A

Nhóm: Nhóm K4 Track 3A

Người phụ trách: Bui Hoang Anh - 2A202602697

Nguồn: `artifacts/ragas_50q.json`; run timestamp: 2026-10-12T11:09:43+00:00.
Generation mode: toàn bộ 50 câu dùng `llm`.
Models generation/evaluator: generation là `gemini-3.1-flash-lite`; evaluator gồm
`cx/gpt-6-luna` (LLM judge qua 9router) và `BAAI/bge-m3` (embedding).

## Điểm theo distribution

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---|---|---|
| faithfulness | 1.0 | 0.6720 | 0.9167 |
| answer_relevancy | 0.8907 | 0.7490 | 0.7825 |
| context_precision | 0.9667 | 0.7167 | 0.8 |
| context_recall | 0.8 | 0.6292 | 0.4417 |
| avg_score | 0.9143 | 0.6917 | 0.7352 |

## Bottom 10 và nguyên nhân

Điền đúng 10 rows từ Task 3, đối chiếu ID/question/distribution/avg_score/worst_metric.

1. rank 1, id 44, adversarial, câu về "Bao lâu phải đổi mật khẩu?", avg 0.4583, worst: answer_relevancy.
2. rank 2, id 21, multi_hop, "Senior 9 năm thâm niên: phép năm và lương?", avg 0.5, worst: answer_relevancy.
3. rank 3, id 33, multi_hop, "Manager 12 năm: phụ cấp và phép v2024?", avg 0.5, worst: answer_relevancy.
4. rank 4, id 40, multi_hop, "thử việc vi phạm bảo mật nên/không nên làm gì?", avg 0.5129, worst: faithfulness.
5. rank 5, id 49, adversarial, "nghỉ phép v2023 vs hiệu lực hiện tại?", avg 0.513, worst: context_recall.
6. rank 6, id 27, multi_hop, "thâm niên 7 năm + trừ 4 ngày ốm không giấy?", avg 0.5379, worst: context_precision.
7. rank 7, id 34, multi_hop, "tạm ứng 4 triệu với 7 triệu khác nhau?", avg 0.5534, worst: context_recall.
8. rank 8, id 41, adversarial, "nghỉ bao nhiêu ngày phép năm?", avg 0.5737, worst: context_recall.
9. rank 9, id 30, multi_hop, "bảo hiểm thử việc vs chính thức?", avg 0.5797, worst: context_precision.
10. rank 10, id 26, multi_hop, "kết hôn của mình và con cùng tuần?", avg 0.6227, worst: context_precision.

Các câu yếu tập trung ở `multi_hop` và bẫy phiên bản/phủ định. Ví dụ id 49 yêu cầu
phân biệt v2023 và v2024, nhưng context recall thấp cho thấy pipeline không giữ đủ
các chunk chính sách cũ lẫn hiện hành. id 40 là câu phân tích hành động nhiều vế,
faithfulness thấp cho thấy answer sinh một phần không được context hỗ trợ.

## Matrix và nhóm yếu nhất

Matrix 4 metric × 3 distributions (mỗi câu được đếm theo worst_metric của câu đó):

| Metric | factual | multi_hop | adversarial |
|---|---:|---:|---:|
| faithfulness | 0 | 6 | 0 |
| context_recall | 6 | 7 | 7 |
| context_precision | 3 | 5 | 1 |
| answer_relevancy | 11 | 2 | 2 |

Nhóm yếu theo mean thấp nhất: multi_hop; mean: 0.6917.
Worst metric xuất hiện nhiều nhất: context_recall; số câu: 20.

Đây là dấu hiệu retrieval thiếu chunk cần thiết cho câu đòi kết hợp nhiều thông
tin và đối chiếu phiên bản, không phải vì multi_hop có 20 câu. Điểm multi_hop thấp
nhất về trung bình trong khi factual cao hơn và adversarial vẫn nhỉnh hơn nhờ bẫy
được trả lời một phần. Đề xuất cụ thể: giữ nhiều chunk theo phiên bản khi index,
tăng top_k kết hợp BM25 và dense, và thêm câu hỏi phụ trước khi trả lời cho multi-hop.

## Bẫy adversarial và giới hạn

Adversarial mean 0.7352, cao hơn multi_hop nhưng thấp hơn factual; hai câu id 44 và
id 49 nằm trong bottom 10. id 49 là xung đột v2023/v2024 và context_recall thấp,
id 44 hỏi mật khẩu nhưng answer_relevancy thấp, cho thấy answer lệch trọng tâm câu.
Điểm thấp không tự chứng minh pipeline nhận ra bẫy; cần đọc answer/context/reference.
Giới hạn hiện tại: bộ sample 50 câu, model generation là flash-lite, evaluator là
một LLM proxy duy nhất; kết quả chưa thể suy rộng ra cỡ dữ liệu lớn hơn.
