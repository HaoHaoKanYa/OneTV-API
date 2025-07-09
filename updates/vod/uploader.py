"""
OneTV-API 点播源 Supabase 上传模块
VOD Source Supabase Uploader Module
"""
import os
import requests


class VODSupabaseUploader:
    """点播源Supabase上传器"""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        # 优先使用SERVICE_KEY，如果没有则使用ANON_KEY
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        self.bucket_name = "vod-sources"

        if not self.supabase_url or not self.supabase_key:
            print("⚠️  Supabase配置未找到，将跳过上传")
        else:
            key_type = "SERVICE_KEY" if os.getenv("SUPABASE_SERVICE_KEY") else "ANON_KEY"
            print(f"🔑 使用Supabase {key_type}进行认证")
    
    def upload_vod_file(self, file_path: str) -> bool:
        """上传点播源文件到Supabase"""
        if not self.supabase_url or not self.supabase_key:
            print("❌ Supabase配置缺失，无法上传")
            return False
        
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return False
        
        try:
            # 读取文件内容
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 上传多仓库配置文件
            current_success = self._upload_to_path("onetv-api-movie.json", content)

            if current_success:
                print("✅ 多仓库配置文件上传成功!")
                print(f"📁 文件路径: vod-sources/onetv-api-movie.json")
                print(f"🔗 访问地址: {self.supabase_url}/storage/v1/object/public/vod-sources/onetv-api-movie.json")
                return True
            else:
                print("❌ 文件上传失败")
                return False
                
        except Exception as e:
            print(f"❌ 上传点播源文件失败: {str(e)}")
            return False
    
    def _upload_to_path(self, path: str, content: str) -> bool:
        """上传内容到指定路径，支持文件替换"""
        try:
            # 首先尝试更新现有文件
            update_url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{path}"

            headers = {
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }

            # 尝试PUT请求更新文件
            response = requests.put(update_url, data=content.encode('utf-8'), headers=headers)

            if response.status_code in [200, 201]:
                print(f"✅ 文件更新成功: {path}")
                return True
            elif response.status_code == 404:
                # 文件不存在，尝试创建新文件
                print(f"📄 文件不存在，创建新文件: {path}")
                create_response = requests.post(update_url, data=content.encode('utf-8'), headers=headers)

                if create_response.status_code in [200, 201]:
                    print(f"✅ 文件创建成功: {path}")
                    return True
                else:
                    print(f"❌ 文件创建失败: {path} - HTTP {create_response.status_code}")
                    print(f"响应: {create_response.text}")
                    return False
            else:
                print(f"❌ 文件更新失败: {path} - HTTP {response.status_code}")
                print(f"响应: {response.text}")
                return False

        except Exception as e:
            print(f"❌ 上传路径 {path} 失败: {str(e)}")
            return False
    
    def get_public_url(self, path: str = "onetv-api-movie.json") -> str:
        """获取文件访问URL（私有存储桶需要认证）"""
        if not self.supabase_url:
            return ""

        # 私有存储桶不支持 /public/ URL，返回需要认证的URL
        return f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{path}"

    def get_authenticated_url(self, path: str) -> str:
        """获取需要认证的文件访问URL（与get_public_url相同，用于私有存储桶）"""
        return self.get_public_url(path)
    
    def create_bucket_if_not_exists(self) -> bool:
        """创建存储桶（如果不存在）"""
        if not self.supabase_url or not self.supabase_key:
            return False
        
        try:
            # 检查存储桶是否存在
            url = f"{self.supabase_url}/storage/v1/bucket/{self.bucket_name}"
            headers = {
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ 存储桶 {self.bucket_name} 已存在")
                return True
            elif response.status_code == 404:
                # 创建存储桶
                create_url = f"{self.supabase_url}/storage/v1/bucket"
                bucket_config = {
                    "id": self.bucket_name,
                    "name": self.bucket_name,
                    "public": True,
                    "file_size_limit": 52428800,  # 50MB
                    "allowed_mime_types": ["application/json", "text/plain"]
                }
                
                create_response = requests.post(create_url, json=bucket_config, headers=headers)
                
                if create_response.status_code in [200, 201]:
                    print(f"✅ 存储桶 {self.bucket_name} 创建成功")
                    return True
                else:
                    print(f"❌ 创建存储桶失败: HTTP {create_response.status_code}")
                    print(f"响应: {create_response.text}")
                    return False
            else:
                print(f"❌ 检查存储桶失败: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 存储桶操作失败: {str(e)}")
            return False
    
def upload_vod_to_supabase(file_path: str):
    """上传点播源到Supabase的主函数"""
    uploader = VODSupabaseUploader()
    
    # 确保存储桶存在
    bucket_created = uploader.create_bucket_if_not_exists()
    
    if not bucket_created:
        return {
            "success": False,
            "message": "存储桶创建或检查失败",
            "public_url": ""
        }
    
    # 上传文件
    upload_success = uploader.upload_vod_file(file_path)
    
    result = {
        "success": upload_success,
        "message": "上传成功" if upload_success else "上传失败",
        "public_url": uploader.get_public_url() if upload_success else ""
    }
    
    return result
