# ViperKernel — Project Log

## Dependencies
- Python 3.11+
- PyTorch 2.1+
- CUDA 12.1
- Ollama
- Qwen2.5-Coder models
- GGUF format

## Runtime Errors
| Date | Error | Status |
|------|-------|--------|
| 2026-07-10 | sandbox snapshot-state error blocks KV writes | Open |
| 2026-07-15 | missing src/action_handlers.py for Aegis Inbox Poll | Fixed |
| 2026-07-20 | Visa-3208 payment declined (Google One, Uber, YouTube Music) | Open |

## Debug Logs
- OLLAMA threads 2->4 only ~6% gain (memory-bandwidth-bound)
- NMCT: 46 sealed-valid / 397 unsealed / 0 tampered
- Correctness audit: 46 approved blocks pass
- Soak foundry: 4395 mined / 45 gated
