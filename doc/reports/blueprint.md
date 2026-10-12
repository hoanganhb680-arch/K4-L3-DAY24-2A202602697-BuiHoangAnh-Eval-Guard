# Blueprint CI/CD cho RAG và guardrails

Nhóm: Nhóm K4 Track 3A

Người phụ trách: Bui Hoang Anh - 2A202602697

Đây là **đề xuất CI/CD**, không phải workflow đã được triển khai/chạy.
Nguồn kết quả: artifacts/ragas_50q.json, judge_results.json, guard_results.json.
Run timestamp: 2026-10-12T12:01:56+00:00; guard models: `cx/gpt-6-luna`.
Models generation/evaluator/judge từ A/B: generation `gemini-3.1-flash-lite`,
evaluator `cx/gpt-6-luna` + `BAAI/bge-m3`, judge `cx/gpt-6-luna`.

## Kiến trúc và failure action

Input → Presidio → NeMo input → RAG → NeMo output → response.
Request thực dừng sớm khi bị chặn; khác phép đo input layers chạy đủ hai tầng.

Presidio quét CCCD/CMND, số điện thoại Việt Nam và email; nếu có PII thì chặn trước
NeMo. NeMo input dùng built-in self-check input, NeMo output dùng self-check output
để từ chối dữ liệu cá nhân/credentials. Secrets nằm ngoài sandbox, chỉ qua `.env`.
Nếu LLM generation lỗi thì fallback extractive; guard không dùng keyword để xác định
block mà đọc activated rails.

## Phạm vi và số đo latency

Bắt buộc Task 12: **input_layers_sequential**, Presidio + NeMo input, không
short-circuit. Engines tạo trước đo; có hai warm-up thật không tính vào mẫu.
Percentile nội suy tuyến tính từ raw samples; tổng từ tổng từng sample.

Số mẫu timed: 20; warm-up: 2; phương pháp: linear.

| Layer / scope | P50 ms | P95 ms | P99 ms | Tình trạng |
|---|---|---|---|---|
| Presidio | 23.708 | 27.397 | 27.435 | Đã đo Task 12 |
| NeMo input | 1506.466 | 2227.530 | 2609.772 | Đã đo Task 12 |
| Input guard sequential | 1525.475 | 2254.125 | 2627.735 | Đã đo Task 12 |
| RAG | 8172.893 | 10517.209 | 11374.258 | Đo bổ sung, ngoài Task 12 |
| NeMo output | 1581.31 | 2699.45 | 3135.151 | Đo bổ sung, ngoài Task 12 |
| Full guard / short-circuit request | chưa đo | chưa đo | chưa đo | Không suy từ input_guard_ms |

Input-layer budget target: 500ms; kết quả thực tế p95 = 2254.125ms, budget_ok = false.
Bottleneck chính là NeMo self-check gọi LLM qua 9router. Kế hoạch: đo full guard riêng,
tăng batch/caching hoặc dùng model nhanh hơn, rồi mới áp target 500ms.

RAG và NeMo output được đo bổ sung với 2 warm-up + 20 mẫu mỗi scope, cùng cách
tính percentile nội suy tuyến tính. RAG chậm do dense search encode lại từng query;
NeMo output chậm do gọi LLM self-check. Full guard request chưa đo vì cần nối
hai runtime (RAG trên Python 3.13 và NeMo trên venv 3.11) trong cùng một process.

## CI gates đề xuất

- RAGAS faithfulness ≥0.75, avg_score ≥0.65 trên 50 câu.
- Attacks ≥18/20 cho CI đề xuất; clean 8/8 allowed; output cases đúng.
- Full guard P95 <500ms chỉ áp dụng sau khi thực sự đo full guard.

Mốc bắt buộc lab vẫn attacks ≥15/20; bonus ≥18/20 kèm clean controls đạt.
Đề xuất một script chạy three runners rồi so sánh số liệu bằng `report_contracts`
và trả nonzero khi ngưỡng không đạt (`MIN_*` là biến cấu hình CI). Workflow này
hiện chưa triển khai thật trong repo.

## Monitoring và cải tiến

Cảnh báo khi clean false_positive_rate tăng, adversarial pass rate giảm, κ giảm
dưới 0.4, hoặc input_guard_ms p95 tăng đột biến. Lấy log PII/decision/activated rails
và response time mỗi request; autô-redact PII. Bộ dữ liệu 50/20/8/4 là nhỏ, cần
đánh giá định kỳ trên sample lớn hơn và kiểm tra drift theo phiên bản chính sách.

RAGAS mean/worst distribution: multi_hop mean 0.6917.
Cohen’s κ: 0.8.
Attacks passed: 18/20; clean false_positive_rate: 0.0.

Các cải tiến có thể kiểm tra: thêm bước phân rã multi-hop trước when trả lời,
giữ chunk theo từng phiên bản chính sách, giảm false positive bằng cách giới hạn
entity PII, và đo full guard latency riêng.
