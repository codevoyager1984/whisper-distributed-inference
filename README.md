# Distributed Whisper Inference

Parallelize [whisper](https://github.com/openai/whisper) inference based on distributed workflow orchestration & GPU worker:

1. Use [conductor](https://github.com/conductor-oss/conductor) as workflow orchestration engine to distrubute tasks across multi workers.
2. Use [Vast.ai](https://vast.ai/) to setup GPU node dynamicly.
3. Split Video into chunks, each avaliable worker consume chunk simultaneously. After chunks all comsumed, combine the result.

