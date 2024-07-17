# Distributed Whisper Inference

Parallelize [whisper](https://github.com/openai/whisper) inference based on distributed workflow orchestration & GPU worker:

1. Use [conductor](https://github.com/conductor-oss/conductor) as workflow orchestration engine to distrubute tasks across multi workers.
2. Use [Vast.ai](https://vast.ai/) to setup GPU node dynamicly.
3. Split Video into chunks, each avaliable worker consume chunk simultaneously. After chunks all comsumed, combine the result.

## Performance

Test sample: Use audio from [https://www.youtube.com/watch?v=34OJXQeIn64](https://www.youtube.com/watch?v=34OJXQeIn64), audio length 94 mins 30 seconds, file size 86.5 M.

GPU Machine: 1x RTX 2080 Ti

```txt
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 530.30.02              Driver Version: 530.30.02    CUDA Version: 12.1     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                  Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf            Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 2080 Ti      On | 00000000:0B:00.0 Off |                  N/A |
| 30%   40C    P2               52W / 200W|   1069MiB / 11264MiB |      1%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
+---------------------------------------------------------------------------------------+
```

### Serial Execution by Single GPU

Script:

```py
import whisper
import time

start = time.time()

model = whisper.load_model("MODEL_TYPE")
result = model.transcribe("audio.mp3")
print(result["text"])

end = time.time()
print(f"Tooks {end - start} s")
```

| Model Type | GPU Ram Required | Tooks   |
| ---------- | ---------------- | ------- |
| `tiny.en`  | ~1 GB            | 171.1 s |
| `base.en`  | ~1 GB            | 260.8 s |
| `small.en`  | ~1 GB            | 432.4 s |
| `medium.en`  | ~1 GB            | 171.1 s |
