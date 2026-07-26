# GeneticFoundry — Project Log

## Dependencies
- Python 3.11+
- Karoo GP (genetic programming)
- SymPy (symbolic simplification)
- ZeroMQ / PyArrow (distributed workers)
- Ray Core / Dask (optional)

## Runtime Errors
| Date | Error | Status |
|------|-------|--------|
| 2026-07-25 | Karoo GP monitoring loop design complete | Done |
| 2026-07-25 | 3D Sphere UI for Karoo GP — visual dashboard | Pending |

## Debug Logs
- Symbolic Miner architecture: Machine 2 (Worker) runs Karoo GP → Evaluator → Block Assembly/AST
- Ships via ZeroMQ/PyArrow to Machine 1 (Primary/Mint)
- Block criteria: fitness threshold exceeded
- Payload: block_id, fitness_score, expression_sympy, ast_tree, execution_time_ms, worker_id
