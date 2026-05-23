import os
import uuid
import datetime
import json
import duckdb

class LocalDuckDBClient:
    def __init__(self, db_path: str = "outputs/artifact_storage.ddb"):
        """로컬 DuckDB 클라이언트 초기화 (파일 기반 영구 저장)"""
        self.db_path = db_path
        # 데이터가 저장될 디렉토리가 없으면 자동 생성
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            
        self._init_table()

    def _get_connection(self):
        """DuckDB 연결 객체 반환"""
        return duckdb.connect(self.db_path)

    def _init_table(self):
        """테이블 및 스키마 초기화 (JSON 네이티브 타입 활용)"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS image_artifacts (
                    uuid UUID PRIMARY KEY,
                    timestamp TIMESTAMP WITH TIME ZONE,
                    request JSON,
                    response JSON,
                    review JSON
                )
            """)

    def insert_artifact(self, request_data: dict, response_data: dict, review_data: dict = None) -> str:
        """
        이미지 생성 아티팩트 메타데이터를 DB에 적재합니다.
        :return: 생성된 고유 UUID 문자열
        """
        generated_uuid = str(uuid.uuid4())
        current_timestamp = datetime.datetime.now(datetime.timezone.utc)
        
        # 기본값 처리 및 문자열 직렬화
        review_payload = review_data if review_data is not None else {}

        with self._get_connection() as conn:
            # DuckDB는 파이썬 dict를 유연하게 JSON 타입으로 바인딩합니다.
            conn.execute(
                """
                INSERT INTO image_artifacts (uuid, timestamp, request, response, review)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    generated_uuid, 
                    current_timestamp, 
                    json.dumps(request_data), 
                    json.dumps(response_data), 
                    json.dumps(review_payload)
                ]
            )
        return generated_uuid

    def query_high_rated_artifacts(self, min_score: float = 4.0):
        """[분석용] 특정 리뷰 점수 이상인 아티팩트를 JSON 내부 탐색으로 쿼리"""
        with self._get_connection() as conn:
            # DuckDB의 JSON 화살표 연산자(->>)를 사용하여 중첩 필드에 직접 접근
            query = """
                SELECT 
                    uuid,
                    timestamp,
                    request->>'$.lineage.character_id' AS character_id,
                    response->>'$.output_assets.primary_image' AS image_path,
                    CAST(review->>'$.rating_score' AS DOUBLE) AS score,
                    review->>'$.review_text' AS review_text
                FROM image_artifacts
                WHERE CAST(review->>'$.rating_score' AS DOUBLE) >= ?
                ORDER BY timestamp DESC
            """
            return conn.execute(query, [min_score]).df() # Pandas DataFrame으로 즉시 반환
        
if __name__ == "__main__":
    # 간단한 테스트 케이스
    client = LocalDuckDBClient()
    
    # 샘플 데이터 삽입
    sample_request = {
        "lineage": {
            "character_id": "char_123",
            "scene_id": "scene_456"
        },
        "generation_parameters": {
            "resolution": "1024x1024",
            "style": "cinematic"
        }
    }
    
    sample_response = {
        "output_assets": {
            "primary_image": "/path/to/generated/image.png"
        },
        "generation_metadata": {
            "model_version": "v1.2.3"
        }
    }
    
    sample_review = {
        "rating_score": 4.5,
        "review_text": "Amazing quality, very satisfied!"
    }
    
    artifact_uuid = client.insert_artifact(sample_request, sample_response, sample_review)
    print(f"Inserted artifact with UUID: {artifact_uuid}")
    
    # 고평점 아티팩트 쿼리
    high_rated_artifacts = client.query_high_rated_artifacts(min_score=4.0)
    print(high_rated_artifacts)
