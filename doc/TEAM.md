# Nhóm thực hiện K4 Track 3A

Tên nhóm: K4-Eval-Guard

Repo chung: https://github.com/hoanganhb680-arch/K4-Track-3A-Day24-Eval-Guard

Trưởng nhóm/người nộp: Bui Hoang Anh - 2A202602697

Ngày lab/deadline áp dụng: 2026-10-12 23:59 — Asia/Ho_Chi_Minh (UTC+07:00)

Commit dùng để chấm: 540ec0b7c9cbee4c8513e3cb13b1301b1c3e5b4c

Mỗi nhóm nộp một repo. Điền đủ thành viên và một mục INDIVIDUAL cho từng người.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Bui Hoang Anh | 2A202602697 | Tích hợp m1–m5, hoàn thiện Phase A/B/C, chạy batch và điền reports | commits/src + 4 artifacts |

Người tích hợp/chạy batch/nộp link: Bui Hoang Anh, tích hợp 5 module RAG từ Day18,
hoàn thiện các TODO, chạy setup + three phases và validate 4 artifact.

## Môi trường và chuẩn bị trước lớp

OS/Python/compiler: Windows 11; Python 3.11.9 cài qua winget; MSVC Build Tools 2022.
Virtualenv/dependencies/imports: `.venv311` chứa NeMo 0.10.0, Presidio 2.2.364,
spaCy 3.8.16 và annoy 1.17.3. Runtime phases A/B dùng system Python 3.13 với RAGAS.
Models/Qdrant/50 answers: Qdrant v1.9.7 qua Docker, embedding BGE-M3, reranker
BGE-reranker-v2-m3; 50 answers đã sinh bằng LLM qua 9router/OpenAI-compatible. Ghi
giới hạn: answers generation model là flash-lite, Phase C chạy bằng venv 3.11.

## INDIVIDUAL

### BuiHoangAnh-2A202602697

- Phần được giao và phần thực tế đã làm: mang m1–m5 từ Day18 vào src, adapt m4/m5
  cho config Day24, hoàn thiện mọi TODO Phase A/B/C, cấu hình qdrant + runtime, chạy
  thật setup và 3 phase, kiểm tra schema và điền ba báo cáo.
- Bằng chứng: các commit trong repo + artifacts/answers_50q.json, ragas_50q.json,
  judge_results.json, guard_results.json.
- Cách kiểm tra: `python -m pytest tests/ -q` (86 passed); `check_lab.py` sau khi
  artifact đầy đủ để xác minh schema/contracts.
- Điều đã học: phân biệt evaluator models theo vai trò, RAGAS bottom/cluster, pairwise
  swap-and-average và Cohen kappa, guardrail Presidio/NeMo và đo latency input layers.
- Giới hạn/cách xử lý: NeMo 0.10.0 cần Python 3.11 + MSVC, nên Phase C tách venv riêng;
  generation model khác evaluator/judge model để tránh hết quota, đã ghi trong metadata.
- Nguồn/AI hỗ trợ nếu có: dùng Codex để scaffolding và xử lý môi trường; toàn bộ số đo
  và artifacts đến từ runner thật, không điền giả.

## Cập nhật sau khi nộp

Chưa có cập nhật sau deadline; bản nộp cuối cần ghi commit SHA trước khi gửi link.
