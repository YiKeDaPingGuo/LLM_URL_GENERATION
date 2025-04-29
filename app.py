from flask import Flask, jsonify, request
import csv
from minio import Minio
from minio.error import S3Error
import json

app = Flask(__name__)

# MinIO 配置（请根据实际环境修改）
minio_client = Minio(
    "10.136.196.237:9000",  # MinIO 服务地址
    access_key="minioadmin",  # 访问密钥
    secret_key="minioadmin",  # 私有密钥
    secure=False  # HTTP 访问，HTTPS 设为 True
)
bucket_name = "course-materials"  # MinIO 存储桶名称
csv_path = "course_info.csv"  # CSV 文件路径（请修改为实际路径）


def process_course_name(course_name):
    """根据输入的课程名称生成对应的 MinIO 下载链接"""
    course_name = course_name.strip()

    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            headers = next(reader)

            # 检查必需字段是否存在
            if '课程名称' not in headers:
                return {"answer": "CSV 缺少必需字段（课程名称）"}

            name_idx = headers.index('课程名称')

            for row in reader:
                if course_name == row[name_idx]:  # 精确匹配课程名称
                    # 拼接文件名（严格匹配 MinIO 中的命名规则）
                    file_name = f"{row[0]}_{row[1]}_{row[2]}_{row[3]}_{row[4]}_{row[5]}.zip"
                    try:
                        # 生成预签名链接（有效期 1 小时）
                        presigned_url = minio_client.presigned_get_object(
                            bucket_name=bucket_name,
                            object_name=file_name,
                            expires=3600
                        )
                        return {"answer": presigned_url}
                    except S3Error as e:
                        if "NoSuchKey" in str(e):
                            return {"answer": f"文件未找到：{file_name}"}
                        return {"answer": f"MinIO 错误：{str(e)}"}

            return {"answer": "未找到匹配的课程名称记录"}

    except FileNotFoundError:
        return {"answer": f"CSV 文件未找到：{csv_path}"}
    except Exception as e:
        return {"answer": f"系统错误：{str(e)}"}


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    course_name = data.get('course_name', '')
    result = process_course_name(course_name)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
