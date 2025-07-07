"""
OneTV-API 点播源更新模块
VOD (Video On Demand) Source Update Module
"""

from .request import get_vod_sources, get_vod_sources_info, update_vod_sources, VODSourceManager
from .processor import process_vod_sources, VODProcessor
from .uploader import upload_vod_to_supabase, VODSupabaseUploader

__all__ = [
    'get_vod_sources',
    'get_vod_sources_info', 
    'update_vod_sources',
    'VODSourceManager',
    'process_vod_sources',
    'VODProcessor',
    'upload_vod_to_supabase',
    'VODSupabaseUploader'
]
