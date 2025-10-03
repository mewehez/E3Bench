# E3Bench
E3Bench: Energy, Efficiency, and Edge Benchmarking for Deep Neural Networks

E3Bench provides a reproducible framework for measuring the real efficiency of deep neural networks on edge GPUs. Unlike common proxy metrics such as FLOPs or parameter counts, E3Bench captures latency, power, and energy consumption directly through controlled experiments. The framework supports:

- Adaptive latency measurement with noise reduction.
- Power measurement from both internal sensors and external tools.
- Combined energy evaluation as the backbone for pruning and compression studies.
- Validation of measurement equivalence across devices.

E3Bench is designed as an open research tool: it is the foundation for the experimental results reported in our thesis, and also serves as ground truth for energy prediction models in automated pruning and Neural Operation Search (NOS).
