
### IP Adapter FaceID
- 이미지의 일관성을 지켜주는 모듈 
[ComfyUI IPAdapter Advanced 노드 옵션](https://z03y.tistory.com/36)


# [Phase 1] Digital DNA 설계 (Identity Definition)
- 가장 먼저 '인플루언서의 고정된 유전자'를 정의해야 함.
- 템플릿이 바뀌어도 변하지 않는 데이터셋을 만드는 단계입니다.
Step1: Master Face 결정: 가장 완벽한 얼굴 사진 1장을 생성하거나 선택합니다. (Z-Image Turbo 또는 Flux 기반 모델 권장)

Step2: Prompt Bible 작성: 인플루언서의 고유한 외모 묘사(눈 모양, 점 위치, 헤어 텍스처)를 텍스트로 고정합니다.

Optional: LoRA 학습 (선택적): 얼굴의 미세한 특징을 100% 재현하고 싶다면, 해당 얼굴을 20~30장 생성하여 Ostris AI Toolkit 등을 이용해 전용 LoRA를 1회 학습시킵니다.

# [Phase 2] ComfyUI "Modular" 워크플로우 구축
하나의 거대한 노드 뭉치를 만드는 대신, 기능을 분리하여 관리하는 것이 장기적으로 유리합니다.

1. Image Generation Module (외형)
IP-Adapter FaceID v2: 마스터 얼굴 사진을 입력으로 받아 모든 모델에서 얼굴 일관성을 유지합니다.

ControlNet (Depth/Canny): 포즈와 구도를 고정하여 자연스러운 화보를 만듭니다.

Face Detailer: 생성 후 얼굴 부분만 다시 고해상도로 렌더링하여 실사감을 높입니다. 

2. Motion & Video Module (움직임)
LivePortrait / MimicMotion: 고정된 이미지에 본인의 얼굴 움직임을 입혀 숏폼(Reels, TikTok) 영상을 만듭니다.

AnimateDiff: 캐릭터가 자연스럽게 움직이는 짧은 클립을 생성합니다.

3. Voice & Audio Module (소통)
ElevenLabs API Node: 텍스트를 입력하면 캐릭터의 고정된 목소리가 나오도록 연결합니다.

SadTalker / Wav2Lip: 목소리에 맞춰 캐릭터의 입 모양을 동기화합니다.


[Phase 3] 콘텐츠 생산 자동화 파이프라인
프로토타입이 끝나면, 매일 콘텐츠를 뽑아낼 수 있는 시스템을 구축해야 합니다.

Workflow Snapshot: 완성된 노드 조합을 JSON으로 저장하고 Git으로 관리합니다.

Batch Processing: RunPod의 API 기능을 사용하여 하루치 포스팅(이미지 5장, 영상 1개)을 한 번에 생성하도록 설정합니다.

LayerForge / Photoshop Integration: 배경 제거(RMBG 2.0) 및 레이어 합성을 통해 광고 포스터나 브랜딩 이미지를 최종 검수합니다.


PERSONA IDEATION 
- 요가
- Mixed Ethnicity
- Imperfection : 잔머리, 주근깨 
- 오타쿠적인 면모 
- 역동적인


asset을 많이 늘려나가야 한다. 

### reference
- x-flux-comfyui: ipadapter controlnet을 연동한 Flux모델

git clone https://github.com/XLabs-AI/x-flux-comfyui.git ComfyUI/custom_nodes/x-flux-comfyui/  