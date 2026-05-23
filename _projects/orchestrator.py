import json
import os

class PipelineOrchestrator:
    def __init__(self, character_path: str, scene_path: str):
        self.character_data = self._load_json(character_path)
        self.scene_data = self._load_json(scene_path)
        
    def _load_json(self, path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing essential infrastructure file: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def resolve_style_layer(self) -> dict:
        """
        [First Principle: Override Logic]
        기획자가 지정한 scene의 style_override 가 활성화(true)되어 있다면 고유 캐릭터의
        기본 스타일 감성을 덮어씌우고(Override), 그렇지 않다면 베이스라인 상태를 보존합니다.
        """
        base_style = self.character_data["brand_signature_styles"]
        override = self.scene_data.get("style_override", {})
        
        resolved_style = {}
        
        if override.get("apply_override") is True:
            resolved_style["hair"] = f"{override['hair']['style']} (Color: {override['hair']['color']})"
            resolved_style["makeup"] = override["makeup"]["vibe"]
            resolved_style["wardrobe"] = f"{override['wardrobe']['exact_manifest']}, accessorized with {override['wardrobe']['jewelry']}"
        else:
            resolved_style["hair"] = f"{base_style['default_hair']['cut']} in {base_style['default_hair']['color']}"
            resolved_style["makeup"] = base_style["default_makeup_vibe"]
            resolved_style["wardrobe"] = base_style["default_wardrobe_vibe"]
            
        return resolved_style

    def compile_universal_manifest(self) -> dict:
        """
        어떤 하드웨어/API 인프라(Flux, FaceID, Banana)를 선택하더라도 깨지지 않는
        범용 통합 실행 계획서(Runtime Manifest JSON) 객체를 합성합니다.
        """
        resolved_style = self.resolve_style_layer()
        
        # 다운스트림 확장을 위해 빈 노드 예약어 보존 상태로 머지
        compiled_manifest = {
            "orchestrator_version": "3.0.0",
            "target_character": self.character_data["universal_character_id"],
            "target_scene": self.scene_data["variation_id"],
            "resolved_pipeline_data": {
                "identity_constants": {
                    "biometrics": self.character_data["biometrics"],
                    "facial_framework": self.character_data["facial_anatomy_constants"],
                    "anchor_features": self.character_data["permanent_signature_marks"]
                },
                "creative_context": {
                    "environment": self.scene_data["creative_direction"]["environment"],
                    "cinematography": self.scene_data["creative_direction"]["cinematography"],
                    "actor_state": self.scene_data["creative_direction"]["subject_state"]
                },
                "computed_style_layer": resolved_style
            },
            "downstream_model_extensions": self.character_data["downstream_model_extensions"],
            "downstream_runtime_extensions": self.scene_data["downstream_runtime_extensions"]
        }
        return compiled_manifest

    def generate_natural_language_prompt(self, manifest: dict) -> str:
        """통합 정의된 구조화 객체로부터 완벽한 영문 실사 프롬프트 텍스트를 파싱 빌드합니다."""
        identity = manifest["resolved_pipeline_data"]["identity_constants"]
        creative = manifest["resolved_pipeline_data"]["creative_context"]
        style = manifest["resolved_pipeline_data"]["computed_style_layer"]
        
        # 앵커 마크 문자열화
        marks = ", ".join([f"{m['visual_description']} located {m['anatomical_location']}" for m in identity["anchor_features"]])
        marks_phrase = f" Features include {marks}." if marks else ""

        prompt = (
            f"A professional photorealistic portrait of a {identity['biometrics']['apparent_age']}-year-old "
            f"{identity['biometrics']['ethnicity']} {identity['biometrics']['biological_gender']}. "
            f"Face Details: {identity['facial_framework']['face_shape']}, {identity['facial_framework']['eyes']}, "
            f"{identity['facial_framework']['nose']}.{marks_phrase} Hair is styled in {style['hair']}. "
            f"Makeup is a {style['makeup']}. Wearing {style['wardrobe']}. "
            f"Scene Setup: {creative['actor_state']['pose_action']}, displaying {creative['actor_state']['facial_expression']}. "
            f"Captured at {creative['environment']['location_context']} during {creative['environment']['atmosphere_and_time']} "
            f"with {creative['environment']['background_elements']}. "
            f"Cinematography: {creative['cinematography']['framing']}, {creative['cinematography']['camera_angle']}, {creative['cinematography']['focus_profile']}."
        )
        return prompt

if __name__ == "__main__":
    # 데이터 경로 세팅 가상 시뮬레이션
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    char_json_path = os.path.join(BASE_DIR, "models", "char-001.json")
    scene_json_path = os.path.join(BASE_DIR, "scenes", "seongsu_cafe_evening.json")
    
    # 런타임 오케스트레이터 가동
    orchestrator = PipelineOrchestrator(char_json_path, scene_json_path)
    final_manifest = orchestrator.compile_universal_manifest()
    final_prompt_text = orchestrator.generate_natural_language_prompt(final_manifest)
    
    print("====== 1. COMPILED RUNTIME MANIFEST LAYER ======")
    print(json.dumps(final_manifest, indent=2, ensure_ascii=False)[:600] + "\n...[하위 모델 확장 레이어 생략]...\n")
    
    print("====== 2. EXTRACTED PROMPT ENGINE TEXT ======")
    print(final_prompt_text)